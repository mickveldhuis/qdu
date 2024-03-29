import sys
import argparse
import json
from app import DailyUpdater

def main():
    parser = argparse.ArgumentParser(description='QDU')
    parser.add_argument('--source', '-s', help='set the news source',
                        action='store', dest='source')
    parser.add_argument('--list', '-l', help='list all the news sources',
                        action='store_true', dest='list_sources')
    parser.add_argument('--version', '-v', action='version', version='QKU 0.0.1')
    pres = parser.parse_args()

    up = DailyUpdater()

    if pres.list_sources:
        up.list_providers()

    if not pres.source:
        with open('settings.json', 'r') as sf:
            settings = json.load(sf)

        source_list = [settings['default']]
    else:
        source_list = pres.source.split(',')

    up.main(source_list)

if __name__ == '__main__':
    main()
