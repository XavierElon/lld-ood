/*
Lets an object alter its behavior when its internal state changes. The object will appear to change its class.
When to use
	•	When your object’s behavior depends on its current state and it must change behavior at runtime.
	•	Avoids large switch statements based on an object’s state.
*/

class State {
  clickButton(context) {}
}

class ConcreteStateA extends State {
  clickButton(context) {
    console.log('Handled by State A. Transition to State B.')
    context.setState(new ConcreteStateB())
  }
}

class ConcreteStateB extends State {
  clickButton(context) {
    console.log('Handled by State B. Transition to State A.')
    context.setState(new ConcreteStateA())
  }
}

class Context {
  constructor() {
    this.state = new ConcreteStateA()
  }

  setState(state) {
    this.state = state
  }

  clickButton() {
    this.state.clickButton(this)
  }
}

const context = new Context()
context.clickButton() // Handled by State A -> transitions to B
context.clickButton() // Handled by State B -> transitions to A
