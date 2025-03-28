import numpy as np
import tensorflow as tf
from src.constants import *

class CheckersAI:
    def __init__(self):
        self.model = None
        
    def load_model(self, model_path):
        """Load a trained model from file."""
        try:
            self.model = tf.keras.models.load_model(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            # Create a simple fallback model if loading fails
            self.model = self._create_fallback_model()
    
    def _create_fallback_model(self):
        """Create a simple model for fallback."""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(32,)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(32, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return model
    
    def get_move(self, state, valid_moves):
        """Get the next move from the AI."""
        if not valid_moves:
            return None
            
        # Convert state to model input format
        state_input = self._preprocess_state(state)
        
        # Get model predictions
        try:
            predictions = self.model.predict(state_input, verbose=0)[0]
            
            # Mask invalid moves
            valid_moves_list = list(valid_moves.keys())
            valid_moves_mask = np.zeros(32)
            for move in valid_moves_list:
                action = self._move_to_action(move)
                if action < 32:  # Ensure action is valid
                    valid_moves_mask[action] = 1
                    
            # Apply mask and get best valid move
            masked_predictions = predictions * valid_moves_mask
            if np.sum(masked_predictions) == 0:
                # If no valid moves after masking, choose randomly from valid moves
                return self._action_to_move(np.random.choice(valid_moves_list))
                
            best_action = np.argmax(masked_predictions)
            return self._action_to_move(best_action)
            
        except Exception as e:
            print(f"Error making prediction: {e}")
            # Fallback to random move
            return np.random.choice(list(valid_moves.keys()))
    
    def _preprocess_state(self, state):
        """Convert game state to model input format."""
        # Flatten the state and add batch dimension
        return np.array(state).reshape(1, -1)
    
    def _move_to_action(self, move):
        """Convert a move (row, col) to an action number."""
        if isinstance(move, tuple) and len(move) == 2:
            row, col = move
            return row * 4 + col // 2
        return 0
    
    def _action_to_move(self, action):
        """Convert an action number to a move (row, col)."""
        if isinstance(action, tuple):
            return action
        row = action // 4
        col = (action % 4) * 2 + (row % 2)
        return (row, col) 