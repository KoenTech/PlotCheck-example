from checker import PlotChecker
import numpy as np
import matplotlib.pyplot as plt
import os

# find all *.ipynb files recursively in the current directory (no subdirectories with dots)
notebook_files = []

for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for file in files:
        if file.endswith(".ipynb"):
            notebook_files.append(os.path.join(root, file))

any_warnings = False
for notebook in notebook_files:
    try:
        with open(notebook, "r") as f:
            source_code_from_ipynb = f.read()

        checker = PlotChecker(source_code_from_ipynb)

        # check all cells
        results = checker.checkAllCells()

        for (cell, plots) in results.items():
            for ax in plots:
                if not ax.get_xlabel() or not ax.get_ylabel():
                    # print as warning, but continue checking other cells
                    print(f"WARNING: Cell {cell} in {notebook} has a plot without labels. ❌")
                    any_warnings = True
    finally:
        plt.close("all")

if any_warnings:
    print("\nSome plots are missing labels. ❌")
    exit(1) # fail CI/CD pipeline if any warnings were found
else:
    print("\nAll plots have labels. ✅")
    exit(0) # success