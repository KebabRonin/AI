import math, numpy as np


def vectorize(f):
	def v(array):
		for a in range(len(array)):
			array[a] = f(array[a])
		return array
	return v


def threshold(a):
	return int(a > 0)


def ReLU(a):
	return a if int(a > 0) else 0
def ReLU_d(a):
	return 1 if a > 0 else 0
ReLU_activation = vectorize(ReLU)
ReLU_derivata   = vectorize(ReLU_d)

def sigmoid(a):
	return 1 / (1 + math.e**(-a))
def sigmoid_d(a):
	sig = sigmoid(a)
	return sig * (1 - sig)
sigmoid_activation = vectorize(sigmoid)
sigmoid_derivata   = vectorize(sigmoid_d)

def tanh(a):
	return (1 - math.e**(-2*a)) / (1 + math.e**(-2*a))
def tanh_d(a):
	t = tanh(a)
	return 1 - t**2
tanh_activation = vectorize(tanh)
tanh_derivata   = vectorize(tanh_d)