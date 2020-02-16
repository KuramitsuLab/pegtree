# pegtree
[![Build Status](https://img.shields.io/circleci/project/github/kkuramitsu/pegtree.svg)](https://circleci.com/gh/kkuramitsu/pegtree)
[![Downloads](https://img.shields.io/npm/dt/pegtree.svg)](https://npmcharts.com/compare/pegtree?minimal=true)
[![Version](https://img.shields.io/npm/v/pegtree.svg)](https://www.npmjs.com/package/pegtree)
[![License](https://img.shields.io/npm/l/pegtree.svg)](https://www.npmjs.com/package/pegtree)

[![Python Versions](https://img.shields.io/pypi/pyversions/pegtree.svg)](https://pypi.org/project/pegtree/)
[![PyPI version](https://badge.fury.io/py/pegtree.svg)](https://badge.fury.io/py/pegtree)

PEG-Tree Parser Combinator for Python3 and TypeScript

## Installation

### Python3

```sh
pip3 install pegtree
```

### TypeScript

```sh
npm install pegtree --save
```

## Usage

### Python3

```python
from pegtree import Grammar

peg = Grammar('''

''')
parser = peg.generate()
tree = parser('1+2*3')
print(repr(tree))
```

### TypeScript

```typescript
import { Grammar } from 'pegtree'
const peg = new Grammar(`

`)
const parser = peg.generate()
const tree = parser('1+2*3')
console.log(tree)
```

## Test

### TypeScript
```sh
npm run test
```