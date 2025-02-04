# Requirements
# The vending machine should support multiple products with different prices and quantities.
# The machine should accept coins and notes of different denominations.
# The machine should dispense the selected product and return change if necessary.
# The machine should keep track of the available products and their quantities.
# The machine should handle multiple transactions concurrently and ensure data consistency.
# The machine should provide an interface for restocking products and collecting money.
# The machine should handle exceptional scenarios, such as insufficient funds or out-of-stock products.

# Classes, Interfaces and Enumerations
# The Product class represents a product in the vending machine, with properties such as name and price.
# The Coin and Note enums represent the different denominations of coins and notes accepted by the vending machine.
# The Inventory class manages the available products and their quantities in the vending machine. It uses a concurrent hash map to ensure thread safety.
# The VendingMachineState interface defines the behavior of the vending machine in different states, such as idle, ready, and dispense.
# The IdleState, ReadyState, and DispenseState classes implement the VendingMachineState interface and define the specific behaviors for each state.
# The VendingMachine class is the main class that represents the vending machine. It follows the Singleton pattern to ensure only one instance of the vending machine exists.
# The VendingMachine class maintains the current state, selected product, total payment, and provides methods for state transitions and payment handling.
# The VendingMachineDemo class demonstrates the usage of the vending machine by adding products to the inventory, selecting products, inserting coins and notes, dispensing products, and returning change.

# Design Pattern Analysis:

# Active Object Pattern:
# Usage: Each Elevator runs in its own thread, managing its own state and processing requests asynchronously.
# Why: Decouples method execution from invocation, allowing elevators to operate concurrently and independently. 
# This pattern helps manage shared resources (floor requests) safely across threads.

# Producer-Consumer Pattern:
# Usage: The add_request method (producer) adds requests to a shared queue, while get_next_request (consumer) retrieves and processes them.
# Why: Coordinates communication between the controller thread (producing requests) and elevator threads (consuming requests). The Condition variable ensures thread-safe queue operations.

# Command Pattern:
# Usage: The Request class encapsulates elevator movement commands (source and destination floors).
# Why: Allows parameterization of elevator operations and enables queuing of requests. Makes it easy to extend the system with different request types.

# Strategy Pattern (Emerging):
# Usage: The find_optimal_elevator method implements a simple strategy (nearest elevator selection).
# Why: While currently implemented as a simple algorithm, the structure allows for different elevator selection strategies to be plugged in easily.

# Observer Pattern (Similar Mechanism):
# Usage: The Condition variable in Elevator uses notification mechanism to alert waiting threads about new requests.
# Why: Enables efficient waiting for state changes without busy-waiting, similar to observer notification systems.


import time
from threading import Thread, Lock, Condition
from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    
class Request:
    def __init__(self, source_floor, destination_floor):
        self.source_floor = source_floor
        self.destination_floor = destination_floor

class Elevator:
    def __init__(self, id: int, capacity: int):
        self.id = id
        self.capacity = capacity
        self.current_floor = 1
        self.current_direction = Direction.UP
        self.requests = []
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.running = True
    
    def add_requests(self, request: Request):
        with self.lock:
            if len(self.requests) < self.capacity:
                self.requests.append(request)
                print(f"Elevator {self.id} queued request: {request.source_floor}→{request.destination_floor}")
                self.condition.notify_all()
                
    def get_next_request(self) -> Request:
        with self.lock:
            while self.running and not self.requests:
                self.condition.wait()
            return self.requests.pop(0) if self.requests else None
        
    def move_to_floor(self, target_floor: int):
        while self.current_floor != target_floor and self.running:
            if self.current_floor < target_floor:
                self.current_direction = Direction.UP
                self.current_floor += 1
            else:
                self.current_direction = Direction.DOWN
                self.current_floor -= 1
                
            print(f"Elevator {self.id} [{self.current_direction.name}] -> Floor {self.current_floor}")
            time.sleep(1)
            
    def process_request(self, request: Request):
        print(f"\nElevator {self.id} processing request: {request.source_floor}->{request.destination_floor}")
        
        if self.current_floor != request.source_floor:
            print(f"Elevator {self.id} moving to pickup floor {request.source_floor}")
            self.move_to_floor(request.source_floor)
            print(f"Elevator {self.id} picked up passengers at floor {request.source_floor}")
            
        if request.source_floor != request.destination_floor:
            print(f"Elevator {self.id} moving to destination floor {request.destination_floor}")
            self.move_to_floor(request.destination_floor)
            print(f"Elevator {self.id} dropped off passengers at floor {request.destination_floor}")
        
    def run(self):
        with self.lock:
            self.running = False
            self.condition.notify_all()
            
    def stop(self):
        with self.lock:
            self.running = False
            self.condition.notify_all()
            
class ElevatorController:
    def __init__(self, num_elevators: int, capacity: int):
        self.elevators = [Elevator(i+1, capacity) for i in range(num_elevators)]
        for elevator in self.elevators:
            Thread(target=elevator.run, daemon=True).start()
            
    def request_elevator(self, source_floor: int, destination_floor: int):
        optimal_elevator = self.find_optimal_elevator(source_floor)
        if optimal_elevator:
            optimal_elevator.add_request(Request(source_floor, destination_floor))
            
    def find_optimal_elevator(self, source_floor: int) -> Elevator:
        with self.elevators[0].lock:
            return min(self.elevators, key=lambda e: (abs(e.current_floor - source_floor), len(e.requests)))
        
    def shutdown(self):
        for elevator in self.elevators:
            elevator.stop()
            
class ElevatorSystemDemo:
    @staticmethod
    def run():
        controller = ElevatorController(3, 5)
        try:
            controller.request_elevator(10, 12)
            time.sleep(2)
            controller.request_elevator(1, 7)
            time.sleep(3)
            controller.request_elevator(2, 5)
            time.sleep(1)
            controller.request_elevator(1, 9)
            
            while True:
                time.sleep(1)
            
        except KeyboardInterrupt:
            controller.shutdown()
            print("\nElevator system stopped safely.")
            
if __name__ == "__main__":
    ElevatorSystemDemo.run()
