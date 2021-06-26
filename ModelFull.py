# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:32:03 2021

@author: kohai
"""

from numpy import loadtxt
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
def createModel():
    # load the dataset
    dataset = loadtxt('FullSnake.csv', delimiter=',')
    # split into input (X) and output (y) variables
    X = dataset[:,0:9]
    y = dataset[:,9:13]
    # define the keras model
    model = Sequential()
    model.add(Dense(10, input_dim=9, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(4, activation='sigmoid'))
    # compile the keras model
    opt = SGD(lr=0.01, momentum=0.9)
    model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
    # fit the keras model on the dataset
    model.fit(X, y, epochs=150, batch_size=10, verbose=0)
    # evaluate the keras model
    _, accuracy = model.evaluate(X, y, verbose=0)
    print('Accuracy: %.2f' % (accuracy*100))
    return model
createModel()