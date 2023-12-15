import numpy as np, matplotlib.pyplot as mpl

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
	# lista de instante cu expected == x
	labels = [list(filter(lambda data: data[1][x] == 1, dataset)) for x in range(3)]
	train_set = []
	test_set = []
	for x in range(3):
		l = int(p_train*len(labels[x]))
		train_set += labels[x][:l]
		test_set += labels[x][l:]
	return train_set, test_set


def interpret(arr):
	max = 0
	for id, val in enumerate(arr):
		if val > arr[max]:
			max = id
	return max + 1


def get_stats(tested_nn, test_set):

	if 'epoch_progress' in dir(tested_nn):
		mpl.plot(list(range(tested_nn.max_epochs)), tested_nn.epoch_progress)
		mpl.xticks(range(tested_nn.max_epochs))

	correct = 0
	n = len(test_set)
	confusion_matrix = [[0.0 for i in range(3)] for i in range(3)]

	for (sample, expected_label) in test_set:
		label = tested_nn.forward(sample)
		confusion_matrix[interpret(label)-1][interpret(expected_label)-1] += 1 / len(test_set)
		if interpret(label) == interpret(expected_label):
			correct += 1

	print("Test accuracy:", correct/n)
	print("Confusion matrix:")
	for i in range(3):
		print(confusion_matrix[i])

	mpl.matshow(confusion_matrix)
	mpl.show()