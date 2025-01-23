# /*
# Requirements
# The parking lot should have multiple levels, each level with a certain number of parking spots.
# The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
# Each parking spot should be able to accommodate a specific type of vehicle.
# The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
# The system should track the availability of parking spots and provide real-time information to customers.
# The system should handle multiple entry and exit points and support concurrent access.

# Classes, Interfaces and Enumerations
# The ParkingLot class follows the Singleton pattern to ensure only one instance of the parking lot exists. 
# It maintains a list of levels and provides methods to park and unpark vehicles.
# The Level class represents a level in the parking lot and contains a list of parking spots. It handles parking and unparking of vehicles within the level.
# The ParkingSpot class represents an individual parking spot and tracks the availability and the parked vehicle.
# The Vehicle class is an abstract base class for different types of vehicles. It is extended by Car, Motorcycle, and Truck classes.
# The VehicleType enum defines the different types of vehicles supported by the parking lot.
# Multi-threading is achieved through the use of synchronized keyword on critical sections to ensure thread safety.
# The Main class demonstrates the usage of the parking lot system.
# */

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import math

class PaymentMethod(Enum):
    CASH = 'CASH'
    CREDIT_CARD = 'CREDIT_CARD'
    DEBIT_CARD = 'DEBIT_CARD'
    MOBILE_PAYMENT = 'MOBILE_PAYMENT'
    
class Payment:
    def __init__(self, amount: float, method: PaymentMethod):
        self.amount = amount
        self.method = method
        self.timestamp = datetime.now()
        self.status = 'Pending'
        
    def process_payment(self):
        print(f"Processing {self.method.value} payment of ${self.amount:.2f}...")
        self.status = 'Completed'
        print(f"Payment of ${self.amount:.2f} completed via {self.method.value}.")
        return self.status == 'Completed'

class Invoice:
    def __init__(self, vehicle: 'Vehicle', entry_time: datetime, exit_time: datetime, amount: float):
        self.vehicle = vehicle
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.amount = amount
        self.payment = None
        
    def generate_invoice(self):
        duration = self.exit_time - self.entry_time
        hours = duration.total_seconds() / 3600
        print(f"Generating invoice for {self.vehicle.license_plate}:")
        print(f"Vehicle Type: {self.vehicle.get_type().value}")
        print(f"Parking Duration: {hours:.2f} hours")
        print(f"Amount Due: ${self.amount:.2f}")
        
    def make_payment(self, method: PaymentMethod):
        self.payment = Payment(self.amount, method)
        success = self.payment.process_payment()
        if success:
            print('Payment was successful')
        else:
            print('Payment failed')
        return success
    
class VehicleType(Enum):
    CAR = 'CAR'
    MOTORCYCLLE = 'MOTORCYCLE'
    TRUCK = 'TRUCK'
    
class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        if type(self) is Vehicle:
            raise TypeError("Cannot instantiate abstract class Vehicle directly")
        self.license_plate = license_plate
        self.type = vehicle_type
        self.entry_time = datetime = None
        self.exit_time = datetime = None
        
    def get_type(self) -> VehicleType:
        return self.type
    
    def set_entry_tikme(self, time: datetime):
        self.entry_time = time
        
    def set_exit_time(self, time: datetime):
        self.exit_time = time
        
class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLLE)
        
class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)
        
class Truck(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.TRUCK)
        
class ParkingSpot:
    def __init__(self, spot_number: int, vehicle_type: VehicleType):
        self.spot_number = spot_number
        self.vehicle_type = vehicle_type
        self.parked_vehicle = Vehicle = None
        
    def is_available(self) -> bool:
        return self.parked_vehicle is None
    
    def park_vehicle(self, vehicle: Vehicle):
        if self.is_available() and vehicle.get_type() == self.vehicle_type:
            self.parked_vehicle = vehicle
            vehicle.set_entry_time(datetime.now())
            print(f"Vehicle {vehicle.license_plate} parked at Spot {self.get_spot_number()} on Level {self.vehicle_type.value}.")
        else:
            raise ValueError('Invalid vehicle type or spot already occupied.')
    
    def unpark_vehicle(self):
        if not self.is_available():
            self.parked_vehicle.set_exit_time(datetime.now())
            print(f"Vehicle {self.license_plate} unparked from Spot {self.get_spot_number()}")
            self.parked_vehicle = None
        else:
            raise ValueError('Parking spot is already empty')
    
    def get_parked_vehicle(self) -> Vehicle:
        return self.parked_vehicle
    
    def get_vehicle_type(self) -> VehicleType:
        return self.vehicle_type
    
    def get_spot_number(self) -> int:
        return self.spot_number
    
