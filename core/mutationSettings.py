class MutationSettings:
    def __init__(self, radius, cap, brain, number_of_brain_changes=None, change_gene_probability=None, gene_max=None):
        # for all agents
        self.change_radius_probability = radius
        self.change_energy_cap_probability = cap
        self.change_brain_probability = brain
        
        # for interpreter brain
        self.number_of_brain_changes = number_of_brain_changes
        self.change_gene_probability = change_gene_probability
        self.gene_max = gene_max
