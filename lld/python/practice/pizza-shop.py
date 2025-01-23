from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict

# ----------------------
# Behavioral Patterns
# ----------------------

# 1. Observer Pattern (Order status notifications)
class OrderObserver(ABC):
    @abstractmethod
    def update(self, order: 'Order'):
        pass

# 2. State Pattern (Order lifecycle states)
class OrderState(ABC):
    @abstractmethod
    def process_order(self, order: 'Order'):
        pass

    @abstractmethod
    def cancel_order(self, order: 'Order'):
        pass

# 3. Strategy Pattern (Payment methods)
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

# 4. Command Pattern (Kitchen operations)
class KitchenCommand(ABC):
    @abstractmethod
    def execute(self):
        pass

# ----------------------
# Core Domain Classes
# ----------------------

class PizzaSize(Enum):
    SMALL = 8
    MEDIUM = 10
    LARGE = 12

class PizzaBase(Enum):
    THIN = "Thin Crust"
    THICK = "Thick Crust"
    GLUTEN_FREE = "Gluten Free"

class Topping(Enum):
    CHEESE = 1.00
    PEPPERONI = 2.50
    MUSHROOMS = 1.75
    OLIVES = 1.50
    ANCHOVIES = 3.00

class Pizza:
    def __init__(self, name: str, base_price: float):
        self.name = name
        self.base_price = base_price
        self.size = PizzaSize.MEDIUM
        self.base = PizzaBase.THICK
        self.toppings: List[Topping] = []

    def calculate_cost(self) -> float:
        topping_cost = sum(t.value for t in self.toppings)
        return self.base_price + topping_cost + self.size.value

    def __str__(self):
        return f"{self.size.name} {self.name} Pizza ({self.base.value})"

# ----------------------
# State Pattern Implementation
# ----------------------

class NewOrderState(OrderState):
    def process_order(self, order: 'Order'):
        print("Order received, processing payment...")
        order.state = PaymentPendingState()

    def cancel_order(self, order: 'Order'):
        print("Order cancelled before processing")
        order.state = CancelledState()

class PaymentPendingState(OrderState):
    def process_order(self, order: 'Order'):
        if order.process_payment():
            print("Payment successful! Preparing order...")
            order.state = InPreparationState()
        else:
            print("Payment failed! Order cancelled")
            order.state = CancelledState()

    def cancel_order(self, order: 'Order'):
        print("Order cancelled during payment processing")
        order.state = CancelledState()

class InPreparationState(OrderState):
    def process_order(self, order: 'Order'):
        print("Order being prepared...")
        order.state = ReadyForDeliveryState()

    def cancel_order(self, order: 'Order'):
        print("Order cancelled during preparation")
        order.state = CancelledState()

class ReadyForDeliveryState(OrderState):
    def process_order(self, order: 'Order'):
        print("Order out for delivery!")
        order.state = DeliveredState()

    def cancel_order(self, order: 'Order'):
        print("Too late to cancel - order already prepared")

class DeliveredState(OrderState):
    def process_order(self, order: 'Order'):
        print("Order already delivered")

    def cancel_order(self, order: 'Order'):
        print("Cannot cancel delivered order")

class CancelledState(OrderState):
    def process_order(self, order: 'Order'):
        print("Cannot process cancelled order")

    def cancel_order(self, order: 'Order'):
        print("Order already cancelled")

# ----------------------
# Observer Implementation
# ----------------------

class Customer(OrderObserver):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, order: 'Order'):
        print(f"Notification for {self.name}: Order status changed to {order.state.__class__.__name__}")

# ----------------------
# Strategy Implementations
# ----------------------

class CreditCardPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        print(f"Processing credit card payment for ${amount}")
        return True

class CashPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        print(f"Preparing cash transaction for ${amount}")
        return True

class PayPalPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        print(f"Redirecting to PayPal for ${amount}")
        return True

# ----------------------
# Command Pattern Implementation
# ----------------------

class PreparePizzaCommand(KitchenCommand):
    def __init__(self, pizza: Pizza):
        self.pizza = pizza

    def execute(self):
        print(f"Preparing {self.pizza} with toppings:")
        for topping in self.pizza.toppings:
            print(f"- {topping.name}")
        print("Pizza ready for baking!")

