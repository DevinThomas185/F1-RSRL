import torch


class SharedAdam(torch.optim.Adam):
    def __init__(self, params, lr, weight_decay):
        super(SharedAdam, self).__init__(params, lr=lr, weight_decay=weight_decay)

        # State initialization
        for group in self.param_groups:
            for p in group["params"]:
                state = self.state[p]
                state["step"] = 0
                state["exp_avg"] = torch.zeros_like(p.data)
                state["exp_avg_sq"] = torch.zeros_like(p.data)

                # Share in memory
                state["exp_avg"].share_memory_()
                state["exp_avg_sq"].share_memory_()
