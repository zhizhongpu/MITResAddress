#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np

def CreateTestPlot():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, 'b-', linewidth=2)
    plt.grid(True)
    
    plt.savefig('test_plot.eps', format='eps')
    plt.savefig('test_plot_quoted.eps')
    
if __name__ == '__main__':
    CreateTestPlot()