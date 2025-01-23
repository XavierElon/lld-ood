function reverse(s) {
  let length = s.length
  if (length === 0) {
    return ''
  }

  let left = s[0]
  let right = s[length - 1]
  let substring = s.substring(1, length - 1)

  // Don't swap left and right.
  // The correct logic: right + reverse(middle) + left
  return right + reverse(substring) + left
}

const str = 'hello'
console.log(reverse(str)) // "olleh"
