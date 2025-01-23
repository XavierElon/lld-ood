/*
Adapter (aka Wrapper)

Summary
Converts the interface of a class into another interface clients expect, allowing classes with incompatible interfaces to work together.
When to use
	•	When you have existing classes or external libraries whose interfaces aren’t compatible with your current code.
	•	To avoid rewriting or modifying existing code, you wrap it with an adapter.
*/
// Existing interface
class RoundHole {
  constructor(radius) {
    this.radius = radius
  }
  fits(roundPeg) {
    return this.radius >= roundPeg.getRadius()
  }
}

// Incompatible class
class SquarePeg {
  constructor(width) {
    this.width = width
  }
}

// Adapter
class SquarePegAdapter {
  constructor(squarePeg) {
    this.squarePeg = squarePeg
  }
  getRadius() {
    // Transform square peg width to an equivalent radius
    return (this.squarePeg.width * Math.sqrt(2)) / 2
  }
}

// Usage
const hole = new RoundHole(5)
const peg = new SquarePeg(7)
const adaptedPeg = new SquarePegAdapter(peg)
console.log(hole.fits(adaptedPeg)) // checks if 5 >= 7*sqrt(2)/2
