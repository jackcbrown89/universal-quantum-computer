import matplotlib.pyplot as plt
import numpy as np
from numpy import log


def graph_fails():
    data = np.load('results.npy')
    numbers_avg, fail_counts_avg = data[0], data[1]
    plt.errorbar(numbers_avg, fail_counts_avg, yerr=np.std(fail_counts_avg))
    plt.scatter(numbers_avg, fail_counts_avg)
    plt.xlabel('log N')
    plt.ylabel('Average Failures')
    plt.title('Average Failures vs log N')
    plt.show()


def graph_period():
    data = np.load('results_period.npy').T
    numbers, find_times = [x[0] for x in data if x[1] < 8000], [x[1] for x in data if x[1] < 8000]
    # plt.errorbar(numbers, find_times, yerr=np.std(find_times))
    plt.scatter(log(numbers), find_times)
    plt.xlabel('log N')
    plt.ylabel('Period Finding Time (s)')
    plt.title('Period Finding Time vs log N')
    plt.show()

if __name__ == '__main__':
    graph_period()
