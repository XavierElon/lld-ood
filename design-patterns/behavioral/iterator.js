/*
Iterator

Summary:
	•	Provides a way to access the elements of an aggregate object (like a list) sequentially without exposing its internal structure.
	•	Extracts the iteration logic into a dedicated class so the collection’s code isn’t cluttered with iteration details.

When to use:
	•	When you need to traverse different data structures (arrays, trees, lists) in a uniform way.
	•	To achieve the Single Responsibility Principle: keep traversal logic separate from the collection itself.
*/
class CustomCollection {
  constructor() {
    this.items = []
  }
  addItem(item) {
    this.items.push(item)
  }
  // Return an iterator
  createIterator() {
    let index = 0
    const items = this.items
    return {
      next: function() {
        return index < items.length ? { value: items[index++], done: false } : { done: true }
      }
    }
  }
}

// Usage
const collection = new CustomCollection()
collection.addItem('Apple')
collection.addItem('Banana')
collection.addItem('Cherry')

const iterator = collection.createIterator()
let result = iterator.next()
while (!result.done) {
  console.log(result.value)
  result = iterator.next()
}
