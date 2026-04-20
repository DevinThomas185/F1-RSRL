import torch
from torch import nn
import torch.nn.functional as F

from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState


class HPT_1_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_1_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 128

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=64,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_2_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_2_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 256

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_3_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_3_RecurrentQN, self).__init__()
        self.num_layers = 3
        self.hidden_size = 128

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=64,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_4_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_4_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 128

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=64,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_5_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_5_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 128

        self.pre_gru = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.gru = nn.GRU(
            input_size=64,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_gru = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_gru(x)
        x, new_h = self.gru(x, h)
        x = self.post_gru(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)


class HPT_6_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_6_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 128

        self.pre_gru = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.gru = nn.GRU(
            bidirectional=True,
            input_size=64,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_gru = nn.Sequential(
            nn.Linear(self.hidden_size * 2, 64),
            nn.ReLU(),
            nn.Linear(64, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_gru(x)
        x, new_h = self.gru(x, h)
        x = self.post_gru(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return torch.zeros(self.num_layers * 2, batch_size, self.hidden_size).to(device)


class HPT_7_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_7_RecurrentQN, self).__init__()
        self.num_layers = 3
        self.hidden_size = 128

        self.pre_gru = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.gru = nn.GRU(
            input_size=64,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_gru = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_gru(x)
        x, new_h = self.gru(x, h)
        x = self.post_gru(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)


class HPT_8_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_8_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 128

        self.pre_rnn = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.rnn = nn.RNN(
            input_size=64,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_rnn = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_rnn(x)
        x, new_h = self.rnn(x, h)
        x = self.post_rnn(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)


class HPT_9_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_9_RecurrentQN, self).__init__()
        self.num_layers = 3
        self.hidden_size = 128

        self.pre_rnn = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
        )
        self.rnn = nn.RNN(
            input_size=64,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_rnn = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_rnn(x)
        x, new_h = self.rnn(x, h)
        x = self.post_rnn(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)


class HPT_10_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_10_RecurrentQN, self).__init__()
        self.num_layers = 3
        self.hidden_size = 128

        self.lstm = nn.LSTM(
            input_size=UnifiedRaceState.size(),
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, len(SimpleRaceStrategy)),
        )

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_11_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_11_RecurrentQN, self).__init__()
        self.num_layers = 3
        self.hidden_size = 128

        self.gru = nn.GRU(
            input_size=UnifiedRaceState.size(),
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_gru = nn.Sequential(
            nn.Linear(self.hidden_size, len(SimpleRaceStrategy)),
        )

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x, new_h = self.gru(x, h)
        x = self.post_gru(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)


class HPT_12_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_12_RecurrentQN, self).__init__()
        self.num_layers = 3
        self.hidden_size = 128

        self.rnn = nn.RNN(
            input_size=UnifiedRaceState.size(),
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_rnn = nn.Sequential(
            nn.Linear(self.hidden_size, len(SimpleRaceStrategy)),
        )

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x, new_h = self.rnn(x, h)
        x = self.post_rnn(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device)


class HPT_13_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_13_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 256

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_14_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_14_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 256

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 128),
            nn.ELU(),
            nn.Linear(128, 128),
            nn.ELU(),
            nn.Linear(128, 128),
            nn.ELU(),
        )
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ELU(),
            nn.Linear(128, 128),
            nn.ELU(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_15_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_15_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 256

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 128),
            nn.Tanh(),
            nn.Linear(128, 128),
            nn.Tanh(),
            nn.Linear(128, 128),
            nn.Tanh(),
        )
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.Tanh(),
            nn.Linear(128, 128),
            nn.Tanh(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_16_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_16_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 256

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 128),
            nn.Sigmoid(),
            nn.Linear(128, 128),
            nn.Sigmoid(),
            nn.Linear(128, 128),
            nn.Sigmoid(),
        )
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.Sigmoid(),
            nn.Linear(128, 128),
            nn.Sigmoid(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_17_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_17_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 256

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 128),
            nn.ReLU6(),
            nn.Linear(128, 128),
            nn.ReLU6(),
            nn.Linear(128, 128),
            nn.ReLU6(),
        )
        self.lstm = nn.LSTM(
            input_size=128,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 128),
            nn.ReLU6(),
            nn.Linear(128, 128),
            nn.ReLU6(),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_18_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_18_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 512

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=256,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_19_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_19_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 1024

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=512,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )


class HPT_20_RecurrentQN(nn.Module):
    def __init__(self):
        super(HPT_20_RecurrentQN, self).__init__()
        self.num_layers = 1
        self.hidden_size = 1024

        self.pre_lstm = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=512,
            hidden_size=self.hidden_size,
            batch_first=True,
            num_layers=self.num_layers,
        )
        self.post_lstm = nn.Sequential(
            nn.Linear(self.hidden_size, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, len(SimpleRaceStrategy)),
        )

        self.__init_weights()

    def __init_weights(self):
        for m in self.modules():
            if type(m) == nn.Linear:
                torch.nn.init.xavier_normal_(m.weight)
                m.bias.data.fill_(0.01)

    def forward(self, x, h=None, device="cpu"):
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)

        # Input x: (batch_size, time_steps, input_size)
        x = self.pre_lstm(x)
        x, new_h = self.lstm(x, h)
        x = self.post_lstm(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )

