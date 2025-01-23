/*
Builder

Summary
Separates the construction of a complex object from its representation, allowing the same construction process to create different representations.
When to use
	•	When the construction process of an object is complex, involving multiple steps.
	•	When you want to be able to create various representations of an object by using the same building process.
*/
class HouseBuilder {
  reset() {}
  buildWalls() {}
  buildDoors() {}
  buildRoof() {}
  // ...
}

class ConcreteHouseBuilder extends HouseBuilder {
  constructor() {
    super()
    this.reset()
  }
  reset() {
    this.house = {}
  }
  buildWalls() {
    this.house.walls = '4 concrete walls'
  }
  buildDoors() {
    this.house.doors = '2 wooden doors'
  }
  buildRoof() {
    this.house.roof = 'Concrete roof'
  }
  getResult() {
    return this.house
  }
}

// Director
class HouseDirector {
  setBuilder(builder) {
    this.builder = builder
  }
  constructMinimalViableHouse() {
    this.builder.reset()
    this.builder.buildWalls()
    this.builder.buildDoors()
  }
  constructFullFeaturedHouse() {
    this.builder.reset()
    this.builder.buildWalls()
    this.builder.buildDoors()
    this.builder.buildRoof()
  }
}
