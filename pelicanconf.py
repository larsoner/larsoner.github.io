#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import html

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
    ('orcid-square', 'https://orcid.org/0000-0003-4782-5360'),
    ('linkedin', 'https://www.linkedin.com/in/larsoner')
)

DEFAULT_PAGINATION = 10
PAGE_ORDER_BY = 'sortorder'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "themes/pure-eric"
PROFILE_IMG_URL = '/images/profile.jpg'
PROFILE_IMAGE_URL = '/images/profile.jpg'

GOOGLE_ANALYTICS = "G-LQRZSPRFBY"

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
FILENAME_METADATA = r'(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'

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


def clean_latex(text):
    """Convert the bits of LaTeX we use in the .bib file to plain text."""
    for latex, plain in (("\\&", "&"), ("\\_", "_"), ("\\%", "%")):
        text = text.replace(latex, plain)
    text = text.replace("{", "").replace("}", "").replace("\\", "")
    return " ".join(text.split())


def make_initials(given):
    """Turn given names into initials, e.g. 'Jean-Rémi' -> 'J.-R.', 'Adrian KC' -> 'A. K. C.'."""
    initials = []
    for token in given.replace(".", ". ").split():
        if token.isupper() and token.isalpha() and len(token) > 1:  # e.g. KC
            initials.extend(f"{c}." for c in token)
        else:
            initials.append("-".join(f"{part[:1]}." for part in token.split("-") if part))
    return " ".join(initials)


def make_nice_author(author, emphasize="Larson", max_authors=12, n_first=6):
    names = []
    emphasized = []
    for name in clean_latex(author).split(" and "):
        surname, _, given = name.partition(", ")
        nice = f"{surname}, {make_initials(given)}" if given else surname
        is_me = surname == emphasize and given.startswith("E")
        if is_me:
            nice = f"<strong>{nice}</strong>"
        names.append(nice)
        emphasized.append(is_me)
    if len(names) > max_authors:  # first few, me, and the last author
        mine = [ii for ii, me in enumerate(emphasized) if me]
        keep = sorted(set(range(n_first)) | set(mine) | {len(names) - 1})
        shown = []
        for prev, ii in zip([-1] + keep[:-1], keep):
            if ii - prev > 1:
                shown.append("…")
            shown.append(names[ii])
        return ", ".join(shown[:-1]) + ", and " + shown[-1]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return " and ".join(names)
    return ", ".join(names[:-1]) + ", and " + names[-1]


def make_nice_title(title):
    return clean_latex(title)


def make_venue(item):
    """Build the HTML citation line (journal, volume, pages, etc.) for an entry."""
    get = {key: html.escape(clean_latex(item.get(key, "")), quote=False)
           for key in ("journal", "booktitle", "volume", "number", "pages",
                       "publisher", "edition")}
    pages = get["pages"].replace("--", "–")
    if item["ENTRYTYPE"] == "article":
        venue = f"<em>{get['journal']}</em>"
        issue = f"({get['number']})" if get["number"] else ""
        if get["volume"] or issue:
            venue += f" {get['volume']}{issue}"
            if pages:
                venue += f": {pages}"
        elif pages:
            venue += f", {pages}"
    elif item["ENTRYTYPE"] in ("inproceedings", "incollection"):
        venue = f"In <em>{get['booktitle']}</em>"
        if get["edition"]:
            edition = get["edition"]
            suffix = {"1": "st", "2": "nd", "3": "rd"}.get(edition, "th")
            venue += f" ({edition}{suffix} ed.)"
        if get["publisher"] and item["ENTRYTYPE"] == "incollection":
            venue += f", {get['publisher']}"
        if pages:
            venue += f", pp. {pages}"
    else:
        venue = get["publisher"]
    return venue + "." if venue else ""


""" XXX
- make sure not to use unicode or LaTeX code
- only full author records, in "surname, name and" format
"""


