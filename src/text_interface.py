def ask_question(question: str) -> bool:
    answer = input(question + " (y/n): ")
    while not is_answer(answer):
        answer = input(question + " (y/n): ")

    answer = answer.lower()
    return answer == "y"


def is_answer(answer: str) -> bool:
    answer = answer.lower()
    return answer == "y" or answer == "n"