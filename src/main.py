from diagnostics_expert_system import runex
from diagnostics_bayes_network import runbn
from dataset_gen import gen_data, load_dataset

path = "data/dataset.csv"

def expert_system():
    runex()

def bayes_network():
    runbn()

def dataset_gen():
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
    bayes_network()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
