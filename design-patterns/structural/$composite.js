/*
Composite

Summary
Composes objects into tree structures to represent part-whole hierarchies. It lets clients treat individual objects and compositions uniformly.

When to use
	•	When you need to represent hierarchical object structures (e.g., GUI elements, file system).
	•	When you want clients to treat individual and composite objects in the same way.
*/
// Component interface
class Graphic {
  draw() {}
}

// Leaf
class Circle extends Graphic {
  draw() {
    console.log('Drawing a circle...')
  }
}

// Composite
class CompoundGraphic extends Graphic {
  constructor() {
    super()
    this.children = []
  }
  add(child) {
    this.children.push(child)
  }
  draw() {
    for (const child of this.children) {
      child.draw()
    }
  }
}

const circle1 = new Circle()
const circle2 = new Circle()
const group = new CompoundGraphic()
group.add(circle1)
group.add(circle2)
group.draw()
// Draws two circles
