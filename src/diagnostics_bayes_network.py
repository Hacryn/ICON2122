import bnlearn, pandas
from dataset import Dataset
from text_interface import ask_question
from pgmpy.factors.discrete import TabularCPD

DEBUG = False


def runbn(dataset: Dataset, mode: str = "normal", method: str = "ml"):
    if dataset.training is None and  method == "learn":
        print("Dataset di training vuoto, carica un dataset")
        return

    evidences = {
        'Nausea': int(ask_question("Avverti un senso di nausea?")),
        'Vomito': int(ask_question("Hai avuto attacchi di vomito ultimamente?")),
        'Perdita di peso': int(ask_question("Hai subito una perdita di peso inaspettata ultimamente?")),
        'Diarrea': int(ask_question("Hai avuto attachi di diarrea nell'ultimo periodo?")),
        'Dolore addominale': int(ask_question("Avverti dolore nella zona addominale?")),
        'Rigonfiamento': int(ask_question("Noti dei rigonfiamenti nella zona addominale?")),
        'Acidità di stomaco': int(ask_question("Stai soffrendo di acidità di stomaco?"))
    }
    if ask_question("Hai effettuato un esame gastrointestinale (come RM/TAC)?"):
        evidences["Ciste"] = ask_question("L'esame ha rilevato la presenza di una cisti nella zona?")
    bayes_network = DiagnosticsBN()
    if mode == "learn": bayes_network.learn_from_dataset(dataset.training, method)
    result = get_result(bayes_network.inference(evidences))
    probability = (result["p"])[1] * 100
    print("La probabilità di avere la malattia è %.2f" % probability)
    if probability >= 50: print("È consigliabile recarsi da un medico da un medico per ulteriori accertamenti")


def testbn(dataset: Dataset, method: str = 'ml'):
    if dataset.training is None:
        print("Dataset di training vuoto, carica un dataset")
        return
    if dataset.test is None:
        print("Dataset di test vuoto, carica un dataset")
        return

    bayes_network = DiagnosticsBN()
    bayes_network.learn_from_dataset(dataset.training, method)

    tp: int = 0
    tn: int = 0
    fp: int = 0
    fn: int = 0
    for i in range(len(dataset.test)):
        evidences = {
            'Nausea': dataset.test.loc[i, 'Nausea'],
            'Vomito': dataset.test.loc[i, 'Vomito'],
            'Perdita di peso': dataset.test.loc[i, 'Perdita di peso'],
            'Diarrea': dataset.test.loc[i, 'Diarrea'],
            'Dolore addominale': dataset.test.loc[i, 'Dolore addominale'],
            'Rigonfiamento': dataset.test.loc[i, 'Rigonfiamento'],
            'Acidità di stomaco': dataset.test.loc[i, 'Acidità di stomaco']
        }
        probability = (get_result(bayes_network.inference(evidences))["p"])[1] * 100
        if probability >= 50 and dataset.test.loc[i, 'Malattia'] == 1: tp = tp + 1
        if probability >= 50 and dataset.test.loc[i, 'Malattia'] == 0: fp = fp + 1
        if probability < 50 and dataset.test.loc[i, 'Malattia'] == 1: fn = fn + 1
        if probability < 50 and dataset.test.loc[i, 'Malattia'] == 0: tn = tn + 1

    accuracy = safe_division(tp + tn, tp + tn + fp + fn)
    precision = safe_division(tp, tp + fp)
    recall = safe_division(tp, tp + fn)
    f1 = safe_division(2 * precision * recall, precision + recall)

    print("TP %d TN %d FP %d FN %d" % (tp, tn, fp, fn))

    print("Accuratezza: %.4f" % accuracy)
    print("Precisione: %.4f" % precision)
    print("Richiamo: %.4f" % recall)
    print("Punteggio F1: %.4f" % f1)


def safe_division(n, d):
    return n / d if d else 0


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
        self.DAG = bnlearn.make_DAG(self.Edges, verbose=0)
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

