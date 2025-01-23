/*
Encapsulates a request as an object, allowing you to parameterize clients with different requests, queue or log requests, and support undo operations.
When to use
	•	When you want to separate the action (request) from the object that calls it.
	•	To implement undo/redo functionality or to queue and execute actions at different times.
*/
class Command {
  execute() {}
}

class CopyCommand extends Comamnd {
  constructor(editor) {
    super()
    this.editor = editor
  }

  execute() {
    this.editor.clipboard = this.editor.getSelectedText()
  }
}

class Button {
  constructor(command) {
    this.command = command
  }

  click() {
    this.command.execute
  }
}

// Usage
const editor = { getSelectedText: () => 'Hello', clipboard: '' }
const copyButton = new Button(new CopyCommand(editor))
copyButton.click()
console.log(editor.clipboard) // "Hello"
