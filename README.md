# Estimate of Public Jupyter Notebooks on GitHub

* [Daily report](http://nbviewer.jupyter.org/github/parente/nbestimate/blob/master/estimate.ipynb)
* [Historical counts](ipynb_counts.csv)

[Getting the count](https://github.com/search/count?q=extension%3Aipynb+nbformat_minor&ref=searchresults&type=Code) from GitHub now requires user authentication. Here's the steps to update the count data manually for the time being.

```
anaconda-project run update <count>
anaconda-project run render
anaconda-project run push
anaconda-project run show
```

Originally located at https://gist.github.com/parente/facb555dfbae28e817e0.
