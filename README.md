# Summary of Tic Tac Toe Game and Reinforcement Learning Agent

**1. 'TicTacToeGame' Class**
- Initialization: Initializes a Tic Tac Toe game with an empty board (" "), sets the starting player as 'X', and initializes 'winner' as 'None'.
- Allowed Moves: Returns a list of all possible board states after the current player makes a move.
- Make Move: Updates the game state to the next state provided it's a valid move.
- Playable: Checks if the game is still ongoing (no winner yet and there are allowed moves).
- Predict Winner: Determines if there is a winner based on the current board state.
- Print Board: Prints the current state of the board in a formatted manner.

**2. 'Agent' Class**
- Initialization: Initializes the reinforcement learning agent with parameters like 'epsilon' (exploration rate), 'alpha' (learning rate), and the player it will optimize for ('value_player').
- State Value: Returns the estimated value (Q-value) of a given game state.
- Learn Game: Trains the agent by playing multiple episodes of Tic Tac Toe.
- Learn From Episode: Plays a single episode of Tic Tac Toe and learns from it.
- Learn From Move: Updates the Q-value of the current state based on the reward received and the predicted future rewards.
- Learn Select Move: Selects the next move based on the current policy (exploitation vs exploration).
- Play Select Move: Selects the next move during gameplay based on the learned Q-values.
- Demo Game: Plays a complete game of Tic Tac Toe either silently or with verbose output.
- Interactive Game: Allows the user to interactively play Tic Tac Toe against the trained agent.
- Round V: Rounds all Q-values to one decimal place.
- Save V Table: Saves the learned Q-values to a CSV file.
  
  **Private Helper Methods:**
  - '__state_values': Calculates Q-values for all possible moves.
  - 'argmax_V', 'argmin_V', '__random_V': Helper methods for selecting moves based on Q-values.
  - '__reward': Computes the reward for the agent based on the game outcome.
  - '__request_human_move': Prompts the user for a valid move during interactive gameplay.

**3. 'demo_game_stats' Function**
- Demo Game Stats: Runs multiple Tic Tac Toe games to gather statistics on win/draw percentages for 'X', 'O', and draws.

**4. Main Execution Block**
- Initializes an instance of 'Agent' with 'TicTacToeGame'.
- Trains the agent ('learn_game') over 30,000 episodes.
- Offers the user the option to play interactive games against the trained agent.

**Functionality Overview:**
- **Training:** The agent learns to play Tic Tac Toe by playing against itself using reinforcement learning (Q-learning).
- **Interactive Gameplay:** Users can choose to play Tic Tac Toe against the trained agent, selecting 'X' or 'O'.
- **Statistics:** After training, the code provides statistics on game outcomes (win/draw percentages).

**Usage:**
- Copy the entire code into a Jupyter Notebook or Python script.
- Run the script to train the agent and interactively play Tic Tac Toe.
- Modify parameters such as "epsilon", 'alpha', or the number of training episodes to experiment with different learning behaviors.

This setup encapsulates a complete implementation of Tic Tac Toe with a reinforcement learning agent, demonstrating both training and interactive gameplay capabilities. Adjustments can be made for further customization or integration into larger projects.
