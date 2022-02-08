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
        yield Fact(question = 1)

    @Rule(Fact(question = 1))
    def ask_nausea(self):
        if askquestion("Hai la nausea?"): self.declare(Fact(nausea = True))
        self.declare(Fact(question = 2))
