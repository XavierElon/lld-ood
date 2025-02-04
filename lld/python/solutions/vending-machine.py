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

import time
from threading import Thread, Lock, Condition
from enum import Enum
from abc import ABC, abstractmethod

# Enums for currency denominations
class Coin(Enum):
    PENNY = 0.01
    NICKEL = 0.05
    DIME = 0.1
    QUARTER = 0.25
    
class Note(Enum):
    ONE = 1
    FIVE = 5
    TEN = 10
    TWENTY = 20
    
# PRODUCT
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
# INVENTORY MANAGEMENT
class Inventory:
    def __init__(self):
        self.products = {}
        
    def add_product(self, product, quantity):
        self.products[product] = quantity
        
    def remove_product(self, product):
        if product in self.products:
            del self.products[product]
            
    def update_quantity(self, product, quantity):
        self.products[product] = quantity
    
    def get_quantity(self, product):
        return self.products.get(product, 0)
    
    def is_available(self, product):
        return self.get_quantity(product) > 0
    
class VendingMachineState(ABC):
    @abstractmethod
    def select_product(self, product):
        pass
    
    @abstractmethod
    def insert_coin(self, coin):
        pass

    @abstractmethod
    def insert_note(self, note):
        pass
    
    @abstractmethod
    def dispense_product(self):
        pass
    
    @abstractmethod
    def return_change(self):
        pass
    
class IdleState(VendingMachineState):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine
        
    def select_product(self, product):
        if self.vending_machine.inventory.is_available(product):
            self.vending_machine.selected_product = product
            self.vending_machine.set_state(self.vending_machine.ready_state)
            print(f"Product seelcted: {product.name}")
        else:
            print(f"Product selected: {product.name}")
            
    def insert_coin(self, coin):
        print("Please select a product first.")
        
    def insert_note(self, note):
        print("Please select a product first.")\
    
    def dispense_product(self):
        print("Please select a product and make payment.")
        
    def return_change(self):
        print("No change to return.")
        

class ReadyState(VendingMachineState):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine
        
    def select_product(self, product):
        print("Product already selected. Please make payment.")
        
    def insert_coin(self, coin):
        self.vending_machine.total_payment += coin.value
        print(f"Inserted {coin.name} (${coin.value:.2f})")
        self.check_payment_status()
        
    def insert_note(self, note):
        self.vending_machine.total_payment += note.value
        print(f"Inserted {note.name} (${note.value:.2f})")
        self.check_payment_status()
    
    def check_payment_status(self):
        if self.vending_machine.total_payment >= self.vending_machine.selected_product.price:
            self.vending_machine.set_state(self.vending_machine.dispense_state)
            print("Payment sufficient. Please dispense product.")
        else:
            remaining = self.vending_machine.selected_product.price - self.vending_machine.total_payment
            print(f"Remaining: ${remaining:.2f}")
            
    def dispense_product(self):
        print("Please complete payment first.")
    
    def return_change(self):
        change = self.vending_machine.total_payment
        if change > 0:
            print(f"Returning ${change:.2f}")
            self.vending_machine.total_payment = 0.0
        self.vending_machine.set_state(self.vending_machine.idle_state)
        self.vending_machine.reset_selected_product()
        
class DispenseState(VendingMachineState):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    def select_product(self, product):
        print("Please collect current transaction first.")

    def insert_coin(self, coin):
        print("Please collect current transaction first.")

    def insert_note(self, note):
        print("Please collect current transaction first.")

    def dispense_product(self):
        product = self.vending_machine.selected_product
        if self.vending_machine.inventory.get_quantity(product) > 0:
            self.vending_machine.inventory.update_quantity(
                product, 
                self.vending_machine.inventory.get_quantity(product) - 1
            )
            print(f"Dispensing {product.name}")
            self.vending_machine.set_state(self.vending_machine.return_change_state)
        else:
            print("Product out of stock! Returning payment.")
            self.vending_machine.set_state(self.vending_machine.ready_state)
            self.vending_machine.return_change()
        
        def return_change(self):
            print("Please dispense product first.") 
            
    def return_change(self):
        print("Please dispense product first.")
    
class ReturnChangeState(VendingMachineState):
    def __init__(self, vending_machine):
        self.vending_machine = vending_machine

    def select_product(self, product):
        print("Please collect change first.")

    def insert_coin(self, coin):
        print("Please collect change first.")

    def insert_note(self, note):
        print("Please collect change first.")

    def dispense_product(self):
        print("Product already dispensed. Collect change.")
        
    def return_change(self):
        product = self.vending_machine.selected_product
        change = self.vending_machine.total_payment - product.price
        if change > 0:
            print(f"Returning change: ${change:.2f}")
        self.vending_machine.total_payment = 0.0
        self.vending_machine.reset_selected_product()
        self.vending_machine.set_state(self.vending_machine.idle_state)
        
class VendingMachine:
    _instance = None
    _lock = Lock()
    
    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.inventory = Inventory()
                cls._instance.idle_state = IdleState(cls._instance)
                cls._instance.ready_state = ReadyState(cls._instance)
                cls._instance.dispense_state = DispenseState(cls._instance)
                cls._instance.return_change_state = ReturnChangeState(cls._instance)
                cls._instance.current_state = cls._instance.idle_state
                cls._instance.selected_product = None
                cls._instance.total_payment = 0.0
        return cls._instance
    
    def set_state(self, state):
        self.current_state = state
    
    def reset_selected_product(self):
        self.current_state = None
        
    # Public Methods
    def select_product(self, product):
        self.current_state.select_product(product)
        
    def insert_coin(self, coin):
        self.current_state.insert_coin(coin)
        
    def insert_note(self, note):
        self.current_state.insert_note(note)
        
    def dispense_product(self):
        self.current_state.dispense_product()
    
    def return_change(self):
        self.current_state.return_change()
        

# Demo and test cases
class VendingMachineDemo:
    @staticmethod
    def run():
        vm = VendingMachine()
        coke = Product("Coke", 1.50)
        pepsi = Product("Pepsi", 1.75)
        water = Product("Water", 1.00)

        vm.inventory.add_product(coke, 3)
        vm.inventory.add_product(pepsi, 2)
        vm.inventory.add_product(water, 5)

        print("\n--- Test 1: Successful purchase ---")
        vm.select_product(coke)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)
        vm.insert_coin(Coin.QUARTER)  # 6 * 0.25 = $1.50
        vm.dispense_product()
        vm.return_change()

        print("\n--- Test 2: Insufficient funds ---")
        vm.select_product(pepsi)
        vm.insert_coin(Coin.QUARTER)  # 0.25
        vm.insert_note(Note.ONE)      # 1.00 (total 1.25)
        vm.dispense_product()         # Needs 1.75
        vm.insert_coin(Coin.QUARTER)  # 0.25 (total 1.50)
        vm.insert_coin(Coin.QUARTER)  # 0.25 (total 1.75)
        vm.dispense_product()
        vm.return_change()

        print("\n--- Test 3: Out of stock ---")
        vm.select_product(water)
        vm.insert_note(Note.FIVE)  # 5.00
        vm.dispense_product()
        vm.select_product(water)
        vm.insert_note(Note.ONE)
        vm.dispense_product()

if __name__ == "__main__":
    VendingMachineDemo.run()