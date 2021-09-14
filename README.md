## Hare and Hounds AI

Implemented **Minimax** and **Alpha–beta pruning** algorithms into the game of Hare and Hounds and developed a simple GUI using Pygame.

"Hare games are two-player abstract strategy board games that were popular in medieval northern Europe up until the 19th century. In this game, a hare is trying to get past three dogs who are trying to surround it and trap it. The three dogs are represented by three pieces which normally start on one end of the board, and the hare is represented by one piece that usually starts in the middle of the board or is dropped on any vacant point in the beginning of the game." [(Source)](https://en.wikipedia.org/wiki/Hare_games#Hare_and_Hounds)

### Game rules:
- One player represents the three Hounds, which try to corner the other player's Hare as it seeks to win by escaping them.
- The Hounds move first. Each player can move one piece one step in each turn. The Hounds can only move forward or diagonally (left to right) or vertically (up and down). The Hare can move in any direction.
- The Hounds win if they "trap" the Hare so that it can no longer move.
- The Hare wins if it "escapes" (gets to the left of all the Hounds).
- If the Hounds move vertically ten moves in a row, they are considered to be "stalling" and the Hare wins

### GUI:
![](https://github.com/cosminbvb/Hare-and-Hounds-AI/blob/main/demo.gif)

### Score estimation for non-final states: 
##### Estimation 2 (stronger)
Estimation 2 involves performing a BFS search starting from Hare's location and counting the total number of reachable positions. When the player is the Hare, the goal is to maximize that number. Meanwhile, for the Hounds, the goal is to trap the Hare, meaning that the goal is to minimize that number (we do that by maximizing 11-counter).
##### Estimation 1 (weaker)
Estimation 1 is the equivalent of a 1-ranged BFS.
Counting how many adjacent positions are free from the Hare POV. When the player is the Hare, the goal is to maximize the number of free adjacent positions. When the player uses Hounds, the goal is to trap the Hare, meaning that the goal is to minimize the number of free positions (we do that by maximizing -(number of free positions))

### Difficulty:
The difficulty is set by mapping each level to a searching depth limit. (Easy - 1, Medium - 3, Hard - 6).


