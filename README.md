# Plot checking demo repository
[![Plot Check](https://github.com/KoenTech/PlotCheck-example/actions/workflows/check-labels.yaml/badge.svg)](https://github.com/KoenTech/PlotCheck-example/actions/workflows/check-labels.yaml)

The branch `fixed` contains a notebook with proper plots. (See pull request #1)

## Example usage
```
koen@Koens-Laptop  % pixi run check
✨ Pixi task (check): python3 ./scripts/checknotebooks.py
WARNING: Cell 3 in ./main.ipynb has a plot without labels. ❌
WARNING: Cell 3 in ./main.ipynb has a plot without labels. ❌
WARNING: Cell 1 in ./assignment_1.ipynb has a plot without labels. ❌

Some plots are missing labels. ❌
```