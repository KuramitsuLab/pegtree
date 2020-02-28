import { PAsm, ParseTree } from './pasm';

export const CJ = (peg?: any) => {
  if (peg === undefined) {
    peg = {}
  }
  return peg;
}