import time
import sys
import argparse

from F123.F123Translator import F123Translator
from Models.StrategyRLModel import StrategyRLModel

from Classes.RaceState.UnifiedRaceState import UnifiedRaceState


def __main(udp_ip, udp_port):
    sim = F123Translator(udp_ip=udp_ip, udp_port=udp_port)

    dqn_model = StrategyRLModel.load_model("Saved Models/DQN Bahrain Thomas Testing/dqn_model_500.pth")

    t = False
    while not t:
        s = sim.step()
        if s is not None and isinstance(s, UnifiedRaceState):
            print(s, dqn_model.predict(s))
            t = s.terminal
        time.sleep(2)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", help="UDP IP address", default="192.168.0.109")
    parser.add_argument("--port", type=int, help="UDP port number", default=20780)
    args = parser.parse_args()

    sys.exit(__main(args.ip, args.port))
