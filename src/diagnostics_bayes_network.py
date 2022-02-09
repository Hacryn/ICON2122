import bnlearn
from pgmpy.factors.discrete import TabularCPD

def runbn():
    bn = DiagnosticsBN()
    #bn.plotDAG()
    #bn.plotCPD()
    bn.testMalattia()

class DiagnosticsBN:

    def __init__(self):
        # Make a DAG with the edges
        self.Edges = [('Malattia', 'Nausea'),
                 ('Malattia', 'Perdita di peso'),
                 ('Malattia', 'Diarrea'),
                 ('Malattia', 'Ciste'),
                 ('Malattia', 'Ulcera'),
                 ('Ciste', 'Nausea'),
                 ('Ciste', 'Dolore addominale'),
                 ('Ciste', 'Ulcera'),
                 ('Ulcera', 'Dolore addominale'),
                 ('Ulcera', 'Acidità di stomaco'),
                 ('Nausea', 'Vomito')]
        # Assign CPT (Conditional Probabilities Table) for every node in the DAG
        self.MalattiaCPT = TabularCPD(variable='Malattia',
                                      variable_card=2,
                                      values=[[0.99],
                                              [0.01]])
        self.DiarreaCPT = TabularCPD(variable='Diarrea',
                                     variable_card=2,
                                     values=[[0.70, 0.30],
                                             [0.30, 0.70]],
                                     evidence=['Malattia'],
                                     evidence_card=[2])
        self.PesoCPT = TabularCPD(variable="Perdita di peso",
                                  variable_card=2,
                                  values=[[0.95, 0.40],
                                          [0.05, 0.60]],
                                  evidence=['Malattia'],
                                  evidence_card=[2])
        self.CisteCPT = TabularCPD(variable="Ciste",
                                   variable_card=2,
                                   values=[[0.95, 0.50],
                                           [0.05, 0.50]],
                                   evidence=['Malattia'],
                                   evidence_card=[2])
        self.NauseaCPT = TabularCPD(variable='Nausea',
                                    variable_card=2,
                                    values=[[0.75, 0.70, 0.50, 0],
                                            [0.25, 0.30, 0.50, 1]],
                                    evidence=['Malattia', 'Ciste'],
                                    evidence_card=[2,2])
        self.VomitoCPT = TabularCPD(variable='Vomito',
                                    variable_card=2,
                                    values=[[0.85, 0.40],
                                            [0.15, 0.60]],
                                    evidence=['Nausea'],
                                    evidence_card=[2])
        self.UlceraCPT = TabularCPD(variable='Ulcera',
                                    variable_card=2,
                                    values=[[0.95, 0.95, 0.70, 1],
                                            [0.05, 0.05, 0.30, 0]],
                                    evidence=['Malattia', 'Ciste'],
                                    evidence_card=[2,2])
        self.DoloreCPT = TabularCPD(variable='Dolore addominale',
                                    variable_card=2,
                                    values=[[0.80, 0, 0.80, 0],
                                            [0.20, 1, 0.20, 1]],
                                    evidence=['Ciste', 'Ulcera'],
                                    evidence_card=[2,2])
        self.AcidoCPT = TabularCPD(variable='Acidità di stomaco',
                                   variable_card=2,
                                   values=[[0.70, 0],
                                           [0.30, 1]],
                                   evidence=['Ulcera'],
                                   evidence_card=[2])
        # Connect the DAG with the CPTS
        self.DAG = bnlearn.make_DAG(self.Edges, CPD=[
            self.MalattiaCPT,
            self.DiarreaCPT,
            self.PesoCPT,
            self.CisteCPT,
            self.NauseaCPT,
            self.VomitoCPT,
            self.UlceraCPT,
            self.DoloreCPT,
            self.AcidoCPT
        ])


    def plotDAG(self): bnlearn.plot(self.DAG)

    def plotCPD(self): bnlearn.print_CPD(self.DAG)

    def testMalattia(self):
        q = bnlearn.inference.fit(self.DAG, variables=['Malattia'], evidence={'Vomito': 1})
        print(q)