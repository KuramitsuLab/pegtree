from pegtree.pasm import *


def TPEG(peg):
    pRule(peg, 'Start', pSeq3(pRef(peg, '__'), pRef(
        peg, 'Source'), pRef(peg, 'EOF')))
    pRule(peg, '__', pMany(pOre2(pRange(' \t\r\n', ''), pRef(peg, 'COMMENT'))))
    pRule(peg, '_', pMany(pOre2(pRange(' \t', ''), pRef(peg, 'COMMENT'))))
    pRule(peg, 'COMMENT', pOre2(pSeq3(pChar('/*'), pMany(pSeq2(pNot(pChar('*/')), pAny())),
                                      pChar('*/')), pSeq2(pChar('//'), pMany(pSeq2(pNot(pRef(peg, 'EOL')), pAny())))))
    pRule(peg, 'EOL', pOre(pChar('\n'), pChar('\r\n'), pRef(peg, 'EOF')))
    pRule(peg, 'EOF', pNot(pAny()))
    pRule(peg, 'S', pRange(' \t', ''))
    pRule(peg, 'Source', pNode(
        pMany(pEdge('', pRef(peg, 'Statement'))), 'Source', 0))
    pRule(peg, 'EOS', pOre2(pSeq2(pRef(peg, '_'), pMany1(pSeq2(pChar(';'), pRef(
        peg, '_')))), pMany1(pSeq2(pRef(peg, '_'), pRef(peg, 'EOL')))))
    pRule(peg, 'Statement', pOre(pRef(peg, 'Import'), pRef(
        peg, 'Example'), pRef(peg, 'Rule')))
    pRule(peg, 'Import', pSeq2(pNode(pSeq(pChar('from'), pRef(peg, 'S'), pRef(peg, '_'), pEdge('name', pOre2(pRef(peg, 'Identifier'), pRef(peg, 'Char'))), pOption(
        pSeq(pRef(peg, '_'), pChar('import'), pRef(peg, 'S'), pRef(peg, '_'), pEdge('names', pRef(peg, 'Names'))))), 'Import', 0), pRef(peg, 'EOS')))
    pRule(peg, 'Example', pSeq2(pNode(pSeq(pChar('example'), pRef(peg, 'S'), pRef(peg, '_'), pEdge(
        'names', pRef(peg, 'Names')), pEdge('doc', pRef(peg, 'Doc'))), 'Example', 0), pRef(peg, 'EOS')))
    pRule(peg, 'Names', pNode(pSeq3(pEdge('', pRef(peg, 'Identifier')), pRef(peg, '_'), pMany(pSeq(
        pChar(','), pRef(peg, '_'), pEdge('', pRef(peg, 'Identifier')), pRef(peg, '_')))), '', 0))
    pRule(peg, 'Doc', pOre(pRef(peg, 'Doc1'),
                           pRef(peg, 'Doc2'), pRef(peg, 'Doc0')))
    pRule(peg, 'Doc0', pNode(pMany(pSeq2(pNot(pRef(peg, 'EOL')), pAny())), 'Doc', 0))
    pRule(peg, 'Doc1', pSeq(pRef(peg, 'DELIM1'), pMany(pRef(peg, 'S')), pRef(peg, 'EOL'), pNode(pMany(
        pSeq2(pNot(pSeq2(pRef(peg, 'DELIM1'), pRef(peg, 'EOL'))), pAny())), 'Doc', 0), pRef(peg, 'DELIM1')))
    pRule(peg, 'DELIM1', pChar("'''"))
    pRule(peg, 'Doc2', pSeq(pRef(peg, 'DELIM2'), pMany(pRef(peg, 'S')), pRef(peg, 'EOL'), pNode(pMany(
        pSeq2(pNot(pSeq2(pRef(peg, 'DELIM2'), pRef(peg, 'EOL'))), pAny())), 'Doc', 0), pRef(peg, 'DELIM2')))
    pRule(peg, 'DELIM2', pChar('```'))
    pRule(peg, 'Rule', pSeq2(pNode(pSeq(pEdge('name', pOre2(pRef(peg, 'Identifier'), pRef(peg, 'QName'))), pRef(peg, '__'), pOre2(pChar('='), pChar(
        '<-')), pRef(peg, '__'), pOption(pSeq2(pRange('/|', ''), pRef(peg, '__'))), pEdge('e', pRef(peg, 'Expression'))), 'Rule', 0), pRef(peg, 'EOS')))
    pRule(peg, 'Identifier', pNode(pRef(peg, 'NAME'), 'Name', 0))
    pRule(peg, 'NAME', pSeq2(pRange('_', 'AZaz'),
                             pMany(pRange('_.', 'AZaz09'))))
    pRule(peg, 'Expression', pSeq2(pRef(peg, 'Choice'), pOption(pFold('', pMany1(pSeq(pRef(peg, '__'), pChar(
        '|'), pNot(pChar('|')), pRef(peg, '_'), pEdge('', pRef(peg, 'Choice')))), 'Alt', 0))))
    pRule(peg, 'Choice', pSeq2(pRef(peg, 'Sequence'), pOption(pFold('', pMany1(pSeq(pRef(peg, '__'), pOre2(
        pChar('/'), pChar('||')), pRef(peg, '_'), pEdge('', pRef(peg, 'Sequence')))), 'Ore', 0))))
    pRule(peg, 'Sequence', pSeq2(pRef(peg, 'Predicate'), pOption(pFold('', pMany1(
        pSeq2(pRef(peg, 'SS'), pEdge('', pRef(peg, 'Predicate')))), 'Seq', 0))))
    pRule(peg, 'SS', pOre2(pSeq3(pRef(peg, 'S'), pRef(peg, '_'), pNot(pRef(peg, 'EOL'))), pSeq3(
        pMany1(pSeq2(pRef(peg, '_'), pRef(peg, 'EOL'))), pRef(peg, 'S'), pRef(peg, '_'))))
    pRule(peg, 'Predicate', pOre(pRef(peg, 'Not'), pRef(
        peg, 'And'), pRef(peg, 'Suffix')))
    pRule(peg, 'Not', pSeq2(pChar('!'), pNode(
        pEdge('e', pRef(peg, 'Predicate')), 'Not', 0)))
    pRule(peg, 'And', pSeq2(pChar('&'), pNode(
        pEdge('e', pRef(peg, 'Predicate')), 'And', 0)))
    pRule(peg, 'Suffix', pSeq2(pRef(peg, 'Term'), pOption(pOre(pFold('e', pChar(
        '*'), 'Many', 0), pFold('e', pChar('+'), 'Many1', 0), pFold('e', pChar('?'), 'Option', 0)))))
    pRule(peg, 'Term', pOre(pRef(peg, 'Group'), pRef(peg, 'Char'), pRef(peg, 'Class'), pRef(peg, 'Any'), pRef(
        peg, 'Node'), pRef(peg, 'Fold'), pRef(peg, 'EdgeFold'), pRef(peg, 'Edge'), pRef(peg, 'Func'), pRef(peg, 'Ref')))
    pRule(peg, 'Empty', pNode(pEmpty(), 'Empty', 0))
    pRule(peg, 'Group', pSeq(pChar('('), pRef(peg, '__'), pOre2(
        pRef(peg, 'Expression'), pRef(peg, 'Empty')), pRef(peg, '__'), pChar(')')))
    pRule(peg, 'Any', pNode(pChar('.'), 'Any', 0))
    pRule(peg, 'Char', pSeq3(pChar("'"), pNode(pMany(pOre2(pSeq2(
        pChar('\\'), pAny()), pSeq2(pNot(pChar("'")), pAny()))), 'Char', 0), pChar("'")))
    pRule(peg, 'Class', pSeq3(pChar('['), pNode(pMany(pOre2(pSeq2(
        pChar('\\'), pAny()), pSeq2(pNot(pChar(']')), pAny()))), 'Class', 0), pChar(']')))
    pRule(peg, 'Node', pNode(pSeq(pChar('{'), pRef(peg, '__'), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pEdge('e', pOre2(pSeq2(pRef(
        peg, 'Expression'), pRef(peg, '__')), pRef(peg, 'Empty'))), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pRef(peg, '__'), pChar('}')), 'Node', 0))
    pRule(peg, 'Tag', pSeq2(pChar('#'), pNode(
        pMany1(pSeq2(pNot(pRange(' \t\r\n}', '')), pAny())), 'Tag', 0)))
    pRule(peg, 'Fold', pNode(pSeq(pChar('^'), pRef(peg, '_'), pChar('{'), pRef(peg, '__'), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pEdge('e', pOre2(pSeq2(
        pRef(peg, 'Expression'), pRef(peg, '__')), pRef(peg, 'Empty'))), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pRef(peg, '__'), pChar('}')), 'Fold', 0))
    pRule(peg, 'Edge', pNode(pSeq(pEdge('edge', pRef(peg, 'Identifier')), pChar(':'), pRef(
        peg, '_'), pNot(pChar('^')), pEdge('e', pRef(peg, 'Term'))), 'Edge', 0))
    pRule(peg, 'EdgeFold', pNode(pSeq(pEdge('edge', pRef(peg, 'Identifier')), pChar(':'), pRef(peg, '_'), pChar('^'), pRef(peg, '_'), pChar('{'), pRef(peg, '__'), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(
        peg, '__'))), pEdge('e', pOre2(pSeq2(pRef(peg, 'Expression'), pRef(peg, '__')), pRef(peg, 'Empty'))), pOption(pSeq2(pEdge('tag', pRef(peg, 'Tag')), pRef(peg, '__'))), pRef(peg, '__'), pChar('}')), 'Fold', 0))
    pRule(peg, 'Func', pNode(pSeq(pChar('@'), pEdge('', pRef(peg, 'Identifier')), pChar('('), pRef(peg, '__'), pOre2(pEdge('', pRef(peg, 'Expression')), pEdge(
        '', pRef(peg, 'Empty'))), pMany(pSeq(pRef(peg, '_'), pChar(','), pRef(peg, '__'), pEdge('', pRef(peg, 'Expression')))), pRef(peg, '__'), pChar(')')), 'Func', 0))
    pRule(peg, 'Ref', pOre2(pRef(peg, 'Identifier'), pRef(peg, 'QName')))
    pRule(peg, 'QName', pNode(pSeq3(pChar('"'), pMany(pOre2(pSeq2(
        pChar('\\'), pAny()), pSeq2(pNot(pChar('"')), pAny()))), pChar('"')), 'Name', 0))
    return peg


TPEGGrammar = TPEG({})
# print(TPEGGrammar)
