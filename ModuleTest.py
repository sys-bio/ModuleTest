
import tellurium as te
import numpy as np


def create_test(target, name, test_reactions='all'):
    # todo: This is crude and should be revised to remove as much extraneous
    #  information as possible from the truncated model.
    # todo: test_reactions can be improved. Currently relies on rxn names.

    test_file = ''
    is_list = isinstance(test_reactions, list)
    with open(target, 'r') as tf:
        lines = tf.readlines()

        if is_list:
            for line in lines:
                if '->' in line or '=>' in line:
                    if line.split(':')[0] in test_reactions:
                        test_file += line
                    else:
                        test_file += '// '
                        test_file += line
                else:
                    test_file += line
        else:
            for line in lines:
                test_file += line

    with open(name, 'w') as test:
        test.write(test_file)


class Compare:
    # can be used to compare any model
    def __init__(self, model, test, species=None, tol=1e-03, time_points=None):
        self.model = model
        self.test = test
        self.species = species
        self.tol = tol
        self.rxns = []
        self.submodel = ''
        self.sim1 = None
        self.sim2 = None
        self.np_sim1 = None
        self.np_sim2 = None
        self.diff = None
        self.abs_diff = None
        if not time_points:
            self.tp = [0, 10, 11]
        else:
            self.tp = time_points

        with open(self.test, 'r') as tf:
            lines = tf.readlines()
            for line in lines:
                if ('->' in line or '=>' in line or ':=' in line) and line[:2] != '//':
                    self.rxns.append(line.split(':')[0])

        with open(self.model, 'r') as tf:
            lines = tf.readlines()

            for line in lines:
                if '->' in line or '=>' in line or ':=' in line:
                    if line.split(':')[0] in self.rxns:
                        self.submodel += line
                    else:
                        self.submodel += '// '
                        self.submodel += line
                else:
                    self.submodel += line

    def compare_trace(self):

        r1 = te.loada(self.test)
        r2 = te.loada(self.submodel)

        if not self.species:
            self.species = r1.getFloatingSpeciesIds()

        self.sim1 = r1.simulate(self.tp[0], self.tp[1], self.tp[2], self.species)
        self.sim2 = r2.simulate(self.tp[0], self.tp[1], self.tp[2], self.species)

        # self.np_sim1 = np.array(self.sim1)
        # self.np_sim2 = np.array(self.sim2)

        # self.diff = self.np_sim1 - self.np_sim2
        self.diff = self.sim1 - self.sim2
        self.abs_diff = np.abs(self.diff)

