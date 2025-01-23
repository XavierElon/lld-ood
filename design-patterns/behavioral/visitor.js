/*
Visitor

Summary:
	•	Separates an algorithm from the object structure on which it operates.
	•	Allows you to add new operations to existing class hierarchies without modifying those classes.

When to use:
	•	When you have a complex object structure (like an AST for a compiler) and want to perform operations on many distinct object types.
	•	When the object structure rarely changes, but you need to add new operations frequently.
*/
// Visitable interface
class Element {
  accept(visitor) {}
}

// Concrete Elements
class Book extends Element {
  constructor(price) {
    super()
    this.price = price
  }
  accept(visitor) {
    visitor.visitBook(this)
  }
}

class Fruit extends Element {
  constructor(price, weight) {
    super()
    this.price = price
    this.weight = weight
  }
  accept(visitor) {
    visitor.visitFruit(this)
  }
}

// Visitor interface
class ShoppingCartVisitor {
  visitBook(book) {}
  visitFruit(fruit) {}
}

// Concrete Visitor
class ShoppingCart extends ShoppingCartVisitor {
  visitBook(book) {
    console.log(`Book costs \$${book.price}`)
  }
  visitFruit(fruit) {
    console.log(`Fruit costs \$${fruit.price * fruit.weight} total`)
  }
}

// Usage
const items = [
  new Book(10),
  new Fruit(2, 3) // $2 per kg, 3 kg
]
const visitor = new ShoppingCart()
items.forEach((item) => item.accept(visitor))
// Book costs $10
// Fruit costs $6 total
