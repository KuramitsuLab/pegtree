import {
  pRule, pSeq3, pRef, pMany,
  pOre2, pRange, pChar, pSeq2, pNot, pAny,
  pOre4, pNode, pAnd, pMany1, pSeq4, pOption,
  pOre3, pEmpty, example, pDict, pFold,
} from './pasm';

export const CJ = (peg?: any) => {
  if (peg === undefined) {
    peg = {}
  }
  return peg;
}