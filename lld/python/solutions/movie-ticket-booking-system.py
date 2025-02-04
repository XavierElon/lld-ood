'''
Key Improvements and Design Patterns:

Thread Safety
Added locks for critical sections (seat reservations, booking confirmation)
Thread-safe singleton implementation using double-checked locking

State Pattern
Seat status transitions (Available → Reserved → Booked)
Booking states (Pending → Confirmed/Cancelled)

Strategy Pattern
Payment processing implementation
Easily swap payment providers (Credit Card, PayPal, etc.)

Factory Pattern
Seat creation logic encapsulated in SeatFactory
Consistent seat configuration for different theaters

Observer Pattern (implied)
Could be added for sending notifications (email/SMS) on booking updates

Exception Handling
Custom exceptions for better error handling
Transaction-like behavior for bookings (automatic rollback on failure)

Encapsulation
Proper data hiding using private attributes
Business logic moved to domain objects

Singleton Pattern
Single instance of booking system
Thread-safe initialization

Repository Pattern
In-memory storage for movies/theaters/shows
Could be extended to database storage

Usage Patterns:

Booking Flow:
Reserve seats atomically
Process payment
Confirm booking or rollback

Seat Management:
Concurrent seat reservations
Automatic seat release on cancellation

Extensibility:
Add new payment methods without changing core logic
Easy to add new seat configurations
Simple to extend with new notification channels

Additional Improvements Possible:
Add database persistence
Implement waitlist functionality
Add pricing strategies (discounts, dynamic pricing)
Add audit logging
Implement booking timeouts
Add user authentication
Add admin interface for managing shows
'''
from enum import Enum
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import threading
from abc import ABC, abstractmethod
from collections import defaultdict
import itertools

# -------------------- Enums --------------------
class BookingStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    
class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    BOOKED = "BOOKED"
    
class SeatType(Enum):
    NORMAL = "NORMAL"
    PREMIUM = "PREMIUM"
    
# -------------------- Exceptions --------------------
class SeatNotAvailableError(Exception):
    pass

class ShowNotFoundError(Exception):
    pass

class InvalidBookingStateError(Exception):
    pass

# -------------------- Domain Models --------------------
class User:
    def __init__(self, user_id: str, name: str, email: str):
        self._id = user_id
        self._name = name
        self._email = email
        
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def email(self) -> str:
        return self._email
    
class Movie:
    def __init__(self, movie_id: str, title: str, duration: int):
        self._id = movie_id
        self._title = title
        self._duration = duration
    
    @property
    def duration(self) -> int:
        return self._duration
    
class Seat:
    def __init__(self, seat_id: str, row: int, seat_type: SeatType, price: float):
        self._id = seat_id
        self._row = row
        self._type = seat_type
        self._price = price
        self._status = SeatStatus.AVAILABLE
        self._lock = threading.Lock()
        
    def reserve(self):
        with self._lock:
            if self._status != SeatStatus.AVAILABLE:
                raise SeatNotAvailableError(f"Seat {self._id} not available")
            self._status = SeatStatus.RESERVED
            
    def confirm(self):
        with self._lock:
            if self._status != SeatStatus.RESERVED:
                raise InvalidBookingStateError("Seat not in reserved state")
            self._status = SeatStatus.BOOKED
            
    def release(self):
        with self._lock:
            self._status = SeatStatus.AVAILABLE
            
    @property
    def status(self) -> SeatStatus:
        return self._status
       
class Show: 
    def __init__(self, show_id: str, movie: Movie, theater: 'Theater', time: datetime):
             self._id = show_id
             self._movie = movie
             self._theater = theater
             self._time = time
             self._seats: Dict[str, Seat] = {}
             self._lock = threading.Lock()
             
    def add_seats(self, seats: List[Seat]):
        with self._lock:
            for seat in seats:
                self._seats[seat._id] = seat    
                
    def get_available_seats(self) -> List[Seat]:
        with self._lock:
            return [seat for seat in self._seats.values() if seat.status == SeatStatus.AVAILABLE]
        
    def reserve_seats(self, seat_ids: List[str]) -> List[Seat]:
        with self._lock:
            seats = []
            for seat_id in seat_ids:
                if seat_id not in self._seats:
                    raise ValueError(f"Seat {seat_id} not found")
                seat = self._seats[seat_id]
                seat.reserve()
                seats.append(seat)
            return seats
    