def get_bib_entries(bib_fname):
    with open(bib_fname) as bib:
        bib_str = bib.read()

    library = bibtexparser.parse_string(bib_str)
    assert not library.failed_blocks, "Failed to parse:\n" + "\n".join(
        block.raw for block in library.failed_blocks)

    entries = []

    missing_dates = []
    for k, entry in enumerate(library.entries):
        for key in ['annote', 'owner', 'group', 'topic']:
            entry.pop(key)
        item = {field.key: field.value for field in entry.fields}
        item['ENTRYTYPE'] = entry.entry_type.lower()
        item['ID'] = entry.key
        item['bibtex'] = html.escape(bibtexparser.write_string(
            bibtexparser.Library([entry])).strip(), quote=False)
        item['author'] = make_nice_author(item['author'])
        item['title'] = html.escape(make_nice_title(item['title']), quote=False)
        item['venue'] = make_venue(item)
        item['index'] = k
        if 'doi' in item:
            item['link'] = f'https://doi.org/{item["doi"]}'
            item['link_text'] = 'DOI'
        elif 'url' in item:
            item['link'] = item['url']
            item['link_text'] = 'Link'
        entries.append(item)
        if "date" not in item and "year" not in item:
            missing_dates.append(item['title'][:80])
    assert not missing_dates, "Missing dates:\n" + "\n".join(missing_dates)

    # with open("/Users/larsoner/Desktop/zotero.txt", "w") as fid:
    #     for ent in sorted(entries, key=lambda e: e["title"]):
    #         fid.write(f"{ent['title'][:80].lower()}\n")

    return entries


entries = get_bib_entries('./data/larsoner.bib')

def date_sort(record):
    date = record.get('date', record.get('year', '')).split('/')[0].split('-')[0]
    if date == 'in press':
        date = '9999'
    date = int(date)
    return date

entries.sort(key=date_sort, reverse=True)

PUBLICATION_LIST = entries
PUBLICATION_LIST_SLAB = entries
PUBLICATION_LIST_SHORT = PUBLICATION_LIST[:5]
TAGLINE = 'UW ILABS'
N_PUBLICATIONS = len(PUBLICATION_LIST)

# Landing page

SOFTWARE = (  # (name, URL, role, description)
    ('MNE-Python', 'https://mne.tools', 'Steering Council',
     'Complete M/EEG analysis: preprocessing, forward and inverse modeling, '
     'connectivity, statistics, and machine learning.'),
    ('SciPy', 'https://scipy.org', 'Maintainer',
     'Core scientific Python library, including the signal processing '
     'routines used across the ecosystem.'),
    ('PyVistaQt', 'https://qt.pyvista.org', 'Maintainer',
     'Qt integration for PyVista, enabling interactive 3D visualization in '
     'desktop applications.'),
    ('sphinx-gallery', 'https://sphinx-gallery.github.io', 'Maintainer',
     'Builds rich HTML example galleries from Python scripts for project '
     'documentation.'),
)

# Repositories (not owned by me, excluding conda-forge feedstocks) with merged
# PRs from me, counted via the GitHub GraphQL API in Oct 2026: 209
SOFTWARE_MORE = (
    '200+ more open-source projects on GitHub',
    'Including VisPy, PyVista, Matplotlib, NumPy, scikit-learn, nilearn, '
    'DIPY, and Sphinx. See also my '
    '<a href="https://gitlab.kitware.com/vtk/vtk/-/merge_requests'
    '?scope=all&amp;state=merged&amp;author_username=larsoner">'
    'VTK contributions</a> on GitLab.',
)

TIMELINE = (  # (years, logo, institution, URL, description)
    ('2014–present', 'UW.svg', 'University of Washington', 'https://ilabs.uw.edu',
     'Research scientist, Institute for Learning & Brain Sciences'),
    ('2011–2013', 'UW.svg', 'University of Washington',
     'https://labsn.uw.edu',
     'Postdoctoral fellow, Speech & Hearing Sciences, with Adrian KC Lee'),
    ('2006–2011', 'BU.svg', 'Boston University',
     'https://www.bu.edu/eng/departments/bme/',
     'MS and PhD in Biomedical Engineering'),
    ('2002–2006', 'K.png', 'Kalamazoo College', 'https://www.kzoo.edu/',
     'BA in Mathematics, Physics, and Philosophy'),
)
