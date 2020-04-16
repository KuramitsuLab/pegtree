
import {
  PAsm,
} from '../pegtree/pasm';

const pRule = PAsm.pRule;
const pEmpty = PAsm.pEmpty;
const pChar = PAsm.pChar;
const pRange = PAsm.pRange;

test(`'a'`, () => {
  const peg = {}
  pRule(peg, 'A', pChar('a'));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(`a`);
});

test(`''`, () => {
  const peg = {}
  pRule(peg, 'A', pChar(''));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(``);
});

test(`''`, () => {
  const peg = {}
  pRule(peg, 'A', pEmpty());
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(``);
});

test(`A`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pRef(peg, 'B'));
  pRule(peg, 'B', pChar('aa'));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(`aa`);
});

test(`A`, () => {
  const peg = {}
  pRule(peg, 'B', pChar('aa'));
  pRule(peg, 'A', PAsm.pRef(peg, 'B'));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(`aa`);
});

test(`'a' 'a'`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pSeq2(pChar('a'), pChar('a')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaa')
  expect(tree.getToken()).toStrictEqual(`aa`);
});


test(`'a' 'a' 'a'`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pSeq3(pChar('a'), pChar('a'), pChar('a')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(`aaa`);
});

test(`'a' 'a' 'a' 'a'`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pSeq4(pChar('a'), pChar('a'), pChar('a'), pChar('a')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(`aaaa`);
});

test(`'a' 'a' 'a' 'a' 'a'`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pSeq(pChar('a'), pChar('a'), pChar('a'), pChar('a'), pChar('a')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(`aaaaa`);
});

test(`[Aa]`, () => {
  const peg = {}
  pRule(peg, 'A', pRange('Aa'));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aaaaaa')
  expect(tree.getToken()).toStrictEqual(`a`);
});

test(`[a-z]`, () => {
  const peg = {}
  pRule(peg, 'A', pRange('', 'az'));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('zazb')
  expect(tree.getToken()).toStrictEqual(`z`);
});

test(`&'ab'`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pAnd(pChar('ab')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('aba')
  expect(tree.getToken()).toStrictEqual(``);
});

test(`!'ab'`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pNot(pChar('ab')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('bab')
  expect(tree.getToken()).toStrictEqual(``);
});

test(`'ab'*`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pMany(pChar('ab')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('ababb')
  expect(tree.getToken()).toStrictEqual(`abab`);
});

test(`'ab'+`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pOneMany(pChar('ab')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('ababb')
  expect(tree.getToken()).toStrictEqual(`abab`);
});

test(`'ab'?`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pOption(pChar('ab')));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('ababb')
  expect(tree.getToken()).toStrictEqual(`ab`);
});

test(`pDict`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pDict('aa ab ac ad ae af'));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('acf')
  expect(tree.getToken()).toStrictEqual(`ac`);
});

test(`pDict(trie)`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pDict('aa ab ac ad ae af a a1 a2 a3 a4 a5 a6 a7 a8 a9'));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('acf')
  expect(tree.getToken()).toStrictEqual(`ac`);
});

test(`pDict(trie)`, () => {
  const peg = {}
  pRule(peg, 'A', PAsm.pDict('aa ab ac ad ae af a a1 a2 a3 a4 a5 a6 a7 a8 a9'));
  const parser = PAsm.generate(peg, 'A')
  const tree = parser('a1x')
  expect(tree.getToken()).toStrictEqual(`a`);
});
