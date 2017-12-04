#!/usr/bin/env python
import sys
import webbrowser

from datetime import datetime
from subprocess import check_call

import nbformat

from nbconvert.preprocessors import ExecutePreprocessor


def main():
    print("Opening search results")
    webbrowser.open('https://github.com/search?q=extension%3Aipynb+nbformat_minor&ref=searchresu')

    dt = datetime.now().strftime('%Y-%m-%d')
    try:
        count = sys.argv[1]
    except IndexError:
        count = input('Enter the search hit count for {}: '.format(dt))
    count = count.strip().replace(',', '')
    line = '{},{}\n'.format(dt, int(count))

    print("Appending hit count to CSV")
    with open('ipynb_counts.csv', 'a') as f:
        f.write(line)

    print("Executing estimate notebook")
    with open('estimate.src.ipynb') as fp:
        nb = nbformat.read(fp, 4)

    exp = ExecutePreprocessor(timeout=60)
    updated_nb, _ = exp.preprocess(nb, {})

    print("Saving estimate results")
    with open('estimate.ipynb', 'w') as fp:
        nbformat.write(updated_nb, fp)

    print("Git committing and pushing")
    check_call(['git', 'commit', '-a', '-m', 'Update for {}'.format(dt)])
    check_call(['git', 'push'])

    print('Done!')
    webbrowser.open('http://nbviewer.jupyter.org/github/parente/nbestimate/blob/master/estimate.ipynb')


if __name__ == '__main__':
    main()
