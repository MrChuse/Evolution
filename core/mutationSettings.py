class MutationSettings:
    def __init__(self, radius, cap, brain, brain_changes=None, gene=None, gene_max=None):
        # for all agents
        self.change_radius_probability = radius
        self.change_energy_cap_probability = cap
        self.change_brain_probability = brain
        
        # for enterpreter brain
        self.number_of_brain_changes = brain_changes
        self.change_gene_probability = gene
        self.gene_max = gene_max
