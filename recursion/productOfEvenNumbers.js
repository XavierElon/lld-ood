function productOfEvenNumbers(list) {
  product = recurse(0, list)

  if (product === null) return 0
  return product
}

function recurse(index, list) {
  if (index === list.length) return null

  product = recurse(index + 1, list)
  if (list[index] % 2 !== 0) {
    return product
  }

  if (product === null) return list[index]

  return list[index] * product
}

let list = [1, 2, 3, 4, 5]
console.log(productOfEvenNumbers(list)) // 8
let list2 = [2, 4, 6, 8, 10]
let list3 = [0, 2, 4, 6, 8]
console.log(productOfEvenNumbers(list2)) // 3840
console.log(productOfEvenNumbers(list3)) // 0
