# Explanation of Design Patterns
# Singleton Pattern (HotelManagementSystem)
# What: Ensures that only one instance of the HotelManagementSystem class can exist at a time.
# Why: In a hotel management context, you generally want a single point of reference to the system that tracks all reservations, rooms, and guests.

# Strategy Pattern (Payment Interface)
# What: Provides a family of interchangeable algorithms (payment methods) for performing the same task (processing payment).
# Why: This allows adding new payment methods (e.g., PayPal, mobile wallets) without modifying existing code. Each payment method implements the process_payment method differently.
# Additional potential patterns could be introduced (e.g., a Factory to create different kinds of Room objects), but in its current state, the most evident patterns are Singleton and Strategy.

# Explanation of Object-Oriented Principles
# Encapsulation
# Example: The Room class encapsulates its status and lock. Methods like book(), check_in(), and check_out() manage how the status changes.
# Why: Prevents direct access to internal data, ensuring the status transitions are always valid and thread-safe.

# # Abstraction
# Example: The Payment class is an abstract base class that defines an interface for process_payment.
# Why: Hides the details of each payment method, allowing the system to handle any payment object that implements the Payment interface.

# Inheritance
# Example: CashPayment and CreditCardPayment both inherit from the abstract class Payment.
# Why: Allows code reusability and the extension of the Payment interface for specific payment methods.

# Polymorphism
# Example: The process_payment method can be called on any Payment subclass (CashPayment, CreditCardPayment, etc.), and it will execute the subclass-specific logic.
# Why: Improves flexibility, letting the system handle various payment types without knowing their internal details.

# Thread Safety
# Example: The Lock objects in Room and in the HotelManagementSystem help ensure that operations on shared state (like changing a room’s status or adding reservations) are safe in a multi-threaded environment.
# Why: Concurrency control prevents race conditions and inconsistent data.
# Overall, this system design aims to be scalable and maintainable by following solid OOP principles and employing well-known design patterns.

import uuid
from abc import ABC, abstractmethod
from datetime import date, timedelta
from enum import Enum
from threading import Lock
from typing import Dict, Optional


# -------------------------
# ENUMS
# -------------------------

class RoomType(Enum):
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    DELUXE = "DELUXE"
    SUITE = "SUITE"


