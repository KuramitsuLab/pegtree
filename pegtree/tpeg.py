from pegtree.pasm import *


def TPEG(peg):
    pRule(peg, "S", pRange(" \t　", ""))
    pRule(peg, "EOF", pNot(pAny()))
    pRule(peg, "NAME", pSeq2(pRange("_", "AZaz"), pManyRange("_.", "AZaz09")))
    pRule(peg, "UNAME", pOneMany(
        pSeq2(pNotRange("(){}^[]&! \t\r\n　/|*+?.\'\"@:#", ""), pAny())))
    pRule(peg, "Char", pSeq3(pChar("\'"), pNode(pMany(pOre2(pSeq2(pChar("\\"),
                                                                  pAny()), pSeq2(pNotChar("\'"), pAny()))), "Char", 0), pChar("\'")))
    pRule(peg, "DELIM1", pChar("\'\'\'"))
    pRule(peg, "DELIM2", pChar("```"))
    pRule(peg, "Quoted", pSeq2(pChar("\""), pNode(pSeq2(pMany(pOre2(pSeq2(pChar(
        "\\"), pAny()), pSeq2(pNotChar("\""), pAny()))), pChar("\"")), "Quoted", -1)))
    pRule(peg, "Empty", pNode(pEmpty(), "Empty", 0))
    pRule(peg, "Class", pSeq3(pChar("["), pNode(pMany(pOre2(pSeq2(
        pChar("\\"), pAny()), pSeq2(pNotChar("]"), pAny()))), "Class", 0), pChar("]")))
    pRule(peg, "Any", pSeq2(pChar("."), pNode(pEmpty(), "Any", -1)))
    pRule(peg, "Tag", pSeq2(pChar("#"), pSeq2(pSeq2(pNotRange(" \t　\r\n}", ""),
                                                    pAny()), pNode(pMany(pSeq2(pNotRange(" \t　\r\n}", ""), pAny())), "Tag", -1))))
    pRule(peg, "EOL", pOre3(pChar("\n"), pChar("\r\n"), pRef(peg, "EOF")))
    pRule(peg, "Identifier", pNode(
        pOre2(pRef(peg, "NAME"), pRef(peg, "UNAME")), "Name", 0))
    pRule(peg, "COMMENT", pOre2(pSeq3(pChar("/*"), pMany(pSeq2(pNotChar("*/"), pAny())),
                                      pChar("*/")), pSeq2(pChar("//"), pMany(pSeq2(pNot(pRef(peg, "EOL")), pAny())))))
    pRule(peg, "Doc1", pSeq(pChar("\'\'\'"), pManyRange(" \t　", ""), pRef(peg, "EOL"), pNode(pMany(
        pSeq2(pNot(pSeq2(pChar("\'\'\'"), pRef(peg, "EOL"))), pAny())), "Doc", 0), pChar("\'\'\'")))
    pRule(peg, "Doc2", pSeq(pChar("```"), pManyRange(" \t　", ""), pRef(peg, "EOL"), pNode(
        pMany(pSeq2(pNot(pSeq2(pChar("```"), pRef(peg, "EOL"))), pAny())), "Doc", 0), pChar("```")))
    pRule(peg, "Doc0", pNode(pMany(pSeq2(pNot(pRef(peg, "EOL")), pAny())), "Doc", 0))
    pRule(peg, "Ref", pOre2(pRef(peg, "Identifier"), pRef(peg, "Quoted")))
    pRule(peg, "__", pMany(pOre3(pRange(" \t　", ""),
                                 pRange("\r\n", ""), pRef(peg, "COMMENT"))))
    pRule(peg, "_", pMany(pOre2(pRange(" \t　", ""), pRef(peg, "COMMENT"))))
    pRule(peg, "Doc", pOre3(pRef(peg, "Doc1"),
                            pRef(peg, "Doc2"), pRef(peg, "Doc0")))
    pRule(peg, "Names", pNode(pSeq3(pRef(peg, "Identifier"), pRef(peg, "_"), pMany(
        pSeq4(pChar(","), pRef(peg, "_"), pRef(peg, "Identifier"), pRef(peg, "_")))), "", 0))
    pRule(peg, "EOS", pOre2(pSeq2(pRef(peg, "_"), pOneMany(pSeq2(pChar(";"),
                                                                 pRef(peg, "_")))), pOneMany(pSeq2(pRef(peg, "_"), pRef(peg, "EOL")))))
    pRule(peg, "SS", pOre2(pSeq3(pRange(" \t　", ""), pRef(peg, "_"), pNot(pRef(peg, "EOL"))), pSeq3(
        pOneMany(pSeq2(pRef(peg, "_"), pRef(peg, "EOL"))), pRange(" \t　", ""), pRef(peg, "_"))))
    pRule(peg, "Import", pSeq2(pSeq2(pSeq2(pChar("from"), pRange(" \t　", "")), pNode(pSeq3(pRef(peg, "_"), pEdge("name", pOre2(pRef(peg, "Identifier"), pRef(peg, "Char"))),
                                                                                           pOption(pSeq(pRef(peg, "_"), pChar("import"), pRange(" \t　", ""), pRef(peg, "_"), pEdge("names", pRef(peg, "Names"))))), "Import", -9)), pRef(peg, "EOS")))
    pRule(peg, "Example", pSeq2(pSeq2(pSeq2(pChar("example"), pRange(" \t　", "")), pNode(pSeq3(pRef(peg, "_"),
                                                                                               pEdge("names", pRef(peg, "Names")), pEdge("doc", pRef(peg, "Doc"))), "Example", -15)), pRef(peg, "EOS")))
    pRule(peg, "Not", pSeq2(pChar("!"), pNode(
        pEdge("e", pRef(peg, "Predicate")), "Not", 0)))
    pRule(peg, "And", pSeq2(pChar("&"), pNode(
        pEdge("e", pRef(peg, "Predicate")), "And", 0)))
    pRule(peg, "Group", pSeq(pChar("("), pRef(peg, "__"), pOre2(
        pRef(peg, "Expression"), pRef(peg, "Empty")), pRef(peg, "__"), pChar(")")))
    pRule(peg, "Fold", pSeq2(pChar("{"), pNode(pSeq(pRef(peg, "_"), pOre2(pSeq2(pChar("^"), pRef(peg, "__")), pSeq2(pRef(peg, "__"), pEdge("edge", pSeq(pRef(peg, "Identifier"), pChar(":"), pRef(peg, "_"), pChar("^"), pRef(peg, "__"))))), pOption(pSeq2(
        pEdge("tag", pRef(peg, "Tag")), pRef(peg, "__"))), pEdge("e", pOre2(pSeq2(pRef(peg, "Expression"), pRef(peg, "__")), pRef(peg, "Empty"))), pOption(pSeq2(pEdge("tag", pRef(peg, "Tag")), pRef(peg, "__"))), pRef(peg, "__"), pChar("}")), "Fold", -1)))
    pRule(peg, "Node", pSeq2(pChar("{"), pNode(pSeq(pRef(peg, "__"), pOption(pSeq2(pEdge("tag", pRef(peg, "Tag")), pRef(peg, "__"))), pEdge("e", pOre2(pSeq2(pRef(
        peg, "Expression"), pRef(peg, "__")), pRef(peg, "Empty"))), pOption(pSeq2(pEdge("tag", pRef(peg, "Tag")), pRef(peg, "__"))), pRef(peg, "__"), pChar("}")), "Node", -1)))
    pRule(peg, "OldFold", pSeq2(pChar("^"), pNode(pSeq(pRef(peg, "_"), pChar("{"), pRef(peg, "__"), pOption(pSeq2(pEdge("tag", pRef(peg, "Tag")), pRef(peg, "__"))), pEdge("e", pOre2(
        pSeq2(pRef(peg, "Expression"), pRef(peg, "__")), pRef(peg, "Empty"))), pOption(pSeq2(pEdge("tag", pRef(peg, "Tag")), pRef(peg, "__"))), pRef(peg, "__"), pChar("}")), "Fold", -1)))
    pRule(peg, "EdgeFold", pNode(pSeq(pEdge("edge", pRef(peg, "Identifier")), pChar(":"), pRef(peg, "_"), pChar("^"), pRef(peg, "_"), pChar("{"), pRef(peg, "__"), pOption(pSeq2(pEdge("tag", pRef(peg, "Tag")), pRef(
        peg, "__"))), pEdge("e", pOre2(pSeq2(pRef(peg, "Expression"), pRef(peg, "__")), pRef(peg, "Empty"))), pOption(pSeq2(pEdge("tag", pRef(peg, "Tag")), pRef(peg, "__"))), pRef(peg, "__"), pChar("}")), "Fold", 0))
    pRule(peg, "Edge", pNode(pSeq(pEdge("edge", pRef(peg, "Identifier")), pChar(
        ":"), pRef(peg, "_"), pNotChar("^"), pEdge("e", pRef(peg, "Term"))), "Edge", 0))
    pRule(peg, "Func", pSeq2(pChar("@"), pNode(pSeq(pRef(peg, "Identifier"), pChar("("), pRef(peg, "__"), pOre2(pSeq2(pRef(peg, "Expression"), pRef(peg, "_")), pRef(
        peg, "Empty")), pMany(pSeq(pRef(peg, "_"), pChar(","), pRef(peg, "__"), pRef(peg, "Expression"), pRef(peg, "_"))), pRef(peg, "__"), pChar(")")), "Func", -1)))
    pRule(peg, "Suffix", pSeq2(pRef(peg, "Term"), pOption(pOre3(pSeq2(pChar("*"), pFold("e", pEmpty(), "Many", -1)),
                                                                pSeq2(pChar("+"), pFold("e", pEmpty(), "OneMany", -1)), pSeq2(pChar("?"), pFold("e", pEmpty(), "Option", -1))))))
    pRule(peg, "Sequence", pSeq2(pRef(peg, "Predicate"), pOption(
        pFold("", pOneMany(pSeq2(pRef(peg, "SS"), pRef(peg, "Predicate"))), "Seq", 0))))
    pRule(peg, "Choice", pSeq2(pRef(peg, "Sequence"), pOption(pFold("", pOneMany(pSeq4(
        pRef(peg, "__"), pDict("/ ||"), pRef(peg, "_"), pRef(peg, "Sequence"))), "Ore", 0))))
    pRule(peg, "Expression", pSeq2(pRef(peg, "Choice"), pOption(pFold("", pOneMany(pSeq(pRef(
        peg, "__"), pChar("|"), pNotChar("|"), pRef(peg, "_"), pRef(peg, "Choice"))), "Alt", 0))))
    pRule(peg, "Rule", pSeq2(pNode(pSeq(pEdge("name", pOre2(pRef(peg, "Identifier"), pRef(peg, "Quoted"))), pRef(peg, "__"), pDict("= <-"),
                                        pRef(peg, "__"), pOption(pSeq2(pRange("/|", ""), pRef(peg, "__"))), pEdge("e", pRef(peg, "Expression"))), "Rule", 0), pRef(peg, "EOS")))
    pRule(peg, "Statement", pOre3(pRef(peg, "Import"),
                                  pRef(peg, "Example"), pRef(peg, "Rule")))
    pRule(peg, "Source", pNode(pMany(pRef(peg, "Statement")), "Source", 0))
    pRule(peg, "Start", pSeq3(pRef(peg, "__"),
                              pRef(peg, "Source"), pRef(peg, "EOF")))
    pRule(peg, "Term", pOre(pRef(peg, "Group"), pRef(peg, "Char"), pRef(peg, "Class"), pRef(peg, "Any"), pRef(peg, "Fold"), pRef(
        peg, "Node"), pRef(peg, "OldFold"), pRef(peg, "EdgeFold"), pRef(peg, "Edge"), pRef(peg, "Func"), pRef(peg, "Ref")))
    pRule(peg, "Predicate", pOre3(pRef(peg, "Not"),
                                  pRef(peg, "And"), pRef(peg, "Suffix")))
    return peg


TPEGGrammar = TPEG({})
# print(TPEGGrammar)