class BakePizzaCommand(KitchenCommand):
    def __init__(self, pizza: Pizza):
        self.pizza = pizza

    def execute(self):
        print(f"Baking {self.pizza} at 400°F for 15 minutes")

# ----------------------
# Order Management
# ----------------------

class Order:
    def __init__(self, customer: Customer):
        self.state: OrderState = NewOrderState()
        self.pizzas: List[Pizza] = []
        self.customer = customer
        self._observers: List[OrderObserver] = [customer]
        self.payment_strategy: PaymentStrategy = None

    def attach(self, observer: OrderObserver):
        self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def process_order(self):
        self.state.process_order(self)
        self.notify()

    def cancel_order(self):
        self.state.cancel_order(self)
        self.notify()

    def total_cost(self) -> float:
        return sum(p.calculate_cost() for p in self.pizzas)

    def process_payment(self) -> bool:
        if self.payment_strategy:
            return self.payment_strategy.pay(self.total_cost())
        return False

    def add_pizza(self, pizza: Pizza):
        self.pizzas.append(pizza)

    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy

# ----------------------
# Usage Example
# ----------------------

if __name__ == "__main__":
    # Create customer
    john = Customer("John Doe")
    
    # Create order
    order = Order(john)
    
    # Add pizzas
    margherita = Pizza("Margherita", 10.00)
    margherita.toppings.extend([Topping.CHEESE, Topping.OLIVES])
    order.add_pizza(margherita)
    
    pepperoni = Pizza("Pepperoni", 12.00)
    pepperoni.size = PizzaSize.LARGE
    pepperoni.toppings.append(Topping.PEPPERONI)
    order.add_pizza(pepperoni)
    
    # Set payment strategy
    order.set_payment_strategy(CreditCardPayment())
    
    # Process order
    print("=== Processing Order ===")
    order.process_order()  # New -> Payment Pending
    order.process_order()  # Process payment
    order.process_order()  # Preparation
    order.process_order()  # Delivery
    
    print("\n=== Order Total ===")
    print(f"Total: ${order.total_cost():.2f}")
    
    print("\n=== Trying to Cancel ===")
    order.cancel_order()
    

class PizzaFactory:
    def create_pizza(self, pizza_type: str) -> Pizza:
        if pizza_type == "MARGHERITA":
            pizza = Pizza("Margherita", 10.00)
            pizza.toppings = [Topping.CHEESE, Topping.OLIVES]
            return pizza
        elif pizza_type == "PEPPERONI":
            pizza = Pizza("Pepperoni", 12.00)
            pizza.toppings = [Topping.CHEESE, Topping.PEPPERONI]
            return pizza
        else:
            raise ValueError("Invalid pizza type")

# Usage:
factory = PizzaFactory()
margherita = factory.create_pizza("MARGHERITA")

class PizzaBuilder:
    def __init__(self, name: str, base_price: float):
        self.pizza = Pizza(name, base_price)
    
    def set_size(self, size: PizzaSize) -> 'PizzaBuilder':
        self.pizza.size = size
        return self
    
    def set_base(self, base: PizzaBase) -> 'PizzaBuilder':
        self.pizza.base = base
        return self
    
    def add_topping(self, topping: Topping) -> 'PizzaBuilder':
        self.pizza.toppings.append(topping)
        return self
    
    def build(self) -> Pizza:
        return self.pizza

# Usage:
custom_pizza = (PizzaBuilder("Custom", 9.00)
                .set_size(PizzaSize.LARGE)
                .set_base(PizzaBase.GLUTEN_FREE)
                .add_topping(Topping.MUSHROOMS)
                .add_topping(Topping.OLIVES)
                .build())

class PizzaShop:
    def __init__(self):
        self.factory = PizzaFactory()
        self.builder = PizzaBuilder

    def order_predefined(self, pizza_type: str) -> Pizza:
        return self.factory.create_pizza(pizza_type)

    def order_custom(self, name: str, base_price: float) -> PizzaBuilder:
        return self.builder(name, base_price)

# Usage:
shop = PizzaShop()

# Predefined pizza
pepperoni = shop.order_predefined("PEPPERONI")

# Custom pizza
veggie_special = (shop.order_custom("Veggie Special", 11.00)
                  .set_size(PizzaSize.MEDIUM)
                  .add_topping(Topping.MUSHROOMS)
                  .add_topping(Topping.OLIVES)
                  .build())