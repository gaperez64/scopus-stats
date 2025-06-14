import csv
import sys

import pybliometrics

pybliometrics.init()

# map author ID to name
author_names = {}

for file in sys.argv[1:]:
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for author in row['Author full names'].split(';'):
                id_start = author.rfind('(')
                author_name = author[:id_start].strip()
                author_id = author[id_start:].strip('()')
                author_names[author_id] = author_name

# for author_id, author_name in author_names.items():
#     if author_id != 'h':
#         print(author_id, author_name)
w = csv.writer(sys.stdout)
for author_id, author_name in author_names.items():
    if author_id and author_id not in ['57105333100', 'h']:
        author = pybliometrics.scopus.AuthorRetrieval(author_id)
        w.writerow((author.h_index, author_id, author_name, author.indexed_name))
        sys.stdout.flush()
