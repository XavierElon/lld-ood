/*
Memento

Summary:
	•	Captures and externalizes an object’s internal state so it can be restored later without violating encapsulation.
	•	Often used to implement undo/redo functionality.

When to use:
	•	When you need to save snapshots of an object’s state to restore later.
	•	Must preserve encapsulation; internal details of the object shouldn’t be exposed to the outside world.
*/
class Editor {
  constructor() {
    this.content = ''
  }

  setContent(content) {
    this.content = content
  }

  createSnapshot() {
    return new EditorMemento(this.content)
  }

  restoreSnapshot(memento) {
    this.content = memento.getContent()
  }
}

class EditorMemento {
  constructor(content) {
    this.content = content // internal state saved
  }

  getContent() {
    return this.content
  }
}

// Usage
const editor = new Editor()
editor.setContent('Version 1')
const saved = editor.createSnapshot()

editor.setContent('Version 2')
console.log(editor.content) // "Version 2"

// Undo
editor.restoreSnapshot(saved)
console.log(editor.content) // "Version 1"
