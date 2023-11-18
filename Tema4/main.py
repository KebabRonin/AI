"""
The examined group comprised kernels belonging to three different varieties of wheat: Kama, Rosa and Canadian, 70 elements each, randomly selected for the experiment. High quality visualization of the internal kernel structure was detected using a soft X-ray technique. It is non-destructive and considerably cheaper than other more sophisticated imaging techniques like scanning microscopy or laser technology. The images were recorded on 13x18 cm X-ray KODAK plates. Studies were conducted using combine harvested wheat grain originating from experimental fields, explored at the Institute of Agrophysics of the Polish Academy of Sciences in Lublin.

To construct the data, seven geometric parameters of wheat kernels were measured:
1. area A,
2. perimeter P,
3. compactness C = 4*pi*A/P^2,
4. length of kernel,
5. width of kernel,
6. asymmetry coefficient
7. length of kernel groove.
All of these parameters were real-valued continuous.
"""

import random, math, numpy as np, matplotlib.pyplot as mpl

def import_data():
	data = []
	with open("seeds_dataset.txt", "r") as fd:
		for line in fd:
			attrs = line.split()
			sample = np.array([float(attr) for attr in attrs[:-1]])
			expected_label = np.array([int(t==(int(attrs[-1])-1)) for t in range(3)])
			data.append((sample, expected_label))
	return data


def split_dataset(dataset: list[tuple], p_train: float):
	train_len = int(p_train*len(dataset))
	return dataset[:train_len], dataset[train_len:]


class Layer:
	def __init__(self, inputs: int, neurons: int, activation, derivata):
		self.inputs = inputs
		self.neurons = neurons

		self.weights = np.random.rand(inputs, neurons)
		self.biases  = np.random.rand(neurons)
		self.activation = activation
		self.derivata   = derivata

	def __repr__(self):
		return str({
			'inputs': self.inputs,
			'neurons': self.neurons,
			'biases': self.biases,
			'weights': self.weights,
		})

	def forward_step(self, input, expected_label=None):
		prediction = np.dot(input, self.weights) + self.biases
		self.last_results = np.copy(prediction)
		# if expected_label:
		# 	# Calculez eroarea
		# 	self.delta = expected_label - prediction
		return self.activation(prediction)

	def backward_step(self, expected_label):
		delta = self.last_results * self.derivata(expected_label)
		return delta


class NeuralNetwork:
	def __init__(self, layers: list[Layer], learning_rate, max_epochs):
		for l in range(1, len(layers)):
			if layers[l].inputs != layers[l-1].neurons:
				raise Exception("Layers do not connect properly")

		self.layers = layers
		self.learning_rate = learning_rate
		self.max_epochs = max_epochs

	def __repr__(self):
		return str({
			'learning_rate': self.learning_rate,
			'max_epochs': self.max_epochs,
			'layers': self.layers,
		})

	def predict(self, sample):
		inp = sample
		for l in self.layers:
			inp = l.forward_step(inp)
		return inp

	def train_batch(self, train_set):
		self.epoch_progress = []

		for epoch in range(self.max_epochs):
			print("Epoch:", epoch)
			loss = 0
			for sample, expected_label in train_set:
				label = self.predict(sample)
				loss += loss_MSE(label, expected_label)

			self.epoch_progress.append(loss)

			# Backpropagation
			# ...

		# Confusion Matrix in test
		# rows = nn_label, columns = expected


def interpret(arr):
	max = 0
	for id, val in enumerate(arr):
		if val > arr[max]:
			max = id
	return max + 1


def get_accuracy(nn, test_set):
	correct = 0
	n = len(test_set)

	for (sample, expected_label) in test_set:
		label = nn.predict(sample)
		# if (label == expected_label).all():
		if interpret(label) == interpret(expected_label):
			correct += 1

	print("Test accuracy:", correct/n)


def threshold_activation(array):
	for a in range(len(array)):
		array[a] = int(array[a] > 0)
	return array

def ReLU_activation(array):
	for a in range(len(array)):
		array[a] = array[a] if int(array[a] > 0) else 0
	return array
def ReLU_derivata(array):
	for a in range(len(array)):
		array[a] = 1 if array[a] > 0 else 0
	return array

def sigmoid_activation(array):
	for a in range(len(array)):
		array[a] = math.e**(array[a]) / (1 + math.e**(array[a]))
	return array
def sigmoid_derivata(array):
	for a in range(len(array)):
		sig = math.e**(array[a]) / (1 + math.e**(array[a]))
		array[a] = sig * (1 - sig)
	return array



def loss_MSE(label, expected_label):
	s = 0
	for l, el in zip(label, expected_label):
		s += (el - l)**2
	s /= 2
	return s

nn = NeuralNetwork(layers=[
	Layer(inputs=7, neurons=5, activation=ReLU_activation, derivata=ReLU_derivata),
	Layer(inputs=5, neurons=3, activation=sigmoid_activation, derivata=sigmoid_derivata),
], learning_rate=0.1, max_epochs=5)

# Import Data
dataset = import_data()
print("Done importing")
dataset.sort(key= lambda _: random.random())
train_set, test_set = split_dataset(dataset, p_train= 0.8)


# nn.train_batch(train_set)

# mpl.plot(list(range(nn.max_epochs)), nn.epoch_progress)
# mpl.xticks(range(nn.max_epochs))
# mpl.show()

print(nn)
get_accuracy(nn, test_set)

print("Prediction for ", test_set[0][0])
print(f"(Expected {test_set[0][1]})")
print(nn.predict(test_set[0][0])) # prima instanta, doar input-ul

for id, l in enumerate(nn.layers):
	print("Layer", id, l.last_results)