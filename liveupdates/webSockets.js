const WebSocket = require('ws')

// WebSocket in a JavaScript client
const socket = new WebSocket('ws://example.com')

socket.onopen = function (event) {
  console.log('Connection established')
  // Sending a message to the server
  socket.send('Hello Server!')
}

socket.onmessage = function (event) {
  console.log('Message from server:', event.data)
}
