from experta import *
from text_interface import ask_question

def runex():
    engine = DiagnosticsES()
    engine.reset()
    engine.run()

class DiagnosticsES(KnowledgeEngine):

    @DefFacts()
    def _initial_action(self):
        yield Fact(question=True)

    # SINTOMI DI BASE

    @Rule(Fact(question=True))
    def ask_pdp(self):
        self.declare(Fact(pdp=ask_question("Hai subito una perdita di peso inaspettata ultimamente?")))

    @Rule(Fact(question=True))
    def ask_diarrea(self):
        self.declare(Fact(diarrea=ask_question("Hai avuto attachi di diarrea nell'ultimo periodo?")))

    @Rule(OR(Fact(pdp=True), Fact(diarrea=True)))
    def sintomi_base(self):
        self.declare(Fact(sintomi_base=True))

    @Rule(AND(Fact(pdp=False), Fact(diarrea=False)))
    def no_sintomi_base(self):
        self.declare(Fact(sintomi_base=False))

    # NAUSEA
    @Rule(Fact(sintomi_base=True))
    def ask_nausea(self):
        self.declare(Fact(nausea=ask_question("Avverti un senso di nausea?")))

    # VOMITO
    @Rule(Fact(nausea=True))
    def ask_vomito(self):
        self.declare(Fact(vomito=ask_question("Hai avuto attacchi di vomito ultimamente?")))

    # ESAME
    @Rule(Fact(vomito=True))
    def ask_esame(self):
        self.declare(Fact(esame_fatto=ask_question("Hai svolto un esame per vedere se hai cisti?")))

    @Rule(Fact(esame_fatto=True))
    def ask_positivo(self):
        self.declare(Fact(esame=ask_question("L'esito dell'esame è positivo?")))

    # RIGONFIAMENTO
    @Rule(Fact(esame_fatto=False))
    def ask_rigonfiamento(self):
        self.declare(Fact(rigonfiamento=ask_question("Noti dei rigonfiamenti nella zona addominale?")))

    # ACIDITA' DI STOMACO
    @Rule(OR(Fact(esame=False), Fact(rigonfiamento=False), Fact(vomito=False)))
    def ask_acidita(self):
        self.declare(Fact(acidita=ask_question("Stai soffrendo di acidità di stomaco?")))

    # DOLORE ADDOMINALE
    @Rule(OR(Fact(rigonfiamento=True), Fact(acidita=True)))
    def ask_doloreaddominale(self):
        self.declare(Fact(dolore_addominale=ask_question("Avverti dolore nella zona addominale?")))

    # CISTI
    @Rule(OR(AND(Fact(dolore_addominale=True), Fact(rigonfiamento=True)), Fact(esame=True)))
    def cisti(self):
        self.declare(Fact(cisti=True))

    # ULCERA
    @Rule(OR(AND(Fact(dolore_addominale=True), Fact(acidita=True), Fact(nausea=True))))
    def ulcera(self):
        self.declare(Fact(ulcera=True))

    # MALATTIA LIEVE
    @Rule(AND(Fact(sintomi_base=True), Fact(vomito=True), Fact(cisti=True)))
    def malattia_lieve(self):
        print("I sintomi indicano che potresti aver contratto il virus.")
        print("È consigliabile recarsi da un medico da un medico per ulteriori accertamenti.")
        self.reset()

    # MALATTIA GRAVE
    @Rule(AND(Fact(sintomi_base=True), Fact(ulcera=True)))
    def malattia_grave(self):
        print("I sintomi indicano che potresti essere in uno stadio avanzato della malattia causata dal virus.")
        print("È consiglibile recarsi un una struttura ospedaliera il prima possibile.")
        self.reset()

    # ASSENZA DI MALATTIA
    @Rule(OR(Fact(sintomi_base=False), Fact(nausea=False), Fact(dolore_addominale=False),
          AND(Fact(rigonfiamento=False), Fact(acidita=False)),
          AND(Fact(acidita=False), Fact(vomito=False)),
          AND(Fact(acidita=False), Fact(dolore_addominale=True))))
    def malattia_assente(self):
        print("Con i sintomi indicati non dovresti aver contratto il virus.")
        self.reset()
