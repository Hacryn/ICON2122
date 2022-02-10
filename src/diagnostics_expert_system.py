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
        yield Fact(question=1)

    @DefFacts()
    def _initial_action(self):
        yield Fact(malattia=False)

    # SINTOMI DI BASE

    @Rule(Fact(question=1))
    def ask_pdp(self):
        if askquestion("Hai riscontrato perdita di peso?"):
            self.declare(Fact(pdp=True))
            self.declare(Fact(question=2))
        else:
            self.declare(Fact(pdp=False))
            self.declare(Fact(question=2))

    @Rule(Fact(question=2))
    def ask_diarrea(self):
        if askquestion("Hai la diarrea?"):
            self.declare(Fact(diarrea=True))
            self.declare(Fact(question=3))
        else:
            self.declare(Fact(diarrea=False))

    # NAUSEA
    @Rule(Fact(question=3))
    def ask_nausea(self):
        if askquestion("Hai la nausea?"):
            self.declare(Fact(nausea=True))
            self.declare(Fact(question=4))
        else:
            self.declare(Fact(nausea=False))
            self.declare(Fact(question=9))

    # VOMITO
    @Rule(Fact(question=4))
    def ask_vomito(self):
        if askquestion("Hai il vomito?"):
            self.declare(Fact(vomito=True))
            self.declare(Fact(question=5))
        else:
            self.declare(Fact(vomito=False))
            self.declare(Fact(question=1))

    # SINTOMI
    @Rule(AND(Fact(question=4), Fact(vomito=True)))
    def ask_esame(self):
        if askquestion("Hai svolto un esame per vedere se hai una ciste?"):
            self.declare(Fact(esame=True))
            self.declare(Fact(question=6))
        else:
            self.declare(Fact(esame=False))
            self.declare(Fact(question=7))

    @Rule(Fact(question=6))
    def ask_positivo(self):
        if askquestion("L'esito dell'esame è positivo?"):
            self.declare(Fact(positivo=True))
        else:
            self.declare(Fact(positivo=False))

    @Rule(Fact(question=7))
    def ask_doloreaddominale(self):
        if askquestion("Hai dolore addominale?"):
            self.declare(Fact(doloreAddominale=True))
            self.declare(Fact(question=8))

    @Rule(Fact(question=8))
    def ask_rigonfiamento(self):
        if askquestion("Hai un rigonfiamento?"):
            self.declare(Fact(rigonfiamento=True))
        else:
            self.declare(Fact(question=9))

    @Rule(Fact(question=9))
    def ask_acidita(self):
        if askquestion("Hai acidità di stomaco?"):
            self.declare(Fact(acidita=True))
        else:
            self.declare(Fact(acidita=False))

    # SINTOMI DI BASE
    @Rule(OR(Fact(pds=True), Fact(diarrea=True)))
    def sintomi_base(self):
        self.declare(Fact(sintomi_base=True))

    # CISTI
    @Rule(OR(AND(Fact(doloreAddominale=True), Fact(rigonfiamento=True), Fact(esame=False))),
          AND(Fact(esame=True), Fact(positivo=True)))
    def cisti(self):
        self.declare(Fact(cisti=True))

    # ULCERA
    @Rule(AND(Fact(doloreAddominale=True), Fact(aciditàDiStomaco=True), Fact(nausea=True)))
    def ulcera(self):
        self.declare(Fact(ulcera=True))

    # MALATTIA LIEVE
    @Rule(AND(Fact(sintomi_base=True), Fact(vomito=True), Fact(cisti=True)))
    def malattia_lieve(self):
        print("I sintomi indicano che potresti essere malato. Ti consigliamo di recarti da un medico.")

    # MALATTIA GRAVE
    @Rule(AND(Fact(sintomi_base=True), Fact(ulcera=True)))
    def malattia_grave(self):
        print("I sintomi indicano che potresti essere in uno stadio avanzato della malattia. Recati in ospedale.")

    # ASSENZA DI MALATTIA
    @Rule(Fact(sintomi_base=False))
    def malattia_assente(self):
        print("Con i sintomi indicati non dovresti essere malato.")
