import keras as ks
import numpy as np
import os
import sys
import random
path = os.path.dirname(os.path.abspath(__file__))[0:-10]
sys.path.insert(0, path)

from Game.ChessState import *
from Search import SearchAgent

# class RLSearchAgent(SearchAgent):

#     def __init__(self):
#         pass

#     def get_action(self, chess_state: ChessState, agent: Color):
#         return
        


MAX_TURNS = 200
EPSILON = 0.25
ALPHA = 0.1
GAMMA = 0.9

class RLModel():

    def __init__(self):

        state_input = ks.Input(shape=(8,8,12))
        action_input = ks.Input(shape=(8,8,2))
        combined_input = ks.layers.Concatenate()([state_input, action_input])
        flatten = ks.layers.Flatten()(combined_input)
        first_dense = ks.layers.Dense(128, activation='relu')(flatten)


        last_dense = ks.layers.Dense(1, activation='linear')(first_dense)

        model = ks.Model(inputs={"state_input": state_input, "action_input": action_input}, outputs={"Q_value": last_dense})



        self.model = model
        self.model.compile(optimizer=ks.optimizers.Adam(learning_rate=0.05), loss='MeanSquaredError', metrics=['Accuracy'])
        self.model.summary()


    def train(self, epochs: int):
        for epoch in range(epochs):
            sequence = []
            
            chess_state = ChessState(DEFAULT_BOARD)
            agent = Color.WHITE

            for turn in range(MAX_TURNS):
                if chess_state.is_end_state(agent):
                    break
                legal_moves = chess_state.get_legal_moves(agent)
                if random.random() < EPSILON:
                    action = random.choice(legal_moves)
                else:
                    q_values = []
                    for l in legal_moves:
                        q_values.append(self.get_q_value(chess_state, l))
                    if agent == Color.WHITE:
                        action = legal_moves[q_values.index(max(q_values))]
                    else:
                        action = legal_moves[q_values.index(min(q_values))]

                successor_state = chess_state.get_successor_state(action, agent)
                reward = chess_state.get_reward_from(action, agent)
                current_q = self.get_q_value(chess_state, action)
                successor_q = max([self.get_q_value(successor_state, succ_action) for succ_action in successor_state.get_legal_moves(agent.get_opposite())])

                updated_q = current_q + ALPHA * (reward + GAMMA * successor_q - current_q)

                sequence.append(({"state_input": self.vectorize_state(chess_state), "action_input": self.vectorize_action(action)}, {"Q_value": updated_q}))

                agent = agent.get_opposite()
                chess_state = successor_state
                
            
            self.model.fit(x=iter(sequence))


            if epoch % 20 == 0:
                self.model.save('my_model.h5')
            print(epoch)



    def get_q_value(self, chess_state: ChessState, action: Action):
        one_hot_state = self.vectorize_state(chess_state)
        one_hot_action = self.vectorize_action(action)
        return self.model.predict({"state_input": one_hot_state, "action_input": one_hot_action})['Q_value']



    def vectorize_state(self, chess_state: ChessState):
        
        one_hot = []
        for i, row in enumerate(chess_state.pieces):
            one_hot.append([])
            for j, piece in enumerate(row):
                one_hot[i].append([0] * 12)
                if piece != Piece.EMPTY:
                    one_hot[i][j][piece.value] = 1

        result = np.array(one_hot)
        result = np.expand_dims(result, 0)
        return result


    def vectorize_action(self, action: Action):
        
        one_hot = []
        for i in range(8):
            one_hot.append([])
            for j in range(8):
                one_hot[i].append([])
                one_hot[i][j].append(1 if (i, j) == action.start_pos else 0)
                one_hot[i][j].append(1 if (i, j) == action.end_pos else 0)

        result = np.array(one_hot)
        result = np.expand_dims(result, 0)
        return result


if __name__ == '__main__':
    model = RLModel()
    model.train(10000000)
