
import { Grammar } from '../pegtree/pegtree';

test(`A='a'`, () => {
  const peg = new Grammar(`
A = 'a'
  `)
  const parser = peg.generate('A')
  const tree = parser('aa')
  expect(tree.toString()).toStrictEqual(`a`);
});
