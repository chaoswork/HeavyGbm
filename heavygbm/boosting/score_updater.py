#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ScoreUpdater(object):

    """Docstring for ScoreUpdater. """

    def __init__(self, train_data):
        """TODO: to be defined1. """
        self.data_ = train_data
        self.num_data_ = self.data_.num_data()
        self.score_ = [0.0] * self.num_data_
        init_score = self.data_.meta_data().init_score()
        if init_score:
            for i in range(self.num_data_):
                self.score_[i] = init_score[i]

    def score(self):
        return self.score_

    def add_score(self, tree_learner):
        tree_learner.add_prediction_to_score(self.score_)

