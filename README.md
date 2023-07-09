# Estimate of Public Jupyter Notebooks on GitHub

- [View the daily report notebook](https://github.com/parente/nbestimate/blob/master/estimate.ipynb)
- [See the raw count data in a CSV](https://github.com/parente/nbestimate/blob/master/ipynb_counts.csv)

## Data Collection History

- Late-2014 to mid-2016: I wrote a script that scrapes the GitHub web search UI for the count,
  appends to a CSV, executes a notebook, and stores the results in a gist at
  https://gist.github.com/parente/facb555dfbae28e817e0. I scheduled the script to run daily.
- Mid-2106 to Late-2016: The GitHub web search UI started requiring authentication to see global
  search results. I stopped collecting data.
- Late-2016 to early-2019: I rewrote the process to include a human-in-the-loop who entered the hit
  count after viewing the search results page. I moved the CSV, notebook, and scripts to this repo,
  and sporadically ran the script.
- Early-2019: I found out that the GitHub search API now supports global search. I automated the
  entire collection process again and set it to run on TravisCI on a daily schedule.
- December 2020: [GitHub changed their code search index results](https://github.blog/changelog/2020-12-17-changes-to-code-search-indexing/)
  to exclude repositories without activity for the past year. The ipynb search result count
  dropped from nearly 10 million to 4.5 million `ipynb` files, stayed there for a day or so, and
  then began climbing again from that new origin.
- June 2021: I started collecting data again but disabled the notebook showing the historical and
  predicted counts.
- July 2021: I revived the notebook showing the historical counts but kept prediction disabled.
- April 2023: I noticed that after reporting an all time high of 11 million search results on
  2023-04-19, the GitHub code search API started returning orders of magnitude fewer results in the
  following days (1M, 100k, 1k). In contrast, the GitHub search UI reports 3.4M hits for the same
  query, which is still a far cry from the 11M reported by the API previously.

## Assumptions

- That the search query hits are less than or equal to the total number of `*.ipynb` files on GitHub.
- That the result is **not** inflated due to GitHub forks.
  - Evidence: We do not see the tutorial notebooks from the ipython/ipython GitHub repository
    duplicated in the search results because of the 2,000+ forks of the ipython/ipython repo.
- That the result **is** inflated a tiny bit by manually created duplicates of notebooks.
  - Evidence: Some people seem to download their favorite notebooks and then upload them into
    their own git repositories for safe keeping.
