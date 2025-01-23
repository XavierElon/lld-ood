/*
Decorator

Summary
Attaches additional responsibilities or behaviors to an object dynamically by placing these objects inside special wrapper objects.
When to use
	•	When you want to add responsibilities (features, behaviors) dynamically, without subclassing.
	•	When extension by inheritance would result in too many subclasses.
*/
// Base interface
class Coffee {
  getCost() {
    return 0
  }
  getDescription() {
    return ''
  }
}

// Concrete Component
class SimpleCoffee extends Coffee {
  getCost() {
    return 5
  }
  getDescription() {
    return 'Simple coffee'
  }
}

// Decorator
class CoffeeDecorator extends Coffee {
  constructor(coffee) {
    super()
    this.decoratedCoffee = coffee
  }
  getCost() {
    return this.decoratedCoffee.getCost()
  }
  getDescription() {
    return this.decoratedCoffee.getDescription()
  }
}

// Concrete Decorator
class MilkDecorator extends CoffeeDecorator {
  getCost() {
    return this.decoratedCoffee.getCost() + 2
  }
  getDescription() {
    return this.decoratedCoffee.getDescription() + ', milk'
  }
}

// Usage
let coffee = new SimpleCoffee()
coffee = new MilkDecorator(coffee)
console.log(coffee.getCost(), coffee.getDescription())
// 7, "Simple coffee, milk"