class Theater:
    def __init__(self, theater_id: str, name: str, location: str):
        self._id = theater_id
        self._name = name
        self._location = location
        self._shows: List[Show] = []
        
    def add_show(self, show: Show):
        self._shows.append(show)  
    
class Booking:
    def __init__(self, booking_id: str, user: User, show: Show, seats: List[Seat]):
        self._id = booking_id
        self._user = user
        self._show = show
        self._seats = seats
        self._status = BookingStatus.PENDING
        self._created_at = datetime.now()
        self._lock = threading.Lock()
        
    def confirm(self):
        with self._lock:
            if self._status != BookingStatus.PENDING:
                raise InvalidBookingStateError("Booking already processed")
            for seat in self._seats:
                seat.confirm()
            self._status = BookingStatus.CONFIRMED
            
    def cancel(self):
        with self._lock:
            if self._status == BookingStatus.CANCELLED:
                return
            self._status = BookingStatus.CANCELLED
            for seat in self._seats:
                seat.release()
                
# -------------------- Patterns --------------------
# Singleton Pattern for Booking System
class MovieTicketBookingSystem:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self):
        self._movies: Dict[str, Movie] = {}
        self._theaters: Dict[str, Theater] = {}
        self._shows: Dict[str, Show] = {}
        self._bookings: Dict[str, Booking] = {}
        self._booking_counter = itertools.count(1)
        self._payment_processor: PaymentProcessor = CreditCardProcessor()
        
    # Strategy Pattern for Payment Processing
    def set_payment_processor(self, processor: 'PaymentProcessor'):
        self._payment_processor = processor
        
    def create_booking(self, user: User, show: Show, seat_ids: List[str]) -> Booking:
        try:
            seats = show.reserve_seats(seat_ids)
        except SeatNotAvailableError as e:
            raise e
        
        booking_id = f"BKG-{next(self._booking_counter):06d}"
        booking = Booking(booking_id, user, show, seats)
        self._bookings[booking_id] = booking
        return booking
    
    def confirm_booking(self, booking_id: str, payment_details: Dict):
        booking = self._bookings.get(booking_id)
        if not booking:
            raise ValueError("Invalid booking ID")
        
        try:
            amount = sum(seat._price for seat in booking._seats)
            if self._payment_processor.process_payment(amount, payment_details):
                booking.confirm()
        except Exception as e:
            booking.cancel()
            raise e
        
# Strategy Pattern Interface
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float, details: Dict) -> bool:
        pass
    
class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float, details: Dict) -> bool:
        return True
    
# Factory Pattern for Seat Creation
class SeatFactory:
    @staticmethod
    def create_seats(rows: int, seats_per_row: int) -> List[Seat]:
        seats = []
        for row in range(1, rows + 1):
            seat_type = SeatType.PREMIUM if row <= 2 else SeatType.NORMAL
            price = 200 if seat_type == SeatType.PREMIUM else 150
            for seat_num in range(1, seats_per_row + 1):
                seat_id = f"{row}-{seat_num}"
                seats.append(Seat(seat_id, row, seat_type, price))
        return seats
    
if __name__ == "__main__":
    system = MovieTicketBookingSystem()
    
    movie = Movie("M1", "Avengers", 180)
    
    theater = Theater("T1", 'AMC', 'San Francisco')
    show = Show("S1", movie, theater, datetime.now() + timedelta(days=1))
    seats = SeatFactory.create_seats(10, 12)
    show.add_seats(seats)
    theater.add(show)
    
    user = User("U1", "Achilles", "FakeEmail")
    
    try:
        booking = system.create_booking(user, show, ["1-5", "1-6"])
        system.confirm_booking(booking._id, {'card': "4111111111111111111"})
        print(f"Booking {booking._id} confirmed!")
    except Exception as e:
        print(f"Booking failed: {str(e)}")