class Level:
    def __init__(self, floor: int, num_spots: int):
        self.floor(floor)
        self.parking_spots = []
        
        spots_for_bikes = 0.1
        spots_for_cars = 0.7
        spots_for_trucks = 0.2
        
        num_bikes = math.floor(num_spots * spots_for_bikes)
        num_cars = math.floor(num_spots * spots_for_cars)
        num_trucks = math.floor(num_spots * spots_for_trucks)
        
        spot_number = 1
        for _ in range(num_bikes):
            self.parking_spots.append(ParkingSpot(spot_number, VehicleType.MOTORCYCLE))
            spot_number += 1
        
        for _ in range(num_cars):
            self.parking_spots.append(ParkingSpot(spot_number, VehicleType.CAR))
            spot_number +=1
        
        for _ in range(num_trucks):
            self.parking_spots.append(ParkingSpot(spot_number, VehicleType.TRUCK))
            spot_number += 1
        
    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for spot in self.parking_spots:
            if spot.is_available() and spot.get_vehicle_type() == vehicle.get_type():
                try:
                    spot.park_vehicle(vehicle)
                    return True
                except ValueError:
                    continue
        return False
    
    def unpark_vehicle(self, vehicle: Vehicle) -> Invoice:
        for spot in self.parking_spots:
            if not spot.is_available() and spot.get_parked_vehicle() == vehicle:
                spot.unpark_vehicle()
                invoice = self.generate_invoice(vehicle)
                return invoice
        return None

    def generate_invoice(self, vehicle: Vehicle) -> Invoice:
        if vehicle.entry_time is None or vehicle.exit_time is None:
            raise ValueError("Vehicle has invalid entry or exit time.")
        
        # Define rate per hour based on vehicle type
        rate_per_hour = {
            VehicleType.MOTORCYCLE: 1.0,  # $1 per hour
            VehicleType.CAR: 2.0,         # $2 per hour
            VehicleType.TRUCK: 3.5        # $3.5 per hour
        }

        duration = vehicle.exit_time - vehicle.entry_time
        hours = duration.total_seconds() / 3600
        amount = math.ceil(hours) * rate_per_hour[vehicle.get_type()]  # Round up to next hour

        invoice = Invoice(vehicle, vehicle.entry_time, vehicle.exit_time, amount)
        invoice.generate_invoice()
        return invoice
     
    def display_availability(self):
        print(f"Level {self.floor} Availability:")
        for spot in self.parking_spots:
            if spot.is_available():
                status = f"Available For {spot.get_vehicle_type().value}"
            else:
                status = f"Occupied By {spot.get_parked_vehicle().get_type().value} ({spot.get_parked_vehicle().license_plate})"
            print(f"Spot {spot.get_spot_number()}: {status}")
        print("\n")   

class ParkingLot:
    _instance = None
    
    def __init__(self):
        if ParkingLot._instance is not None:
            raise Exception("Use ParkingLot.get_instance() to get the singleton instance")
        self.levels = []
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ParkingLot()
        return cls._instance
    
    def add_level(self, level: Level):
        self.levels.append(level)
        print(f"Added Level {level.floor} with {len(level.parking_spots)} spots.")
        
    def park_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            if level.park_vehicle(vehicle):
                print(f"Vehicle {vehicle.license_plate} parked successfully. \n")
                return True
        print(f"Could not park vehicle {vehicle.license_plate}. \n")
        return False
    
    def unpark_vehicle(self, vehicle: Vehicle) -> bool:
        for level in self.levels:
            invoice = level.unpark_vehicle(vehicle)
            if invoice:
                print("Vehicle unparked successfully.")
                
                payment_method = self.select_payment_method()
                if invoice.make_payment(payment_method):
                    print("Payment processed successfully. \n")
                else:
                    print("Payment failed. \n")
                return True
        print(f"Could not unpark vehicle {vehicle.license_plate} \n")
        return False
    
    def select_payment_method(self) -> PaymentMethod:
        print('Select Payment Method: ')
        for method in PaymentMethod:
            print(f"- {method.name}")
        selected_method = PaymentMethod.CREDIT_CARD
        print(f"Selected Payment Method: {selected_method.value}")
        return selected_method
    
    def display_availability(self):
        for level in self.levels:
            level.display_availability()


if __name__ == "__main__":
    # Initialize the parking lot singleton
    parking_lot = ParkingLot.get_instance()

    # Create and add levels
    parking_lot.add_level(Level(1, 100))
    parking_lot.add_level(Level(2, 80))

    # Create vehicles
    car = Car('ABC123')
    truck = Truck('XYZ789')
    motorcycle = Motorcycle('M1234')

    # Park vehicles
    parking_lot.park_vehicle(car)
    parking_lot.park_vehicle(truck)
    parking_lot.park_vehicle(motorcycle)

    # Simulate some time passing
    import time
    time.sleep(2)  # Sleep for 2 seconds to simulate parking duration

    # Display availability
    parking_lot.display_availability()

    # Unpark a vehicle
    parking_lot.unpark_vehicle(motorcycle)

    # Display updated availability
    parking_lot.display_availability()

    # Unpark remaining vehicles
    parking_lot.unpark_vehicle(car)
    parking_lot.unpark_vehicle(truck)

    # Final availability
    parking_lot.display_availability()