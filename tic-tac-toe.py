import numpy as np
import csv
import random
from itertools import groupby

class TicTacToeGame():
    def __init__(self):
        self.state = '         '
        self.player = 'X'
        self.winner = None

    def allowed_moves(self):
        states = []
        for i in range(len(self.state)):
            if self.state[i] == ' ':
                states.append(self.state[:i] + self.player + self.state[i+1:])
        return states

    def make_move(self, next_state):
        if self.winner:
            raise(Exception("Game already completed, cannot make another move!"))
        if not self.__valid_move(next_state):
            raise(Exception("Cannot make move {} to {} for player {}".format(
                    self.state, next_state, self.player)))

        self.state = next_state
        self.winner = self.predict_winner(self.state)
        if self.winner:
            self.player = None
        elif self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'

    def playable(self):
        return ( (not self.winner) and any(self.allowed_moves()) )

    def predict_winner(self, state):
        lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        winner = None
        for line in lines:
            line_state = state[line[0]] + state[line[1]] + state[line[2]]
            if line_state == 'XXX':
                winner = 'X'
            elif line_state == 'OOO':
                winner = 'O'
        return winner

    def __valid_move(self, next_state):
        allowed_moves = self.allowed_moves()
        if any(state == next_state for state in allowed_moves):
            return True
        return False

    def print_board(self):
        s = self.state
        print('     {} | {} | {} '.format(s[0],s[1],s[2]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[3],s[4],s[5]))
        print('    -----------')
        print('     {} | {} | {} '.format(s[6],s[7],s[8]))


class Agent():
    def __init__(self, game_class, epsilon=0.1, alpha=0.5, value_player='X'):
        self.V = dict()
        self.NewGame = game_class
        self.epsilon = epsilon
        self.alpha = alpha
        self.value_player = value_player

    def state_value(self, game_state):
        return self.V.get(game_state, 0.0)

    def learn_game(self, num_episodes=1000):
        for episode in range(1, num_episodes + 1):
            self.learn_from_episode()
            if episode in [500, 1000, 5000, 10000, 20000, 30000]:
                print(f"After {episode} games:")
                demo_game_stats(self)

    def learn_from_episode(self):
        game = self.NewGame()
        _, move = self.learn_select_move(game)
        while move:
            move = self.learn_from_move(game, move)

    def learn_from_move(self, game, move):
        game.make_move(move)
        r = self.__reward(game)
        td_target = r
        next_state_value = 0.0
        selected_next_move = None
        if game.playable():
            best_next_move, selected_next_move = self.learn_select_move(game)
            next_state_value = self.state_value(best_next_move)
        current_state_value = self.state_value(move)
        td_target = r + next_state_value
        self.V[move] = current_state_value + self.alpha * (td_target - current_state_value)
        return selected_next_move

    def learn_select_move(self, game):
        allowed_state_values = self.__state_values(game.allowed_moves())
        if game.player == self.value_player:
            best_move = self.__argmax_V(allowed_state_values)
        else:
            best_move = self.__argmin_V(allowed_state_values)

        selected_move = best_move
        if random.random() < self.epsilon:
            selected_move = self.__random_V(allowed_state_values)

        return best_move, selected_move

    def play_select_move(self, game):
        allowed_state_values = self.__state_values(game.allowed_moves())
        if game.player == self.value_player:
            return self.__argmax_V(allowed_state_values)
        else:
            return self.__argmin_V(allowed_state_values)

    def demo_game(self, verbose=False):
        game = self.NewGame()
        t = 0
        while game.playable():
            if verbose:
                print(f"\nTurn {t}\n")
                game.print_board()
            move = self.play_select_move(game)
            game.make_move(move)
            t += 1
        if verbose:
            print(f"\nTurn {t}\n")
            game.print_board()
        if game.winner:
            if verbose:
                print(f"\n{game.winner} is the winner!")
            return game.winner
        else:
            if verbose:
                print("\nIt's a draw!")
            return '-'

    def interactive_game(self):
        while True:
            play_game = input("Do you want to play a game of Tic Tac Toe? (yes/no): ").lower()
            if play_game != 'yes':
                print("Maybe next time!")
                return
            
            while True:
                agent_player = input("Do you want to play as 'X' or 'O'? ").upper()
                if agent_player == 'X' or agent_player == 'O':
                    break
                else:
                    print("Invalid choice. Please choose 'X' or 'O'.")

            while True:
                game = self.NewGame()
                human_player = agent_player
                if agent_player == 'X':
                    agent_player = 'O'
                else:
                    agent_player = 'X'

                t = 0
                while game.playable():
                    print(f"\nTurn {t}\n")
                    game.print_board()
                    if game.player == agent_player:
                        move = self.play_select_move(game)
                        game.make_move(move)
                    else:
                        move = self.__request_human_move(game)
                        game.make_move(move)
                    t += 1

                print(f"\nTurn {t}\n")
                game.print_board()

                if game.winner:
                    print(f"\n{game.winner} is the winner!")
                else:
                    print("\nIt's a draw!")

                break

        print("Thanks for playing!")
        
    def round_V(self):
        for k in self.V.keys():
            self.V[k] = round(self.V[k], 1)

    def save_v_table(self):
        with open('state_values.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['State', 'Value'])
            all_states = list(self.V.keys())
            all_states.sort()
            for state in all_states:
                writer.writerow([state, self.V[state]])

    def __state_values(self, game_states):
        return {state: self.state_value(state) for state in game_states}

    def __argmax_V(self, state_values):
        max_V = max(state_values.values())
        chosen_state = random.choice([state for state, v in state_values.items() if v == max_V])
        return chosen_state

    def __argmin_V(self, state_values):
        min_V = min(state_values.values())
        chosen_state = random.choice([state for state, v in state_values.items() if v == min_V])
        return chosen_state

    def __random_V(self, state_values):
        return random.choice(list(state_values.keys()))

    def __reward(self, game):
        if game.winner == self.value_player:
            return 1.0
        elif game.winner:
            return -1.0
        else:
            return 0.0

    def __request_human_move(self, game):
        allowed_moves = [i + 1 for i in range(9) if game.state[i] == ' ']
        human_move = None
        while not human_move:
            idx = int(input(f'Choose move for {game.player}, from {allowed_moves}: '))
            if idx in allowed_moves:
                human_move = game.state[:idx - 1] + game.player + game.state[idx:]
        return human_move

def demo_game_stats(agent):
    results = [agent.demo_game() for _ in range(10000)]
    game_stats = {k: results.count(k) / 100 for k in ['X', 'O', '-']}
    print(f"    Percentage results: {game_stats}")

if __name__ == '__main__':
    agent = Agent(TicTacToeGame, epsilon=0.1, alpha=1.0)
    print("Training the agent...")
    agent.learn_game(30000)
    print("Training completed.")

    while True:
        agent.interactive_game()
        break
    print("Thanks for playing")
