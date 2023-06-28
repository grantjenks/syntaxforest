=============
Syntax Forest
=============

Syntax Forest web service for searching syntax trees.

TODO: Yoda style if statements

TODO: Strings as comments: see py-tree-sitter-languages

TODO: Most imported module
(import_statement (dotted_name) @import_name)
(import_from_statement
  module_name: (dotted_name) @import_name)


TODO
====

- Improve performance of search result rendering

- Provide an endpoint for snippets as CSV?

- Deploy new version to PyPI

- Deploy new version to syntaxforest.com

  - Increase scale for workers

  - Import Python 3.11.4 sources

- Separate Django app from project (see django-rrweb for example)

- Update py-tree-sitter-languages to be source-only
