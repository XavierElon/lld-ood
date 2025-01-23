/*
Summary:
	•	A fine-grained object-sharing pattern.
	•	Minimizes memory use by sharing as much data as possible with similar objects.
	•	Stored intrinsic state in the shared object, while extrinsic state is kept outside.

When to use:
	•	When you need to create a massive number of small, similar objects (e.g., rendering characters in a text editor).
	•	To reduce memory footprint by reusing objects that share intrinsic data.
*/
// Flyweight (shared object)
class Character {
  constructor(symbol, font) {
    this.symbol = symbol // intrinsic state
    this.font = font // intrinsic state
  }

  printCharacter(extrinsicState) {
    // extrinsicState could be position, color, etc.
    console.log(`Char: ${this.symbol}, Font: ${this.font}, Position: ${extrinsicState.position}`)
  }
}

// Flyweight Factory
class CharacterFactory {
  constructor() {
    this.characters = {}
  }

  getCharacter(symbol, font) {
    const key = symbol + font
    if (!this.characters[key]) {
      this.characters[key] = new Character(symbol, font)
    }
    return this.characters[key]
  }
}

// Usage
const factory = new CharacterFactory()
const c1 = factory.getCharacter('A', 'Arial')
const c2 = factory.getCharacter('A', 'Arial')

console.log(c1 === c2) // true (same shared object!)

c1.printCharacter({ position: 1 })
c2.printCharacter({ position: 2 })
