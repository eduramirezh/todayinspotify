from bs4 import BeautifulSoup
import requests

def get_sections(parsed_html):
    sections = {}
    key = ''
    for tag in parsed_html.select('table .accordion')[0].children:
        if tag.name == 'h3':
            key = tag.name
        elif tag.name == 'table':
            sections[key] = parse_section(tag)
    return sections

def parse_section(section):
    filtered = [s for s in section.children if s.__class__.__name__ != 'NavigableString']
    for fact in filtered:
        for link in fact.select('a'):
            print(link.text)


added = []
html_file = requests.get('http://calendar.songfacts.com').text
soup = BeautifulSoup(html_file, 'html.parser')
get_sections(soup)


