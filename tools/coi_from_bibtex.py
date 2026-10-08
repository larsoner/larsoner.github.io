#!/usr/bin/env python
"""List recent co-authors from a BibTeX file for conflict-of-interest forms.

The output is CSV rows of ``"Surname, Given",,,M/D/YYYY`` (name, two blank
columns for organizational affiliation and optional contact info, and the
last-active date), matching the co-author table of the NSF Collaborators and
Other Affiliations (COA) template. Paste the rows into the template and fill
in affiliations.

Authors are matched on surname plus first initial, so "Taulu, S." and
"Taulu, Samu" are merged (keeping the most complete given name). Two
different people with the same surname and first initial would be merged as
well, so skim the output before submitting it.

Examples
--------
$ python tools/coi_from_bibtex.py > coi.csv
$ python tools/coi_from_bibtex.py --months 48 --self "Larson, E"
"""

import argparse
import csv
import datetime
import sys
from pathlib import Path

import bibtexparser

DEFAULT_BIB = Path(__file__).resolve().parents[1] / "data" / "larsoner.bib"
MONTHS = {
    month: ii
    for ii, month in enumerate(
        ("jan", "feb", "mar", "apr", "may", "jun",
         "jul", "aug", "sep", "oct", "nov", "dec"),
        1,
    )
}


def clean(text):
    """Strip BibTeX braces/escapes and normalize whitespace."""
    text = text.replace("{", "").replace("}", "").replace("\\", "")
    return " ".join(text.split())


def split_name(name):
    """Split 'Surname, Given' into (surname, given); mononyms have no given."""
    surname, _, given = clean(name).partition(", ")
    return surname.strip(), given.strip()


def name_key(surname, given):
    return (surname.lower(), given[:1].lower())


def entry_date(entry, today):
    """Publication date (year, month), defaulting to today for in-press work."""
    fields = {field.key.lower(): clean(str(field.value)) for field in entry.fields}
    year = fields.get("year", "")
    if not year.isdigit():  # empty, "in press", etc.
        return today.year, today.month
    month = fields.get("month", "").lower()[:3]
    # When the month is unknown, assume the latest possible one (but not in the
    # future) so the entry is not wrongly dropped from the look-back window
    month = MONTHS.get(month, int(month) if month.isdigit() else 12)
    return min((int(year), month), (today.year, today.month))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--bib", type=Path, default=DEFAULT_BIB,
                        help="BibTeX file (default: %(default)s)")
    parser.add_argument("--self", dest="self_name", default="Larson, E",
                        help="your name as 'Surname, First initial' so you are "
                             "excluded (default: %(default)s)")
    parser.add_argument("--months", type=int, default=48,
                        help="look-back window in months (default: %(default)s, "
                             "the NSF COA window)")
    args = parser.parse_args(argv)

    today = datetime.date.today()
    cutoff = today.year * 12 + today.month - args.months
    self_key = name_key(*split_name(args.self_name))

    library = bibtexparser.parse_file(str(args.bib))
    if library.failed_blocks:
        sys.exit(f"Failed to parse {len(library.failed_blocks)} block(s) in {args.bib}")

    coauthors = {}  # key -> [surname, given, (year, month)]
    for entry in library.entries:
        date = entry_date(entry, today)
        if date[0] * 12 + date[1] < cutoff or "author" not in entry.fields_dict:
            continue
        for name in clean(entry["author"]).split(" and "):
            surname, given = split_name(name)
            key = name_key(surname, given)
            if key == self_key or not surname:
                continue
            if key not in coauthors:
                coauthors[key] = [surname, given, date]
                continue
            record = coauthors[key]
            # keep the most complete spelling of the given name
            if len(given.replace(".", "")) > len(record[1].replace(".", "")):
                record[0], record[1] = surname, given
            record[2] = max(record[2], date)

    writer = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
    for surname, given, (year, month) in sorted(
        coauthors.values(), key=lambda rec: (rec[0].lower(), rec[1].lower())
    ):
        writer.writerow([f"{surname}, {given}" if given else surname,
                         "", "", f"{month}/1/{year}"])


if __name__ == "__main__":
    main()
