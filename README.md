# hsan
C/C++ headers analyser/sanitizer.

## Features
* Analyze C/C++ ```#include``` dependencies and produce a graph using DOT graph description language.

## Required packages
* ```python```
* [opt] ```graphviz``` (for visualization purposes)

## Example
```bash
python makegraph.py
dot -Tsvg graph.dot -o graph.svg
```

## Todo
* Add CLI options.
* Check that all of the involved headers files actually exist.
* Check that a file *explicitly* (by itself) includes any required header.
* Generalize the searched token, to extend the analysis beyond only ```#include``` directives.
* Use another language (e.g. Rust)?
