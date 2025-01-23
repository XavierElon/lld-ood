/*
Chain of Responsibility

Summary:
	•	Lets you pass requests along a chain of handlers.
	•	Each handler either processes the request or forwards it to the next handler in the chain.

When to use:
	•	When you have a sequence of processing steps for a request, but you want flexibility in how it’s handled.
	•	Avoids coupling the sender of a request to a single receiver.
*/
class Handler {
  setNext(handler) {
    this.next = handler
    return handler
  }
  handle(request) {
    if (this.next) {
      return this.next.handle(request)
    }
    return null // no handler could process
  }
}

class AuthHandler extends Handler {
  handle(request) {
    if (!request.isAuthenticated) {
      console.log('AuthHandler: User not authenticated, request denied.')
      return null
    }
    return super.handle(request)
  }
}

class LoggingHandler extends Handler {
  handle(request) {
    console.log('LoggingHandler: Logging request...')
    return super.handle(request)
  }
}

class DataHandler extends Handler {
  handle(request) {
    console.log('DataHandler: Handling data for request...')
    return 'Data response'
  }
}

// Usage
const auth = new AuthHandler()
const log = new LoggingHandler()
const data = new DataHandler()

// Build the chain
auth.setNext(log).setNext(data)

const request = { isAuthenticated: true }
const response = auth.handle(request)
console.log(response)
// Output:
// AuthHandler -> LoggingHandler -> DataHandler -> "Data response"
