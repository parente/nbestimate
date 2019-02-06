# Estimate of Public Jupyter Notebooks on GitHub

* [View the latest report on nbviewer](http://nbviewer.jupyter.org/github/parente/nbestimate/blob/master/estimate.ipynb)
* [See the historical count data in a CSV](ipynb_counts.csv)
* Play with the data yourself: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/parente/nbestimate/master?filepath=estimate.src.ipynb)

A brief history of this project:

* Late-2014 to mid-2016: I write a script scrapes the GitHub web search UI for the count, appends to to a CSV, executes a notebook, and stores the results in a gist at https://gist.github.com/parente/facb555dfbae28e817e0. I schedule the script to run daily.
* Mid-2106 to Late-2016: The GitHub web search UI starts requiring authentication to see global search results. I stop collecting data.
* Late-2016 to early-2019: I rewrite the process to include a human-in-the-loop who enters the hit count after viewing the search results page. I move the CSV, notebook, and scripts to this repo, and sporadically run the script.
* Early-2019: I find out the GitHub search API now supports global search. I automate the entire collection process again and set it to run on TravisCI on a daily schedule.
