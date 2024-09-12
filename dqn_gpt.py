import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import random
from collections import namedtuple, deque

# 定义 Q 网络
class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 24)
        self.fc2 = nn.Linear(24, action_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)

# 初始化经验回放记忆
Transition = namedtuple('Transition', ('state', 'action', 'reward', 'next_state', 'done'))
class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

# 设置超参数
state_dim = 4  # 状态维度，例如 CartPole 环境
action_dim = 2  # 动作维度
replay_memory_capacity = 1000
batch_size = 32
gamma = 0.99
epsilon = 0.1
epsilon_final = 0.01
epsilon_decay = 1000
target_update = 10
learning_rate = 0.001

# 初始化网络和优化器
policy_net = QNetwork(state_dim, action_dim)
target_net = QNetwork(state_dim, action_dim)
optimizer = optim.Adam(policy_net.parameters(), lr=learning_rate)
target_net.load_state_dict(policy_net.state_dict())

# 初始化经验回放记忆
memory = ReplayMemory(replay_memory_capacity)

def select_action(state, epsilon):
    if random.random() < epsilon:
        return torch.tensor([[random.randrange(action_dim)]], dtype=torch.long)
    else:
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)

def optimize_model():
    if len(memory) < batch_size:
        return

    transitions = memory.sample(batch_size)
    batch = Transition(*zip(*transitions))

    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    next_state_batch = torch.cat(batch.next_state)
    done_batch = torch.cat(batch.done)

    # 计算当前状态和动作的 Q 值
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # 计算目标 Q 值
    next_state_values = target_net(next_state_batch).max(1)[0].detach()
    expected_state_action_values = reward_batch + (1 - done_batch) * gamma * next_state_values

    # 计算损失
    loss = F.mse_loss(state_action_values, expected_state_action_values.unsqueeze(1))

    # 反向传播和优化
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

def main():
    num_episodes = 1000
    for episode in range(num_episodes):
        state = torch.tensor([[0.0, 0.0, 0.0, 0.0]], dtype=torch.float)  # 示例状态
        for t in range(100):  # 假设每个 episode 100 步
            action = select_action(state, epsilon)
            next_state = torch.tensor([[0.0, 0.0, 0.0, 0.0]], dtype=torch.float)  # 示例下一状态
            reward = torch.tensor([1.0], dtype=torch.float)  # 示例奖励
            done = torch.tensor([0], dtype=torch.float)  # 示例是否终止
            memory.push(state, action, reward, next_state, done)
            state = next_state

            optimize_model()

            if episode % target_update == 0:
                target_net.load_state_dict(policy_net.state_dict())

        # 更新 epsilon
        epsilon = max(epsilon_final, epsilon - (epsilon / epsilon_decay))

if __name__ == '__main__':
    main()
