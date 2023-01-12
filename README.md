# LudoGame
A simple board game made using python

## Description
This board game takes 2 - 4 players and gives them two tokens each to move around the board to reach the final square. Once they reach the final square, they win!

# Program Description
The game is made with two different classes: 
# Player 
This classs is used to represent a Player object and control each token (token p and Token q).
* Each Player object will have: a position (for identification - A, B, C, or D)
* A start and end space respective of each position
* the location of the current player's two tokens: in the home yard, ready to go, somewhere on the board, or has finished.
* the current state of the player: whether the player has won (completed the game) or is still playing

Methods:
* get_completed: returns True or False depending on if the player has finished or not finished the game
* get_token_p_step_count: returns the total steps the token p has taken on the board
* get_token_q_step_count: returns the total steps the token q has taken on the board
* get_space_name: returns the name of the space the token has landed on on the board as a string using the total spaces moved as the parameter. 

# LudoGame
This class is used to the currently playing game - recalling this method will reset the game. 
Methods:
* get_player_by_position: returns the player object using the player’s position (the identifier).
*play_game method starts a new game using two parameters, the players list, and the turns list. 

# Example Usuage
```python
players = ['A', 'B']
turns = [('A', 6), ('A', 4), ('A', 5), ('A', 4), ('B', 6), ('B', 4), ('B', 1), ('B', 2), ('A', 6), ('A', 4), ('A', 6), ('A', 3), ('A', 5), ('A', 1), ('A', 5), ('A', 4)]
game = LudoGame()
current_tokens_space = game.play_game(players, turns)
player_A = game.get_player_by_position('A')
print(player_A.get_completed())
print(player_A.get_token_p_step_count())
print(current_tokens_space)
player_B = game.get_player_by_position('B')
print(player_B.get_space_name(55))

# the output :
False
28
[‘28’, ‘28’, ‘21’, ‘H’]
B5
```
