import bnlearn
import pandas
from pgmpy.factors.discrete import TabularCPD
from dataset_gen import load_dataset
from diagnostics_expert_system import askquestion

DEBUG = False

def runbn(mode: str = "normal", method: str = "ml",dataset = "data/dataset.csv"):
    evidences = {
        'Nausea': int(askquestion("Hai la nausea?")),
        'Vomito': int(askquestion("Soffri di vomito?")),
        'Perdita di peso': int(askquestion("Hai subito una perdita di peso inaspettata?")),
        'Diarrea': int(askquestion("Soffri di diarrea?")),
        'Dolore addominale': int(askquestion("Soffri di dolore addominale?")),
        'Rigonfiamento': int(askquestion("Hai un rigonfiamento nella zona addominale?")),
        'Acidità di stomaco': int(askquestion("Soffri di acidità di stomaco?"))
    }
    if askquestion("Hai effettuato un esame gastrointestinale (come RM/TAC)?"):
        evidences["Ciste"] = askquestion("L'esame ha rilevato la presenza di una ciste nella zona?")
    bayes_network = DiagnosticsBN()
    if mode == "learn": bayes_network.learn_from_dataset(load_dataset(dataset), method)
    result = get_result(bayes_network.inference(evidences))
    probability = (result["p"])[1] * 100
    print("La probabilità di avere la malattia è %.2f" % probability)
    if probability >= 50: print("Ti conviene contattare il tuo medico")

def testrun():
    bn = DiagnosticsBN()
    rs = bn.test()
    df = bnlearn.bnlearn.query2df(rs)
    pm = df['p']
    print("La probabilità di avere la malattia è %.2f" % (pm[1] * 100))

def get_result(query) -> pandas.DataFrame:
    return bnlearn.bnlearn.query2df(query)

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
                 ('Ciste', 'Rigonfiamento'),
                 ('Ulcera', 'Dolore addominale'),
                 ('Ulcera', 'Acidità di stomaco'),
                 ('Nausea', 'Vomito')]
        # Assign CPT (Conditional Probabilities Table) for every node in the DAG
        self.MalattiaCPT = TabularCPD(variable='Malattia',
                                      variable_card=2,
                                      values=[[0.97],
                                              [0.03]])
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
                                    values=[[0.80, 0, 0.70, 0],
                                            [0.20, 1, 0.30, 1]],
                                    evidence=['Ciste', 'Ulcera'],
                                    evidence_card=[2,2])
        self.RigonfiamentoCPT = TabularCPD(variable="Rigonfiamento",
                                           variable_card=2,
                                           values=[[0.90, 0.50],
                                                  [0.10, 0.50]],
                                           evidence=['Ciste'],
                                            evidence_card = [2])
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
            self.RigonfiamentoCPT,
            self.AcidoCPT
        ], verbose=0)

    def learn_from_dataset(self, dataset, method):
        self.DAG = bnlearn.make_DAG(self.Edges)
        self.DAG = bnlearn.parameter_learning.fit(self.DAG, dataset,
                                                  methodtype=method,
                                                  verbose=0)
        if DEBUG: bnlearn.print_CPD(self.DAG)

    def plot_dag(self): bnlearn.plot(self.DAG)

    def plot_cpd(self): bnlearn.print_CPD(self.DAG)

    def test(self): return bnlearn.inference.fit(self.DAG, variables=['Malattia'],
                                                 evidence={'Ciste': 1}, verbose=0)
    def inference(self, evidences): return bnlearn.inference.fit(self.DAG, variables=['Malattia'],
                                                                 evidence=evidences, verbose=0)

