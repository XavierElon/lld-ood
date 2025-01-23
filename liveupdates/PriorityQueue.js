// Import the PriorityQueue from the library
import { PriorityQueue } from '@datastructures-js/priority-queue'

/**
 * @param {string[]} words
 * @param {number} k
 * @return {string[]}
 */
const topKFrequent = (words, k) => {
  if (!words || words.length === 0) return []

  // Step 1: Calculate Frequencies
  const freq = getFrequencies(words)

  // Step 2: Initialize a generic PriorityQueue with the custom comparator
  const pq = new PriorityQueue({ compare: compareFunc })

  // Step 3: Enqueue each [word, count] pair into the PriorityQueue
  for (let [word, count] of freq) {
    pq.enqueue([word, count])
  }

  // Step 4: Dequeue the top k elements
  const result = []
  for (let i = 0; i < k && !pq.isEmpty(); i++) {
    const [word, count] = pq.dequeue().element
    result.push(word)
  }

  return result
}

/**
 * Helper function to count the frequency of each word
 * @param {string[]} words
 * @return {Map<string, number>}
 */
const getFrequencies = (words) => {
  const freq = new Map()
  words.forEach((word) => {
    freq.set(word, (freq.get(word) || 0) + 1)
  })
  return freq
}

/**
 * Custom comparator function for the PriorityQueue
 * @param {[string, number]} a
 * @param {[string, number]} b
 * @return {number}
 */
const compareFunc = (a, b) => {
  if (a[1] !== b[1]) {
    // Higher frequency comes first
    return b[1] - a[1]
  }
  // If frequencies are equal, lexicographically smaller word comes first
  return a[0].localeCompare(b[0])
}

// Example Usage:
const words1 = ['i', 'love', 'leetcode', 'i', 'love', 'coding']
const k1 = 2
console.log(topKFrequent(words1, k1)) // Output: ["i", "love"]

const words2 = ['the', 'day', 'is', 'sunny', 'the', 'the', 'the', 'sunny', 'is', 'is']
const k2 = 4
console.log(topKFrequent(words2, k2)) // Output: ["the", "is", "sunny", "day"]

const words3 = ['i', 'i', 'i']
const k3 = 1
console.log(topKFrequent(words3, k3)) // Output: ["i"]
