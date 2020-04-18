# pegtree
[![Build Status](https://img.shields.io/circleci/project/github/kkuramitsu/pegtree.svg)](https://circleci.com/gh/kkuramitsu/pegtree)
[![Downloads](https://img.shields.io/npm/dt/pegtree.svg)](https://npmcharts.com/compare/pegtree?minimal=true)
[![Version](https://img.shields.io/npm/v/pegtree.svg)](https://www.npmjs.com/package/pegtree)
[![License](https://img.shields.io/npm/l/pegtree.svg)](https://www.npmjs.com/package/pegtree)

[![Python Versions](https://img.shields.io/pypi/pyversions/pegtree.svg)](https://pypi.org/project/pegtree/)
[![PyPI version](https://badge.fury.io/py/pegtree.svg)](https://badge.fury.io/py/pegtree)

A PEG Parser Combinator Generator with Tree Annotation

## Installation

### Python3

```sh
pip3 install pegtree
```

## Usage

### Python3

```python
import pegtree as pg

# 1. load a sample grammar 'math.tpeg'

peg = pg.grammar('math.tpeg')

# 2. generate parser from a grammar

parser = pg.generate(peg)

# 3. parse an input text, then you will obtain parse tree

tree = parser('1+2*3')

print(repr(tree))
```

