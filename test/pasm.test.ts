
import {
  pRule, pChar,
  generate,
  pSeq2,
  pSeq3,
  pSeq4,
  pSeq,
  pEmpty,
  pRef,
  pRange,
  pOption,
  pAnd,
  pNot,
  pMany,
  pMany1
} from '../pegtree/pasm';

test(`'a'`, () => {
  const peg = {}
  pRule(peg, 'A', pChar('a'));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(`a`);
});

test(`''`, () => {
  const peg = {}
  pRule(peg, 'A', pChar(''));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(``);
});

test(`''`, () => {
  const peg = {}
  pRule(peg, 'A', pEmpty());
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(``);
});

test(`A`, () => {
  const peg = {}
  pRule(peg, 'A', pRef(peg, 'B'));
  pRule(peg, 'B', pChar('aa'));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(`aa`);
});

test(`A`, () => {
  const peg = {}
  pRule(peg, 'B', pChar('aa'));
  pRule(peg, 'A', pRef(peg, 'B'));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(`aa`);
});

test(`'a' 'a'`, () => {
  const peg = {}
  pRule(peg, 'A', pSeq2(pChar('a'), pChar('a')));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaa')
  expect(tree.toString()).toStrictEqual(`aa`);
});


test(`'a' 'a' 'a'`, () => {
  const peg = {}
  pRule(peg, 'A', pSeq3(pChar('a'), pChar('a'), pChar('a')));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(`aaa`);
});

test(`'a' 'a' 'a' 'a'`, () => {
  const peg = {}
  pRule(peg, 'A', pSeq4(pChar('a'), pChar('a'), pChar('a'), pChar('a')));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(`aaaa`);
});

test(`'a' 'a' 'a' 'a' 'a'`, () => {
  const peg = {}
  pRule(peg, 'A', pSeq(pChar('a'), pChar('a'), pChar('a'), pChar('a'), pChar('a')));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(`aaaaa`);
});

test(`[Aa]`, () => {
  const peg = {}
  pRule(peg, 'A', pRange('Aa'));
  const parser = generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.toString()).toStrictEqual(`a`);
});

test(`[a-z]`, () => {
  const peg = {}
  pRule(peg, 'A', pRange('', 'az'));
  const parser = generate(peg, 'A')
  const tree = parser('zazb')
  expect(tree.toString()).toStrictEqual(`z`);
});

test(`&'ab'`, () => {
  const peg = {}
  pRule(peg, 'A', pAnd(pChar('ab')));
  const parser = generate(peg, 'A')
  const tree = parser('aba')
  expect(tree.toString()).toStrictEqual(``);
});

test(`!'ab'`, () => {
  const peg = {}
  pRule(peg, 'A', pNot(pChar('ab')));
  const parser = generate(peg, 'A')
  const tree = parser('bab')
  expect(tree.toString()).toStrictEqual(``);
});

test(`'ab'*`, () => {
  const peg = {}
  pRule(peg, 'A', pMany(pChar('ab')));
  const parser = generate(peg, 'A')
  const tree = parser('ababb')
  expect(tree.toString()).toStrictEqual(`abab`);
});

test(`'ab'+`, () => {
  const peg = {}
  pRule(peg, 'A', pMany1(pChar('ab')));
  const parser = generate(peg, 'A')
  const tree = parser('ababb')
  expect(tree.toString()).toStrictEqual(`abab`);
});

test(`'ab'?`, () => {
  const peg = {}
  pRule(peg, 'A', pOption(pChar('ab')));
  const parser = generate(peg, 'A')
  const tree = parser('ababb')
  expect(tree.toString()).toStrictEqual(`ab`);
});
