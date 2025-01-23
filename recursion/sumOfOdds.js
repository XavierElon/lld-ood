function sumOfOdds(list) {
  return sumOdds(0, list)
}

function sumOdds(index, list) {
  if (index === list.length) return 0

  let value = 0
  if (list[index] % 2 !== 0) {
    value = list[index]
  }

  return sumOdds(index + 1, list) + value
}

const list1 = [1, 2, 3, 4, 5]
console.log(sumOfOdds(list1)) // 9
const list2 = [2, 4, 6, 8, 10]
console.log(sumOfOdds(list2)) // 0
