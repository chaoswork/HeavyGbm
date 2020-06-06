#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse


from heavygbm.io import DataSet

class App(object):

    """
    Application
    """

    def __init__(self, argv):
        """
        init heavygbm
        """
        self.train_data_ = None
        self.config_ = self.load_parameters(argv)

    def load_parameters(self, argv):
        """TODO: Docstring for load_parameters.

        :argv: TODO
        :returns: TODO

        """
        parser = argparse.ArgumentParser(description='Parse command line')
        parser.add_argument('--config', dest='config_file', required=True,
                            action='store', help='config file')
        args = parser.parse_args(argv[1:])

        config = {}
        with open(args.config_file, 'r') as f:
            for line in f:
                segs = line.strip().split('=')
                if len(segs) != 2:
                    continue
                config[segs[0].strip()] = segs[1].strip()

        return config

    def load_data(self):
        # load train
        self.train_data_ = DataSet(self.config_['data'],
                                   max_bin=self.config_['max_bin'])
        self.train_data_.load_train_data()
        # load valid

    def init_train(self):
        # boosting = 
        # objective_fun_ = 
        self.load_data()
        # objective_fun_.init
        # boosting.init
        pass

    def train(self):
        # boosting.train
        pass



if __name__ == "__main__":
    import sys
    app = App(sys.argv)
    print(app.config_['task'])
    print(app.config_['num_leaves'])
    app.init_train()