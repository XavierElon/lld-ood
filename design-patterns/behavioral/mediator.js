/*
Mediator

Summary:
	•	Defines an object that encapsulates how a set of objects interact.
	•	Promotes loose coupling by keeping objects from referring to each other explicitly and letting them communicate via a mediator object.

When to use:
	•	When you have a lot of complex object-to-object interactions, forming a “spaghetti” of references.
	•	Reduces coupling by moving all interaction logic into a single mediator.
*/
class ChatRoom {
  showMessage(user, message) {
    const time = new Date().toLocaleTimeString()
    console.log(`[${time}] ${user.getName()}: ${message}`)
  }
}

class User {
  constructor(name, chatroom) {
    this.name = name
    this.chatroom = chatroom
  }

  getName() {
    return this.name
  }

  send(message) {
    this.chatroom.showMessage(this, message)
  }
}

// Usage
const chatroom = new ChatRoom()
const user1 = new User('Alice', chatroom)
const user2 = new User('Bob', chatroom)

user1.send('Hello Bob!')
user2.send('Hi Alice!')
