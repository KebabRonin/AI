import copy
import matplotlib.pyplot as plt
import numpy as np
import random


# folosim 75% dintre date pentru antrenare si 25% pentru test
# 210 date => 157 de antrenare, 53 de testare
def import_data():
    data = []
    database = open("seeds_dataset.txt", "r")
    for line in database:
        data.append([float(x) for x in (line.split())])
    random.shuffle(data)

    original_data = data
    normalized_data = copy.deepcopy(original_data)

    normalize_data(normalized_data)
    return normalized_data[:len(normalized_data) * 3 // 4], normalized_data[len(normalized_data) * 3 // 4:], original_data[:len(original_data) * 3 // 4], original_data[len(original_data) * 3 // 4:]


# folosim functia de activare sigmoid pentru stratul ascuns
# folosim functia de activare softmax pentru stratul de iesire
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_derivative(z):
    return sigmoid(z) * (1 - sigmoid(z))


def softmax(v_z):
    z_sum = np.sum(np.exp(v_z))
    return np.exp(v_z) / z_sum


def softmax_derivative(v_z):
    return softmax(v_z) * (1 - softmax(v_z))


def cost(output, target):
    v_target = [1 if x == target else 0 for x in range(1, 4)]
    return sum([(t - o) ** 2 / 2 for t, o in zip(v_target, output)])


def cost_derivative(output, target):
    v_target = [1 if x == target else 0 for x in range(1, 4)]
    return np.array([(o - t) for t, o in zip(v_target, output)])


def normalize_data(data):
    data_min = []
    data_max = []
    for index in range(0, 7):
        data_min.append(data[0][index])
        data_max.append(data[0][index])
        for d in data[1:]:
            data_min[index] = min(data_min[index], d[index])
            data_max[index] = max(data_max[index], d[index])

    for d_index, _ in enumerate(data):
        data[d_index][0:7] = [(x - data_min[index]) / (data_max[index] - data_min[index]) for index, x in enumerate(data[d_index][:-1])]


# o sa avem 4 straturi: intrare, 2 * ascuns si iesire
# stratul 1 are 7 neuroni -> 35 weighturi, 0 biasuri
# stratul 2 are 5 neuroni -> 25 weighturi, 5 bisauri
# stratul 3 are 5 neuroni -> 15 weighturi, 5 bisauri
# stratul 4 are 3 neuroni -> 0 weighturi, 3 biasuri
# => 75 weighturi, 13 biasuri = 88 de parametri
class Network:
    def __init__(self, layer_sizes):
        self.layer_count = len(layer_sizes)
        self.layer_sizes = layer_sizes
        self.biases = [np.random.randn(y, 1) for y in layer_sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(layer_sizes[:-1], layer_sizes[1:])]
        self.learning_rate = 0.02

    def feedforward(self, net):
        for weights, biases in zip(self.weights[:-1], self.biases[:-1]):
            net = sigmoid(np.dot(weights, net) + biases)
        net = softmax(np.dot(self.weights[-1], net) + self.biases[-1])
        return net

    def update_parameters(self, input_data):
        delta_biases = [np.zeros(bias.shape) for bias in self.biases]
        delta_weights = [np.zeros(weight.shape) for weight in self.weights]

        for data in input_data:
            input = np.array(data[:-1]).reshape(-1, 1)
            output = data[-1]

            new_delta_biases, new_delta_weights = self.backpropagate(input, output)

            delta_biases = [db + ndb for db, ndb in zip(delta_biases, new_delta_biases)]
            delta_weights = [dw + ndw for dw, ndw in zip(delta_weights, new_delta_weights)]

        self.biases = [bias - self.learning_rate * db for bias, db in zip(self.biases, delta_biases)]
        self.weights = [weight - self.learning_rate * dw for weight, dw in zip(self.weights, delta_weights)]
        pass

    def backpropagate(self, input, target):
        delta_biases = [np.zeros(bias.shape) for bias in self.biases]
        delta_weights = [np.zeros(weight.shape) for weight in self.weights]

        current_activation = input
        activations = [current_activation]

        z_values = []

        # Feedforward
        for weights, biases in zip(self.weights[:-1], self.biases[:-1]):
            current_z = np.dot(weights, current_activation) + biases
            z_values.append(current_z)
            current_activation = sigmoid(current_z)
            activations.append(current_activation)


        # Output Layer
        current_z = np.dot(self.weights[-1], current_activation) + self.biases[-1]
        z_values.append(current_z)
        current_activation = softmax(current_z)
        activations.append(current_activation)

        # Backprop

        # Output Layer
        current_delta = cost_derivative(activations[-1], target) * softmax_derivative(z_values[-1])
        delta_biases[-1] = current_delta
        delta_weights[-1] = np.dot(current_delta, activations[-2].transpose())

        # Rest of Layers
        for layer in range(2, self.layer_count):
            current_z = z_values[-layer]
            z_derivative = sigmoid_derivative(current_z)

            current_delta = np.dot(self.weights[-layer + 1].transpose(), current_delta) * z_derivative

            delta_biases[-layer] = current_delta
            delta_weights[-layer] = np.dot(current_delta, activations[-layer - 1].transpose())

        return delta_biases, delta_weights

    def gradient_descent(self, epoch_count):
        correct_x = []
        correct_y = []
        wrong_x = []
        wrong_y = []
        x = []
        y = []
        training_data, test_data, original_training_data, original_test_data = import_data()
        for epoch_index in range(1, epoch_count + 1):
            self.update_parameters(training_data)

            correctly_classified = 0
            total = 0
            index = 0
            for data in test_data:
                input = np.array(data[:-1]).reshape(-1, 1)
                output = data[-1]

                result = np.argmax(self.feedforward(input))

                if result == output - 1:
                    correctly_classified += 1
                    if epoch_index == epoch_count:
                        correct_x.append(original_test_data[index][0])
                        correct_y.append(original_test_data[index][1])
                else:
                    if epoch_index == epoch_count:
                        wrong_x.append(original_test_data[index][0])
                        wrong_y.append(original_test_data[index][1])

                total += 1
                index += 1

            if epoch_index % 2 == 0:
                x.append(epoch_index)
                y.append(correctly_classified / total)
            if epoch_index % 50 == 0:
                print(f"Epoch {epoch_index} finished")
                print(f"Correctly classified examples: {correctly_classified}/{total}, {correctly_classified/total}")

        print_first_graphic(correct_x, correct_y, wrong_x, wrong_y)
        print_second_graphic(x, y)

def print_first_graphic(correct_x, correct_y, wrong_x, wrong_y):
    plt.scatter(correct_x, correct_y, color='blue', label='Correctly Classified')
    plt.scatter(wrong_x, wrong_y, color='red', label='Incorrectly Classified')

    plt.xlabel('First attribute')
    plt.ylabel('Second attribute')
    plt.title('Neural Network Classification Results')

    plt.legend()
    plt.show()

def print_second_graphic(x, y):
    plt.plot(x, y)
    plt.xlabel('Number of Epochs')
    plt.ylabel('Accuracy on test data')
    plt.title('Neural Network Classification Results')

    plt.show()




network = Network([7, 5, 5, 3])
network.gradient_descent(1000)

