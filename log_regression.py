
from collections import namedtuple

import random
import math
from math import sqrt, atan, pi
from matplotlib import pyplot as plt

N_SETS = 4
Point = namedtuple("Point", ["x", "y", "ans"])


def read_input():
    with open("chips.txt") as handle:
        results = []
        for line in handle:
            x, y, ans = (float(i) for i in line.split())
            r = sqrt(x ** 2 + y ** 2)
            if x > 0:
                phi = atan(y/x)
            elif x < 0:
                phi = atan(y/x) + pi
            elif y > 0:
                phi = pi / 2
            else:
                phi = 3 * pi / 2
            results.append(Point(r, phi, 1 if int(ans) == 1 else -1))
        random.shuffle(results)
        return results


def f(x, y, k=None):
    assert k, "k not valid"
    return k[0] + x * k[1] + y * k[2]


def get_koeficients(lrn_fs):
    k = [0, 0, 0]
    n_iter = 1000
    al = 1. / len(lrn_fs) * 0.3
    new = [0, 0, 0]
    for _ in range(n_iter):
        new[0] -= sum(f(p.x, p.y, k) - p.ans for p in lrn_fs) * al
        new[1] -= sum((f(p.x, p.y, k) - p.ans) * p.x for p in lrn_fs) * al
        new[2] -= sum((f(p.x, p.y, k) - p.ans) * p.y for p in lrn_fs) * al
        k = new.copy()
    return k


def get_learning_and_testing_sets(all_set, id_set):
    _testing_set = []
    _learning_set = []
    for i in range(len(all_set)):
        if i % N_SETS == id_set:
            _testing_set.append(all_set[i])
        else:
            _learning_set.append(all_set[i])
    return _learning_set, _testing_set


def log_func(z):
    return 1. / (1 + math.e ** (-z))


def eval_answer(_test_chip, _k):
    z = f(_test_chip.x, _test_chip.y, _k)
    if log_func(z) < 0.46:
        return -1
    else:
        return 1

pt = 0
nt = 0
pf = 0
nf = 0

chips = read_input()
for id_testing_set in range(N_SETS):
    sum_abs = 0
    learning_set, testing_set = \
        get_learning_and_testing_sets(chips, id_testing_set)
    k = get_koeficients(learning_set)
    for test_chip in testing_set:
        eval_ans = eval_answer(test_chip, k)
        if eval_ans == test_chip.ans and eval_ans == 1:
            pt += 1
        elif eval_ans == test_chip.ans and eval_ans == -1:
            nt += 1
        elif eval_ans != test_chip.ans and test_chip.ans == -1:
            pf += 1
        elif eval_ans != test_chip.ans and test_chip.ans == 1:
            nf += 1

print("pt = {} "
      "nt = {} "
      "pf = {} "
      "nf = {} ".format(pt, nt, pf, nf))

precision = pt / (pt + pf)
recall = pt / (pt + nf)
accuracy = (pt + nt) / (pt + nt + pf + nf)
f1_measure = 2 * precision * recall / (precision + recall)

print("precision = {}".format(precision))
print("recall = {} ".format(recall))
print("accuracy = {}".format(accuracy))
print("f1-measure = {}".format(f1_measure))

# x0 = [i.x for i in chips if i.ans == -1]
# y0 = [i.y for i in chips if i.ans == -1]
# x1 = [i.x for i in chips if i.ans == 1]
# y1 = [i.y for i in chips if i.ans == 1]
# plt.plot(x0, y0, 'bo', x1, y1, 'ro')
# plt.show()
