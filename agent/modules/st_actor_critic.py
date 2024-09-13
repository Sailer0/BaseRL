import torch
import torch.nn as nn
import torch.nn.functional as F
from modules.base_network import ChkptModule


# define the actor network
class Actor(ChkptModule):
    def __init__(self, args, network_type):
        super(Actor, self).__init__(args, network_type)
        # 获取 args 中的维度信息
        self.fc_input_dim = args.agent_obs_dim
        self.hidden_dim = args.actor_hidden_dim
        self.output_dim = args.agent_action_dim

        # 定义 actor 的核心网络
        self.fc1 = nn.Linear(self.fc_input_dim, self.hidden_dim)
        self.fc2 = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.action_out = nn.Linear(self.hidden_dim, self.output_dim)
        self.std_out = nn.Linear(self.hidden_dim, self.output_dim)

        self.fc1.weight.data.normal_(0, 0.1)
        self.fc2.weight.data.normal_(0, 0.1)
        self.action_out.weight.data.normal_(0, 0.1)
        self.std_out.weight.data.normal_(0, 0.1)

    def forward(self, x):
        # 转换观测三维为二维
        x = x.reshape([-1, self.fc_input_dim])

        # 三层全连接神经网络
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        actions = torch.tanh(self.action_out(x))
        std = F.softplus(self.std_out(x))
        return actions, std


class Critic(ChkptModule):
    def __init__(self, args, network_type):
        super(Critic, self).__init__(args, network_type)

        # 获取 args 中的维度信息
        self.fc_input_dim = args.agent_obs_dim
        self.hidden_dim = args.critic_hidden_dim
        self.output_dim = 1

        # 定义 Critic 的核心网络
        self.fc1 = nn.Linear(self.fc_input_dim, self.hidden_dim)
        self.fc2 = nn.Linear(self.hidden_dim, self.hidden_dim)
        self.q_out = nn.Linear(self.hidden_dim, 1)

        self.fc1.weight.data.normal_(0, 0.1)
        self.fc2.weight.data.normal_(0, 0.1)
        self.q_out.weight.data.normal_(0, 0.1)

    def forward(self, state):
        # 转化观测三维为二维，并concat与action
        x = state.reshape([-1, self.fc_input_dim])

        # 三层全连接神经网络
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        q_value = self.q_out(x)
        return q_value