class RoomStatus(Enum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    OCCUPIED = "OCCUPIED"


class ReservationStatus(Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


# -------------------------
# PAYMENT (Strategy Pattern)
# -------------------------

class Payment(ABC):
    """
    Abstract base class representing a payment method.
    The Strategy pattern is used here so that different
    payment methods can be used interchangeably.
    """
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


class CashPayment(Payment):
    def process_payment(self, amount: float) -> bool:
        """
        Processes cash payment.
        Always returns True for this simplified example.
        """
        # In a real-world scenario, you'd handle actual cash payment logic here.
        print(f"Processing cash payment of {amount:.2f}")
        return True


class CreditCardPayment(Payment):
    def process_payment(self, amount: float) -> bool:
        """
        Processes credit card payment.
        Always returns True for this simplified example.
        """
        # In a real-world scenario, you'd integrate with a payment gateway here.
        print(f"Processing credit card payment of {amount:.2f}")
        return True


# -------------------------
# GUEST
# -------------------------

class Guest:
    """
    Represents a hotel guest.
    """
    def __init__(self, guest_id: str, name: str, email: str, phone_number: str):
        self._id = guest_id
        self._name = name
        self._email = email
        self._phone_number = phone_number

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @property
    def phone_number(self) -> str:
        return self._phone_number


# -------------------------
# ROOM
# -------------------------

class Room:
    """
    Represents a hotel room.
    Uses a Lock to handle concurrent access to room status.
    """
    def __init__(self, room_id: str, room_type: RoomType, price: float):
        self.id = room_id
        self.type = room_type
        self.price = price
        self.status = RoomStatus.AVAILABLE
        self.lock = Lock()

    def book(self):
        """
        Changes the room status to BOOKED if it's AVAILABLE.
        """
        with self.lock:
            if self.status == RoomStatus.AVAILABLE:
                self.status = RoomStatus.BOOKED
            else:
                raise ValueError("Room is not available for booking.")

    def check_in(self):
        """
        Changes the room status to OCCUPIED if it's BOOKED.
        """
        with self.lock:
            if self.status == RoomStatus.BOOKED:
                self.status = RoomStatus.OCCUPIED
            else:
                raise ValueError("Room is not booked.")

    def check_out(self):
        """
        Changes the room status to AVAILABLE if it's OCCUPIED.
        """
        with self.lock:
            if self.status == RoomStatus.OCCUPIED:
                self.status = RoomStatus.AVAILABLE
            else:
                raise ValueError("Room is not occupied.")


# -------------------------
# RESERVATION
# -------------------------

class Reservation:
    """
    Represents a reservation made by a guest for a room.
    """
    def __init__(
        self,
        reservation_id: str,
        guest: Guest,
        room: Room,
        check_in_date: date,
        check_out_date: date
    ):
        self.id = reservation_id
        self.guest = guest
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.status = ReservationStatus.CONFIRMED
        self.lock = Lock()

    def cancel(self):
        """
        Cancels the reservation (if it is still CONFIRMED) and frees the room.
        """
        with self.lock:
            if self.status == ReservationStatus.CONFIRMED:
                self.status = ReservationStatus.CANCELLED
                self.room.check_out()  # Mark the room as AVAILABLE
            else:
                raise ValueError("Reservation is not confirmed.")


# -------------------------
# HOTEL MANAGEMENT SYSTEM (Singleton Pattern)
# -------------------------

class HotelManagementSystem:
    """
    Manages rooms, reservations, and guests. Ensures only one instance
    via the Singleton pattern.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.guests: Dict[str, Guest] = {}
            cls._instance.rooms: Dict[str, Room] = {}
            cls._instance.reservations: Dict[str, Reservation] = {}
            cls._instance.lock = Lock()
        return cls._instance

    def add_guest(self, guest: Guest):
        self.guests[guest.id] = guest

    def get_guest(self, guest_id: str) -> Optional[Guest]:
        return self.guests.get(guest_id)

    def add_room(self, room: Room):
        self.rooms[room.id] = room

    def get_room(self, room_id: str) -> Optional[Room]:
        return self.rooms.get(room_id)

    def book_room(
        self,
        guest: Guest,
        room: Room,
        check_in_date: date,
        check_out_date: date
    ) -> Optional[Reservation]:
        """
        Reserves a room if it is AVAILABLE and returns the Reservation object.
        """
        with self.lock:
            if room.status == RoomStatus.AVAILABLE:
                room.book()
                reservation_id = self._generate_reservation_id()
                reservation = Reservation(
                    reservation_id,
                    guest,
                    room,
                    check_in_date,
                    check_out_date
                )
                self.reservations[reservation_id] = reservation
                return reservation
            return None

    def cancel_reservation(self, reservation_id: str):
        """
        Cancels a reservation by its ID.
        """
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            if reservation:
                reservation.cancel()
                del self.reservations[reservation_id]

    def check_in(self, reservation_id: str):
        """
        Checks a guest into the room if the reservation is CONFIRMED.
        """
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            if reservation and reservation.status == ReservationStatus.CONFIRMED:
                reservation.room.check_in()
            else:
                raise ValueError("Invalid reservation or reservation not confirmed.")

    def check_out(self, reservation_id: str, payment: Payment):
        """
        Checks a guest out of the room, processes payment, and removes the reservation.
        """
        with self.lock:
            reservation = self.reservations.get(reservation_id)
            if reservation and reservation.status == ReservationStatus.CONFIRMED:
                room = reservation.room
                # Calculate price based on the number of days
                days_stayed = (reservation.check_out_date - reservation.check_in_date).days
                amount = room.price * days_stayed
                if payment.process_payment(amount):
                    room.check_out()
                    del self.reservations[reservation_id]
                else:
                    raise ValueError("Payment failed.")
            else:
                raise ValueError("Invalid reservation or reservation not confirmed.")

    def _generate_reservation_id(self) -> str:
        """
        Generate a unique reservation identifier.
        """
        return f"RES{uuid.uuid4().hex[:8].upper()}"


# -------------------------
# DEMO
# -------------------------

class HotelManagementSystemDemo:
    """
    Demonstration of how to use the HotelManagementSystem.
    """
    @staticmethod
    def run():
        hotel_management_system = HotelManagementSystem()

        # Create guests
        guest1 = Guest("G001", "John Doe", "john@example.com", "1234567890")
        guest2 = Guest("G002", "Jane Smith", "jane@example.com", "9876543210")
        hotel_management_system.add_guest(guest1)
        hotel_management_system.add_guest(guest2)

        # Create rooms
        room1 = Room("R001", RoomType.SINGLE, 100.0)
        room2 = Room("R002", RoomType.DOUBLE, 200.0)
        hotel_management_system.add_room(room1)
        hotel_management_system.add_room(room2)

        # Book a room
        check_in_date = date.today()
        check_out_date = check_in_date + timedelta(days=3)
        reservation1 = hotel_management_system.book_room(guest1, room1, check_in_date, check_out_date)
        if reservation1:
            print(f"Reservation created: {reservation1.id}")
        else:
            print("Room not available for booking.")

        # Check-in
        hotel_management_system.check_in(reservation1.id)
        print(f"Checked in: {reservation1.id}")

        # Check-out and process payment
        payment = CreditCardPayment()
        hotel_management_system.check_out(reservation1.id, payment)
        print(f"Checked out: {reservation1.id}")

        # Cancel a reservation
        # (In real usage, you'd typically only cancel prior to check-in,
        # but this is just a demonstration.)
        hotel_management_system.cancel_reservation(reservation1.id)
        print(f"Reservation cancelled: {reservation1.id}")


if __name__ == "__main__":
    HotelManagementSystemDemo.run()
