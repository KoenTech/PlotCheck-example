import json
import ast
import pickle

from matplotlib.axes import Axes
import numpy as np
import matplotlib.pyplot as plt
from pyparsing import warnings



class CodeCell:
    tags = []
    source = ""

    def __init__(self, source, tags):
        self.source = source
        self.tags = tags

class PlotChecker():
    namespace = {}

    def __init__(self, source_code):
        notebook = json.loads(source_code)
        plt.switch_backend("Agg")
        warnings.filterwarnings("ignore")
        cells = []

        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                cells.append(CodeCell("".join(cell["source"]), cell.get("metadata", {}).get("tags", [])))

        self.cells = cells
        self.namespace = globals()

    def checkWithTag(self, tag):
        # get id of first cell with tag
        cell_id = None
        for index, cell in enumerate(self.cells):
            if tag in cell.tags:
                cell_id = index
                break

        if cell_id is None:
            return None

        for cell in self.cells[:cell_id]:
            self.executeSource(cell.source)

        return self.executeSourceTraced(self.cells[cell_id].source)

    def checkAllCells(self):
        results = {}
        for index, cell in enumerate(self.cells):
            results[index] = self.executeSourceTraced(cell.source)

        return results


    def prepareSource(self, source):
        tree = ast.parse(source, mode="exec")

        # remove imports to prevent re-importing matplotlib and overwriting the tracing functions
        class ImportRemover(ast.NodeTransformer):

            def visit_Import(self, node):
                return None

            def visit_ImportFrom(self, node):
                if node.module in ("matplotlib", "numpy"):
                    return None
                return node

        tree = ImportRemover().visit(tree)
        ast.fix_missing_locations(tree)

        code = compile(tree, "<plot-source>", "exec")

        return code

    # execute cell normally, without tracing
    def executeSource(self, source):
        code = self.prepareSource(source)

        if self.namespace is None:
            self.namespace = globals()

        exec(code, self.namespace, self.namespace)
        plt.close("all")

    # execute cell with tracing, capturing all figures and returning their axes
    def executeSourceTraced(self, source):
        code = self.prepareSource(source)

        if self.namespace is None:
            self.namespace = globals()

        captured_figures = []

        original_show = plt.show
        original_axes_show = getattr(Axes, "show", None)

        def snapshot_figure(fig):
            return pickle.loads(
                pickle.dumps(
                    fig,
                    protocol=pickle.HIGHEST_PROTOCOL
                )
            )

        def traced_show(*args, **kwargs):

            figure_numbers = list(plt.get_fignums())

            current_figures = [
                plt.figure(num)
                for num in figure_numbers
            ]

            for fig in current_figures:

                snapshot = snapshot_figure(fig)

                captured_figures.append(snapshot)

            plt.close("all")

            return None

        def traced_axes_show(self, *args, **kwargs):

            # Snapshot the specific figure containing this Axes.
            snapshot = snapshot_figure(self.figure)

            captured_figures.append(snapshot)

            # Immediately remove all pyplot state.
            plt.close("all")

            return None

        # replace maplotlib functions with traced dummy functions that capture the figures
        plt.show = traced_show
        Axes.show = traced_axes_show

        try:

            exec(
                code,
                self.namespace,
                self.namespace
            )

        finally:

            # Restore original matplotlib functions.
            plt.show = original_show

            if original_axes_show is None:
                try:
                    del Axes.show
                except AttributeError:
                    pass
            else:
                Axes.show = original_axes_show

            # Also leave the process completely clean.
            plt.close("all")

        result = []

        for fig in captured_figures:
            result.extend(fig.axes)

        return result


        