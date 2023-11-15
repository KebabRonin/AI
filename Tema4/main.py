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

import random, math, numpy as np, matplotlib as mpl

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
		self.derviata   = derivata

	def __repr__(self):
		return str({
			'inputs': self.inputs,
			'neurons': self.neurons,
			'biases': self.biases,
			'weights': self.weights,
		})

	def forward_step(self, input, expected_label=None):
		prediction = self.activation(np.dot(input, self.weights) + self.biases)
		self.last_results = np.copy(prediction)
		# if expected_label:
		# 	# Calculez eroarea
		# 	self.delta = expected_label - prediction
		return prediction

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

	def train_online(self, train_set):
		for epoch in range(self.max_epochs):
			print("Epoch:", epoch)
			for sample, expected_label in train_set:

				# TODO Va trebui sa retin weight-urile intermediare probabil
				# inp = sample
				# for l in self.layers:
				# 	inp = l.forward_step(inp)
				# label = inp

				label = self.predict(sample)

				if (label != expected_label).any():
					# TODO Do this properly
					# print(self.layers[-1])
					error = np.array([(b - a) for a, b in zip(label, expected_label)])
					self.layers[-1].weights += self.learning_rate * np.atleast_2d(sample).T * error
					self.layers[-1].biases  += self.learning_rate * error
					for layer in self.layers[:-1]:
						layer.backward_step(expected_label)
					# print(self.layers[-1])
					# print(label, self.interpret(expected_label), error)


	def test(self, test_set):
		correct = 0
		n = len(test_set)

		for (sample, expected_label) in test_set:
			label = self.predict(sample)
			if (label == expected_label).all():
				correct += 1

		print("Test accuracy:", correct/n)

	def predict(self, sample):
		inp = sample
		for l in self.layers:
			inp = l.forward_step(inp)
		return inp


def linear_activation(array):
	for a in range(len(array)):
		array[a] = int(array[a] > 0)
	return array
def ReLU_activation(array):
	for a in range(len(array)):
		array[a] = array[a] if int(array[a] > 0) else 0
	return array


def loss_MSE(label, expected_label):
	s = 0
	for l, el in zip(label, expected_label):
		s += (el - l)**2
	s /= 2
	return s
# def loss_CrossEntropy(label, expected_label):
# 	# s = 0
# 	# for l, el in zip(label, expected_label):
# 	# 	s += l * math.log(1e-15 + el)
# 	return  

nn = NeuralNetwork(layers=[
	Layer(inputs=7, neurons=5, activation=ReLU_activation, derivata=lambda x: 1 if x > 0 else 0),
	Layer(inputs=5, neurons=3, activation=linear_activation, derivata=lambda _: 1),
], learning_rate=0.1, max_epochs=5)

# Import Data
dataset = import_data()
print("Done importing")
dataset.sort(key= lambda _: random.random())
train_set, test_set = split_dataset(dataset, p_train= 0.5)


# nn.train_online(train_set)
# print(nn)
nn.test(test_set)
print(nn.predict(test_set[0][0])) # prima instanta, doar input-ul