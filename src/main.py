from diagnostics_expert_system import runex
from diagnostics_bayes_network import runbn, testrun
from dataset_gen import gen_data, load_dataset
from text_interface import ask_question, user_menu, wait_user

path = "data/dataset.csv"

def expert_system():
    runex()

def bayes_network():
    if ask_question("Vuoi usare l'apprendimento parametrizzato?"):
        if ask_question("Vuoi usare l'estimatore di massima verosomiglianza?"):
            runbn("learn", "ml", path)
        elif ask_question("Vuoi usare l'estimatore di bayes?"):
            runbn("learn", "bayes", path)
        else: print("Non esistono altri estiamatori disponibili nel programma, uscita dalla procedura...")
    else:
        print("Uso del modello preimpostato per la DAG e le probabilità condizionate dei nodi")
        runbn("normal")

def dataset():
    dataset = load_dataset(path)
    #dataset = gen_data(10000)
    #dataset.to_csv(path)
    print(dataset["Perdita di peso"].value_counts())
    print(dataset["Diarrea"].value_counts())
    print(dataset["Nausea"].value_counts())
    print(dataset["Vomito"].value_counts())
    print(dataset["Acidità di stomaco"].value_counts())
    print(dataset["Dolore addominale"].value_counts())
    print(dataset["Ciste"].value_counts())
    print(dataset["Ulcera"].value_counts())
    print(dataset["Malattia"].value_counts())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    title = "Modello da usare"
    options = [
        "Sistema esperto",
        "Rete Bayesiana",
        "Esci"
    ]
    res = 0
    while res != 3:
        res = user_menu(title, options)
        if res == 1:
            expert_system()
            wait_user()
        elif res == 2:
            bayes_network()
            wait_user()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
