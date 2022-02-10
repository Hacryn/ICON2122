from diagnostics_expert_system import runex
from diagnostics_bayes_network import runbn
from dataset_gen import gendata, load_dataset

def expert_system():
    runex()

def bayes_network():
    runbn()

def dataset_gen():
    dataset = load_dataset("data/dataset.csv")
    print(dataset["Malattia"].value_counts())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bayes_network()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
