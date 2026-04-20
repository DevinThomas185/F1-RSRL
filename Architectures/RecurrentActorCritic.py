import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def normalized_columns_initializer(weights, std=1.0):
    out = torch.randn(weights.size())
    out *= std / torch.sqrt(out.pow(2).sum(1, keepdim=True))
    return out


def weights_init(m):
    classname = m.__class__.__name__
    if classname.find("Linear") != -1:
        weight_shape = list(m.weight.data.size())
        fan_in = weight_shape[1]
        fan_out = weight_shape[0]
        w_bound = np.sqrt(6.0 / (fan_in + fan_out))
        m.weight.data.uniform_(-w_bound, w_bound)
        m.bias.data.fill_(0)


class RecurrentActorCritic(nn.Module):
    __slots__ = []

    def __init__(self, input_size, hidden_size, output_size, num_layers=1):
        super(RecurrentActorCritic, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers

        self.pre_lstm = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.LeakyReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.LeakyReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.LeakyReLU(),
        )

        self.lstm_cell = nn.LSTMCell(
            input_size=hidden_size,
            hidden_size=hidden_size,
        )

        self.actor_linear = nn.Linear(hidden_size, output_size)
        self.critic_linear = nn.Linear(hidden_size, 1)

        self.apply(weights_init)
        self.actor_linear.weight.data = normalized_columns_initializer(
            self.actor_linear.weight.data, 0.01
        )
        self.actor_linear.bias.data.fill_(0)
        self.critic_linear.weight.data = normalized_columns_initializer(
            self.critic_linear.weight.data, 1.0
        )
        self.critic_linear.bias.data.fill_(0)

        self.lstm_cell.bias_ih.data.fill_(0)
        self.lstm_cell.bias_hh.data.fill_(0)

        self.train()

    def forward(self, x, h_c=None, device="cpu"):
        if h_c is None:
            h_c = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)

        x = self.pre_lstm(x)
        hx, cx = self.lstm_cell(x, h_c)
        x = hx

        actor_output = self.actor_linear(x)
        critic_output = self.critic_linear(x)

        return actor_output, critic_output, (hx, cx)

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.hidden_size).to(device),
            torch.zeros(self.hidden_size).to(device),
        )



#############################


class ACNet(nn.Module):
    def __init__(self, s_dim, a_dim):
        super(ACNet, self).__init__()

        self.policy = nn.Sequential(
            nn.Linear(s_dim, 128),
            nn.LeakyReLU(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.1),
            nn.Linear(128, a_dim),
        )

        self.value = nn.Sequential(
            nn.Linear(s_dim, 128),
            nn.LeakyReLU(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.1),
            nn.Linear(128, 1),
        )

        # Init weights of policy and value
        self.policy.apply(self._weights_init)
        self.value.apply(self._weights_init)

        self.distribution = torch.distributions.Categorical

    def _weights_init(self, m):
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, 0, 0.1)
            nn.init.constant_(m.bias, 0.1)


    def forward(self, x):
        logits = self.policy(x)
        values = self.value(x)
        return logits, values
    
    def choose_action(self, s):
        self.eval()
        logits, _ = self.forward(s)
        prob = F.softmax(logits, dim=-1).data
        m = self.distribution(prob)
        return m.sample().numpy()
    
    def max_action(self, s):
        self.eval()
        logits, _ = self.forward(s)
        prob = F.softmax(logits, dim=-1).data
        return prob.argmax(-1).numpy()
    
    def loss_func(self, s, a, v_t):
        self.train()
        logits, values = self.forward(s)
        td = v_t - values
        c_loss = td.pow(2)

        probs = F.softmax(logits, dim=1)
        m = self.distribution(probs)
        exp_v = m.log_prob(a) * td.detach().squeeze()
        a_loss = -exp_v
        return a_loss, c_loss
