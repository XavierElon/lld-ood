/*
Requirements
The parking lot should have multiple levels, each level with a certain number of parking spots.
The parking lot should support different types of vehicles, such as cars, motorcycles, and trucks.
Each parking spot should be able to accommodate a specific type of vehicle.
The system should assign a parking spot to a vehicle upon entry and release it when the vehicle exits.
The system should track the availability of parking spots and provide real-time information to customers.
The system should handle multiple entry and exit points and support concurrent access.

Classes, Interfaces and Enumerations
The ParkingLot class follows the Singleton pattern to ensure only one instance of the parking lot exists. It maintains a list of levels and provides methods to park and unpark vehicles.
The Level class represents a level in the parking lot and contains a list of parking spots. It handles parking and unparking of vehicles within the level.
The ParkingSpot class represents an individual parking spot and tracks the availability and the parked vehicle.
The Vehicle class is an abstract base class for different types of vehicles. It is extended by Car, Motorcycle, and Truck classes.
The VehicleType enum defines the different types of vehicles supported by the parking lot.
Multi-threading is achieved through the use of synchronized keyword on critical sections to ensure thread safety.
The Main class demonstrates the usage of the parking lot system.
*/

const VehicleType = {
  CAR: 'CAR',
  MOTORCYCLE: 'MOTORCYCLE',
  TRUCK: 'TRUCK'
}

class Vehicle {
  constructor(licensePlate, type) {
    if (new.target === Vehicle) {
      throw new Error('Cannot instantiate abstract class Vehicle directly.')
    }
    this.licensePlate = licensePlate
    this.type = type
  }

  getType() {
    return this.type
  }
}

class Motorcycle extends Vehicle {
  constructor(licensePlate) {
    super(licensePlate, VehicleType.MOTORCYCLE)
  }
}

class Car extends Vehicle {
  constructor(licensePlate) {
    super(licensePlate, VehicleType.CAR)
  }
}

class Truck extends Vehicle {
  constructor(licensePlate) {
    super(licensePlate, VehicleType.TRUCK)
  }
}

class ParkingSpot {
  constructor(spotNumber, vehicleType) {
    this.spotNumber = spotNumber
    this.vehicleType = vehicleType
    this.parkedVehicle = null
  }

  isAvailable() {
    return this.parkedVehicle === null
  }

  parkVehicle(vehicle) {
    if (this.isAvailable() && vehicle.getType() === this.vehicleType) {
      this.parkedVehicle = vehicle
    } else {
      throw new Error('Invalid vehicle type or spot already occupied.')
    }
  }

  unparkVehicle() {
    this.parkedVehicle = null
  }

  getParkedVehicle() {
    return this.parkedVehicle
  }

  getVehicleType() {
    return this.vehicleType
  }

  getSpotNumber() {
    return this.spotNumber
  }
}

class Level {
  constructor(floor, numSpots) {
    this.floor = floor
    this.parkingSpots = []

    const spotsForBikes = 0.1
    const spotsForCars = 0.7
    const spotsForTrucks = 0.2

    const numBikes = Math.floor(numSpots * spotsForBikes)
    const numCars = Math.floor(numSpots * spotsForCars)
    const numTrucks = numSpots - (numBikes + numCars)

    let i
    for (i = 1; i <= numBikes; i++) {
      this.parkingSpots.push(new ParkingSpot(i, VehicleType.MOTORCYCLE))
    }
    for (let j = i; j < i + numCars; j++) {
      this.parkingSpots.push(new ParkingSpot(j, VehicleType.CAR))
    }
    for (let k = i + numCars; k <= numSpots; k++) {
      this.parkingSpots.push(new ParkingSpot(k, VehicleType.TRUCK))
    }
  }

  parkVehicle(vehicle) {
    for (let spot of this.parkingSpots) {
      if (spot.isAvailable() && spot.getVehicleType() === vehicle.getType()) {
        spot.parkVehicle(vehicle)
        return true
      }
    }
    return false
  }

  unparkVehicle(vehicle) {
    for (let spot of this.parkingSpots) {
      if (!spot.isAvailable() && spot.getParkedVehicle() === vehicle) {
        spot.unparkVehicle()
        return true
      }
    }
    return false
  }

  displayAvailability() {
    console.log(`Level ${this.floor} Availability:`)
    for (let spot of this.parkingSpots) {
      const status = spot.isAvailable() ? `Available For ${spot.getVehicleType()}` : `Occupied By ${spot.getParkedVehicle().getType()}`
      console.log(`Spot ${spot.getSpotNumber()}: ${status}`)
    }
  }
}

let instance = null

class ParkingLot {
  constructor() {
    if (instance) {
      throw new Error('Use ParkingLot.getInstance() to get the singleton instance.')
    }
    this.levels = []
  }

  static getInstance() {
    if (!instance) {
      instance = new ParkingLot()
    }
    return instance
  }

  addLevel(level) {
    this.levels.push(level)
  }

  parkVehicle(vehicle) {
    for (let level of this.levels) {
      if (level.parkVehicle(vehicle)) {
        console.log('Vehicle parked successfully.')
        return true
      }
    }
    console.log('Could not park vehicle.')
    return false
  }

  unparkVehicle(vehicle) {
    for (let level of this.levels) {
      if (level.unparkVehicle(vehicle)) {
        return true
      }
    }
    return false
  }

  displayAvailability() {
    for (let level of this.levels) {
      level.displayAvailability()
    }
  }
}

const parkingLot = ParkingLot.getInstance()

// Create and add levels
parkingLot.addLevel(new Level(1, 100))
parkingLot.addLevel(new Level(2, 80))

// Create vehicles
const car = new Car('ABC123')
const truck = new Truck('XYZ789')
const motorcycle = new Motorcycle('M1234')

// Park vehicles
parkingLot.parkVehicle(car)
parkingLot.parkVehicle(truck)
parkingLot.parkVehicle(motorcycle)

// Display availability
parkingLot.displayAvailability()

// Unpark a vehicle
parkingLot.unparkVehicle(motorcycle)

// Display updated availability
parkingLot.displayAvailability()
