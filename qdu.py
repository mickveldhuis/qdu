import sys
import argparse
from app import DailyUpdater

def main():
    parser = argparse.ArgumentParser(description='QDU')
    parser.add_argument('--source', '-s', help='set the news source.',
                        action='store', dest='source')
    parser.add_argument('--version', '-v', action='version', version='QKU 0.0.1')
    pres = parser.parse_args()

    if not pres.source:
        print('News source not specified, please use the --source flag!')
        sys.exit()

    up = DailyUpdater()
    up.main(pres.source)

if __name__ == '__main__':
    main()