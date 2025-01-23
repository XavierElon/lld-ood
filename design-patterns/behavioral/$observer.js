/*
Observer (aka Publish-Subscribe)

Summary
Defines a one-to-many relationship so that when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically.
When to use
	•	When changes to one object require updating dependent objects, and you want to avoid tight coupling.
	•	Common in event-driven systems, GUIs, real-time data feeds, etc.
*/

class Subject {
  constructor() {
    this.observers = []
  }

  attach(observer) {
    this.observers.push(observer)
  }

  detach(observer) {
    this.observers = this.observers.filter((o) => o !== observer)
  }

  notify(observer) {
    this.observers.forEach((o) => o.update(data))
  }
}

class ConcreteObserver {
  update(data) {
    console.log('Observer notified with data:', data)
  }
}

const subject = new Subject()
const observer1 = new ConcreteObserver()
const observer2 = new ConcreteObserver()

subject.attach(observer1)
subject.attach(observer2)

subject.notify('Something changed!')
// Both observer1 and observer2 receive the update
