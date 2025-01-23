// ===========================
// getSpecialString Implementation
// ===========================

function getSpecialString(s) {
  const n = s.length
  const chars = s.split('')

  for (let index = n - 1; index >= 0; index--) {
    const currentCharCode = chars[index].charCodeAt(0)
    for (let code = currentCharCode + 1; code <= 122; code++) {
      // 'z' = 122
      const nextChar = String.fromCharCode(code)
      if (index === 0 || nextChar !== chars[index - 1]) {
        // Ensure no duplication with previous character
        // Replace the current character with the valid next character
        chars[index] = nextChar

        // Reset the subsequent characters to the smallest valid characters
        if (fillRest(chars, index + 1)) {
          return chars.join('')
        }
      }
    }
    // If no valid character found, continue to the previous position
  }

  return '-1' // No valid special string found
}

// Helper function to fill the rest of the string
function fillRest(chars, startIndex) {
  const n = chars.length
  for (let i = startIndex; i < n; i++) {
    let found = false
    for (let code = 97; code <= 122; code++) {
      // 'a' to 'z'
      const nextChar = String.fromCharCode(code)
      if (i === 0 || nextChar !== chars[i - 1]) {
        // Ensure no duplication with previous character
        chars[i] = nextChar
        found = true
        break // Assign the smallest possible valid character
      }
    }
    if (!found) {
      return false // Cannot assign a valid character
    }
  }
  return true
}

// ===========================
// Test Cases Definition
// ===========================

// Define an array of test cases
const testCases = [
  // ===========================
  // Small Test Cases
  // ===========================
  {
    description: "Test Case 1: Single 'a'",
    input: 'a',
    expected: 'b'
  },
  {
    description: 'Test Case 2: Increment last character without duplicates',
    input: 'ab',
    expected: 'ac'
  },
  {
    description: 'Test Case 3: Increment with adjacent duplicates avoided',
    input: 'aba',
    expected: 'abc' // Corrected Expected Output from "abb" to "abc"
  },
  {
    description: 'Test Case 4: No possible increment without causing duplicates',
    input: 'zz',
    expected: '-1'
  },
  // ===========================
  // Edge Test Cases
  // ===========================
  {
    description: "Test Case 5: All characters are 'z'",
    input: 'zzzzzz',
    expected: '-1'
  },
  {
    description: "Test Case 6: Single character 'z'",
    input: 'z',
    expected: '-1'
  },
  {
    description: 'Test Case 7: Alternating characters',
    input: 'ababab',
    expected: 'ababac'
  },
  {
    description: "Test Case 8: String ending with 'z'",
    input: 'abcdez',
    expected: 'abcdfa'
  },
  // ===========================
  // Medium Test Cases
  // ===========================
  {
    description: 'Test Case 9: Moderate length string with duplicates',
    input: 'abccde',
    expected: 'abcdab'
  },
  {
    description: "Test Case 10: Increment last character in 'abcdefg'",
    input: 'abcdefg',
    expected: 'abcdefh'
  },
  {
    description: 'Test Case 11: String with multiple duplicates',
    input: 'aabccbaa',
    expected: 'aabccbab'
  },
  {
    description: 'Test Case 12: Increment causing multiple fills',
    input: 'abcxyz',
    expected: 'abcxza'
  },
  // ===========================
  // Large Test Cases
  // ===========================
  {
    description: "Test Case 13: Very long string with all 'a's",
    input: 'a'.repeat(100000),
    expected: 'a'.repeat(99999) + 'b'
  },
  {
    description: "Test Case 14: Very long alternating 'a' and 'b'",
    input: generateRepeatingPattern('ab', 50000), // 'ab' repeated 50,000 times to make 100,000 characters
    expected: undefined // Expected output is not predefined
  },
  {
    description: 'Test Case 15: Long string with duplicates spread throughout',
    input: generateRepeatingPattern('aabbcc', 16666) + 'aabb', // Approximately 100,000 characters
    expected: undefined // Expected output is not predefined
  },
  {
    description: "Test Case 16: String ending with multiple 'z's",
    input: 'abcde' + 'z'.repeat(99995),
    expected: undefined // Expected output is not predefined
  },
  // ===========================
  // Stress Test Cases
  // ===========================
  {
    description: "Test Case 17: Maximum length string with all 'z's",
    input: 'z'.repeat(100000),
    expected: '-1'
  },
  {
    description: 'Test Case 18: Long string with blocks of identical letters',
    input: generateRepeatingPattern('aaabbbccc', 11111) + 'aaabbb', // Approximately 100,000 characters
    expected: undefined
  },
  {
    description: "Test Case 19: String with last character 'z'",
    input: generateRepeatingPattern('abcxyz', 16666) + 'xyz', // Approximately 100,000 characters
    expected: undefined
  },
  {
    description: 'Test Case 20: Palindrome string with maximum length',
    input: generateRepeatingPattern('abccba', 16666) + 'abccba', // Approximately 100,000 characters
    expected: undefined
  },
  // ===========================
  // Randomized Test Cases
  // ===========================
  {
    description: 'Test Case 21: Random string of lowercase letters, 100,000 characters',
    input: generateRandomString(100000),
    expected: undefined
  },
  {
    description: "Test Case 22: Random string with high frequency of 'a'",
    input: 'a'.repeat(90000) + generateRandomString(10000),
    expected: undefined
  },
  {
    description: "Test Case 23: Alternating 'a' and 'z'",
    input: generateRepeatingPattern('az', 50000),
    expected: undefined
  },
  {
    description: 'Test Case 24: Long string with incremental patterns',
    input: generateRepeatingPattern('abcde', 20000), // 'abcde' repeated 20,000 times to make 100,000 characters
    expected: undefined
  },
  // ===========================
  // Special Pattern Test Cases
  // ===========================
  {
    description: 'Test Case 25: Increasing sequence with duplicates',
    input: generateRepeatingPattern('aababbababa', 9091), // Approximately 100,000 characters
    expected: undefined
  },
  {
    description: 'Test Case 26: Decreasing sequence with duplicates',
    input: generateRepeatingPattern('zzzyyyxxx', 11111) + 'zzz',
    expected: undefined
  },
  {
    description: "Test Case 27: Repeating 'abc' pattern",
    input: generateRepeatingPattern('abc', 33333) + 'ab',
    expected: undefined
  },
  {
    description: 'Test Case 28: Clusters of identical letters',
    input: generateRepeatingPattern('aaabbbcccdddeee', 6666) + 'aaabbb',
    expected: undefined
  }
]

