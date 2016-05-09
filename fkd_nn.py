# coding:utf-8

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD

from input_data import load

import matplotlib.pyplot as plt

from keras.models import model_from_json

LOAD = False
TEST = True

def load_model():
	model = model_from_json(open('./model/my_model_architecture.json').read())
	model.load_weights('./model/my_model_weights.h5')
	sgd = SGD(lr=0.01, decay=0.0, momentum=0.9, nesterov=True)
	model.compile(loss='mse', optimizer=sgd)
	print('successfully loaded')

	return model

def nn_model():
	model = Sequential()
	model.add(Dense(100, input_dim=9216, init='uniform'))
	model.add(Activation('relu'))
	model.add(Dense(30, init='uniform'))
	model.add(Activation('linear'))

	sgd = SGD(lr=0.01, decay=0.0, momentum=0.9, nesterov=True)
	model.compile(loss='mse', optimizer=sgd)

	X, y = load()
	hist = model.fit(X, y, nb_epoch=10, verbose=1, validation_split=0.2)

	return model, hist

def plot_loss(hist):
	loss = hist.history['loss']
	val_loss = hist.history['val_loss']
	plt.plot(loss, linewidth=3, label="train")
	plt.plot(val_loss, linewidth=3, label="valid")
	plt.grid()
	plt.legend()
	plt.xlabel("epoch")
	plt.ylabel("loss")
	plt.ylim(1e-3, 1e-2)
	plt.yscale("log")
	plt.show()

def check_test(model):

	def plot_sample(x, y, axis):
	    img = x.reshape(96, 96)
	    axis.imshow(img, cmap='gray')
	    axis.scatter(y[0::2] * 48 + 48, y[1::2] * 48 + 48, marker='x', s=10)

	X, _ = load(test=True)
	y_pred = model.predict(X)

	fig = plt.figure(figsize=(6, 6))
	fig.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0.05, wspace=0.05)

	for i in range(16):
	    ax = fig.add_subplot(4, 4, i + 1, xticks=[], yticks=[])
	    plot_sample(X[i], y_pred[i], ax)

	plt.show()

def save_model(model):
	json_string = model.to_json()
	open('./model/my_model_architecture.json', 'w').write(json_string)
	model.save_weights('./model/my_model_weights.h5')
	print('successfully saved')

def main():
	if LOAD:
		model = load_model()
	else:
		model, hist = nn_model()
		plot_loss(hist)

	if TEST:
		check_test(model)

	if not LOAD:
		save_model(model)

if __name__ == '__main__':
	main()