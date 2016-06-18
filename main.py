from bs4 import BeautifulSoup
import requests
import spotipy
import yaml

def get_auth_spotify():
    config = {}
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)
    return spotipy.Spotify(auth=config['token'])

def get_sections(parsed_html):
    sections_dict = {}
    key = ''
    for tag in parsed_html.select('table .accordion')[0].children:
        if tag.name == 'h3':
            key = tag.text[0:tag.text.index('(') - 1]
        elif tag.name == 'table':
            sections_dict[key] = tag
    return sections_dict

def parse_births(birth_section):
    """Return array of artist names present on Spotify"""
    filtered = [s for s in birth_section.children if s.__class__.__name__ != 'NavigableString']
    results = []
    for fact in filtered:
        artist = extract_birth_artist(fact)
        results.append(artist)

def extract_birth_artist(fact):
    html_content = str(fact).split(':')[1]
    artist_name = ''
    if '(' in html_content and ')' in html_content:
        artist_name = html_content[html_content.index('(') + 1:html_content.rindex(')')]
    elif len(fact.select('a')):
        artist_name = fact.select('a')[0].text
    else:
        artist_name = fact.text.split(':')[1]
    return verify_in_spotify(artist_name, 'artist')

def verify_in_spotify(name, content_type):
    spotify = get_auth_spotify()
    return spotify.search(name, 1, 0, content_type)

def main():
    added = []
    sp_auth = get_auth_spotify()
    html_file = requests.get('http://calendar.songfacts.com').text
    soup = BeautifulSoup(html_file, 'html.parser')
    sections = get_sections(soup)
    births_artists = parse_births(sections['Births'])
    print(births_artists)
    #queries = list(itertools.chain.from_iterable(sections.values()))
    # print(sp_unauth.search(queries[0]))

main()
