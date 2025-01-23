/*
Factory Method (often just called Factory)

Summary
Defines an interface for creating objects, but lets subclasses decide which class to instantiate. The factory method defers object creation to subclasses.
When to use
	•	When you have a superclass that defines a method for object creation, but subclasses decide the actual product’s class.
	•	When you want to decouple object creation so the code using the objects is simpler or more flexible.
*/
// Creator class
class Dialog {
  createButton() {
    // Factory Method - overridden by subclasses
    throw new Error('This method should be overridden!')
  }
  render() {
    const okButton = this.createButton()
    okButton.onClick(() => console.log('Button clicked!'))
    okButton.render()
  }
}

// Concrete Creator
class WindowsDialog extends Dialog {
  createButton() {
    return new WindowsButton()
  }
}

// Another Concrete Creator
class WebDialog extends Dialog {
  createButton() {
    return new HTMLButton()
  }
}
