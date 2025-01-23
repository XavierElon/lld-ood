/*
 Prototype

Summary:
	•	Clones existing objects instead of creating new ones from scratch.
	•	Reduces the overhead of creating heavy objects repeatedly.
	•	Each class implements its own clone method, returning a copy of itself.

When to use:
	•	When object creation is expensive (complex initialization) and you need many instances.
	•	When you want to avoid subclassing for every possible configuration.
*/
// Prototype interface
class Shape {
  clone() {
    throw new Error('clone() not implemented')
  }
}

// Concrete Prototype
class Circle extends Shape {
  constructor(radius) {
    super()
    this.radius = radius
  }

  clone() {
    // Return a new Circle with the same radius
    return new Circle(this.radius)
  }
}

// Usage
const originalCircle = new Circle(10)
const clonedCircle = originalCircle.clone()
console.log(clonedCircle.radius) // 10
console.log(originalCircle !== clonedCircle) // true (different instances)
