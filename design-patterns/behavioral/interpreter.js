/*
Interpreter

Summary:
	•	Defines a representation for a simple language or grammar and provides an interpreter to process the language’s statements.
	•	Typically used when you want to parse or evaluate expressions in a domain-specific language.

When to use:
	•	When you need to evaluate or translate specialized scripts or expressions repeatedly.
	•	Often used in configurations, scripting, or small language processing scenarios.
*/
// Abstract Expression
class Expression {
  interpret(context) {}
}

// Terminal Expression
class NumberExpression extends Expression {
  constructor(value) {
    super()
    this.value = parseInt(value, 10)
  }
  interpret() {
    return this.value
  }
}

// Non-Terminal Expression
class AddExpression extends Expression {
  constructor(left, right) {
    super()
    this.left = left
    this.right = right
  }
  interpret() {
    return this.left.interpret() + this.right.interpret()
  }
}

// Simple Parser
function parse(expressionStr) {
  // Example: "3 + 5"
  const tokens = expressionStr.split(' ')
  const left = new NumberExpression(tokens[0])
  const right = new NumberExpression(tokens[2])
  if (tokens[1] === '+') {
    return new AddExpression(left, right)
  }
  throw new Error('Unsupported operator')
}

// Usage
const expr = parse('3 + 5')
console.log(expr.interpret()) // 8
