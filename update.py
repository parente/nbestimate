from __future__ import print_function
import sys
from datetime import datetime


def main():
    dt = datetime.now().strftime('%Y-%m-%d')
    try:
        count = sys.argv[1].strip()
    except IndexError:
        count = input('Count for {}: '.format(dt))
    line = '{},{}\n'.format(dt, int(count))
    with open('ipynb_counts.csv', 'a') as f:
        f.write(line)
    print('Done')

if __name__ == '__main__':
    main()
