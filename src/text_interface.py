def ask_question(question: str) -> bool:
    answer = input(question + " (y/n): ")
    while not is_answer(answer):
        answer = input(question + " (y/n): ")

    answer = answer.lower()
    return answer == "y"


def is_answer(answer: str) -> bool:
    answer = answer.lower()
    return answer == "y" or answer == "n"

def user_menu(title: str, options: list[str]) -> int:
    response = 0
    while response == 0:
        print(title + ":")
        i = 1
        for option in options:
            print(str(i) + ") " + option)
            i = i + 1
        response = int(input("Seleziona il numero della scelta: "))
        if (response < 1) or (response > len(options)): response = 0

    return response

def wait_user(): input("Premi un pulsante qualsiasi per continuare...")