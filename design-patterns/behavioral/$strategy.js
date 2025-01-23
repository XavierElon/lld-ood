/*
Defines a family of algorithms, encapsulates each one, and makes them interchangeable. 
Strategy lets the algorithm vary independently from clients that use it.
When to use
	•	When you have multiple ways (algorithms/behaviors) to perform an operation, and you want to choose which one at runtime.
	•	To avoid large conditional statements and to enable easy switching of algorithms.
*/

class PaymentStrategy {
  pay(amount) {}
}

class CreditCardStrategy extends PaymentStrategy {
  constructor(cardNumber) {
    super()
    this.cardNumber = cardNumber
  }

  pay(amount) {
    console.log(`Paying \$${amount} using Credit Card ${this.cardNumber}.`)
  }
}

class PayPalStrategy extends PaymentStrategy {
  constructor(email) {
    super()
    this.email = email
  }
  pay(amount) {
    console.log(`Paying \$${amount} using PayPal account ${this.email}.`)
  }
}

// Context
class ShoppingCart {
  constructor() {
    this.total = 0
  }
  addItem(price) {
    this.total += price
  }
  pay(paymentStrategy) {
    paymentStrategy.pay(this.total)
  }
}

const cart = new ShoppingCart()
cart.addItem(20)
cart.addItem(30)
cart.pay(new CreditCardStrategy('1234-5678-9012-3456'))
cart.addItem(100)
cart.pay(new PayPalStrategy('xavierelon93@gmail.com'))
