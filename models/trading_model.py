from stable_baselines3 import PPO
import gym
from gym import spaces
import numpy as np

# Function to load the model
def load_model():
    """Load the pre-trained PPO trading model."""
    return PPO.load("stock_trading_ppo_model")

# Custom Gym environment for stock trading
class StockTradingEnv(gym.Env):
    """Custom environment for stock trading."""
    
    def __init__(self, data):
        super(StockTradingEnv, self).__init__()
        self.data = data.reset_index(drop=True)
        self.current_step = 0
        self.balance = 100000
        self.shares_held = 0
        self.net_worth = self.balance
        self.max_steps = len(self.data) - 1

        # Define action and observation space
        self.action_space = spaces.Discrete(3)  # [Hold, Buy, Sell]
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32
        )

    def reset(self):
        """Reset the environment to an initial state."""
        self.current_step = 0
        self.balance = 100000
        self.shares_held = 0
        self.net_worth = self.balance
        return self._get_observation()

    def _get_observation(self):
        """Get the current observation of the environment."""
        obs = self.data[['Price', 'Change %', 'Volume', 'High', 'Low', 'Volatility', 'Price_SMA10']].iloc[self.current_step].values
        obs = np.nan_to_num(obs, nan=0.0, posinf=0.0, neginf=0.0)
        return obs.astype(np.float32)

    def step(self, action):
        """Execute one step in the environment."""
        current_price = self.data['Price'].iloc[self.current_step]

        # Execute the action
        if action == 1 and self.balance >= current_price:  # Buy
            self.shares_held += 1
            self.balance -= current_price
        elif action == 2 and self.shares_held > 0:  # Sell
            self.shares_held -= 1
            self.balance += current_price

        # Update net worth and reward
        self.net_worth = self.balance + (self.shares_held * current_price)
        reward = (self.net_worth - 100000) / 100000

        # Advance step
        self.current_step += 1
        done = self.current_step >= self.max_steps

        return self._get_observation(), reward, done, {}
