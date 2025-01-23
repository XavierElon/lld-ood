// Defines the skeleton of an algorithm in a method, deferring some steps to subclasses.
// Template Method lets subclasses redefine certain steps without changing the structure of the algorithm.
/*
When to use:
	•	When you have a fixed algorithm structure, but some steps can vary or need to be implemented differently by subclasses.
	•	Ensures the common behavior remains in one place while allowing subclasses to customize certain steps.
*/

class Game {
  play() {
    this.initialize()
    this.startPlay()
    this.endPlay()
  }
  initialize() {}
  startPlay() {}
  endPlay() {}
}

class Football extends Game {
  initialize() {
    console.log('Football Game Initialized')
  }
  startPlay() {
    console.log('Football Game Started')
  }
  endPlay() {
    console.log('Football Game Finished')
  }
}

// Usage
const game = new Football()
game.play()
