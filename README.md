# Estimate of Public Jupyter Notebooks on GitHub

* [Daily report](estimate.ipynb)
* [Historical counts](ipynb_counts.csv)

Getting the count from GitHub now requires user authentication. Here's the steps to update the count manually for the time being.

```
conda kapsel run update <count>
conda kapsel run render
git commit -A -m "Update for $(date '+%Y-%m-%d')"
```

Originally located at https://gist.github.com/parente/facb555dfbae28e817e0.
