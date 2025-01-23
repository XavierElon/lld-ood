// function findMatrixMax(matrix) {
//   return matrixMax(0, 0, matrix)
// }

// function matrixMax(row, col, matrix) {
//   if (row === matrix.length) return [null, null]
//   if (col === matrix[row].length) return matrixMax(row + 1, 0, matrix)

//   let [maxRow, maxCol] = matrixMax(row, col + 1, matrix)

//   if (maxRow === null || maxCol === null) {
//     maxRow = row
//     maxCol = col
//   }
//   if (matrix[row][col] > matrix[maxRow][maxCol]) {
//     maxRow = row
//     maxCol = col
//   }

//   return [maxRow, maxCol]
// }

// const matrix = [
//   [1, 2, 3, 4, 5],
//   [6, 7, 8, 9, 10]
// ]
// console.log(findMatrixMax(matrix)) // [1, 4]
function findMatrixMax(lst) {
  return matrixMax(0, 0, lst)
}

function matrixMax(row, col, matrix) {
  // Base case: If we've traversed all rows
  if (row === matrix.length) return { maxValue: -Infinity, row: -1, col: -1 }

  // If we've reached the end of a row, move to the next row
  if (col === matrix[row].length) return matrixMax(row + 1, 0, matrix)

  // Recursive call to process the next element
  const nextMax = matrixMax(row, col + 1, matrix)

  // Compare the current element with the maximum element found so far
  if (matrix[row][col] > nextMax.maxValue) {
    return { maxValue: matrix[row][col], row: row, col: col }
  } else {
    return nextMax // Return the previous maximum
  }
}

const matrix = [
  [1, 2, 3, 4, 5],
  [6, 7, 8, 9, 10]
]

const result = findMatrixMax(matrix)
console.log(result) // { maxValue: 10, row: 1, col: 4 }
