#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import bibtexparser


AUTHOR = 'Eric Larson'
SITENAME = 'Eric Larson'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Detroit'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (
    ('github', 'https://github.com/larsoner/'),
    # ('twitter-square', 'https://twitter.com/agramfort'),
    ('google-scholar-square',
     'https://scholar.google.com/citations?user=87KLuLUAAAAJ'),
    ('linkedin', 'www.linkedin.com/in/larsoner')
)

DEFAULT_PAGINATION = 10
PAGE_ORDER_BY = 'sortorder'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "themes/pure-eric"
PROFILE_IMG_URL = '/images/profile.jpg'
PROFILE_IMAGE_URL = '/images/profile.jpg'

GOOGLE_ANALYTICS = "UA-35793277-1"

STATIC_PATHS = ['images', 'extra']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/.nojeykyll': {'path': '.nojekyll'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}
PAGE_EXCLUDES = ['widgets', '.ipynb_checkpoints']
ARTICLE_EXCLUDES = ['widgets', '.ipynb_checkpoints']
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = False
DEFAULT_DATE = 'fs'
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'

DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

PLUGIN_PATHS = ['../pelican-plugins']

TEMPLATE_PAGES = {
    'publications.html': 'publications.html',
}

# Publications


def make_nice_author(author, emphasize='Larson, E'):
    split_author = author.split(' and ')
    insert_pos = len(split_author) - 1
    names_split = [au.split(', ') for au in split_author]
    names = list()
    for n in names_split:
        if len(n) == 1:
            names.append(n[0])
        else:
            assert len(n) == 2, n
            for ii in range(2):
                if n[ii].startswith('{') and n[ii].endswith('}'):
                    n[ii] = n[ii][1:-1]
            names.append('{}, {}.'.format(n[0], n[1][:1]))
    if len(split_author) > 1:
        author_edit = ', '.join(names[:insert_pos]) + ' and ' + names[insert_pos]
    else:
        author_edit = names[insert_pos]
    if emphasize:
        author_edit = author_edit.replace(
            emphasize, '<strong><em>' + emphasize + '</em></strong>')
    return author_edit


def make_nice_title(title):
    title = title.replace('{', '')
    title = title.replace('}', '')
    return title


""" XXX
- make sure not to use unicode or LaTeX code
- only full author records, in "surname, name and" format
"""


def get_bib_entries(bib_fname):
    with open(bib_fname) as bib:
        bib_str = bib.read()

    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    records = parser.parse(bib_str)
    parser2 = bibtexparser.bparser.BibTexParser(common_strings=True)
    one_records = parser2.parse(bib_str)

    entries = []

    for k, item in enumerate(records.entries):
        one_records.entries = records.entries[k:k + 1]
        item['author'] = make_nice_author(item['author'])
        for key in ['annote', 'owner', 'group', 'topic']:
            if key in item:
                del item[key]

        item['bibtex'] = bibtexparser.dumps(one_records).strip()
        item['title'] = make_nice_title(item['title'])
        item['index'] = k
        if 'doi' in item:
            item['link'] = f'https://doi.org/{item["doi"]}'
        elif 'url' in item:
            item['link'] = item['url']
        entries.append(item)
        assert 'date' in item or 'year' in item, item['title']
    return entries


entries = get_bib_entries('./data/larsoner.bib')

entries.sort(key=lambda record: record.get('date', record.get('year', None)),
             reverse=True)

PUBLICATION_LIST = entries
PUBLICATION_LIST_SLAB = entries
PUBLICATION_LIST_SHORT = PUBLICATION_LIST[:7]
TAGLINE = 'UW ILABS'
N_PUBLICATIONS = len(PUBLICATION_LIST)
