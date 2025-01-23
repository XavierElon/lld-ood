function findMaximumElement(lst) {
  const [maxValue, maxIndex] = findMax(0, lst)
  return { maxValue, maxIndex } // Returning as an object for clarity
}

function findMax(i, lst) {
  // If we've reached the end of the array, return [null, null]
  if (i === lst.length) {
    return [null, null]
  }

  // Recursively find the max in the rest of the array
  let [bestMax, bestIndex] = findMax(i + 1, lst)

  // If bestMax is null (empty list ahead) or current element is greater, update
  if (bestMax === null || lst[i] > bestMax) {
    bestMax = lst[i]
    bestIndex = i
  }

  return [bestMax, bestIndex]
}

// Example usage:
const arr = [3, 1, 4, 2, 5]
const result = findMaximumElement(arr)
console.log(result) // { maxValue: 5, maxIndex: 4 }
