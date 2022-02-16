import os.path

import pandas

from dataset import Dataset
from diagnostics_expert_system import runex
from diagnostics_bayes_network import runbn, testbn
from text_interface import ask_integer, user_menu, wait_user

global dataset

def expert_system():
    print("Benvenuto nel sistema diagnostico con modello a sistema esperto")
    runex()

def bayes_network():
    print("Benvenuto nel sistema diagnostico con modello a rete bayesiana")
    title = "Menù gestione modello di rete bayesiana"
    options = [
        "Diagnostica con rete bayesiana ideale",
        "Diagnostica con rete bayesiana ad appredimento parametrizzato (richiede database)",
        "Simulazione con rete bayesiana ad appredimento parametrizzato (richiede database, può richiedere molto tempo)",
        "Ritorna al menù principale"
    ]
    res = user_menu(title, options)
    title = "Seleziona il tipo di stimatore che si vuole utilizzare"
    options = [
        "Stimatore di massima verosomiglianza",
        "Stimatore di bayes"
    ]
    if res == 1:
        runbn(dataset, "normal")
    if res == 2:
        response = user_menu(title, options)
        if response == 1:
            runbn(dataset, "learn", "ml")
        if response == 2:
            runbn(dataset, "learn", "bayes")
    if res == 3:
        response = user_menu(title, options)
        if response == 1:
            testbn(dataset, "ml")
        if response == 2:
            testbn(dataset, "bayes")

def dataset_manager():
    title = "Menù gestione dataset"
    options = [
        "Genera dataset per il training",
        "Genera dataset per il test",
        "Genera dataset per training&test",
        "Salva i dataset in memoria",
        "Carica i dataset dalla memoria",
        "Ritorna al menù principale"
    ]
    res = user_menu(title, options)
    if res == 1:
        size = ask_integer("Inserisci la dimensione del dataset")
        dataset.generate_training(size)
    if res == 2:
        size = ask_integer("Inserisci la dimensione del dataset")
        dataset.generate_test(size)
    if res == 3:
        size = ask_integer("Inserisci la dimensione dei dataset")
        dataset.generate_dataset(size)
    if res == 4:
        dataset.save_to_files()
    if res == 5:
        dataset.load_from_files()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    title = "Modello da usare"
    options = [
        "Sistema esperto",
        "Rete Bayesiana",
        "Gestione dataset",
        "Esci"
    ]
    dataset = Dataset("data/train.csv", "data/test.csv")
    if os.path.exists("data/train.csv"):
        dataset.training = pandas.read_csv("data/train.csv")
        print("Caricato database di training da memoria")
    if os.path.exists("data/test.csv"):
        dataset.test = pandas.read_csv("data/test.csv")
        print("Caricato database di test da memoria")
    res = 0
    while res != 4:
        res = user_menu(title, options)
        if res == 1:
            expert_system()
            wait_user()
        if res == 2:
            bayes_network()
            wait_user()
        if res == 3:
            dataset_manager()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