// ===========================
// Helper Functions to Generate Patterns and Random Strings
// ===========================

function generateRandomString(length) {
  const characters = 'abcdefghijklmnopqrstuvwxyz'
  let result = ''
  const charactersLength = characters.length
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength))
  }
  return result
}

function generateRepeatingPattern(pattern, repeatTimes) {
  return pattern.repeat(repeatTimes)
}

// ===========================
// Test Execution and Timing
// ===========================

// Function to run all test cases
function runAllTestCases(testCases) {
  console.log('Starting Test Cases Execution...\n')

  testCases.forEach((testCase, index) => {
    const { description, input, expected } = testCase

    // Start timing
    console.time(description)

    // Execute the function
    let output
    try {
      output = getSpecialString(input)
    } catch (error) {
      output = `Error: ${error.message}`
    }

    // End timing
    console.timeEnd(description)

    // Verify the result if expected output is provided
    if (expected !== undefined) {
      const pass = output === expected
      console.log(`Test ${index + 1}: ${description}`)
      console.log(`Expected: ${truncateString(expected, 50)}`)
      console.log(`Got     : ${truncateString(output, 50)}`)
      console.log(`Result  : ${pass ? '✅ Passed' : '❌ Failed'}\n`)
    } else {
      // For large test cases without predefined expected output
      console.log(`Test ${index + 1}: ${description}`)
      console.log(`Output Length: ${output.length}`)
      console.log(`Sample Output Start: ${truncateString(output, 50)}\n`)
    }
  })

  console.log('All Test Cases Executed.')
}

// Helper function to truncate long strings for display
function truncateString(str, maxLength) {
  if (str.length <= maxLength) {
    return str
  }
  return str.substring(0, maxLength) + '...'
}

// ===========================
// Execute Tests
// ===========================

runAllTestCases(testCases)
