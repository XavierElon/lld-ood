/*
Abstract Factory

Summary
Provides an interface to create families of related or dependent objects without specifying their concrete classes.
When to use
	•	When you need to create families of related objects (e.g., different UI themes: Windows, Mac, Linux) without coupling to their specific classes.
	•	Ensures consistent usage of related objects (buttons, checkboxes, text fields) that are meant to go together.
*/
// Abstract Factory
class GUIFactory {
  createButton() {}
  createCheckbox() {}
}

// Concrete Factory for Windows
class WinFactory extends GUIFactory {
  createButton() {
    return new WinButton()
  }
  createCheckbox() {
    return new WinCheckbox()
  }
}

// Concrete Factory for Mac
class MacFactory extends GUIFactory {
  createButton() {
    return new MacButton()
  }
  createCheckbox() {
    return new MacCheckbox()
  }
}

// Client
function buildUI(factory) {
  const button = factory.createButton()
  const checkbox = factory.createCheckbox()
  // use button, checkbox...
}
