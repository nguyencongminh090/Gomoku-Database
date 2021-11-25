# Gomoku-Database

### File

- DEMO_SEARCH_TREE
- search_tree.py : SEARCH_TREE algorithm
- search_list.py : SEARCH_LIST algorithm

### What for?
- Copy move from PGN text format to Renlib to easily look.
### How to?
Step 1: Looking for the moves in PGN format, export to text.

Step 2: Systematize the moves -> Make it under a database (Use Tree Data Structure)

Step 3: Make a bot to auto click on Renlib board.

+ Use BFS (Breadth-First Search) or DFS (Depth-First Search)
  + BFS: Click all 1st moves then all 2nd moves in each child nodes ... etc
  + DFS: Click the first move in list (main node) -> move to child node of that move -> click and click... return back to the main node and do again until end.
