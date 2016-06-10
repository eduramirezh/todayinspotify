from bs4 import BeautifulSoup
import itertools
import requests
import spotipy
import yaml

config = {}
with open('config.yml', 'r') as f:
    config = yaml.load(f)

sp = spotipy.Spotify(auth=config['token'])

def get_sections(parsed_html):
    sections = {}
    key = ''
    for tag in parsed_html.select('table .accordion')[0].children:
        if tag.name == 'h3':
            key = tag.text
        elif tag.name == 'table':
            sections[key] = parse_section(tag)
    return sections

def parse_section(section):
    filtered = [s for s in section.children if s.__class__.__name__ != 'NavigableString']
    results = []
    for fact in filtered:
        for link in fact.select('a'):
            results.append(link.text)
    return results


added = []
html_file = requests.get('http://calendar.songfacts.com').text
soup = BeautifulSoup(html_file, 'html.parser')
sections = get_sections(soup)
queries = list(itertools.chain.from_iterable(sections.values()))
print(queries)


