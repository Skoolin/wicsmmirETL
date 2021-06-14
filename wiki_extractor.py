from urllib.request import urlopen
import xml.etree.ElementTree as ET

def create_wiki_list(url):
    var_url = urlopen(url)
    webpage = var_url.read().decode('utf-8')

    # parse xml.
    root = ET.fromstring(webpage)
    # a default xsi namespace has been prepended to all tags
    ns = {'loc': 'http://www.mediawiki.org/xml/export-0.10/', }
    text = root.find('loc:page', ns).find('loc:revision', ns).find('loc:text', ns).text

    names = []

    lines = text.split('\n')
    it = iter(lines)

    try:
        row = next(it)
        while True:
            # search for tables on page
            if row.startswith('{|class="sortable wikitable"') or row.startswith('{|class="wikitable sortable"'):
                print("found table")
                # skip until first table row
                while not row.startswith('{{'):
                    row = next(it)
                # add the first column to the names list
                while row.startswith('{{'):
                    names.append(row.split('|')[1].split(']]')[0][2:])
                    row = next(it)
            row = next(it)
    except StopIteration:
        row = None

    return names
