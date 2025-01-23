/*
Proxy

Summary:
	•	Provides a placeholder for another object to control access to it.
	•	The proxy can control creation, access, caching, or any additional logic before delegating to the real object.

When to use:
	•	Remote proxy: Access objects running on a remote server.
	•	Virtual proxy: Delay the creation of expensive objects until truly needed.
	•	Protection proxy: Control access rights to an object (e.g., different user permissions).
*/
// Subject Interface
class Image {
  display() {}
}

// Real Subject
class RealImage extends Image {
  constructor(filename) {
    super()
    this.filename = filename
    this.loadFromDisk(filename)
  }

  loadFromDisk(filename) {
    console.log(`Loading image from ${filename}`)
  }

  display() {
    console.log(`Displaying ${this.filename}`)
  }
}

// Proxy
class ProxyImage extends Image {
  constructor(filename) {
    super()
    this.filename = filename
    this.realImage = null
  }

  display() {
    if (!this.realImage) {
      this.realImage = new RealImage(this.filename)
    }
    this.realImage.display()
  }
}

// Usage
const img = new ProxyImage('photo.jpg')
img.display() // Loads from disk, then displays
img.display() // Uses already loaded RealImage
