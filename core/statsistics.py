class Statistics:

    def __init__(self):
        self.num_agents = []
        self.bots_energy = []
        self.env_energy = []
        self.total_energy = []
        self.avg_brain_len = []
        self.max_brain_len = []

    def add_tick(self, num_agents, bots_energy, env_energy, avg_brain_len, max_brain_len):
        self.num_agents.append(num_agents)
        self.bots_energy.append(bots_energy)
        self.env_energy.append(env_energy)
        self.total_energy.append(bots_energy + env_energy)
        self.avg_brain_len.append(avg_brain_len)
        self.max_brain_len.append(max_brain_len)

    def get_tick(self, i):
        return (self.num_agents[i], self.bots_energy[i], self.env_energy[i], self.total_energy[i],
                self.avg_brain_len[i], self.max_brain_len[i])
