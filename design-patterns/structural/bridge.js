/*
Bridge

Summary:
	•	Separates an object’s abstraction from its implementation, letting them vary independently.
	•	You have two hierarchies (e.g., shape vs. how it is drawn), and you want to keep them decoupled.

When to use:
	•	When you have multiple dimensions of variation and want to avoid a combinatorial explosion of subclasses (e.g., a Circle that can be drawn in Raster or Vector mode).
	•	Simplifies maintaining multiple variants of an abstraction and its implementation.
*/
// Implementor
class Renderer {
  renderCircle(radius) {
    throw new Error('renderCircle() not implemented')
  }
}

// Concrete Implementors
class VectorRenderer extends Renderer {
  renderCircle(radius) {
    console.log(`Drawing a circle of radius ${radius} in Vector mode.`)
  }
}

class RasterRenderer extends Renderer {
  renderCircle(radius) {
    console.log(`Drawing pixels for a circle of radius ${radius}.`)
  }
}

// Abstraction
class Shape {
  constructor(renderer) {
    this.renderer = renderer
  }
  draw() {
    throw new Error('draw() not implemented')
  }
}

// Refined Abstraction
class Circle extends Shape {
  constructor(renderer, radius) {
    super(renderer)
    this.radius = radius
  }

  draw() {
    this.renderer.renderCircle(this.radius)
  }
}

// Usage
const vectorCircle = new Circle(new VectorRenderer(), 5)
vectorCircle.draw()
// "Drawing a circle of radius 5 in Vector mode."

const rasterCircle = new Circle(new RasterRenderer(), 5)
rasterCircle.draw()
// "Drawing pixels for a circle of radius 5."
