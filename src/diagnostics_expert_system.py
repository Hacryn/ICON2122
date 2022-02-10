from experta import *


def runex():
    engine = DiagnosticsES()
    engine.reset()
    engine.run()


def askquestion(question: str) -> bool:
    answer = input(question + " (y/n): ")
    while not isanswer(answer):
        answer = input(question + " (y/n): ")

    answer = answer.lower()
    return answer == "y"


def isanswer(answer: str) -> bool:
    answer = answer.lower()
    return answer == "y" or answer == "n"


class DiagnosticsES(KnowledgeEngine):

    @DefFacts()
    def _initial_action(self):
        yield Fact(question=True)
        yield Fact(malattia=False)

    # SINTOMI DI BASE

    @Rule(Fact(question=True))
    def ask_pdp(self):
        self.declare(Fact(pdp=askquestion("Hai riscontrato perdita di peso?")))


    @Rule(Fact(question=True))
    def ask_diarrea(self):
        self.declare(Fact(diarrea=askquestion("Hai la diarrea?")))

    # NAUSEA
    @Rule(Fact(sintomi_base=True))
    def ask_nausea(self):
        self.declare(Fact(nausea=askquestion("Hai la nausea?")))

    # VOMITO
    @Rule(Fact(nausea=True))
    def ask_vomito(self):
        self.declare(Fact(vomito=askquestion("Hai il vomito?")))

    # DOLORE ADDOMINALE
    @Rule(Fact(nausea=True))
    def ask_doloreaddominale(self):
        self.declare(Fact(doloreAddominale=askquestion("Hai dolore addominale?")))

    # ESAME
    @Rule(Fact(vomito=True))
    def ask_esame(self):
        self.declare(Fact(esame_fatto=askquestion("Hai svolto un esame per vedere se hai una ciste?")))

    @Rule(Fact(esame_fatto=True))
    def ask_positivo(self):
        self.declare(Fact(esame=askquestion("L'esito dell'esame è positivo?")))

    # RIGONFIAMENTO
    @Rule(Fact(doloreAddominale=True))
    def ask_rigonfiamento(self):
        self.declare(Fact(rigonfiamento=askquestion("Hai un rigonfiamento?")))

    # ACIDITA' DI STOMACO
    @Rule(Fact(doloreAddominale=True))
    def ask_acidita(self):
        self.declare(Fact(acidita=askquestion("Hai acidità di stomaco?")))

    # SINTOMI DI BASE
    @Rule(OR(Fact(pdp=True), Fact(diarrea=True)))
    def sintomi_base(self):
        self.declare(Fact(sintomi_base=True))

    @Rule(AND(Fact(pdp=False), Fact(diarrea=False)))
    def no_sintomi_base(self):
        self.declare(Fact(sintomi_base=False))

    # CISTI
    @Rule(OR(AND(Fact(doloreAddominale=True), Fact(rigonfiamento=True)), Fact(esame=True)))
    def cisti(self):
        self.declare(Fact(cisti=True))

    # ULCERA
    @Rule(AND(Fact(doloreAddominale=True), Fact(acidita=True), Fact(nausea=True)))
    def ulcera(self):
        self.declare(Fact(ulcera=True))

    # MALATTIA LIEVE
    @Rule(AND(Fact(sintomi_base=True), Fact(vomito=True), Fact(cisti=True)))
    def malattia_lieve(self):
        print("I sintomi indicano che potresti essere malato. Ti consigliamo di recarti da un medico.")
        self.reset()

    # MALATTIA GRAVE
    @Rule(AND(Fact(sintomi_base=True), Fact(ulcera=True)))
    def malattia_grave(self):
        print("I sintomi indicano che potresti essere in uno stadio avanzato della malattia. Recati in ospedale.")
        self.reset()

    # ASSENZA DI MALATTIA
    @Rule(OR(Fact(sintomi_base=False), Fact(nausea=False), Fact(doloreAddominale=False),
          AND(Fact(rigonfiamento=False),Fact(acidita=False))))
    def malattia_assente(self):
        print("Con i sintomi indicati non dovresti essere malato.")
        self.reset()
