import matplotlib.pyplot as plt
import pickle, gzip, numpy as np
import copy


class Layer:
    def __init__(self, weights, biases, activation):
        self.weights = weights
        self.biases = biases
        self.activation = activation

    def __str__(self):
        return "{}".format({'Weights': self.weights, 'Biases': self.biases})


def import_data():
    with gzip.open("mnist.pkl.gz", "rb") as fd:
        train_set, valid_set, test_set = pickle.load(fd, encoding="latin")
    return (train_set, valid_set, test_set)


def predict(layer, data):
    raw = np.dot(data, layer.weights) + layer.biases
    act = layer.activation(raw)

    predicted = None

    for id, (a, r) in enumerate(zip(act, raw)):
        if a == 1:
            if not predicted:
                predicted = id
            elif r > raw[predicted]:
                predicted = id

    return predicted


def get_accuracy(layer, dataset):
    dataset_x, dataset_y = dataset
    n = len(dataset_y)
    correct = 0

    for sample, expected_label in zip(dataset_x, dataset_y):
        label = predict(layer, sample)
        if label == expected_label:
            correct += 1

    return correct/n


# Asta face toata munca practic
def learn_batch(layer, dataset, learning_rate):
    dataset_x, dataset_y = dataset

    d_bias = np.zeros_like(layer.biases)
    d_weights = np.zeros_like(layer.weights)

    for sample, expected_label in zip(dataset_x, dataset_y):
        raw = np.dot(sample, layer.weights)
        label = layer.activation(raw + layer.biases)

        expected_label = np.array([int(l == expected_label) for l in range(10)])

        error = np.array([(b - a) for a, b in zip(label, expected_label)])
        d_weights += learning_rate * np.atleast_2d(sample).T * error
        d_bias += learning_rate * error

    return d_weights, d_bias


# Se opreste dupa epochs epoci
# val_set e folosit doar pentru afisare
def train_minibatch_ep(layer, dataset, val_set, epochs, BATCHES = 10, learning_rate = 0.01):
    dataset_x, dataset_y = dataset
    batches = list(map(lambda x: \
                       (dataset_x[x[0]:x[max(1,len(x)-1)]],dataset_y[x[0]:x[max(1,len(x)-1)]]), \
                        np.array_split(np.arange(len(dataset_y) + 1), BATCHES)))

    for i in range(1,epochs+1):
        print(f"Epoch {i}...{get_accuracy(layer, val_set)}")
        for batch in batches:
            delta, beta = learn_batch(layer, batch, learning_rate)
            layer.weights += delta
            layer.biases += beta


# Se opreste dupa ce a gasit maximul si a asteptat patience epoci
# val_set e folosit doar pentru afisare
def train_minibatch_pat(layer, dataset, val_set, patience, BATCHES = 10, learning_rate = 0.01):
    dataset_x, dataset_y = dataset
    batches = list(map(lambda x: \
                       (dataset_x[x[0]:x[max(1,len(x)-1)]],dataset_y[x[0]:x[max(1,len(x)-1)]]), \
                        np.array_split(np.arange(len(dataset_y) + 1), BATCHES)))

    epoch = 1
    acc = get_accuracy(layer, val_set)
    max_e = [copy.copy(epoch), copy.copy(acc), copy.deepcopy(layer)]

    while epoch - max_e[0] < patience:
        print(f"Epoch {epoch}... {acc}")
        for batch in batches:
            delta, beta = learn_batch(layer, batch, learning_rate)
            layer.weights += delta
            layer.biases += beta
        epoch += 1
        acc = get_accuracy(layer, val_set)
        if acc > max_e[1]:
            max_e = [copy.copy(epoch), copy.copy(acc), copy.deepcopy(layer)]

    print(f"Choose epoch {max_e[0]}, with acc_val = {max_e[1]}")
    layer = max_e[2]


train_set, valid_set, test_set = import_data()


layer1_w = np.ones((784, 10))
layer1_b = np.ones((10,))
def layer1_act(results):
    return np.array(list(map(lambda x: int(x > 0), results)))


layer = Layer(layer1_w, layer1_b, layer1_act)
train_minibatch_ep(layer, train_set, valid_set, epochs= 10)
# train_minibatch_pat(layer, train_set, valid_set, patience= 5)
print(layer)
print(get_accuracy(layer, test_set))