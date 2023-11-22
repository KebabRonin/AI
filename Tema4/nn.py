import numpy as np

def loss_MSE(label, expected_label):
	s = 0
	for l, el in zip(label, expected_label):
		s += (el - l)**2
	s /= 2
	return s

def loss_MSE_grad(label, expected_label):
	k = len(label)
	grad = np.zeros(k)
	for id, (l, el) in enumerate(zip(label, expected_label)):
		grad[id] = (el - l)
	return grad

class Layer:
	def __init__(self, inputs: int, neurons: int, activation, derivata):
		self.inputs = inputs
		self.neurons = neurons

		self.weights = np.random.uniform(low=-0.1, high=0.1, size=(inputs, neurons))
		self.biases  = np.random.uniform(low=-0.05, high=0.05, size=(neurons,))

		self.reset_deltas()

		self.activation = activation
		self.derivata   = derivata

	def __repr__(self):
		return str({
			'inputs': self.inputs,
			'neurons': self.neurons,
			'biases': self.biases,
			'weights': self.weights,
		})

	def reset_deltas(self):
		self.delta_w = np.zeros_like(self.weights)
		self.delta_b = np.zeros_like(self.biases)

	def forward_step(self, input, expected_label=None):
		prediction = self.activation(np.dot(input, self.weights) + self.biases)
		self.last_results = np.copy(prediction)
		self.last_input = np.copy(input)
		return prediction


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
			'layers': self.layers,
			'learning_rate': self.learning_rate,
			'max_epochs': self.max_epochs,
		})

	def forward(self, sample):
		inp = sample
		for l in self.layers:
			inp = l.forward_step(inp)
		return inp


	def compute_delta(self, l_index: int):
		layer = self.layers[l_index]
		next_l = self.layers[l_index + 1]
		deriv_grad = layer.derivata(layer.last_results)
		layer.grad = np.multiply(next_l.grad, deriv_grad)
		layer.grad = np.dot(layer.grad, np.transpose(layer.weights))
		layer.d_w = np.atleast_2d(layer.last_input).T * layer.grad
		layer.d_b = layer.grad
		# print(layer.delta_b.shape, layer.d_b.shape, layer.d_w.shape, layer.grad.shape, layer.weights.shape, next_l.grad.shape)
		layer.delta_w += layer.d_w
		layer.delta_b += layer.d_b


	def backprop(self, expected_label):
		# Output Layer
		out_l = self.layers[-1]
		error_grad = loss_MSE_grad(out_l.last_results, expected_label)
		deriv_grad = out_l.derivata(out_l.last_results)
		out_l.grad = np.multiply(error_grad, deriv_grad)
		out_l.d_w = np.atleast_2d(out_l.last_input).T * out_l.grad
		out_l.d_b = out_l.grad
		out_l.grad = np.dot(out_l.grad, np.transpose(out_l.weights))
		out_l.delta_w += out_l.d_w
		out_l.delta_b += out_l.d_b

		# # Remaining Layers
		for l in reversed(range(len(self.layers) - 1)):
			self.compute_delta(l)

	def update_layers(self):
		# Update weights
		for l in self.layers:
			l.weights += self.learning_rate * l.delta_w
			l.biases  += self.learning_rate * l.delta_b

	def reset_deltas(self):
		for l in self.layers:
			l.reset_deltas()

	def train_batch(self, train_set):
		self.epoch_progress = []

		for epoch in range(self.max_epochs):
			if epoch%50 == 0:
				print("Epoch:", epoch)

			loss = 0

			self.reset_deltas()

			for sample, expected_label in train_set:
				label = self.forward(sample)
				self.backprop(expected_label)
				loss += loss_MSE(label, expected_label)

			self.update_layers()
			self.epoch_progress.append(loss)

		# Confusion Matrix in test
		# rows = nn_label, columns = expected