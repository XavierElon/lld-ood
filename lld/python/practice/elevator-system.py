from enum import Enum
from threading import Thread, Lock, Condition
import time

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

    def add_request(self, request: Request):
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
            
            print(f"Elevator {self.id} [{self.current_direction.name}] → Floor {self.current_floor}")
            time.sleep(1)

    def process_request(self, request: Request):
        print(f"\nElevator {self.id} processing request: {request.source_floor}→{request.destination_floor}")
        
        # Move to pick up passenger
        if self.current_floor != request.source_floor:
            print(f"Elevator {self.id} moving to pickup floor {request.source_floor}")
            self.move_to_floor(request.source_floor)
            print(f"Elevator {self.id} picked up passengers at floor {request.source_floor}")
        
        # Move to drop off passenger
        if request.source_floor != request.destination_floor:
            print(f"Elevator {self.id} moving to destination floor {request.destination_floor}")
            self.move_to_floor(request.destination_floor)
            print(f"Elevator {self.id} dropped off passengers at floor {request.destination_floor}")

    def run(self):
        while self.running:
            request = self.get_next_request()
            if request:
                self.process_request(request)

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
        with self.elevators[0].lock:  # Lock for consistent state comparison
            return min(self.elevators, 
                      key=lambda e: (abs(e.current_floor - source_floor), len(e.requests)))

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