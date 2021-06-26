# -*- coding: utf-8 -*-
"""
Created on Tue May 25 12:58:09 2021

@author: kohai
"""

from numpy import loadtxt
from sklearn.tree import DecisionTreeClassifier
def ReturnTree():
    df = loadtxt('FullSnake.csv', delimiter=',')
    X = df[:,0:9]
    y = df[:,9:13]
    decision_tree = DecisionTreeClassifier()
    decision_tree = decision_tree.fit(X, y)
    score = decision_tree.score(X, y)
    print(score)
    return decision_tree
decision_tree = ReturnTree()
print(decision_tree.predict([[4, 1, 0, 1, 1, 0, 0, 0, 0]]))