from checker import PlotChecker
import numpy as np
import matplotlib.pyplot as plt
import os

with open("assignment_1.ipynb", "r") as f:
    source_code_from_ipynb = f.read()

checker = PlotChecker(source_code_from_ipynb)

def check_exercise_1():
    try:
        result = checker.checkWithTag("ex1")
        if result is None:
            print("Unable to find exercise 1 in notebook. ❌")
            return
        if len(result) == 0:
            print("Exercise 1 has no plots. ❌")
            return

        if len(result) > 1:
            print("Exercise 1 has more than one plot. ❌")
            return

        ax = result[0]
        if ax.get_xlabel() != "t (s)" or ax.get_ylabel() != "v (V)":
            print("Exercise 1 plot has incorrect labels. ❌")
            return
        
        t = np.linspace(0, 5, 100)
        v = 2.2*np.sin(5 / 2 / np.pi * t)

        y_data = ax.get_lines()[0].get_ydata()
        if not np.allclose(y_data, v, rtol=1e-2):
            print("Exercise 1 plot has incorrect data. ❌")
            return

        print("Exercise 1 is correct. ✅")
    finally:
        plt.close("all")

check_exercise_1()