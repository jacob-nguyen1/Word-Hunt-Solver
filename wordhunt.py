word_list = set()
word_grid = []
all_valid_words = set()
user_input = ""
max_score = 0
score_by_length = [
  (3, 100),
  (4, 400),
  (5, 800),
  (6, 1400),
  (7, 1800),
  (8, 2200),
  (9, 2600),
  (10, 3000)
]
all_grids = set()

# Prints board
def printBoard():
  for row in word_grid:
    print(row)

# Prints grid
def printGrid(grid):
  for r in grid:
    for x in r:
      print(x, end="")
    print()

def findGridWordLength(grid):
  grid = [value for row in grid for value in row if value != '-']
  return max(grid)

# Finds neighboring letters to a position on the grid
def getNeighbors(row, column):
  neighbors = []
  neighbor_coordinates = [
    [row,column+1],
    [row+1,column+1],
    [row+1,column],
    [row+1,column-1],
    [row,column-1],
    [row-1,column-1],
    [row-1,column],
    [row-1,column+1]
  ]
  for r, c in neighbor_coordinates:
    if 0 <= r <= 3 and 0 <= c <= 3:
      neighbors.append((r, c))
  return neighbors
  
# Find words
def findWords(grid, row, column, visited, current_word, master_word_list, valid_words, current_word_grid):
  
  # Stops recursive call if the tile is already used or if the letters in current word can't form any larger words
  if (row, column) in visited or not any(word.startswith(current_word) for word in master_word_list):
    return valid_words
  
  # Remember that the current tile has been used already in the current word
  visited.add((row, column))

  # Add current letter to the current word
  current_word += (grid[row][column])
  current_word_grid[row][column] = len(current_word)

  # If current word is a word then add it to valid words
  if current_word not in valid_words and len(current_word) >= 3:
    if current_word in master_word_list and current_word not in all_valid_words:
      if len(current_word) >= 7:
        print(current_word) 
        #print(current_word, end=" ") 
        for r in current_word_grid:
          for x in r:
            print(x, end="")
          print()
        #input()
      valid_words.add(current_word)
      all_grids.add(tuple(tuple(row) for row in current_word_grid))


  # For each neighbor of current tile, recursively run the function with neighbor
  for neighbor in getNeighbors(row,column):
    findWords(grid, neighbor[0], neighbor[1], visited, current_word, master_word_list, valid_words, current_word_grid)

  current_word_grid[row][column] = '-'
  visited.remove((row,column))

  return valid_words

# Fill word list
with open("words.txt") as file:
  for word in file:
    word_list.add(word.strip().lower())

# User input for grid
while True:
  user_input = input("enter letters: ").strip().lower()
  if len(user_input) != 16 or not user_input.isalpha():
    print("Invalid input")
  else:
    break

# Create grid
for i in range(0,16,4):
  word_grid.append(user_input[i:i+4])

printBoard()

# Find words starting from all 16 letters
for i in range(0,4):
  for j in range(0,4):
    print(f"Starting on {word_grid[i][j]}")
    # Use a list containing all words that start with the letter of the tile instead of the full list
    temp_list = {word for word in word_list if word.startswith(word_grid[i][j])}
    all_valid_words.update(findWords(word_grid, i, j, set(), "", temp_list, set(), [['-','-','-','-'],['-','-','-','-'],['-','-','-','-'],['-','-','-','-']]))
    print()

# Prints 6 letter grids and below (ordered by length, descending), one at a time
print("####")
for grid in all_grids:
  if findGridWordLength(grid) == 6:
    printGrid(grid)
    print("####")
    input()
for i in range(5,-1,-1):
  for grid in all_grids:
    if findGridWordLength(grid) == i:
      printGrid(grid)
      print("####")
      input()

for word in all_valid_words:
  for length, score in score_by_length:
    if len(word) == length:
      max_score += score
print (f"Max score: {max_score}")
