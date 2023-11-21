import data_ops as data, activations as act, nn

import random, matplotlib.pyplot as mpl

my_nn = nn.NeuralNetwork(layers=[
	nn.Layer(inputs=7, neurons=7, activation=act.ReLU_activation, derivata=act.ReLU_derivata),
	nn.Layer(inputs=7, neurons=3, activation=act.sigmoid_activation, derivata=act.sigmoid_derivata),
], learning_rate=0.1, max_epochs=20)

# Import Data
dataset = data.import_data()
print("Done importing")
dataset.sort(key= lambda _: random.random())
train_set, test_set = data.split_dataset(dataset, p_train= 0.8)


my_nn.train_batch(train_set)

mpl.plot(list(range(my_nn.max_epochs)), my_nn.epoch_progress)
mpl.xticks(range(my_nn.max_epochs))
mpl.show()

print(my_nn)
data.get_stats(my_nn, test_set)

print("Prediction for ", test_set[0][0])
print(f"(Expected {test_set[0][1]})")
print(my_nn.forward(test_set[0][0])) # prima instanta, doar input-ul

for id, l in enumerate(my_nn.layers):
	print("Layer", id, l.last_results)

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