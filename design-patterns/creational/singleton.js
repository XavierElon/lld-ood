/*
Singleton

Summary
Ensures a class has only one instance and provides a global point of access to it.
When to use
	•	When exactly one instance of a class is required (e.g., logging service, configuration manager, connection pool).
	•	When a global point of access is needed but must avoid accidental creation of multiple instances.
*/
class Singleton {
  static instance = null

  constructor() {
    if (Singleton.instance) {
      return Singleton.instance
    }
    // initialization code
    this.someValue = 42
    Singleton.instance = this
  }

  static getInstance() {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton()
    }
    return Singleton.instance
  }
}

const obj1 = new Singleton()
const obj2 = Singleton.getInstance()
console.log(obj1 === obj2) // true
