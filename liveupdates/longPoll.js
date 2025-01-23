// long-polling in a JavaScript client
function longPoll() {
  fetch('http://example.com/poll')
    .then((response) => response.json())
    .then((data) => {
      console.log('Received data:', data)
      longPoll() // Immediately establish a new long polling request
    })
    .catch((error) => {
      /**
       * Errors can appear in normal conditions when a
       * connection timeout is reached or when the client goes offline.
       * On errors we just restart the polling after some delay.
       */
      setTimeout(longPoll, 10000)
    })
}
longPoll() // Initiate the long polling
