function friendDistance(friends, userA, userB) {
  if (userA === userB) return 0

  const visited = new Set()
  const queue = [userA]
  let depth = 0

  while (queue.length > 0) {
    const levelSize = queue.length
    depth++

    for (let i = 0; i < levelSize; i++) {
      const current = queue.shift()

      if (visited.has(current)) continue
      visited.add(current)

      if (friends[current][userB] === 1) {
        return depth
      }

      for (let friend = 0; friend < friends[current].length; friend++) {
        if (friends[current][friend] === 1 && !visited.has(friend)) {
          queue.push(friend)
        }
      }
    }
  }

  return -1
}

// debug your code below
const friends = [
  [0, 1, 0],
  [1, 0, 1],
  [0, 1, 0]
]

console.log(friendDistance(friends, 0, 1))
