
var LibZen_GreekNames_Z0 = ["__a", "__b", "__c"];
var ZType = (function() {
   function ZType(){
      this.TypeFlag = 0;
      this.TypeId = 0;
   }
   return ZType;
})();

var ZTypeUniqueTypeFlag_Z1 = 1 << 16;
var ZTypeUnboxTypeFlag_Z2 = 1 << 10;
var ZTypeOpenTypeFlag_Z3 = 1 << 9;
var ZTypeVarType_Z4 = ZType__4qwg(new ZType(), 1 << 16, "var", null);
var ZTypeVoidType_Z5 = ZType__4qwg(new ZType(), 1 << 16, "void", null);
var ZTypeBooleanType_Z6 = ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null));
var ZTypeIntType_Z7 = ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null));
var ZTypeFloatType_Z8 = ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null));
var ZTypeStringType_Z9 = ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null));
var ZTypeTypeType_Z10 = ZType__4qwg(new ZType(), 1 << 16, "Type", ZType__4qwg(new ZType(), 1 << 16, "var", null));
var ZClassField = (function() {
   function ZClassField(){
      this.FieldFlag = 0;
      this.FieldNativeIndex = 0;
   }
   return ZClassField;
})();

var __extends = this.__extends || function (d, b) {
   for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
   function __() { this.constructor = d; }
   __.prototype = b.prototype;
   d.prototype = new __();
};
var ZClassType = (function(_super) {
   __extends(ZClassType, _super);
   function ZClassType(){
      _super.call(this);
   }
   return ZClassType;
})(ZType);

var ZFunc = (function() {
   function ZFunc(){
      this.FuncFlag = 0;
   }
   return ZFunc;
})();

var ZFunc_NativeNameConnector_Z11 = "__";
var ZFunc_ConverterFunc_Z12 = 1 << 16;
var ZFunc_CoercionFunc_Z13 = (1 << 17) | (1 << 16);
var ZFuncType = (function(_super) {
   __extends(ZFuncType, _super);
   function ZFuncType(){
      _super.call(this);
      this.HasUnknownType = false;
      this.HasGreekType = false;
   }
   return ZFuncType;
})(ZType);

var ZFuncType_FuncType_Z14 = ZFuncType__3qe0(new ZFuncType(), "Func", null);
var ZGenericType = (function(_super) {
   __extends(ZGenericType, _super);
   function ZGenericType(){
      _super.call(this);
   }
   return ZGenericType;
})(ZType);

var ZGenericType_ArrayType_Z15 = ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null));
var ZGenericType_MapType_Z16 = ZGenericType__5qev(new ZGenericType(), 1 << 16, "Map", null, ZType__4qwg(new ZType(), 1 << 16, "var", null));
var ZGreekType = (function(_super) {
   __extends(ZGreekType, _super);
   function ZGreekType(){
      _super.call(this);
      this.GreekId = 0;
   }
   return ZGreekType;
})(ZType);

var ZPrototype = (function(_super) {
   __extends(ZPrototype, _super);
   function ZPrototype(){
      _super.call(this);
      this.DefinedCount = 0;
      this.UsedCount = 0;
   }
   return ZPrototype;
})(ZFunc);

var ZTypePool = (function() {
   function ZTypePool(){
   }
   return ZTypePool;
})();

var ZTypePool_TypeList_Z17 = [];
var ZTypePool_ClassNameMap_Z18 = {};
var ZTypePool_UniqueTypeSetMap_Z19 = {};
var ZVarScope = (function() {
   function ZVarScope(){
      this.VarNodeCount = 0;
      this.UnresolvedSymbolCount = 0;
   }
   return ZVarScope;
})();

var ZVarType = (function(_super) {
   __extends(ZVarType, _super);
   function ZVarType(){
      _super.call(this);
      this.GreekId = 0;
   }
   return ZVarType;
})(ZType);

var ZNode = (function() {
   function ZNode(){
      this.Type = ZType__4qwg(new ZType(), 1 << 16, "var", null);
      this.HasUntypedNode = true;
   }
   return ZNode;
})();

var ZNode_Nop_Z20 = -1;
var ZNode_NameInfo_Z21 = -2;
var ZNode_TypeInfo_Z22 = -3;
var ZNode_AppendIndex_Z23 = -4;
var ZNode_NestedAppendIndex_Z24 = -5;
var ZParamNode = (function(_super) {
   __extends(ZParamNode, _super);
   function ZParamNode(){
      _super.call(this);
      this.ParamIndex = 0;
   }
   return ZParamNode;
})(ZNode);

var ZReturnNode = (function(_super) {
   __extends(ZReturnNode, _super);
   function ZReturnNode(){
      _super.call(this);
   }
   return ZReturnNode;
})(ZNode);

var ZReturnNode_Expr_Z25 = 0;
var ZSetIndexNode = (function(_super) {
   __extends(ZSetIndexNode, _super);
   function ZSetIndexNode(){
      _super.call(this);
   }
   return ZSetIndexNode;
})(ZNode);

var ZSetIndexNode_Recv_Z26 = 0;
var ZSetIndexNode_Index_Z27 = 1;
var ZSetIndexNode_Expr_Z28 = 2;
var ZSetNameNode = (function(_super) {
   __extends(ZSetNameNode, _super);
   function ZSetNameNode(){
      _super.call(this);
      this.VarIndex = 0;
      this.IsCaptured = false;
   }
   return ZSetNameNode;
})(ZNode);

var ZSetNameNode_Expr_Z29 = 0;
var ZSetterNode = (function(_super) {
   __extends(ZSetterNode, _super);
   function ZSetterNode(){
      _super.call(this);
   }
   return ZSetterNode;
})(ZNode);

var ZSetterNode_Recv_Z30 = 0;
var ZSetterNode_Expr_Z31 = 1;
var ZSugarNode = (function(_super) {
   __extends(ZSugarNode, _super);
   function ZSugarNode(){
      _super.call(this);
   }
   return ZSugarNode;
})(ZNode);

var ZSugarNode_DeSugar_Z32 = 0;
var ZThrowNode = (function(_super) {
   __extends(ZThrowNode, _super);
   function ZThrowNode(){
      _super.call(this);
   }
   return ZThrowNode;
})(ZNode);

var ZThrowNode_Expr_Z33 = 0;
var ZTryNode = (function(_super) {
   __extends(ZTryNode, _super);
   function ZTryNode(){
      _super.call(this);
   }
   return ZTryNode;
})(ZNode);

var ZTryNode_Try_Z34 = 0;
var ZTryNode_Catch_Z35 = 1;
var ZTryNode_Finally_Z36 = 2;
var ZUnaryNode = (function(_super) {
   __extends(ZUnaryNode, _super);
   function ZUnaryNode(){
      _super.call(this);
   }
   return ZUnaryNode;
})(ZNode);

var ZUnaryNode_Recv_Z37 = 0;
var ZWhileNode = (function(_super) {
   __extends(ZWhileNode, _super);
   function ZWhileNode(){
      _super.call(this);
   }
   return ZWhileNode;
})(ZNode);

var ZWhileNode_Cond_Z38 = 0;
var ZWhileNode_Block_Z39 = 1;
var ZEmptyValue = (function() {
   function ZEmptyValue(){
   }
   return ZEmptyValue;
})();

var ZEmptyValue_TrueEmpty_Z40 = new ZEmptyValue();
var ZEmptyValue_FalseEmpty_Z41 = new ZEmptyValue();
var ZLogger = (function() {
   function ZLogger(){
      this.ReportedErrorList = [];
   }
   return ZLogger;
})();

var ZMacroFunc = (function(_super) {
   __extends(ZMacroFunc, _super);
   function ZMacroFunc(){
      _super.call(this);
   }
   return ZMacroFunc;
})(ZFunc);

var ZNameSpace = (function() {
   function ZNameSpace(){
      this.SerialId = 0;
   }
   return ZNameSpace;
})();

var ZParserConst = (function() {
   function ZParserConst(){
   }
   return ZParserConst;
})();

var ProgName_Z42 = "LibZen";
var CodeName_Z43 = "Reference Implementation of D-Script";
var MajorVersion_Z44 = 0;
var MinerVersion_Z45 = 1;
var PatchLevel_Z46 = 0;
var Version_Z47 = "0.1";
var Copyright_Z48 = "Copyright (c) 2013-2014, Konoha project authors";
var License_Z49 = "BSD-Style Open Source";
var ZSource = (function() {
   function ZSource(){
      this.LineNumber = 0;
   }
   return ZSource;
})();

var ZSourceBuilder = (function() {
   function ZSourceBuilder(){
      this.SourceList = [];
      this.IndentLevel = 0;
      this.CurrentIndentString = "";
      this.BufferedLineComment = "";
   }
   return ZSourceBuilder;
})();

var ZSourceContext = (function(_super) {
   __extends(ZSourceContext, _super);
   function ZSourceContext(){
      _super.call(this);
      this.SourcePosition = 0;
   }
   return ZSourceContext;
})(ZSource);

var ZSourceMacro = (function(_super) {
   __extends(ZSourceMacro, _super);
   function ZSourceMacro(){
      _super.call(this);
   }
   return ZSourceMacro;
})(ZMacroFunc);

var ZSymbolEntry = (function() {
   function ZSymbolEntry(){
      this.IsDisabled = false;
   }
   return ZSymbolEntry;
})();

var ZSyntax = (function() {
   function ZSyntax(){
      this.SyntaxFlag = 0;
      this.IsDisabled = false;
      this.IsStatement = false;
   }
   return ZSyntax;
})();

var ZSyntax_BinaryOperator_Z50 = 1;
var ZSyntax_LeftJoin_Z51 = 1 << 1;
var ZToken = (function() {
   function ZToken(){
      this.StartIndex = 0;
      this.EndIndex = 0;
   }
   return ZToken;
})();

var ZToken_NullToken_Z52 = ZToken__4qw3(new ZToken(), null, 0, 0);
var ZTokenContext = (function() {
   function ZTokenContext(){
      this.TokenList = [];
      this.CurrentPosition = 0;
      this.IsAllowSkipIndent = false;
   }
   return ZTokenContext;
})();

var ZTokenContext_Required_Z53 = true;
var ZTokenContext_Optional_Z54 = false;
var ZTokenContext_AllowSkipIndent_Z55 = true;
var ZTokenContext_NotAllowSkipIndent_Z56 = false;
var ZTokenContext_AllowNewLine_Z57 = true;
var ZTokenContext_MoveNext_Z58 = true;
var ZTokenFunc = (function() {
   function ZTokenFunc(){
   }
   return ZTokenFunc;
})();

var ZVariable = (function(_super) {
   __extends(ZVariable, _super);
   function ZVariable(){
      _super.call(this);
      this.VarFlag = 0;
      this.VarUniqueIndex = 0;
      this.DefCount = 0;
      this.UsedCount = 0;
   }
   return ZVariable;
})(ZSymbolEntry);

var ZVisitor = (function() {
   function ZVisitor(){
   }
   return ZVisitor;
})();

var ZArrayType = (function(_super) {
   __extends(ZArrayType, _super);
   function ZArrayType(){
      _super.call(this);
   }
   return ZArrayType;
})(ZGenericType);

var ZAnnotationNode = (function(_super) {
   __extends(ZAnnotationNode, _super);
   function ZAnnotationNode(){
      _super.call(this);
   }
   return ZAnnotationNode;
})(ZNode);

var ZAssertNode = (function(_super) {
   __extends(ZAssertNode, _super);
   function ZAssertNode(){
      _super.call(this);
   }
   return ZAssertNode;
})(ZNode);

var ZAssertNode_Expr_Z59 = 0;
var ZBinaryNode = (function(_super) {
   __extends(ZBinaryNode, _super);
   function ZBinaryNode(){
      _super.call(this);
   }
   return ZBinaryNode;
})(ZNode);

var ZBinaryNode_Left_Z60 = 0;
var ZBinaryNode_Right_Z61 = 1;
var ZBreakNode = (function(_super) {
   __extends(ZBreakNode, _super);
   function ZBreakNode(){
      _super.call(this);
   }
   return ZBreakNode;
})(ZNode);

var ZCastNode = (function(_super) {
   __extends(ZCastNode, _super);
   function ZCastNode(){
      _super.call(this);
   }
   return ZCastNode;
})(ZNode);

var ZCastNode_Expr_Z62 = 0;
var ZCatchNode = (function(_super) {
   __extends(ZCatchNode, _super);
   function ZCatchNode(){
      _super.call(this);
      this.ExceptionType = ZType__4qwg(new ZType(), 1 << 16, "var", null);
   }
   return ZCatchNode;
})(ZNode);

var ZCatchNode_Block_Z63 = 0;
var ZComparatorNode = (function(_super) {
   __extends(ZComparatorNode, _super);
   function ZComparatorNode(){
      _super.call(this);
   }
   return ZComparatorNode;
})(ZBinaryNode);

var ZConstNode = (function(_super) {
   __extends(ZConstNode, _super);
   function ZConstNode(){
      _super.call(this);
   }
   return ZConstNode;
})(ZNode);

var ZEmptyNode = (function(_super) {
   __extends(ZEmptyNode, _super);
   function ZEmptyNode(){
      _super.call(this);
   }
   return ZEmptyNode;
})(ZNode);

var ZErrorNode = (function(_super) {
   __extends(ZErrorNode, _super);
   function ZErrorNode(){
      _super.call(this);
   }
   return ZErrorNode;
})(ZConstNode);

var ZFieldNode = (function(_super) {
   __extends(ZFieldNode, _super);
   function ZFieldNode(){
      _super.call(this);
      this.DeclType = ZType__4qwg(new ZType(), 1 << 16, "var", null);
   }
   return ZFieldNode;
})(ZNode);

var ZFieldNode_InitValue_Z64 = 0;
var ZFloatNode = (function(_super) {
   __extends(ZFloatNode, _super);
   function ZFloatNode(){
      _super.call(this);
      this.FloatValue = 0.0;
   }
   return ZFloatNode;
})(ZConstNode);

var ZGetIndexNode = (function(_super) {
   __extends(ZGetIndexNode, _super);
   function ZGetIndexNode(){
      _super.call(this);
   }
   return ZGetIndexNode;
})(ZNode);

var ZGetIndexNode_Recv_Z65 = 0;
var ZGetIndexNode_Index_Z66 = 1;
var ZGetNameNode = (function(_super) {
   __extends(ZGetNameNode, _super);
   function ZGetNameNode(){
      _super.call(this);
      this.IsCaptured = false;
      this.VarIndex = 0;
   }
   return ZGetNameNode;
})(ZNode);

var ZGetterNode = (function(_super) {
   __extends(ZGetterNode, _super);
   function ZGetterNode(){
      _super.call(this);
   }
   return ZGetterNode;
})(ZNode);

var ZGetterNode_Recv_Z67 = 0;
var ZGlobalNameNode = (function(_super) {
   __extends(ZGlobalNameNode, _super);
   function ZGlobalNameNode(){
      _super.call(this);
      this.IsStaticFuncName = false;
   }
   return ZGlobalNameNode;
})(ZNode);

var ZGroupNode = (function(_super) {
   __extends(ZGroupNode, _super);
   function ZGroupNode(){
      _super.call(this);
   }
   return ZGroupNode;
})(ZNode);

var ZGroupNode_Expr_Z68 = 0;
var ZIfNode = (function(_super) {
   __extends(ZIfNode, _super);
   function ZIfNode(){
      _super.call(this);
   }
   return ZIfNode;
})(ZNode);

var ZIfNode_Cond_Z69 = 0;
var ZIfNode_Then_Z70 = 1;
var ZIfNode_Else_Z71 = 2;
var ZImportNode = (function(_super) {
   __extends(ZImportNode, _super);
   function ZImportNode(){
      _super.call(this);
   }
   return ZImportNode;
})(ZNode);

var ZInstanceOfNode = (function(_super) {
   __extends(ZInstanceOfNode, _super);
   function ZInstanceOfNode(){
      _super.call(this);
   }
   return ZInstanceOfNode;
})(ZNode);

var ZInstanceOfNode_Left_Z72 = 0;
var ZIntNode = (function(_super) {
   __extends(ZIntNode, _super);
   function ZIntNode(){
      _super.call(this);
      this.IntValue = 0;
   }
   return ZIntNode;
})(ZConstNode);

var ZLetNode = (function(_super) {
   __extends(ZLetNode, _super);
   function ZLetNode(){
      _super.call(this);
      this.SymbolType = ZType__4qwg(new ZType(), 1 << 16, "var", null);
   }
   return ZLetNode;
})(ZNode);

var ZLetNode_InitValue_Z73 = 0;
var ZListNode = (function(_super) {
   __extends(ZListNode, _super);
   function ZListNode(){
      _super.call(this);
      this.ListStartIndex = 0;
   }
   return ZListNode;
})(ZNode);

var ZMacroNode = (function(_super) {
   __extends(ZMacroNode, _super);
   function ZMacroNode(){
      _super.call(this);
   }
   return ZMacroNode;
})(ZListNode);

var ZMapEntryNode = (function(_super) {
   __extends(ZMapEntryNode, _super);
   function ZMapEntryNode(){
      _super.call(this);
   }
   return ZMapEntryNode;
})(ZNode);

var ZMapEntryNode_Key_Z74 = 0;
var ZMapEntryNode_Value_Z75 = 1;
var ZMapLiteralNode = (function(_super) {
   __extends(ZMapLiteralNode, _super);
   function ZMapLiteralNode(){
      _super.call(this);
   }
   return ZMapLiteralNode;
})(ZListNode);

var ZMethodCallNode = (function(_super) {
   __extends(ZMethodCallNode, _super);
   function ZMethodCallNode(){
      _super.call(this);
   }
   return ZMethodCallNode;
})(ZListNode);

var ZMethodCallNode_Recv_Z76 = 0;
var ZNewArrayNode = (function(_super) {
   __extends(ZNewArrayNode, _super);
   function ZNewArrayNode(){
      _super.call(this);
   }
   return ZNewArrayNode;
})(ZListNode);

var ZNewObjectNode = (function(_super) {
   __extends(ZNewObjectNode, _super);
   function ZNewObjectNode(){
      _super.call(this);
   }
   return ZNewObjectNode;
})(ZListNode);

var ZNotNode = (function(_super) {
   __extends(ZNotNode, _super);
   function ZNotNode(){
      _super.call(this);
   }
   return ZNotNode;
})(ZUnaryNode);

var ZNullNode = (function(_super) {
   __extends(ZNullNode, _super);
   function ZNullNode(){
      _super.call(this);
   }
   return ZNullNode;
})(ZConstNode);

var ZOrNode = (function(_super) {
   __extends(ZOrNode, _super);
   function ZOrNode(){
      _super.call(this);
   }
   return ZOrNode;
})(ZBinaryNode);

var ZPrototypeNode = (function(_super) {
   __extends(ZPrototypeNode, _super);
   function ZPrototypeNode(){
      _super.call(this);
      this.ReturnType = ZType__4qwg(new ZType(), 1 << 16, "var", null);
   }
   return ZPrototypeNode;
})(ZListNode);

var ZStringNode = (function(_super) {
   __extends(ZStringNode, _super);
   function ZStringNode(){
      _super.call(this);
   }
   return ZStringNode;
})(ZConstNode);

var ZStupidCastErrorNode = (function(_super) {
   __extends(ZStupidCastErrorNode, _super);
   function ZStupidCastErrorNode(){
      _super.call(this);
   }
   return ZStupidCastErrorNode;
})(ZErrorNode);

var ZTypeNode = (function(_super) {
   __extends(ZTypeNode, _super);
   function ZTypeNode(){
      _super.call(this);
   }
   return ZTypeNode;
})(ZConstNode);

var ZGenerator = (function(_super) {
   __extends(ZGenerator, _super);
   function ZGenerator(){
      _super.call(this);
      this.UniqueNumber = 0;
      this.DefinedFuncMap = {};
      this.StoppedVisitor = false;
   }
   return ZGenerator;
})(ZVisitor);

var ZIndentToken = (function(_super) {
   __extends(ZIndentToken, _super);
   function ZIndentToken(){
      _super.call(this);
   }
   return ZIndentToken;
})(ZToken);

var ZPatternToken = (function(_super) {
   __extends(ZPatternToken, _super);
   function ZPatternToken(){
      _super.call(this);
   }
   return ZPatternToken;
})(ZToken);

var ZSourceEngine = (function(_super) {
   __extends(ZSourceEngine, _super);
   function ZSourceEngine(){
      _super.call(this);
      this.InteractiveContext = false;
      this.IsVisitableFlag = true;
   }
   return ZSourceEngine;
})(ZVisitor);

var ZSourceGenerator = (function(_super) {
   __extends(ZSourceGenerator, _super);
   function ZSourceGenerator(){
      _super.call(this);
      this.NativeTypeMap = {};
      this.ReservedNameMap = {};
      this.BuilderList = [];
   }
   return ZSourceGenerator;
})(ZGenerator);

var ZTypeChecker = (function(_super) {
   __extends(ZTypeChecker, _super);
   function ZTypeChecker(){
      _super.call(this);
      this.StoppedVisitor = false;
   }
   return ZTypeChecker;
})(ZVisitor);

var ZTypeChecker_DefaultTypeCheckPolicy_Z77 = 0;
var ZTypeChecker_NoCheckPolicy_Z78 = 1;
var ZenTypeSafer = (function(_super) {
   __extends(ZenTypeSafer, _super);
   function ZenTypeSafer(){
      _super.call(this);
   }
   return ZenTypeSafer;
})(ZTypeChecker);

var ZAndNode = (function(_super) {
   __extends(ZAndNode, _super);
   function ZAndNode(){
      _super.call(this);
   }
   return ZAndNode;
})(ZBinaryNode);

var ZArrayLiteralNode = (function(_super) {
   __extends(ZArrayLiteralNode, _super);
   function ZArrayLiteralNode(){
      _super.call(this);
   }
   return ZArrayLiteralNode;
})(ZListNode);

var ZBlockNode = (function(_super) {
   __extends(ZBlockNode, _super);
   function ZBlockNode(){
      _super.call(this);
   }
   return ZBlockNode;
})(ZListNode);

var ZBooleanNode = (function(_super) {
   __extends(ZBooleanNode, _super);
   function ZBooleanNode(){
      _super.call(this);
      this.BooleanValue = false;
   }
   return ZBooleanNode;
})(ZConstNode);

var ZClassNode = (function(_super) {
   __extends(ZClassNode, _super);
   function ZClassNode(){
      _super.call(this);
   }
   return ZClassNode;
})(ZListNode);

var ZFuncCallNode = (function(_super) {
   __extends(ZFuncCallNode, _super);
   function ZFuncCallNode(){
      _super.call(this);
   }
   return ZFuncCallNode;
})(ZListNode);

var ZFuncCallNode_Func_Z79 = 0;
var ZFunctionNode = (function(_super) {
   __extends(ZFunctionNode, _super);
   function ZFunctionNode(){
      _super.call(this);
      this.ReturnType = ZType__4qwg(new ZType(), 1 << 16, "var", null);
      this.VarIndex = 0;
   }
   return ZFunctionNode;
})(ZListNode);

var ZFunctionNode_Block_Z80 = 0;
var ZVarNode = (function(_super) {
   __extends(ZVarNode, _super);
   function ZVarNode(){
      _super.call(this);
      this.DeclType = ZType__4qwg(new ZType(), 1 << 16, "var", null);
      this.VarIndex = 0;
   }
   return ZVarNode;
})(ZBlockNode);

var ZVarNode_InitValue_Z81 = 0;
function ZType__4qwg(self, TypeFlag, ShortName, RefType) {
   self.TypeFlag = TypeFlag;
   self.ShortName = ShortName;
   self.RefType = RefType;
   if (LibZen.IsFlag(TypeFlag, 1 << 16)) {
      self.TypeId = ZTypePool_NewTypeId__1qwg(self);
   };
   return self;
};

function GetRealType__1qwg(self) {
   return self;
};
function ZType_GetRealType(self){ return GetRealType__1qwg(self); }

function GetSuperType__1qwg(self) {
   return self.RefType;
};
function ZType_GetSuperType(self){ return GetSuperType__1qwg(self); }

function GetBaseType__1qwg(self) {
   return self;
};
function ZType_GetBaseType(self){ return GetBaseType__1qwg(self); }

function GetParamSize__1qwg(self) {
   return 0;
};
function ZType_GetParamSize(self){ return GetParamSize__1qwg(self); }

function GetParamType__2qwg(self, Index) {
   return ZType__4qwg(new ZType(), 1 << 16, "var", null);
};
function ZType_GetParamType(self, Index){ return GetParamType__2qwg(self, Index); }

function Equals__2qwg(self, Type) {
   return (self.GetRealType(self) == Type.GetRealType(Type));
};
function ZType_Equals(self, Type){ return Equals__2qwg(self, Type); }

function Accept__2qwg(self, Type) {
   var ThisType = self.GetRealType(self);
   if (ThisType == Type.GetRealType(Type)) {
      return true;
   };
   var SuperClass = Type.GetSuperType(Type);
   while (SuperClass != null) {
      if (SuperClass == ThisType) {
         return true;
      };
      SuperClass = SuperClass.GetSuperType(SuperClass);
   };
   return false;
};
function ZType_Accept(self, Type){ return Accept__2qwg(self, Type); }

function IsGreekType__1qwg(self) {
   return false;
};
function ZType_IsGreekType(self){ return IsGreekType__1qwg(self); }

function GetGreekRealType__2qwg(self, Greek) {
   return self.GetRealType(self);
};
function ZType_GetGreekRealType(self, Greek){ return GetGreekRealType__2qwg(self, Greek); }

function AcceptValueType__4qwg(self, ValueType, ExactMatch, Greek) {
   if (self.GetRealType(self) != ValueType && !ValueType.IsVarType(ValueType)) {
      if (ExactMatch && !Accept__2qwg(self, ValueType)) {
         return false;
      };
   };
   return true;
};
function ZType_AcceptValueType(self, ValueType, ExactMatch, Greek){ return AcceptValueType__4qwg(self, ValueType, ExactMatch, Greek); }

function IsVoidType__1qwg(self) {
   return (self.GetRealType(self) == ZType__4qwg(new ZType(), 1 << 16, "void", null));
};
function ZType_IsVoidType(self){ return IsVoidType__1qwg(self); }

function IsVarType__1qwg(self) {
   return (self.GetRealType(self) == ZType__4qwg(new ZType(), 1 << 16, "var", null));
};
function ZType_IsVarType(self){ return IsVarType__1qwg(self); }

function IsInferrableType__1qwg(self) {
   return (!self.IsVarType(self) && !IsVoidType__1qwg(self));
};
function ZType_IsInferrableType(self){ return IsInferrableType__1qwg(self); }

function IsTypeType__1qwg(self) {
   return (self.GetRealType(self) == ZType__4qwg(new ZType(), 1 << 16, "Type", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
};
function ZType_IsTypeType(self){ return IsTypeType__1qwg(self); }

function IsBooleanType__1qwg(self) {
   return (self.GetRealType(self) == ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
};
function ZType_IsBooleanType(self){ return IsBooleanType__1qwg(self); }

function IsIntType__1qwg(self) {
   return (self.GetRealType(self) == ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
};
function ZType_IsIntType(self){ return IsIntType__1qwg(self); }

function IsFloatType__1qwg(self) {
   return (self.GetRealType(self) == ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
};
function ZType_IsFloatType(self){ return IsFloatType__1qwg(self); }

function IsNumberType__1qwg(self) {
   return (IsIntType__1qwg(self) || IsFloatType__1qwg(self));
};
function ZType_IsNumberType(self){ return IsNumberType__1qwg(self); }

function IsStringType__1qwg(self) {
   return (self.GetRealType(self) == ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
};
function ZType_IsStringType(self){ return IsStringType__1qwg(self); }

function IsArrayType__1qwg(self) {
   return (self.GetBaseType(self) == ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)));
};
function ZType_IsArrayType(self){ return IsArrayType__1qwg(self); }

function IsMapType__1qwg(self) {
   return (self.GetBaseType(self) == ZGenericType__5qev(new ZGenericType(), 1 << 16, "Map", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)));
};
function ZType_IsMapType(self){ return IsMapType__1qwg(self); }

function IsOpenType__1qwg(self) {
   return LibZen.IsFlag(self.TypeFlag, 1 << 9);
};
function ZType_IsOpenType(self){ return IsOpenType__1qwg(self); }

function IsImmutableType__1qwg(self) {
   return false;
};
function ZType_IsImmutableType(self){ return IsImmutableType__1qwg(self); }

function IsNullableType__1qwg(self) {
   return true;
};
function ZType_IsNullableType(self){ return IsNullableType__1qwg(self); }

function toString__1qwg(self) {
   return self.ShortName;
};
function ZType_toString(self){ return toString__1qwg(self); }

function GetAsciiName__1qwg(self) {
   return self.ShortName;
};
function ZType_GetAsciiName(self){ return GetAsciiName__1qwg(self); }

function StringfyClassMember__2qwg(self, Name) {
   return (Name + " of ") + self.ShortName;
};
function ZType_StringfyClassMember(self, Name){ return StringfyClassMember__2qwg(self, Name); }

function GetUniqueName__1qwg(self) {
   return LibZen.Stringfy(self.TypeId);
};
function ZType_GetUniqueName(self){ return GetUniqueName__1qwg(self); }

function IsFuncType__1qwg(self) {
   return ((self.GetRealType(self)).constructor.name == (ZFuncType).name);
};
function ZType_IsFuncType(self){ return IsFuncType__1qwg(self); }

function StringfySignature__2qwg(self, FuncName) {
   return FuncName;
};
function ZType_StringfySignature(self, FuncName){ return StringfySignature__2qwg(self, FuncName); }

function Maybe__3qwg(self, T, SourceToken) {
   return;
};
function ZType_Maybe(self, T, SourceToken){ return Maybe__3qwg(self, T, SourceToken); }

function ZClassField__5qw8(self, ClassType, FieldName, FieldType, SourceToken) {
   self.ClassType = ClassType;
   self.FieldType = FieldType;
   self.FieldName = FieldName;
   self.SourceToken = SourceToken;
   return self;
};

function ZClassType__3qeq(self, ShortName, RefType) {
   ZType__4qwg(self, (1 << 9) | (1 << 16), ShortName, RefType);
   if ((RefType).constructor.name == (ZClassType).name) {
      ResetSuperType__2qeq(self, RefType);
   };
   return self;
};

function ResetSuperType__2qeq(self, SuperClass) {
   self.RefType = SuperClass;
   if (SuperClass.FieldList != null) {
      self.FieldList = [];
      var i = 0;
      while (i < (SuperClass.FieldList).length) {
         var Field = SuperClass.FieldList[i];
         self.FieldList.push(Field);
         i = i + 1;
      };
   };
   return;
};
function ZClassType_ResetSuperType(self, SuperClass){ return ResetSuperType__2qeq(self, SuperClass); }

function GetFieldSize__1qeq(self) {
   if (self.FieldList != null) {
      return (self.FieldList).length;
   };
   return 0;
};
function ZClassType_GetFieldSize(self){ return GetFieldSize__1qeq(self); }

function GetFieldAt__2qeq(self, Index) {
   return self.FieldList[Index];
};
function ZClassType_GetFieldAt(self, Index){ return GetFieldAt__2qeq(self, Index); }

function HasField__2qeq(self, FieldName) {
   if (self.FieldList != null) {
      var i = 0;
      while (i < (self.FieldList).length) {
         if (String_equals(self.FieldList[i].FieldName)) {
            return true;
         };
         i = i + 1;
      };
   };
   return false;
};
function ZClassType_HasField(self, FieldName){ return HasField__2qeq(self, FieldName); }

function GetFieldType__3qeq(self, FieldName, DefaultType) {
   if (self.FieldList != null) {
      var i = 0;
      while (i < (self.FieldList).length) {
         var Field = self.FieldList[i];
         if (String_equals(Field.FieldName)) {
            return Field.FieldType;
         };
         i = i + 1;
      };
   };
   return DefaultType;
};
function ZClassType_GetFieldType(self, FieldName, DefaultType){ return GetFieldType__3qeq(self, FieldName, DefaultType); }

function AppendField__4qeq(self, FieldType, FieldName, SourceToken) {
   console.assert(!FieldType.IsVarType(FieldType), "(libzen/libzen.zen:1442)");
   if (self.FieldList == null) {
      self.FieldList = [];
   };
   var ClassField = ZClassField__5qw8(new ZClassField(), self, FieldName, FieldType, SourceToken);
   self.FieldList.push(ClassField);
   return ClassField;
};
function ZClassType_AppendField(self, FieldType, FieldName, SourceToken){ return AppendField__4qeq(self, FieldType, FieldName, SourceToken); }

function ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, RecvType) {
   return ((FuncName + "__") + (FuncParamSize).toString()) + GetUniqueName__1qwg(RecvType);
};

function ZFunc__4qep(self, FuncFlag, FuncName, FuncType) {
   self.FuncFlag = FuncFlag;
   self.FuncName = FuncName;
   self.FuncType = FuncType;
   return self;
};

function GetFuncType__1qep(self) {
   return self.FuncType;
};
function ZFunc_GetFuncType(self){ return GetFuncType__1qep(self); }

function toString__1qep(self) {
   return (self.FuncName + ": ") + toString__1qwg(self.FuncType);
};
function ZFunc_toString(self){ return toString__1qep(self); }

function IsConverterFunc__1qep(self) {
   return LibZen.IsFlag(self.FuncFlag, 1 << 16);
};
function ZFunc_IsConverterFunc(self){ return IsConverterFunc__1qep(self); }

function IsCoercionFunc__1qep(self) {
   return LibZen.IsFlag(self.FuncFlag, (1 << 17) | 1 << 16);
};
function ZFunc_IsCoercionFunc(self){ return IsCoercionFunc__1qep(self); }

function Is__2qep(self, Flag) {
   return LibZen.IsFlag(self.FuncFlag, Flag);
};
function ZFunc_Is(self, Flag){ return Is__2qep(self, Flag); }

function GetSignature__1qep(self) {
   return StringfySignature__2qe0(self.FuncType, self.FuncName);
};
function ZFunc_GetSignature(self){ return GetSignature__1qep(self); }

function ZFuncType__3qe0(self, ShortName, UniqueTypeParams) {
   ZType__4qwg(self, 1 << 16, ShortName, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   if (UniqueTypeParams == null) {
      self.TypeParams = LibZen.NewTypeArray(1);
      self.TypeParams[0] = ZType__4qwg(new ZType(), 1 << 16, "var", null);
   } else {
      self.TypeParams = UniqueTypeParams;
   };
   var i = 0;
   while (i < (self.TypeParams).length) {
      if (self.TypeParams[i].IsVarType(self.TypeParams[i])) {
         self.HasUnknownType = true;
      };
      if (self.TypeParams[i].IsGreekType(self.TypeParams[i])) {
         self.HasGreekType = true;
      };
      i = i + 1;
   };
   return self;
};

function IsFuncType__1qe0(self) {
   return true;
};
function ZFuncType_IsFuncType(self){ return IsFuncType__1qe0(self); }

function IsVarType__1qe0(self) {
   return self.HasUnknownType;
};
function ZFuncType_IsVarType(self){ return IsVarType__1qe0(self); }

function IsGreekType__1qe0(self) {
   return self.HasGreekType;
};
function ZFuncType_IsGreekType(self){ return IsGreekType__1qe0(self); }

function GetGreekRealType__2qe0(self, Greek) {
   if (self.HasGreekType) {
      var TypeList = [];
      var i = 0;
      while (i < (self.TypeParams).length) {
         TypeList.push(ZType_null(self.TypeParams[i], Greek));
         i = i + 1;
      };
      return ZFuncType_ZTypePool_LookupFuncType(TypeList);
   };
   return self;
};
function ZFuncType_GetGreekRealType(self, Greek){ return GetGreekRealType__2qe0(self, Greek); }

function AcceptValueType__4qe0(self, ValueType, ExactMatch, Greek) {
   if (IsFuncType__1qwg(ValueType) && ValueType.GetParamSize(ValueType) == self.GetParamSize(self)) {
      var i = 0;
      while (i < (self.TypeParams).length) {
         if (!self.TypeParams[i].AcceptValueType(self.TypeParams[i], ValueType.GetParamType(ValueType, i), true, Greek)) {
            return false;
         };
         i = i + 1;
      };
      return true;
   };
   return false;
};
function ZFuncType_AcceptValueType(self, ValueType, ExactMatch, Greek){ return AcceptValueType__4qe0(self, ValueType, ExactMatch, Greek); }

function StringfySignature__2qe0(self, FuncName) {
   return ZFunc_StringfySignature__3qqy(FuncName, GetFuncParamSize__1qe0(self), ZType_GetRecvType(self));
};
function ZFuncType_StringfySignature(self, FuncName){ return StringfySignature__2qe0(self, FuncName); }

function GetBaseType__1qe0(self) {
   return ZFuncType__3qe0(new ZFuncType(), "Func", null);
};
function ZFuncType_GetBaseType(self){ return GetBaseType__1qe0(self); }

function GetParamSize__1qe0(self) {
   return (self.TypeParams).length;
};
function ZFuncType_GetParamSize(self){ return GetParamSize__1qe0(self); }

function GetParamType__2qe0(self, Index) {
   return self.TypeParams[Index];
};
function ZFuncType_GetParamType(self, Index){ return GetParamType__2qe0(self, Index); }

function GetReturnType__1qe0(self) {
   return self.TypeParams[0];
};
function ZFuncType_GetReturnType(self){ return GetReturnType__1qe0(self); }

function GetFuncParamSize__1qe0(self) {
   return (self.TypeParams).length - 1;
};
function ZFuncType_GetFuncParamSize(self){ return GetFuncParamSize__1qe0(self); }

function GetRecvType__1qe0(self) {
   if ((self.TypeParams).length == 1) {
      return ZType__4qwg(new ZType(), 1 << 16, "void", null);
   };
   return self.TypeParams[1];
};
function ZFuncType_GetRecvType(self){ return GetRecvType__1qe0(self); }

function GetFuncParamType__2qe0(self, Index) {
   return self.TypeParams[Index + 1];
};
function ZFuncType_GetFuncParamType(self, Index){ return GetFuncParamType__2qe0(self, Index); }

function NewMethodFuncType__2qe0(self, RecvType) {
   var TypeList = [];
   TypeList.push(ZType_GetReturnType(self));
   TypeList.push(RecvType);
   var i = 0;
   while (i < GetFuncParamSize__1qe0(self)) {
      TypeList.push(ZType_GetFuncParamType(self, i));
      i = i + 1;
   };
   return ZFuncType_ZTypePool_LookupFuncType(TypeList);
};
function ZFuncType_NewMethodFuncType(self, RecvType){ return NewMethodFuncType__2qe0(self, RecvType); }

function AcceptAsFieldFunc__2qe0(self, FuncType) {
   if (GetFuncParamSize__1qe0(FuncType) == GetFuncParamSize__1qe0(self) && Equals__2qwg(ZType_GetReturnType(FuncType), ZType_GetReturnType(self))) {
      var i = 1;
      while (i < GetFuncParamSize__1qe0(FuncType)) {
         if (!Equals__2qwg(ZType_GetFuncParamType(FuncType, i), ZType_GetFuncParamType(self, i))) {
            return false;
         };
         i = i + 1;
      };
   };
   return true;
};
function ZFuncType_AcceptAsFieldFunc(self, FuncType){ return AcceptAsFieldFunc__2qe0(self, FuncType); }

function ZGenericType__5qev(self, TypeFlag, ShortName, BaseType, ParamType) {
   ZType__4qwg(self, TypeFlag, ShortName, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   self.BaseType = BaseType;
   if (self.BaseType == null) {
      self.BaseType = self;
   };
   self.ParamType = ParamType;
   return self;
};

function GetSuperType__1qev(self) {
   if (self.BaseType == self) {
      return self.RefType;
   };
   return self.BaseType;
};
function ZGenericType_GetSuperType(self){ return GetSuperType__1qev(self); }

function GetBaseType__1qev(self) {
   return self.BaseType;
};
function ZGenericType_GetBaseType(self){ return GetBaseType__1qev(self); }

function GetParamSize__1qev(self) {
   return 1;
};
function ZGenericType_GetParamSize(self){ return GetParamSize__1qev(self); }

function GetParamType__2qev(self, Index) {
   if (Index == 0) {
      return self.ParamType;
   };
   return null;
};
function ZGenericType_GetParamType(self, Index){ return GetParamType__2qev(self, Index); }

function IsGreekType__1qev(self) {
   return (self.ParamType.IsGreekType(self.ParamType));
};
function ZGenericType_IsGreekType(self){ return IsGreekType__1qev(self); }

function GetGreekRealType__2qev(self, Greek) {
   if (self.ParamType.IsGreekType(self.ParamType)) {
      return ZType_ZTypePool_GetGenericType1(self.BaseType, ZType_null(self.ParamType, Greek));
   };
   return ZType_null(self);
};
function ZGenericType_GetGreekRealType(self, Greek){ return GetGreekRealType__2qev(self, Greek); }

function AcceptValueType__4qev(self, ValueType, ExactMatch, Greek) {
   if (self.BaseType == ValueType.GetBaseType(ValueType) && ValueType.GetParamSize(ValueType) == 1) {
      return self.ParamType.AcceptValueType(self.ParamType, ValueType.GetParamType(ValueType, 0), true, Greek);
   };
   return false;
};
function ZGenericType_AcceptValueType(self, ValueType, ExactMatch, Greek){ return AcceptValueType__4qev(self, ValueType, ExactMatch, Greek); }

function ZGreekType_NewGreekTypes__1qwh(GreekTypes) {
   if (GreekTypes == null) {
      return LibZen.NewTypeArray((["__a", "__b", "__c"]).length);
   } else {
      var i = 0;
      while (i < (GreekTypes).length) {
         GreekTypes[i] = null;
         i = i + 1;
      };
      return GreekTypes;
   };
};

function ZGreekType__2qe8(self, GreekId) {
   ZType__4qwg(self, 1 << 16, ["__a", "__b", "__c"][GreekId], ZType__4qwg(new ZType(), 1 << 16, "var", null));
   self.GreekId = GreekId;
   return self;
};

function IsGreekType__1qe8(self) {
   return true;
};
function ZGreekType_IsGreekType(self){ return IsGreekType__1qe8(self); }

function GetGreekRealType__2qe8(self, Greek) {
   if (Greek[self.GreekId] == null) {
      return ZType__4qwg(new ZType(), 1 << 16, "var", null);
   };
   return Greek[self.GreekId];
};
function ZGreekType_GetGreekRealType(self, Greek){ return GetGreekRealType__2qe8(self, Greek); }

function AcceptValueType__4qe8(self, ValueType, ExactMatch, Greek) {
   if (Greek[self.GreekId] == null) {
      if (ValueType.IsVarType(ValueType)) {
         return true;
      };
      Greek[self.GreekId] = ValueType;
      return true;
   } else {
      return Greek[self.GreekId].AcceptValueType(Greek[self.GreekId], ValueType, ExactMatch, Greek);
   };
};
function ZGreekType_AcceptValueType(self, ValueType, ExactMatch, Greek){ return AcceptValueType__4qe8(self, ValueType, ExactMatch, Greek); }

function ZPrototype__5qry(self, FuncFlag, FuncName, FuncType, SourceToken) {
   ZFunc__4qep(self, FuncFlag, FuncName, FuncType);
   self.DefinedCount = 0;
   self.UsedCount = 0;
   return self;
};

function Used__1qry(self) {
   self.UsedCount = self.UsedCount + 1;
   return;
};
function ZPrototype_Used(self){ return Used__1qry(self); }

function Defined__1qry(self) {
   self.DefinedCount = self.DefinedCount + 1;
   return;
};
function ZPrototype_Defined(self){ return Defined__1qry(self); }

function ZTypePool_NewTypeId__1qwg(T) {
   var TypeId = ([]).length;
   [].push(T);
   return TypeId;
};
function ZType_ZTypePool_NewTypeId(T){ return ZTypePool_NewTypeId__1qwg(T); }

function TypeOf__1qqr(TypeId) {
   if (TypeId == 0) {
      return ZType__4qwg(new ZType(), 1 << 16, "var", null);
   };
   if (TypeId < ([]).length) {
      return [][TypeId];
   };
   return ZType__4qwg(new ZType(), 1 << 16, "var", null);
};

function ZTypePool_MangleType2__2qwg(Type1, Type2) {
   return ((":" + (Type1.TypeId).toString()) + ":") + (Type2.TypeId).toString();
};
function ZType_ZTypePool_MangleType2(Type1, Type2){ return ZTypePool_MangleType2__2qwg(Type1, Type2); }

function ZTypePool_MangleTypes__1qwh(TypeList) {
   var s = "";
   var i = 0;
   while (i < (TypeList).length) {
      var Type = TypeList[i];
      s = (s + ":") + (Type.TypeId).toString();
      i = i + 1;
   };
   return s;
};

function ZTypePool_UniqueTypes__1qwh(TypeList) {
   var MangleName = "[]" + ZTypePool_MangleTypes__1qwh(TypeList);
   var Types = {}[MangleName];
   if (Types == null) {
      Types = TypeList;
      {}[MangleName] = Types;
   };
   return Types;
};

function ZTypePool_GetGenericType1__2qwg(BaseType, ParamType) {
   var MangleName = ZTypePool_MangleType2__2qwg(BaseType, ParamType);
   var GenericType = {}[MangleName];
   if (GenericType == null) {
      var Name = ((BaseType.ShortName + "<") + toString__1qwg(ParamType)) + ">";
      if (IsArrayType__1qwg(BaseType)) {
         Name = ((BaseType.ShortName + "<") + toString__1qwg(ParamType)) + ">";
      };
      GenericType = ZGenericType__5qev(new ZGenericType(), 1 << 16, Name, BaseType, ParamType);
      {}[MangleName] = GenericType;
   };
   return GenericType;
};
function ZType_ZTypePool_GetGenericType1(BaseType, ParamType){ return ZTypePool_GetGenericType1__2qwg(BaseType, ParamType); }

function ZTypePool_GetGenericType__3qwg(BaseType, TypeList, IsCreation) {
   console.assert(BaseType.GetParamSize(BaseType) > 0, "(libzen/libzen.zen:1759)");
   if ((TypeList).length == 1 && !IsFuncType__1qwg(BaseType)) {
      return ZType_ZTypePool_GetGenericType1(BaseType, TypeList[0]);
   };
   var MangleName = (":" + (BaseType.TypeId).toString()) + ZTypePool_MangleTypes__1qwh(TypeList);
   var GenericType = {}[MangleName];
   if ((GenericType == null) && IsCreation) {
      var ShortName = BaseType.ShortName + "<";
      var i = 0;
      while (i < (TypeList).length) {
         ShortName = ShortName + ZType_null(TypeList[i]).ShortName;
         if ((i + 1) == (TypeList).length) {
            ShortName = ShortName + ">";
         } else {
            ShortName = ShortName + ",";
         };
         i = i + 1;
      };
      if (IsFuncType__1qwg(BaseType)) {
         GenericType = ZFuncType__3qe0(new ZFuncType(), ShortName, ZTypePool_UniqueTypes__1qwh(TypeList));
      } else {
      };
      {}[MangleName] = GenericType;
   };
   return GenericType;
};
function ZType_ZTypePool_GetGenericType(BaseType, TypeList, IsCreation){ return ZTypePool_GetGenericType__3qwg(BaseType, TypeList, IsCreation); }

function ZTypePool_LookupFuncType__1qwh(TypeList) {
   var FuncType = ZType_ZTypePool_GetGenericType(ZFuncType__3qe0(new ZFuncType(), "Func", null), TypeList, true);
   if ((FuncType).constructor.name == (ZFuncType).name) {
      return FuncType;
   };
   return null;
};

function ZTypePool_LookupFuncType__1qwg(R) {
   var TypeList = [];
   TypeList.push(R);
   return ZFuncType_ZTypePool_LookupFuncType(TypeList);
};
function ZType_ZTypePool_LookupFuncType(R){ return ZTypePool_LookupFuncType__1qwg(R); }

function ZTypePool_LookupFuncType__2qwg(R, P1) {
   var TypeList = [];
   TypeList.push(R);
   TypeList.push(P1);
   return ZFuncType_ZTypePool_LookupFuncType(TypeList);
};
function ZType_ZTypePool_LookupFuncType(R, P1){ return ZTypePool_LookupFuncType__2qwg(R, P1); }

function ZTypePool_LookupFuncType__3qwg(R, P1, P2) {
   var TypeList = [];
   TypeList.push(R);
   TypeList.push(P1);
   TypeList.push(P2);
   return ZFuncType_ZTypePool_LookupFuncType(TypeList);
};
function ZType_ZTypePool_LookupFuncType(R, P1, P2){ return ZTypePool_LookupFuncType__3qwg(R, P1, P2); }

function ZTypePool_LookupFuncType__4qwg(R, P1, P2, P3) {
   var TypeList = [];
   TypeList.push(R);
   TypeList.push(P1);
   TypeList.push(P2);
   TypeList.push(P3);
   return ZFuncType_ZTypePool_LookupFuncType(TypeList);
};
function ZType_ZTypePool_LookupFuncType(R, P1, P2, P3){ return ZTypePool_LookupFuncType__4qwg(R, P1, P2, P3); }

function ZVarScope__4qrj(self, Parent, Logger, VarList) {
   self.Parent = Parent;
   self.Logger = Logger;
   self.VarList = VarList;
   if (self.VarList == null) {
      self.VarList = [];
   };
   return self;
};

function NewVarType__4qrj(self, VarType, Name, SourceToken) {
   if (!((VarType).constructor.name == (ZVarType).name) && VarType.IsVarType(VarType)) {
      VarType = ZVarType__4qrl(new ZVarType(), self.VarList, Name, SourceToken);
   };
   return VarType;
};
function ZVarScope_NewVarType(self, VarType, Name, SourceToken){ return NewVarType__4qrj(self, VarType, Name, SourceToken); }

function FoundUnresolvedSymbol__2qrj(self, FuncName) {
   self.UnresolvedSymbolCount = self.UnresolvedSymbolCount + 1;
   return;
};
function ZVarScope_FoundUnresolvedSymbol(self, FuncName){ return FoundUnresolvedSymbol__2qrj(self, FuncName); }

function CheckVarNode__3qrj(self, ContextType, Node) {
   if (IsUntyped__1qwo(Node)) {
      self.VarNodeCount = self.VarNodeCount + 1;
   };
   if (IsInferrableType__1qwg(ContextType) && (Node.Type).constructor.name == (ZVarType).name) {
      Infer__3qrl((Node.Type), ContextType, Node.SourceToken);
      Node.Type = ContextType;
   };
   if ((ContextType).constructor.name == (ZVarType).name && !IsUntyped__1qwo(Node)) {
      Infer__3qrl((ContextType), Node.Type, Node.SourceToken);
   };
   return;
};
function ZVarScope_CheckVarNode(self, ContextType, Node){ return CheckVarNode__3qrj(self, ContextType, Node); }

function TypeCheckStmtList__3qrj(self, TypeSafer, StmtList) {
   var PrevCount = -1;
   while (true) {
      var i = 0;
      self.VarNodeCount = 0;
      self.UnresolvedSymbolCount = 0;
      while (i < (StmtList).length) {
         StmtList[i] = ZNode_CheckType(TypeSafer, StmtList[i], ZType__4qwg(new ZType(), 1 << 16, "void", null));
         i = i + 1;
      };
      if (self.VarNodeCount == 0 || PrevCount == self.VarNodeCount) {
         break;
      };
      PrevCount = self.VarNodeCount;
   };
   if (self.VarNodeCount == 0) {
      return true;
   };
   return false;
};
function ZVarScope_TypeCheckStmtList(self, TypeSafer, StmtList){ return TypeCheckStmtList__3qrj(self, TypeSafer, StmtList); }

function TypeCheckFuncBlock__3qrj(self, TypeSafer, FunctionNode) {
   var PrevCount = -1;
   while (true) {
      self.VarNodeCount = 0;
      self.UnresolvedSymbolCount = 0;
      TypeSafer.DefineFunction(TypeSafer, FunctionNode, false);
      FunctionNode.AST[0] = ZNode_CheckType(TypeSafer, FunctionNode.AST[0], ZType__4qwg(new ZType(), 1 << 16, "void", null));
      if (self.VarNodeCount == 0 || PrevCount == self.VarNodeCount) {
         break;
      };
      PrevCount = self.VarNodeCount;
   };
   if (self.UnresolvedSymbolCount == 0) {
      TypeSafer.DefineFunction(TypeSafer, FunctionNode, true);
   } else {
      TypeSafer.DefineFunction(TypeSafer, FunctionNode, false);
      if (self.Parent != null) {
         self.Parent.UnresolvedSymbolCount = self.UnresolvedSymbolCount + self.Parent.UnresolvedSymbolCount;
      };
   };
   return;
};
function ZVarScope_TypeCheckFuncBlock(self, TypeSafer, FunctionNode){ return TypeCheckFuncBlock__3qrj(self, TypeSafer, FunctionNode); }

function ZVarType__4qrl(self, VarList, Name, SourceToken) {
   ZType__4qwg(self, 0, Name, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   self.VarList = VarList;
   self.SourceToken = SourceToken;
   self.GreekId = (VarList).length;
   VarList.push(self);
   self.TypeId = self.RefType.TypeId;
   return self;
};

function GetRealType__1qrl(self) {
   return self.RefType;
};
function ZVarType_GetRealType(self){ return GetRealType__1qrl(self); }

function GetParamSize__1qrl(self) {
   return self.RefType.GetParamSize(self.RefType);
};
function ZVarType_GetParamSize(self){ return GetParamSize__1qrl(self); }

function GetParamType__2qrl(self, Index) {
   return self.RefType.GetParamType(self.RefType, Index);
};
function ZVarType_GetParamType(self, Index){ return GetParamType__2qrl(self, Index); }

function IsFuncType__1qrl(self) {
   return IsFuncType__1qwg(self.RefType);
};
function ZVarType_IsFuncType(self){ return IsFuncType__1qrl(self); }

function IsVarType__1qrl(self) {
   return self.RefType.IsVarType(self.RefType);
};
function ZVarType_IsVarType(self){ return IsVarType__1qrl(self); }

function Infer__3qrl(self, ContextType, SourceToken) {
   if (self.RefType.IsVarType(self.RefType)) {
      if ((ContextType).constructor.name == (ZVarType).name && ContextType.IsVarType(ContextType)) {
         var VarType = ContextType;
         if (self.GreekId < VarType.GreekId) {
            VarType.GreekId = self.GreekId;
         } else {
            self.GreekId = VarType.GreekId;
         };
      } else {
         self.RefType = ContextType.GetRealType(ContextType);
         self.SourceToken = SourceToken;
         self.TypeId = self.RefType.TypeId;
         self.TypeFlag = self.RefType.TypeFlag;
      };
   };
   return;
};
function ZVarType_Infer(self, ContextType, SourceToken){ return Infer__3qrl(self, ContextType, SourceToken); }

function Maybe__3qrl(self, T, SourceToken) {
   if (self.RefType.IsVarType(self.RefType)) {
      if ((T).constructor.name == (ZVarType).name && T.IsVarType(T)) {
         var VarType = T;
         if (self.GreekId < VarType.GreekId) {
            VarType.GreekId = self.GreekId;
         } else {
            self.GreekId = VarType.GreekId;
         };
      } else {
         self.RefType = T.GetRealType(T);
         self.SourceToken = SourceToken;
         self.TypeId = T.TypeId;
         self.TypeFlag = T.TypeFlag;
      };
   };
   return;
};
function ZVarType_Maybe(self, T, SourceToken){ return Maybe__3qrl(self, T, SourceToken); }

function ZNode__4qwo(self, ParentNode, SourceToken, Size) {
   console.assert(self != ParentNode, "(libzen/libzen.zen:1967)");
   self.ParentNode = ParentNode;
   self.SourceToken = SourceToken;
   if (Size > 0) {
      self.AST = LibZen.NewNodeArray(Size);
   } else {
      self.AST = null;
   };
   return self;
};

function SetChild__2qwo(self, Node) {
   console.assert(Node != null, "(libzen/libzen.zen:1979)");
   if (Node != null) {
      console.assert(self != Node, "(libzen/libzen.zen:1981)");
      Node.ParentNode = self;
   };
   return Node;
};
function ZNode_SetChild(self, Node){ return SetChild__2qwo(self, Node); }

function SetNameInfo__3qwo(self, NameToken, Name) {
   console.assert(Name == null, "(libzen/libzen.zen:1988)");
   return;
};
function ZNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qwo(self, NameToken, Name); }

function SetTypeInfo__3qwo(self, TypeToken, Type) {
   self.Type = Type;
   return;
};
function ZNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3qwo(self, TypeToken, Type); }

function Set__3qwo(self, Index, Node) {
   if (Index >= 0) {
      self.AST[Index] = ZNode_SetChild(self, Node);
   } else if (Index == -4) {
      var ListNode = self;
      if ((ListNode).constructor.name == (ZListNode).name) {
         Append__2quv((ListNode), Node);
      } else {
         console.assert((ListNode).constructor.name == (ZListNode).name, "(libzen/libzen.zen:2005)");
      };
   } else if (Index == -2) {
      self.SetNameInfo(self, Node.SourceToken, GetText__1qw3(Node.SourceToken));
      self.SourceToken = Node.SourceToken;
      return;
   } else if (Index == -3) {
      self.SetTypeInfo(self, Node.SourceToken, Node.Type);
      return;
   };
   return;
};
function ZNode_Set(self, Index, Node){ return Set__3qwo(self, Index, Node); }

function GetAstSize__1qwo(self) {
   if (self.AST == null) {
      return 0;
   };
   return (self.AST).length;
};
function ZNode_GetAstSize(self){ return GetAstSize__1qwo(self); }

function HasAst__2qwo(self, Index) {
   if (self.AST != null && Index < (self.AST).length) {
      return self.AST[Index] != null;
   };
   return false;
};
function ZNode_HasAst(self, Index){ return HasAst__2qwo(self, Index); }

function GetAstType__2qwo(self, Index) {
   return self.AST[Index].Type.GetRealType(self.AST[Index].Type);
};
function ZNode_GetAstType(self, Index){ return GetAstType__2qwo(self, Index); }

function GetSourceLocation__1qwo(self) {
   if (self.SourceToken != null) {
      return ((("(" + GetFileName__1qw3(self.SourceToken)) + ":") + (GetLineNumber__1qw3(self.SourceToken)).toString()) + ")";
   };
   return null;
};
function ZNode_GetSourceLocation(self){ return GetSourceLocation__1qwo(self); }

function toString__1qwo(self) {
   var Self = "#" + LibZen.GetClassName(self);
   if (!self.Type.IsVarType(self.Type)) {
      Self = (Self + ":") + toString__1qwg(self.Type);
   } else {
      Self = Self + ":?";
   };
   if (self.AST != null) {
      var i = 0;
      Self = Self + "[";
      while (i < (self.AST).length) {
         if (i > 0) {
            Self = Self + ",";
         };
         if (self.AST[i] == null) {
            Self = Self + "null";
         } else {
            Self = Self + toString__1qwo(self.AST[i]);
         };
         i = i + 1;
      };
      Self = Self + "]";
   };
   return Self;
};
function ZNode_toString(self){ return toString__1qwo(self); }

function GetScopeBlockNode__1qwo(self) {
   var Node = self;
   while (Node != null) {
      if ((Node).constructor.name == (ZBlockNode).name) {
         return Node;
      };
      console.assert(!(Node == Node.ParentNode), "(libzen/libzen.zen:2078)");
      Node = Node.ParentNode;
   };
   return null;
};
function ZNode_GetScopeBlockNode(self){ return GetScopeBlockNode__1qwo(self); }

function GetNameSpace__1qwo(self) {
   var BlockNode = ZBlockNode_GetScopeBlockNode(self);
   return BlockNode.NameSpace;
};
function ZNode_GetNameSpace(self){ return GetNameSpace__1qwo(self); }

function IsErrorNode__1qwo(self) {
   return ((self).constructor.name == (ZErrorNode).name);
};
function ZNode_IsErrorNode(self){ return IsErrorNode__1qwo(self); }

function IsBreakingBlock__1qwo(self) {
   return false;
};
function ZNode_IsBreakingBlock(self){ return IsBreakingBlock__1qwo(self); }

function DeSugar__2qwo(self, Generator) {
   return ZSugarNode__3qts(new ZSugarNode(), self, ZErrorNode__3qpr(new ZErrorNode(), self.ParentNode, "undefined code generation: " + toString__1qwo(self)));
};
function ZNode_DeSugar(self, Generator){ return DeSugar__2qwo(self, Generator); }

function Accept__2qwo(self, Visitor) {
   Visitor.VisitExtendedNode(Visitor, self);
   return;
};
function ZNode_Accept(self, Visitor){ return Accept__2qwo(self, Visitor); }

function IsUntyped__1qwo(self) {
   return !((self.Type).constructor.name == (ZFuncType).name) && self.Type.IsVarType(self.Type);
};
function ZNode_IsUntyped(self){ return IsUntyped__1qwo(self); }

function HasUntypedNode__1qwo(self) {
   if (self.HasUntypedNode) {
      if (!IsUntyped__1qwo(self)) {
         var i = 0;
         while (i < GetAstSize__1qwo(self)) {
            if (self.AST[i] != null && HasUntypedNode__1qwo(self.AST[i])) {
               return true;
            };
            i = i + 1;
         };
         self.HasUntypedNode = false;
         return false;
      };
   };
   return self.HasUntypedNode;
};
function ZNode_HasUntypedNode(self){ return HasUntypedNode__1qwo(self); }

function VisitTypeChecker__3qwo(self, TypeChecker, ContextType) {
   return ZNode_VisitTypeChecker(TypeChecker, self, ContextType);
};
function ZNode_VisitTypeChecker(self, TypeChecker, ContextType){ return VisitTypeChecker__3qwo(self, TypeChecker, ContextType); }

function ToReturnNode__1qwo(self) {
   return null;
};
function ZNode_ToReturnNode(self){ return ToReturnNode__1qwo(self); }

function ZParamNode__2qtl(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 0);
   return self;
};

function SetNameInfo__3qtl(self, NameToken, Name) {
   self.Name = Name;
   self.NameToken = NameToken;
   return;
};
function ZParamNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qtl(self, NameToken, Name); }

function ZReturnNode__2qtj(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 1);
   return self;
};

function Accept__2qtj(self, Visitor) {
   Visitor.VisitReturnNode(Visitor, self);
   return;
};
function ZReturnNode_Accept(self, Visitor){ return Accept__2qtj(self, Visitor); }

function ToReturnNode__1qtj(self) {
   return self;
};
function ZReturnNode_ToReturnNode(self){ return ToReturnNode__1qtj(self); }

function ZSetIndexNode__3qtc(self, ParentNode, LeftNode) {
   ZNode__4qwo(self, ParentNode, null, 3);
   Set__3qwo(self, 0, LeftNode);
   return self;
};

function Accept__2qtc(self, Visitor) {
   Visitor.VisitSetIndexNode(Visitor, self);
   return;
};
function ZSetIndexNode_Accept(self, Visitor){ return Accept__2qtc(self, Visitor); }

function ZSetNameNode__4qtn(self, ParentNode, Token, VarName) {
   ZNode__4qwo(self, ParentNode, Token, 1);
   self.VarName = VarName;
   return self;
};

function Accept__2qtn(self, Visitor) {
   Visitor.VisitSetNameNode(Visitor, self);
   return;
};
function ZSetNameNode_Accept(self, Visitor){ return Accept__2qtn(self, Visitor); }

function ZSetterNode__3qt5(self, ParentNode, RecvNode) {
   ZNode__4qwo(self, ParentNode, null, 2);
   Set__3qwo(self, 0, RecvNode);
   return self;
};

function SetNameInfo__3qt5(self, NameToken, Name) {
   self.FieldName = Name;
   self.NameToken = NameToken;
   return;
};
function ZSetterNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qt5(self, NameToken, Name); }

function Accept__2qt5(self, Visitor) {
   Visitor.VisitSetterNode(Visitor, self);
   return;
};
function ZSetterNode_Accept(self, Visitor){ return Accept__2qt5(self, Visitor); }

function IsStaticField__1qt5(self) {
   return (self.AST[0]).constructor.name == (ZTypeNode).name;
};
function ZSetterNode_IsStaticField(self){ return IsStaticField__1qt5(self); }

function ZSugarNode__3qts(self, SugarNode, DeSugarNode) {
   ZNode__4qwo(self, SugarNode.ParentNode, null, 1);
   self.SugarNode = SugarNode;
   SugarNode.ParentNode = self;
   Set__3qwo(self, 0, DeSugarNode);
   DeSugarNode.ParentNode = self;
   return self;
};

function Accept__2qts(self, Visitor) {
   Visitor.VisitSugarNode(Visitor, self);
   return;
};
function ZSugarNode_Accept(self, Visitor){ return Accept__2qts(self, Visitor); }

function ZThrowNode__2qyr(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 1);
   return self;
};

function Accept__2qyr(self, Visitor) {
   Visitor.VisitThrowNode(Visitor, self);
   return;
};
function ZThrowNode_Accept(self, Visitor){ return Accept__2qyr(self, Visitor); }

function ZTryNode__2qyu(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 3);
   return self;
};

function Accept__2qyu(self, Visitor) {
   Visitor.VisitTryNode(Visitor, self);
   return;
};
function ZTryNode_Accept(self, Visitor){ return Accept__2qyu(self, Visitor); }

function ZUnaryNode__3qyp(self, ParentNode, Token) {
   ZNode__4qwo(self, ParentNode, Token, 1);
   return self;
};

function Accept__2qyp(self, Visitor) {
   Visitor.VisitUnaryNode(Visitor, self);
   return;
};
function ZUnaryNode_Accept(self, Visitor){ return Accept__2qyp(self, Visitor); }

function ZWhileNode__2qya(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 2);
   return self;
};

function Accept__2qya(self, Visitor) {
   Visitor.VisitWhileNode(Visitor, self);
   return;
};
function ZWhileNode_Accept(self, Visitor){ return Accept__2qya(self, Visitor); }

function toString__1qyf(self) {
   return "";
};
function ZEmptyValue_toString(self){ return toString__1qyf(self); }

function ZLogger_LogError__2qw3(Token, Message) {
   if (Token != null && Token.Source != null) {
      Message = FormatErrorMarker__4qud(Token.Source, "error", Token.StartIndex, Message);
      Report__2qrk(Token.Source.Logger, Message);
   };
   return Message;
};
function ZToken_ZLogger_LogError(Token, Message){ return ZLogger_LogError__2qw3(Token, Message); }

function ZLogger_LogWarning__2qw3(Token, Message) {
   if (Token != null && Token.Source != null) {
      Message = FormatErrorMarker__4qud(Token.Source, "warning", Token.StartIndex, Message);
      Report__2qrk(Token.Source.Logger, Message);
   };
   return;
};
function ZToken_ZLogger_LogWarning(Token, Message){ return ZLogger_LogWarning__2qw3(Token, Message); }

function ZLogger_LogInfo__2qw3(Token, Message) {
   if (Token != null && Token.Source != null) {
      Message = FormatErrorMarker__4qud(Token.Source, "info", Token.StartIndex, Message);
      Report__2qrk(Token.Source.Logger, Message);
   };
   return;
};
function ZToken_ZLogger_LogInfo(Token, Message){ return ZLogger_LogInfo__2qw3(Token, Message); }

function ZLogger_LogDebug__2qw3(Token, Message) {
   if (Token != null && Token.Source != null) {
      Message = FormatErrorMarker__4qud(Token.Source, "debug", Token.StartIndex, Message);
      Report__2qrk(Token.Source.Logger, Message);
   };
   return;
};
function ZToken_ZLogger_LogDebug(Token, Message){ return ZLogger_LogDebug__2qw3(Token, Message); }

function Report__2qrk(self, Message) {
   self.ReportedErrorList.push(Message);
   return;
};
function ZLogger_Report(self, Message){ return Report__2qrk(self, Message); }

function GetReportedErrors__1qrk(self) {
   var List = self.ReportedErrorList;
   self.ReportedErrorList = [];
   return List;
};
function ZLogger_GetReportedErrors(self){ return GetReportedErrors__1qrk(self); }

function ShowErrors__1qrk(self) {
   var Messages = GetReportedErrors__1qrk(self);
   var i = 0;
   while (i < (Messages).length) {
      LibZen.PrintLine(Messages[i]);
      i = i + 1;
   };
   return;
};
function ZLogger_ShowErrors(self){ return ShowErrors__1qrk(self); }

function ZMacroFunc__3qy1(self, FuncName, FuncType) {
   ZFunc__4qep(self, 0, FuncName, FuncType);
   return self;
};

function ZNameSpace_RightPatternSymbol__1qqy(PatternName) {
   return "\t" + PatternName;
};

function ZNameSpace__3qwt(self, Generator, ParentNameSpace) {
   self.ParentNameSpace = ParentNameSpace;
   if (ParentNameSpace == null) {
      self.Generator = Generator;
   } else {
      self.Generator = ParentNameSpace.Generator;
   };
   self.SerialId = 0;
   return self;
};

function toString__1qwt(self) {
   return ("NS[" + (self.SerialId).toString()) + "]";
};
function ZNameSpace_toString(self){ return toString__1qwt(self); }

function CreateSubNameSpace__1qwt(self) {
   return ZNameSpace__3qwt(new ZNameSpace(), null, self);
};
function ZNameSpace_CreateSubNameSpace(self){ return CreateSubNameSpace__1qwt(self); }

function GetRootNameSpace__1qwt(self) {
   return self.Generator.RootNameSpace;
};
function ZNameSpace_GetRootNameSpace(self){ return GetRootNameSpace__1qwt(self); }

function GetTokenFunc__2qwt(self, ZenChar) {
   if (self.TokenMatrix == null) {
      return ZTokenFunc_GetTokenFunc(self.ParentNameSpace, ZenChar);
   };
   return self.TokenMatrix[ZenChar];
};
function ZNameSpace_GetTokenFunc(self, ZenChar){ return GetTokenFunc__2qwt(self, ZenChar); }

function JoinParentFunc__3qwt(self, Func, Parent) {
   if (Parent != null && Parent.Func == Func) {
      return Parent;
   };
   return ZTokenFunc__3qqc(new ZTokenFunc(), Func, Parent);
};
function ZNameSpace_JoinParentFunc(self, Func, Parent){ return JoinParentFunc__3qwt(self, Func, Parent); }

function AppendTokenFunc__3qwt(self, keys, TokenFunc) {
   if (self.TokenMatrix == null) {
      self.TokenMatrix = LibZen.NewTokenMatrix();
      if (self.ParentNameSpace != null) {
         var i = 0;
         while (i < (self.TokenMatrix).length) {
            self.TokenMatrix[i] = ZTokenFunc_GetTokenFunc(self.ParentNameSpace, i);
            i = i + 1;
         };
      };
   };
   var i = 0;
   while (i < String_size()) {
      var kchar = LibZen.GetTokenMatrixIndex(LibZen.GetChar(keys, i));
      self.TokenMatrix[kchar] = ZTokenFunc_JoinParentFunc(self, TokenFunc, self.TokenMatrix[kchar]);
      i = i + 1;
   };
   return;
};
function ZNameSpace_AppendTokenFunc(self, keys, TokenFunc){ return AppendTokenFunc__3qwt(self, keys, TokenFunc); }

function GetSyntaxPattern__2qwt(self, PatternName) {
   var NameSpace = self;
   while (NameSpace != null) {
      if (NameSpace.SyntaxTable != null) {
         return NameSpace.SyntaxTable[PatternName];
      };
      NameSpace = NameSpace.ParentNameSpace;
   };
   return null;
};
function ZNameSpace_GetSyntaxPattern(self, PatternName){ return GetSyntaxPattern__2qwt(self, PatternName); }

function SetSyntaxPattern__3qwt(self, PatternName, Syntax) {
   if (self.SyntaxTable == null) {
      self.SyntaxTable = {};
   };
   self.SyntaxTable[PatternName] = Syntax;
   return;
};
function ZNameSpace_SetSyntaxPattern(self, PatternName, Syntax){ return SetSyntaxPattern__3qwt(self, PatternName, Syntax); }

function GetRightSyntaxPattern__2qwt(self, PatternName) {
   return ZSyntax_GetSyntaxPattern(self, ZNameSpace_RightPatternSymbol__1qqy(PatternName));
};
function ZNameSpace_GetRightSyntaxPattern(self, PatternName){ return GetRightSyntaxPattern__2qwt(self, PatternName); }

function AppendSyntaxPattern__3qwt(self, PatternName, NewPattern) {
   LibZen.Assert(NewPattern.ParentPattern == null);
   var ParentPattern = ZSyntax_GetSyntaxPattern(self, PatternName);
   NewPattern.ParentPattern = ParentPattern;
   SetSyntaxPattern__3qwt(self, PatternName, NewPattern);
   return;
};
function ZNameSpace_AppendSyntaxPattern(self, PatternName, NewPattern){ return AppendSyntaxPattern__3qwt(self, PatternName, NewPattern); }

function DefineStatement__3qwt(self, PatternName, MatchFunc) {
   var Alias = String_indexOf(" ");
   var Name = PatternName;
   if (Alias != -1) {
      Name = String_substring(0, Alias);
   };
   var Pattern = ZSyntax__4qy7(new ZSyntax(), self, Name, MatchFunc);
   Pattern.IsStatement = true;
   AppendSyntaxPattern__3qwt(self, Name, Pattern);
   if (Alias != -1) {
      DefineStatement__3qwt(self, String_substring(Alias + 1), MatchFunc);
   };
   return;
};
function ZNameSpace_DefineStatement(self, PatternName, MatchFunc){ return DefineStatement__3qwt(self, PatternName, MatchFunc); }

function DefineExpression__3qwt(self, PatternName, MatchFunc) {
   var Alias = String_indexOf(" ");
   var Name = PatternName;
   if (Alias != -1) {
      Name = String_substring(0, Alias);
   };
   var Pattern = ZSyntax__4qy7(new ZSyntax(), self, Name, MatchFunc);
   AppendSyntaxPattern__3qwt(self, Name, Pattern);
   if (Alias != -1) {
      DefineExpression__3qwt(self, String_substring(Alias + 1), MatchFunc);
   };
   return;
};
function ZNameSpace_DefineExpression(self, PatternName, MatchFunc){ return DefineExpression__3qwt(self, PatternName, MatchFunc); }

function DefineRightExpression__4qwt(self, PatternName, SyntaxFlag, MatchFunc) {
   var Alias = String_indexOf(" ");
   var Name = PatternName;
   if (Alias != -1) {
      Name = String_substring(0, Alias);
   };
   var Pattern = ZSyntax__4qy7(new ZSyntax(), self, Name, MatchFunc);
   Pattern.SyntaxFlag = SyntaxFlag;
   AppendSyntaxPattern__3qwt(self, ZNameSpace_RightPatternSymbol__1qqy(Name), Pattern);
   if (Alias != -1) {
      DefineRightExpression__4qwt(self, String_substring(Alias + 1), SyntaxFlag, MatchFunc);
   };
   return;
};
function ZNameSpace_DefineRightExpression(self, PatternName, SyntaxFlag, MatchFunc){ return DefineRightExpression__4qwt(self, PatternName, SyntaxFlag, MatchFunc); }

function GetSymbol__2qwt(self, Symbol) {
   var NameSpace = self;
   while (NameSpace != null) {
      if (NameSpace.SymbolTable != null) {
         var Entry = NameSpace.SymbolTable[Symbol];
         if (Entry != null) {
            if (Entry.IsDisabled) {
               return null;
            };
            return Entry;
         };
      };
      NameSpace = NameSpace.ParentNameSpace;
   };
   return null;
};
function ZNameSpace_GetSymbol(self, Symbol){ return GetSymbol__2qwt(self, Symbol); }

function GetSymbolNode__2qwt(self, Symbol) {
   var Entry = ZSymbolEntry_GetSymbol(self, Symbol);
   if (Entry != null) {
      return Entry.Node;
   };
   return null;
};
function ZNameSpace_GetSymbolNode(self, Symbol){ return GetSymbolNode__2qwt(self, Symbol); }

function SetLocalSymbolEntry__3qwt(self, Symbol, Entry) {
   if (self.SymbolTable == null) {
      self.SymbolTable = {};
   };
   self.SymbolTable[Symbol] = Entry;
   return;
};
function ZNameSpace_SetLocalSymbolEntry(self, Symbol, Entry){ return SetLocalSymbolEntry__3qwt(self, Symbol, Entry); }

function SetLocalSymbol__3qwt(self, Symbol, Node) {
   var Parent = ZSymbolEntry_GetSymbol(self, Symbol);
   Node.ParentNode = null;
   SetLocalSymbolEntry__3qwt(self, Symbol, ZSymbolEntry__3quw(new ZSymbolEntry(), Parent, Node));
   return Parent;
};
function ZNameSpace_SetLocalSymbol(self, Symbol, Node){ return SetLocalSymbol__3qwt(self, Symbol, Node); }

function SetGlobalSymbol__3qwt(self, Symbol, Node) {
   return ZSymbolEntry_SetLocalSymbol(ZNameSpace_GetRootNameSpace(self), Symbol, Node);
};
function ZNameSpace_SetGlobalSymbol(self, Symbol, Node){ return SetGlobalSymbol__3qwt(self, Symbol, Node); }

function GetLocalVariable__2qwt(self, VarName) {
   var Entry = ZSymbolEntry_GetSymbol(self, VarName);
   if ((Entry).constructor.name == (ZVariable).name) {
      return Entry;
   };
   return null;
};
function ZNameSpace_GetLocalVariable(self, VarName){ return GetLocalVariable__2qwt(self, VarName); }

function SetLocalVariable__5qwt(self, FunctionNode, VarType, VarName, SourceToken) {
   var Parent = ZSymbolEntry_GetSymbol(self, VarName);
   var VarInfo = ZVariable__7quu(new ZVariable(), Parent, FunctionNode, 0, VarType, VarName, SourceToken);
   SetLocalSymbolEntry__3qwt(self, VarName, VarInfo);
   return VarInfo.VarUniqueIndex;
};
function ZNameSpace_SetLocalVariable(self, FunctionNode, VarType, VarName, SourceToken){ return SetLocalVariable__5qwt(self, FunctionNode, VarType, VarName, SourceToken); }

function SetTypeName__4qwt(self, Name, Type, SourceToken) {
   var Node = ZTypeNode__4qu4(new ZTypeNode(), null, SourceToken, Type);
   ZSymbolEntry_SetLocalSymbol(self, Name, Node);
   return;
};
function ZNameSpace_SetTypeName(self, Name, Type, SourceToken){ return SetTypeName__4qwt(self, Name, Type, SourceToken); }

function SetTypeName__3qwt(self, Type, SourceToken) {
   SetTypeName__4qwt(self, Type.ShortName, Type, SourceToken);
   return;
};
function ZNameSpace_SetTypeName(self, Type, SourceToken){ return SetTypeName__3qwt(self, Type, SourceToken); }

function GetTypeNode__3qwt(self, TypeName, SourceToken) {
   var Node = ZNode_GetSymbolNode(self, TypeName);
   if ((Node).constructor.name == (ZTypeNode).name) {
      return Node;
   };
   if (Node == null && SourceToken != null) {
      var Type = ZClassType__3qeq(new ZClassType(), TypeName, ZType__4qwg(new ZType(), 1 << 16, "var", null));
      SetTypeName__4qwt(ZNameSpace_GetRootNameSpace(self), TypeName, Type, SourceToken);
      return ZTypeNode_GetTypeNode(self, TypeName, null);
   };
   return null;
};
function ZNameSpace_GetTypeNode(self, TypeName, SourceToken){ return GetTypeNode__3qwt(self, TypeName, SourceToken); }

function GetType__3qwt(self, TypeName, SourceToken) {
   var TypeNode = ZTypeNode_GetTypeNode(self, TypeName, SourceToken);
   if (TypeNode != null) {
      return TypeNode.Type;
   };
   return null;
};
function ZNameSpace_GetType(self, TypeName, SourceToken){ return GetType__3qwt(self, TypeName, SourceToken); }

function ZSource__5qud(self, FileName, LineNumber, Source, TokenContext) {
   self.FileName = FileName;
   self.LineNumber = LineNumber;
   self.TokenContext = TokenContext;
   self.SourceText = Source;
   self.Logger = TokenContext.Generator.Logger;
   return self;
};

function GetLineNumber__2qud(self, Position) {
   var LineNumber = self.LineNumber;
   var i = 0;
   while (i < Position) {
      var ch = LibZen.GetChar(self.SourceText, i);
      if (ch == "\n") {
         LineNumber = LineNumber + 1;
      };
      i = i + 1;
   };
   return LineNumber;
};
function ZSource_GetLineNumber(self, Position){ return GetLineNumber__2qud(self, Position); }

function GetLineHeadPosition__2qud(self, Position) {
   var s = self.SourceText;
   var StartIndex = 0;
   var i = Position;
   if (!(i < String_size())) {
      i = String_size() - 1;
   };
   while (i >= 0) {
      var ch = LibZen.GetChar(s, i);
      if (ch == "\n") {
         StartIndex = i + 1;
         break;
      };
      i = i - 1;
   };
   return StartIndex;
};
function ZSource_GetLineHeadPosition(self, Position){ return GetLineHeadPosition__2qud(self, Position); }

function CountIndentSize__2qud(self, Position) {
   var s = self.SourceText;
   var length = 0;
   var i = Position;
   while (i < String_size()) {
      var ch = LibZen.GetChar(s, i);
      if (ch == "\t") {
         length = length + 8;
      } else if (ch == " ") {
         length = length + 1;
      } else {
         break;
      };
      i = i + 1;
   };
   return length;
};
function ZSource_CountIndentSize(self, Position){ return CountIndentSize__2qud(self, Position); }

function GetLineText__2qud(self, Position) {
   var s = self.SourceText;
   var StartIndex = 0;
   var EndIndex = String_size();
   var i = Position;
   if (!(i < String_size())) {
      i = String_size() - 1;
   };
   while (i >= 0) {
      var ch = LibZen.GetChar(s, i);
      if (ch == "\n") {
         StartIndex = i + 1;
         break;
      };
      i = i - 1;
   };
   i = Position;
   while (i < String_size()) {
      var ch = LibZen.GetChar(s, i);
      if (ch == "\n") {
         EndIndex = i;
         break;
      };
      i = i + 1;
   };
   return String_substring(StartIndex, EndIndex);
};
function ZSource_GetLineText(self, Position){ return GetLineText__2qud(self, Position); }

function GetLineMarker__2qud(self, Position) {
   var s = self.SourceText;
   var StartIndex = 0;
   var i = Position;
   if (!(i < String_size())) {
      i = String_size() - 1;
   };
   while (i >= 0) {
      var ch = LibZen.GetChar(s, i);
      if (ch == "\n") {
         StartIndex = i + 1;
         break;
      };
      i = i - 1;
   };
   var Line = "";
   i = StartIndex;
   while (i < Position) {
      var ch = LibZen.GetChar(s, i);
      if (ch == "\n") {
         break;
      };
      if (ch == "\t") {
         Line = Line + "\t";
      } else {
         Line = Line + " ";
      };
      i = i + 1;
   };
   return Line + "^";
};
function ZSource_GetLineMarker(self, Position){ return GetLineMarker__2qud(self, Position); }

function FormatErrorHeader__4qud(self, Error, Position, Message) {
   return (((((("(" + self.FileName) + ":") + (GetLineNumber__2qud(self, Position)).toString()) + ") [") + Error) + "] ") + Message;
};
function ZSource_FormatErrorHeader(self, Error, Position, Message){ return FormatErrorHeader__4qud(self, Error, Position, Message); }

function FormatErrorMarker__4qud(self, Error, Position, Message) {
   var Line = GetLineText__2qud(self, Position);
   var Delim = "\n\t";
   if (String_startsWith("\t") || String_startsWith(" ")) {
      Delim = "\n";
   };
   var Header = FormatErrorHeader__4qud(self, Error, Position, Message);
   var Marker = GetLineMarker__2qud(self, Position);
   Message = (((Header + Delim) + Line) + Delim) + Marker;
   return Message;
};
function ZSource_FormatErrorMarker(self, Error, Position, Message){ return FormatErrorMarker__4qud(self, Error, Position, Message); }

function GetCharAt__2qud(self, n) {
   if (0 <= n && n < String_size()) {
      return LibZen.GetChar(self.SourceText, n);
   };
   return "0";
};
function ZSource_GetCharAt(self, n){ return GetCharAt__2qud(self, n); }

function ZSourceBuilder__3qq2(self, Template, Parent) {
   self.Template = Template;
   self.Parent = Parent;
   return self;
};

function Pop__1qq2(self) {
   return self.Parent;
};
function ZSourceBuilder_Pop(self){ return Pop__1qq2(self); }

function Clear__1qq2(self) {
   Array<String>_clear(0);
   return;
};
function ZSourceBuilder_Clear(self){ return Clear__1qq2(self); }

function GetPosition__1qq2(self) {
   return (self.SourceList).length;
};
function ZSourceBuilder_GetPosition(self){ return GetPosition__1qq2(self); }

function CopyString__3qq2(self, BeginIndex, EndIndex) {
   return LibZen.SourceBuilderToString(self, BeginIndex, EndIndex);
};
function ZSourceBuilder_CopyString(self, BeginIndex, EndIndex){ return CopyString__3qq2(self, BeginIndex, EndIndex); }

function Append__2qq2(self, Text) {
   self.SourceList.push(Text);
   return;
};
function ZSourceBuilder_Append(self, Text){ return Append__2qq2(self, Text); }

function AppendInt__2qq2(self, Value) {
   self.SourceList.push("" + (Value).toString());
   return;
};
function ZSourceBuilder_AppendInt(self, Value){ return AppendInt__2qq2(self, Value); }

function AppendLineFeed__1qq2(self) {
   if (String_size() > 0) {
      self.SourceList.push(self.BufferedLineComment);
      self.BufferedLineComment = "";
   };
   self.SourceList.push(self.Template.LineFeed);
   return;
};
function ZSourceBuilder_AppendLineFeed(self){ return AppendLineFeed__1qq2(self); }

function AppendLineFeed__2qq2(self, AppendIndent) {
   if (String_size() > 0) {
      self.SourceList.push(self.BufferedLineComment);
      self.BufferedLineComment = "";
   };
   self.SourceList.push(self.Template.LineFeed);
   if (AppendIndent) {
      AppendIndent__1qq2(self);
   };
   return;
};
function ZSourceBuilder_AppendLineFeed(self, AppendIndent){ return AppendLineFeed__2qq2(self, AppendIndent); }

function AppendWhiteSpace__1qq2(self) {
   var Size = (self.SourceList).length;
   if (Size > 0) {
      var Last = self.SourceList[Size - 1];
      if (Last != null && (String_endsWith(" ") || String_endsWith("\n") || String_endsWith("\t"))) {
         return;
      };
   };
   self.SourceList.push(" ");
   return;
};
function ZSourceBuilder_AppendWhiteSpace(self){ return AppendWhiteSpace__1qq2(self); }

function AppendToken__2qq2(self, Text) {
   AppendWhiteSpace__1qq2(self);
   self.SourceList.push(Text);
   AppendWhiteSpace__1qq2(self);
   return;
};
function ZSourceBuilder_AppendToken(self, Text){ return AppendToken__2qq2(self, Text); }

function AppendBlockComment__2qq2(self, Text) {
   if (self.Template.BeginComment != null) {
      self.SourceList.push(self.Template.BeginComment);
      self.SourceList.push(Text);
      self.SourceList.push(self.Template.EndComment);
   } else if (self.Template.LineComment != null) {
      self.BufferedLineComment = (self.BufferedLineComment + self.Template.LineComment) + Text;
   };
   return;
};
function ZSourceBuilder_AppendBlockComment(self, Text){ return AppendBlockComment__2qq2(self, Text); }

function AppendCommentLine__2qq2(self, Text) {
   if (self.Template.LineComment == null) {
      self.SourceList.push(self.Template.BeginComment);
      self.SourceList.push(Text);
      self.SourceList.push(self.Template.EndComment);
   } else {
      self.SourceList.push(self.Template.LineComment);
      self.SourceList.push(Text);
   };
   self.SourceList.push(self.Template.LineFeed);
   return;
};
function ZSourceBuilder_AppendCommentLine(self, Text){ return AppendCommentLine__2qq2(self, Text); }

function Indent__1qq2(self) {
   self.IndentLevel = self.IndentLevel + 1;
   self.CurrentIndentString = null;
   return;
};
function ZSourceBuilder_Indent(self){ return Indent__1qq2(self); }

function UnIndent__1qq2(self) {
   self.IndentLevel = self.IndentLevel - 1;
   self.CurrentIndentString = null;
   LibZen.Assert(self.IndentLevel >= 0);
   return;
};
function ZSourceBuilder_UnIndent(self){ return UnIndent__1qq2(self); }

function GetIndentString__1qq2(self) {
   if (self.CurrentIndentString == null) {
      self.CurrentIndentString = LibZen.JoinStrings(self.Template.Tab, self.IndentLevel);
   };
   return self.CurrentIndentString;
};
function ZSourceBuilder_GetIndentString(self){ return GetIndentString__1qq2(self); }

function AppendIndent__1qq2(self) {
   self.SourceList.push(GetIndentString__1qq2(self));
   return;
};
function ZSourceBuilder_AppendIndent(self){ return AppendIndent__1qq2(self); }

function AppendLineFeedIndent__1qq2(self) {
   self.SourceList.push(self.Template.LineFeed);
   self.SourceList.push(GetIndentString__1qq2(self));
   return;
};
function ZSourceBuilder_AppendLineFeedIndent(self){ return AppendLineFeedIndent__1qq2(self); }

function IndentAndAppend__2qq2(self, Text) {
   self.SourceList.push(GetIndentString__1qq2(self));
   self.SourceList.push(Text);
   return;
};
function ZSourceBuilder_IndentAndAppend(self, Text){ return IndentAndAppend__2qq2(self, Text); }

function AppendParamList__4qq2(self, ParamList, BeginIdx, EndIdx) {
   var i = BeginIdx;
   while (i < EndIdx) {
      if (i > BeginIdx) {
         Append__2qq2(self, self.Template.Camma);
      };
      ZNode_GetListAt(ParamList, i).Accept(ZNode_GetListAt(ParamList, i), self.Template);
      i = i + 1;
   };
   return;
};
function ZSourceBuilder_AppendParamList(self, ParamList, BeginIdx, EndIdx){ return AppendParamList__4qq2(self, ParamList, BeginIdx, EndIdx); }

function toString__1qq2(self) {
   return LibZen.SourceBuilderToString(self);
};
function ZSourceBuilder_toString(self){ return toString__1qq2(self); }

function AppendLine__2qq2(self, Text) {
   Append__2qq2(self, Text);
   AppendLineFeed__1qq2(self);
   return;
};
function ZSourceBuilder_AppendLine(self, Text){ return AppendLine__2qq2(self, Text); }

function ZSourceContext__5qwu(self, FileName, LineNumber, Source, TokenContext) {
   ZSource__5qud(self, FileName, LineNumber, Source, TokenContext);
   return self;
};

function GetCharCode__1qwu(self) {
   return LibZen.GetTokenMatrixIndex(LibZen.GetChar(self.SourceText, self.SourcePosition));
};
function ZSourceContext_GetCharCode(self){ return GetCharCode__1qwu(self); }

function GetPosition__1qwu(self) {
   return self.SourcePosition;
};
function ZSourceContext_GetPosition(self){ return GetPosition__1qwu(self); }

function HasChar__1qwu(self) {
   return (String_size() - self.SourcePosition) > 0;
};
function ZSourceContext_HasChar(self){ return HasChar__1qwu(self); }

function GetCurrentChar__1qwu(self) {
   return LibZen.GetChar(self.SourceText, self.SourcePosition);
};
function ZSourceContext_GetCurrentChar(self){ return GetCurrentChar__1qwu(self); }

function GetCharAtFromCurrentPosition__2qwu(self, n) {
   if ((self.SourcePosition + n) < String_size()) {
      return LibZen.GetChar(self.SourceText, self.SourcePosition + n);
   };
   return "0";
};
function ZSourceContext_GetCharAtFromCurrentPosition(self, n){ return GetCharAtFromCurrentPosition__2qwu(self, n); }

function MoveNext__1qwu(self) {
   self.SourcePosition = self.SourcePosition + 1;
   return;
};
function ZSourceContext_MoveNext(self){ return MoveNext__1qwu(self); }

function SkipWhiteSpace__1qwu(self) {
   while (HasChar__1qwu(self)) {
      var ch = GetCurrentChar__1qwu(self);
      if (ch != " " && ch != "\t") {
         break;
      };
      MoveNext__1qwu(self);
   };
   return;
};
function ZSourceContext_SkipWhiteSpace(self){ return SkipWhiteSpace__1qwu(self); }

function FoundIndent__3qwu(self, StartIndex, EndIndex) {
   var Token = ZIndentToken__4qak(new ZIndentToken(), self, StartIndex, EndIndex);
   self.SourcePosition = EndIndex;
   self.TokenContext.TokenList.push(Token);
   return;
};
function ZSourceContext_FoundIndent(self, StartIndex, EndIndex){ return FoundIndent__3qwu(self, StartIndex, EndIndex); }

function Tokenize__3qwu(self, StartIndex, EndIndex) {
   self.SourcePosition = EndIndex;
   if (StartIndex < EndIndex && EndIndex <= String_size()) {
      var Token = ZToken__4qw3(new ZToken(), self, StartIndex, EndIndex);
      self.TokenContext.TokenList.push(Token);
   };
   return;
};
function ZSourceContext_Tokenize(self, StartIndex, EndIndex){ return Tokenize__3qwu(self, StartIndex, EndIndex); }

function Tokenize__4qwu(self, PatternName, StartIndex, EndIndex) {
   self.SourcePosition = EndIndex;
   if (StartIndex <= EndIndex && EndIndex <= String_size()) {
      var Pattern = ZSyntax_GetSyntaxPattern(self.TokenContext.NameSpace, PatternName);
      if (Pattern == null) {
         var Token = ZToken__4qw3(new ZToken(), self, StartIndex, EndIndex);
         ZLogger_LogInfo__2qw3(Token, "unregistered token pattern: " + PatternName);
         self.TokenContext.TokenList.push(Token);
      } else {
         var Token = ZPatternToken__5qa9(new ZPatternToken(), self, StartIndex, EndIndex, Pattern);
         self.TokenContext.TokenList.push(Token);
      };
   };
   return;
};
function ZSourceContext_Tokenize(self, PatternName, StartIndex, EndIndex){ return Tokenize__4qwu(self, PatternName, StartIndex, EndIndex); }

function IsDefinedSyntax__3qwu(self, StartIndex, EndIndex) {
   if (EndIndex < String_size()) {
      var NameSpace = self.TokenContext.NameSpace;
      var Token = String_substring(StartIndex, EndIndex);
      var Pattern = ZSyntax_GetRightSyntaxPattern(NameSpace, Token);
      if (Pattern != null) {
         return true;
      };
   };
   return false;
};
function ZSourceContext_IsDefinedSyntax(self, StartIndex, EndIndex){ return IsDefinedSyntax__3qwu(self, StartIndex, EndIndex); }

function TokenizeDefinedSymbol__2qwu(self, StartIndex) {
   var EndIndex = StartIndex + 2;
   while (IsDefinedSyntax__3qwu(self, StartIndex, EndIndex)) {
      EndIndex = EndIndex + 1;
   };
   Tokenize__3qwu(self, StartIndex, EndIndex - 1);
   return;
};
function ZSourceContext_TokenizeDefinedSymbol(self, StartIndex){ return TokenizeDefinedSymbol__2qwu(self, StartIndex); }

function ApplyTokenFunc__2qwu(self, TokenFunc) {
   var RollbackPosition = self.SourcePosition;
   while (TokenFunc != null) {
      self.SourcePosition = RollbackPosition;
      if (LibZen.ApplyTokenFunc(TokenFunc.Func, self)) {
         return;
      };
      TokenFunc = TokenFunc.ParentFunc;
   };
   TokenizeDefinedSymbol__2qwu(self, RollbackPosition);
   return;
};
function ZSourceContext_ApplyTokenFunc(self, TokenFunc){ return ApplyTokenFunc__2qwu(self, TokenFunc); }

function DoTokenize__1qwu(self) {
   var TokenSize = (self.TokenContext.TokenList).length;
   var CheckPosition = self.SourcePosition;
   while (HasChar__1qwu(self)) {
      var CharCode = GetCharCode__1qwu(self);
      var TokenFunc = ZTokenFunc_GetTokenFunc(self.TokenContext.NameSpace, CharCode);
      ApplyTokenFunc__2qwu(self, TokenFunc);
      if ((self.TokenContext.TokenList).length > TokenSize) {
         break;
      };
      if (self.SourcePosition == CheckPosition) {
         MoveNext__1qwu(self);
      };
   };
   if ((self.TokenContext.TokenList).length > TokenSize) {
      return true;
   };
   return false;
};
function ZSourceContext_DoTokenize(self){ return DoTokenize__1qwu(self); }

function LogWarning__3qwu(self, Position, Message) {
   Report__2qrk(self.Logger, FormatErrorMarker__4qud(self, "warning", Position, Message));
   return;
};
function ZSourceContext_LogWarning(self, Position, Message){ return LogWarning__3qwu(self, Position, Message); }

function ZSourceMacro__4qit(self, FuncName, FuncType, Macro) {
   ZMacroFunc__3qy1(self, FuncName, FuncType);
   self.Macro = Macro;
   return self;
};

function ZSymbolEntry__3quw(self, Parent, Node) {
   self.Parent = Parent;
   self.Node = Node;
   return self;
};

function MergeSyntaxPattern__2qy7(Pattern, Parent) {
   if (Parent == null) {
      return Pattern;
   };
   var MergedPattern = ZSyntax__4qy7(new ZSyntax(), Pattern.PackageNameSpace, Pattern.PatternName, Pattern.MatchFunc);
   MergedPattern.ParentPattern = Parent;
   return MergedPattern;
};
function ZSyntax_MergeSyntaxPattern(Pattern, Parent){ return MergeSyntaxPattern__2qy7(Pattern, Parent); }

function ZSyntax__4qy7(self, NameSpace, PatternName, MatchFunc) {
   self.PackageNameSpace = NameSpace;
   self.PatternName = PatternName;
   self.MatchFunc = MatchFunc;
   return self;
};

function toString__1qy7(self) {
   return self.PatternName;
};
function ZSyntax_toString(self){ return toString__1qy7(self); }

function IsBinaryOperator__1qy7(self) {
   return LibZen.IsFlag(self.SyntaxFlag, 1);
};
function ZSyntax_IsBinaryOperator(self){ return IsBinaryOperator__1qy7(self); }

function IsRightJoin__2qy7(self, Right) {
   var left = self.SyntaxFlag;
   var right = Right.SyntaxFlag;
   return (left < right || (left == right && !LibZen.IsFlag(left, 1 << 1) && !LibZen.IsFlag(right, 1 << 1)));
};
function ZSyntax_IsRightJoin(self, Right){ return IsRightJoin__2qy7(self, Right); }

function ZToken__4qw3(self, Source, StartIndex, EndIndex) {
   self.Source = Source;
   self.StartIndex = StartIndex;
   self.EndIndex = EndIndex;
   return self;
};

function GetFileName__1qw3(self) {
   return self.Source.FileName;
};
function ZToken_GetFileName(self){ return GetFileName__1qw3(self); }

function GetLineNumber__1qw3(self) {
   return GetLineNumber__2qud(self.Source, self.StartIndex);
};
function ZToken_GetLineNumber(self){ return GetLineNumber__1qw3(self); }

function GetChar__1qw3(self) {
   if (self.Source != null) {
      return LibZen.GetChar(self.Source.SourceText, self.StartIndex);
   };
   return "0";
};
function ZToken_GetChar(self){ return GetChar__1qw3(self); }

function GetText__1qw3(self) {
   if (self.Source != null) {
      return String_substring(self.StartIndex, self.EndIndex);
   };
   return "";
};
function ZToken_GetText(self){ return GetText__1qw3(self); }

function toString__1qw3(self) {
   var ch = GetCharAt__2qud(self.Source, self.StartIndex - 1);
   if (ch == "\"") {
      return ("\"" + GetText__1qw3(self)) + "\"";
   };
   return GetText__1qw3(self);
};
function ZToken_toString(self){ return toString__1qw3(self); }

function EqualsText__2qw3(self, Text) {
   if (String_size() == (self.EndIndex - self.StartIndex)) {
      var s = self.Source.SourceText;
      var i = 0;
      while (i < String_size()) {
         if (LibZen.GetChar(s, self.StartIndex + i) != LibZen.GetChar(Text, i)) {
            return false;
         };
         i = i + 1;
      };
      return true;
   };
   return false;
};
function ZToken_EqualsText(self, Text){ return EqualsText__2qw3(self, Text); }

function StartsWith__2qw3(self, Text) {
   if (String_size() <= (self.EndIndex - self.StartIndex)) {
      var s = self.Source.SourceText;
      var i = 0;
      while (i < String_size()) {
         if (LibZen.GetChar(s, self.StartIndex + i) != LibZen.GetChar(Text, i)) {
            return false;
         };
         i = i + 1;
      };
      return true;
   };
   return false;
};
function ZToken_StartsWith(self, Text){ return StartsWith__2qw3(self, Text); }

function IsNull__1qw3(self) {
   return (self == ZToken__4qw3(new ZToken(), null, 0, 0));
};
function ZToken_IsNull(self){ return IsNull__1qw3(self); }

function IsIndent__1qw3(self) {
   return (self).constructor.name == (ZIndentToken).name;
};
function ZToken_IsIndent(self){ return IsIndent__1qw3(self); }

function IsNextWhiteSpace__1qw3(self) {
   var ch = GetCharAt__2qud(self.Source, self.EndIndex);
   if (ch == " " || ch == "\t" || ch == "\n") {
      return true;
   };
   return false;
};
function ZToken_IsNextWhiteSpace(self){ return IsNextWhiteSpace__1qw3(self); }

function IsNameSymbol__1qw3(self) {
   var ch = GetCharAt__2qud(self.Source, self.StartIndex);
   return LibZen.IsSymbol(ch);
};
function ZToken_IsNameSymbol(self){ return IsNameSymbol__1qw3(self); }

function GetIndentSize__1qw3(self) {
   if (self.Source != null) {
      return CountIndentSize__2qud(self.Source, GetLineHeadPosition__2qud(self.Source, self.StartIndex));
   };
   return 0;
};
function ZToken_GetIndentSize(self){ return GetIndentSize__1qw3(self); }

function ZTokenContext__6qwp(self, Generator, NameSpace, FileName, LineNumber, SourceText) {
   self.Generator = Generator;
   self.NameSpace = NameSpace;
   self.Source = ZSourceContext__5qwu(new ZSourceContext(), FileName, LineNumber, SourceText, self);
   return self;
};

function SetParseFlag__2qwp(self, AllowSkipIndent) {
   var OldFlag = self.IsAllowSkipIndent;
   self.IsAllowSkipIndent = AllowSkipIndent;
   return OldFlag;
};
function ZTokenContext_SetParseFlag(self, AllowSkipIndent){ return SetParseFlag__2qwp(self, AllowSkipIndent); }

function GetBeforeToken__1qwp(self) {
   var MovingPos = self.CurrentPosition - 1;
   while (MovingPos >= 0 && MovingPos < (self.TokenList).length) {
      var Token = self.TokenList[MovingPos];
      if (!IsIndent__1qw3(Token)) {
         return Token;
      };
      MovingPos = MovingPos - 1;
   };
   return self.LatestToken;
};
function ZTokenContext_GetBeforeToken(self){ return GetBeforeToken__1qwp(self); }

function CreateExpectedErrorNode__3qwp(self, SourceToken, ExpectedTokenText) {
   if (SourceToken == null || IsNull__1qw3(SourceToken)) {
      SourceToken = ZToken_GetBeforeToken(self);
      SourceToken = ZToken__4qw3(new ZToken(), SourceToken.Source, SourceToken.EndIndex, SourceToken.EndIndex);
      return ZErrorNode__4qpr(new ZErrorNode(), null, SourceToken, ExpectedTokenText + " is expected");
   };
   return ZErrorNode__4qpr(new ZErrorNode(), null, SourceToken, ExpectedTokenText + " is expected");
};
function ZTokenContext_CreateExpectedErrorNode(self, SourceToken, ExpectedTokenText){ return CreateExpectedErrorNode__3qwp(self, SourceToken, ExpectedTokenText); }

function Vacume__1qwp(self) {
   return;
};
function ZTokenContext_Vacume(self){ return Vacume__1qwp(self); }

function MoveNext__1qwp(self) {
   self.CurrentPosition = self.CurrentPosition + 1;
   return;
};
function ZTokenContext_MoveNext(self){ return MoveNext__1qwp(self); }

function GetToken__2qwp(self, EnforceMoveNext) {
   while (true) {
      if (!(self.CurrentPosition < (self.TokenList).length)) {
         if (!DoTokenize__1qwu(self.Source)) {
            break;
         };
      };
      var Token = self.TokenList[self.CurrentPosition];
      if ((self.IsAllowSkipIndent) && IsIndent__1qw3(Token)) {
         self.CurrentPosition = self.CurrentPosition + 1;
      } else {
         self.LatestToken = Token;
         if (EnforceMoveNext) {
            self.CurrentPosition = self.CurrentPosition + 1;
         };
         return Token;
      };
   };
   return ZToken__4qw3(new ZToken(), null, 0, 0);
};
function ZTokenContext_GetToken(self, EnforceMoveNext){ return GetToken__2qwp(self, EnforceMoveNext); }

function GetToken__1qwp(self) {
   return ZToken_GetToken(self, false);
};
function ZTokenContext_GetToken(self){ return GetToken__1qwp(self); }

function HasNext__1qwp(self) {
   return (ZToken_GetToken(self) != ZToken__4qw3(new ZToken(), null, 0, 0));
};
function ZTokenContext_HasNext(self){ return HasNext__1qwp(self); }

function SkipIndent__1qwp(self) {
   var Token = ZToken_GetToken(self);
   while (IsIndent__1qw3(Token)) {
      self.CurrentPosition = self.CurrentPosition + 1;
      Token = ZToken_GetToken(self);
   };
   return;
};
function ZTokenContext_SkipIndent(self){ return SkipIndent__1qwp(self); }

function SkipError__2qwp(self, ErrorToken) {
   var StartIndex = ErrorToken.StartIndex;
   var EndIndex = ErrorToken.EndIndex;
   var length = GetIndentSize__1qw3(ErrorToken);
   while (HasNext__1qwp(self)) {
      var Token = ZToken_GetToken(self);
      EndIndex = Token.EndIndex;
      self.CurrentPosition = self.CurrentPosition + 1;
      if ((Token).constructor.name == (ZIndentToken).name) {
         var ilength = GetIndentSize__1qw3(Token);
         if (ilength <= length) {
            break;
         };
      };
   };
   if (StartIndex < EndIndex) {
      LibZen.PrintDebug((("StartIdx=" + (StartIndex).toString()) + ", EndIndex=") + (EndIndex).toString());
      LibZen.PrintDebug("skipped: \t" + String_substring(StartIndex, EndIndex));
   };
   return;
};
function ZTokenContext_SkipError(self, ErrorToken){ return SkipError__2qwp(self, ErrorToken); }

function IsToken__2qwp(self, TokenText) {
   var Token = ZToken_GetToken(self);
   if (EqualsText__2qw3(Token, TokenText)) {
      return true;
   };
   return false;
};
function ZTokenContext_IsToken(self, TokenText){ return IsToken__2qwp(self, TokenText); }

function IsNewLineToken__2qwp(self, TokenText) {
   var RollbackPos = self.CurrentPosition;
   SkipIndent__1qwp(self);
   var Token = ZToken_GetToken(self);
   if (EqualsText__2qw3(Token, TokenText)) {
      return true;
   };
   self.CurrentPosition = RollbackPos;
   return false;
};
function ZTokenContext_IsNewLineToken(self, TokenText){ return IsNewLineToken__2qwp(self, TokenText); }

function MatchToken__2qwp(self, TokenText) {
   var RollbackPos = self.CurrentPosition;
   var Token = ZToken_GetToken(self, true);
   if (EqualsText__2qw3(Token, TokenText)) {
      return true;
   };
   self.CurrentPosition = RollbackPos;
   return false;
};
function ZTokenContext_MatchToken(self, TokenText){ return MatchToken__2qwp(self, TokenText); }

function MatchNewLineToken__2qwp(self, TokenText) {
   var RollbackPos = self.CurrentPosition;
   SkipIndent__1qwp(self);
   var Token = ZToken_GetToken(self, true);
   if (EqualsText__2qw3(Token, TokenText)) {
      return true;
   };
   self.CurrentPosition = RollbackPos;
   return false;
};
function ZTokenContext_MatchNewLineToken(self, TokenText){ return MatchNewLineToken__2qwp(self, TokenText); }

function ParseLargeToken__1qwp(self) {
   var Token = ZToken_GetToken(self, true);
   if (IsNextWhiteSpace__1qw3(Token)) {
      return Token;
   };
   var StartIndex = Token.StartIndex;
   var EndIndex = Token.EndIndex;
   while (HasNext__1qwp(self) && !IsNextWhiteSpace__1qw3(Token)) {
      var RollbackPosition = self.CurrentPosition;
      Token = ZToken_GetToken(self, true);
      if (IsIndent__1qw3(Token) || EqualsText__2qw3(Token, ";") || EqualsText__2qw3(Token, ",")) {
         self.CurrentPosition = RollbackPosition;
         break;
      };
      EndIndex = Token.EndIndex;
   };
   return ZToken__4qw3(new ZToken(), Token.Source, StartIndex, EndIndex);
};
function ZTokenContext_ParseLargeToken(self){ return ParseLargeToken__1qwp(self); }

function MatchToken__4qwp(self, ParentNode, TokenText, IsRequired) {
   if (!IsErrorNode__1qwo(ParentNode)) {
      var RollbackPosition = self.CurrentPosition;
      var Token = ZToken_GetToken(self, true);
      if (EqualsText__2qw3(Token, TokenText)) {
         if (ParentNode.SourceToken == null) {
            ParentNode.SourceToken = Token;
         };
      } else {
         if (IsRequired) {
            return ZNode_CreateExpectedErrorNode(self, Token, TokenText);
         } else {
            self.CurrentPosition = RollbackPosition;
         };
      };
   };
   return ParentNode;
};
function ZTokenContext_MatchToken(self, ParentNode, TokenText, IsRequired){ return MatchToken__4qwp(self, ParentNode, TokenText, IsRequired); }

function GetApplyingSyntax__1qwp(self) {
   return self.ApplyingPattern;
};
function ZTokenContext_GetApplyingSyntax(self){ return GetApplyingSyntax__1qwp(self); }

function ApplyMatchPattern__5qwp(self, ParentNode, LeftNode, Pattern, IsRequired) {
   var RollbackPosition = self.CurrentPosition;
   var CurrentPattern = Pattern;
   var TopToken = ZToken_GetToken(self);
   var ParsedNode = null;
   while (CurrentPattern != null) {
      var Remembered = self.IsAllowSkipIndent;
      self.CurrentPosition = RollbackPosition;
      self.ApplyingPattern = CurrentPattern;
      ParsedNode = ZNode_LibZen_ApplyMatchFunc(CurrentPattern.MatchFunc, ParentNode, self, LeftNode);
      console.assert(ParsedNode != ParentNode, "(libzen/libzen.zen:3236)");
      self.ApplyingPattern = null;
      self.IsAllowSkipIndent = Remembered;
      if (ParsedNode != null && !IsErrorNode__1qwo(ParsedNode)) {
         return ParsedNode;
      };
      CurrentPattern = CurrentPattern.ParentPattern;
   };
   if (!IsRequired) {
      self.CurrentPosition = RollbackPosition;
      return null;
   };
   if (self.CurrentPosition == RollbackPosition) {
      LibZen.PrintLine((((("DEBUG infinite looping" + (RollbackPosition).toString()) + " Token=") + toString__1qw3(TopToken)) + " ParsedNode=") + toString__1qwo(ParsedNode));
      console.assert(self.CurrentPosition != RollbackPosition, "(libzen/libzen.zen:3250)");
   };
   if (ParsedNode == null) {
      ParsedNode = ZNode_CreateExpectedErrorNode(self, TopToken, Pattern.PatternName);
   };
   return ParsedNode;
};
function ZTokenContext_ApplyMatchPattern(self, ParentNode, LeftNode, Pattern, IsRequired){ return ApplyMatchPattern__5qwp(self, ParentNode, LeftNode, Pattern, IsRequired); }

function ParsePatternAfter__5qwp(self, ParentNode, LeftNode, PatternName, IsRequired) {
   var Pattern = ZSyntax_GetSyntaxPattern(self.NameSpace, PatternName);
   var ParsedNode = ZNode_ApplyMatchPattern(self, ParentNode, LeftNode, Pattern, IsRequired);
   return ParsedNode;
};
function ZTokenContext_ParsePatternAfter(self, ParentNode, LeftNode, PatternName, IsRequired){ return ParsePatternAfter__5qwp(self, ParentNode, LeftNode, PatternName, IsRequired); }

function ParsePattern__4qwp(self, ParentNode, PatternName, IsRequired) {
   return ZNode_ParsePatternAfter(self, ParentNode, null, PatternName, IsRequired);
};
function ZTokenContext_ParsePattern(self, ParentNode, PatternName, IsRequired){ return ParsePattern__4qwp(self, ParentNode, PatternName, IsRequired); }

function MatchPattern__6qwp(self, ParentNode, Index, PatternName, IsRequired, AllowSkipIndent) {
   if (!IsErrorNode__1qwo(ParentNode)) {
      var Rememberd = SetParseFlag__2qwp(self, AllowSkipIndent);
      var ParsedNode = ZNode_ParsePattern(self, ParentNode, PatternName, IsRequired);
      SetParseFlag__2qwp(self, Rememberd);
      if (ParsedNode != null) {
         if (Index == -5) {
            if (!((ParsedNode).constructor.name == (ZEmptyNode).name)) {
               Set__3qwo(ParentNode, -4, ParsedNode);
            };
            if ((ParsedNode).constructor.name == (ZBlockNode).name || IsErrorNode__1qwo(ParsedNode)) {
               return ParsedNode;
            };
         };
         if (IsErrorNode__1qwo(ParsedNode)) {
            return ParsedNode;
         } else {
            if (!((ParsedNode).constructor.name == (ZEmptyNode).name)) {
               Set__3qwo(ParentNode, Index, ParsedNode);
            };
         };
      };
   };
   return ParentNode;
};
function ZTokenContext_MatchPattern(self, ParentNode, Index, PatternName, IsRequired, AllowSkipIndent){ return MatchPattern__6qwp(self, ParentNode, Index, PatternName, IsRequired, AllowSkipIndent); }

function MatchPattern__5qwp(self, ParentNode, Index, PatternName, IsRequired) {
   return ZNode_MatchPattern(self, ParentNode, Index, PatternName, IsRequired, false);
};
function ZTokenContext_MatchPattern(self, ParentNode, Index, PatternName, IsRequired){ return MatchPattern__5qwp(self, ParentNode, Index, PatternName, IsRequired); }

function MatchOptionaPattern__6qwp(self, ParentNode, Index, AllowNewLine, TokenText, PatternName) {
   if (!IsErrorNode__1qwo(ParentNode)) {
      if (MatchToken__2qwp(self, TokenText)) {
         return ZNode_MatchPattern(self, ParentNode, Index, PatternName, false, false);
      };
   };
   return ParentNode;
};
function ZTokenContext_MatchOptionaPattern(self, ParentNode, Index, AllowNewLine, TokenText, PatternName){ return MatchOptionaPattern__6qwp(self, ParentNode, Index, AllowNewLine, TokenText, PatternName); }

function MatchNtimes__6qwp(self, ParentNode, StartToken, PatternName, DelimToken, StopToken) {
   var Rememberd = SetParseFlag__2qwp(self, true);
   var IsRequired = false;
   if (StartToken != null) {
      ParentNode = ZNode_MatchToken(self, ParentNode, StartToken, true);
   };
   while (!IsErrorNode__1qwo(ParentNode)) {
      if (StopToken != null) {
         var Token = ZToken_GetToken(self);
         if (EqualsText__2qw3(Token, StopToken)) {
            break;
         };
         IsRequired = true;
      };
      var ParsedNode = ZNode_ParsePattern(self, ParentNode, PatternName, IsRequired);
      if (ParsedNode == null) {
         break;
      };
      if (IsErrorNode__1qwo(ParsedNode)) {
         return ParsedNode;
      };
      if (!((ParsedNode).constructor.name == (ZEmptyNode).name)) {
         Set__3qwo(ParentNode, -4, ParsedNode);
      };
      if (DelimToken != null) {
         if (!MatchToken__2qwp(self, DelimToken)) {
            break;
         };
      };
   };
   if (StopToken != null) {
      ParentNode = ZNode_MatchToken(self, ParentNode, StopToken, true);
   };
   SetParseFlag__2qwp(self, Rememberd);
   return ParentNode;
};
function ZTokenContext_MatchNtimes(self, ParentNode, StartToken, PatternName, DelimToken, StopToken){ return MatchNtimes__6qwp(self, ParentNode, StartToken, PatternName, DelimToken, StopToken); }

function StartsWithToken__2qwp(self, TokenText) {
   var Token = ZToken_GetToken(self);
   if (EqualsText__2qw3(Token, TokenText)) {
      self.CurrentPosition = self.CurrentPosition + 1;
      return true;
   };
   if (StartsWith__2qw3(Token, TokenText)) {
      Token = ZToken__4qw3(new ZToken(), Token.Source, Token.StartIndex + String_size(), Token.EndIndex);
      self.CurrentPosition = self.CurrentPosition + 1;
      Array<ZToken>_add(self.CurrentPosition, Token);
      return true;
   };
   return false;
};
function ZTokenContext_StartsWithToken(self, TokenText){ return StartsWithToken__2qwp(self, TokenText); }

function SkipEmptyStatement__1qwp(self) {
   while (HasNext__1qwp(self)) {
      var Token = ZToken_GetToken(self);
      if (IsIndent__1qw3(Token) || EqualsText__2qw3(Token, ";")) {
         self.CurrentPosition = self.CurrentPosition + 1;
      } else {
         break;
      };
   };
   return;
};
function ZTokenContext_SkipEmptyStatement(self){ return SkipEmptyStatement__1qwp(self); }

function Dump__1qwp(self) {
   var Position = self.CurrentPosition;
   while (Position < (self.TokenList).length) {
      var Token = self.TokenList[Position];
      var DumpedToken = "[";
      DumpedToken = ((DumpedToken + (Position).toString()) + "] ") + toString__1qw3(Token);
      LibZen.PrintDebug(DumpedToken);
      Position = Position + 1;
   };
   return;
};
function ZTokenContext_Dump(self){ return Dump__1qwp(self); }

function ZTokenFunc__3qqc(self, Func, Parent) {
   self.Func = Func;
   self.ParentFunc = Parent;
   return self;
};

function ZVariable__7quu(self, Parent, FuncNode, VarFlag, VarType, VarName, SourceToken) {
   ZSymbolEntry__3quw(self, Parent, FuncNode);
   self.VarFlag = VarFlag;
   self.VarType = VarType;
   self.VarName = VarName;
   self.SourceToken = SourceToken;
   self.VarUniqueIndex = GetVarIndex__1qrb(FuncNode);
   self.UsedCount = 0;
   self.DefCount = 1;
   return self;
};

function IsCaptured__2quu(self, CurrentFunctionNode) {
   if (CurrentFunctionNode == self.Node) {
      return false;
   };
   return true;
};
function ZVariable_IsCaptured(self, CurrentFunctionNode){ return IsCaptured__2quu(self, CurrentFunctionNode); }

function Defined__1quu(self) {
   self.DefCount = self.DefCount + 1;
   return;
};
function ZVariable_Defined(self){ return Defined__1quu(self); }

function Used__1quu(self) {
   self.UsedCount = self.UsedCount + 1;
   return;
};
function ZVariable_Used(self){ return Used__1quu(self); }

function ZArrayType__3qoe(self, TypeFlag, ParamType) {
   ZGenericType__5qev(self, TypeFlag, toString__1qwg(ParamType) + "[]", ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), ParamType);
   return self;
};

function ZAnnotationNode__4qot(self, ParentNode, Token, Anno) {
   ZNode__4qwo(self, ParentNode, Token, 0);
   return self;
};

function IsBreakingBlock__1qot(self) {
   return self.AnnotatedNode.IsBreakingBlock(self.AnnotatedNode);
};
function ZAnnotationNode_IsBreakingBlock(self){ return IsBreakingBlock__1qot(self); }

function Accept__2qot(self, Visitor) {
   self.AnnotatedNode.Accept(self.AnnotatedNode, Visitor);
   return;
};
function ZAnnotationNode_Accept(self, Visitor){ return Accept__2qot(self, Visitor); }

function ZAssertNode__2qo0(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 1);
   return self;
};

function DeSugar__2qo0(self, Generator) {
   var Func = ZMacroFunc_GetMacroFunc(Generator, "assert", ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)), 2);
   if (Func != null) {
      var MacroNode = ZMacroNode__4q06(new ZMacroNode(), self.ParentNode, self.SourceToken, Func);
      Append__2quv(MacroNode, self.AST[0]);
      Append__2quv(MacroNode, ZStringNode__4q4c(new ZStringNode(), MacroNode, null, GetSourceLocation__1qwo(self)));
      return ZSugarNode__3qts(new ZSugarNode(), self, MacroNode);
   } else {
      var MacroNode = ZFuncCallNode__4q4e(new ZFuncCallNode(), self.ParentNode, "assert", ZType__4qwg(new ZType(), 1 << 16, "var", null));
      Append__2quv(MacroNode, self.AST[0]);
      return ZSugarNode__3qts(new ZSugarNode(), self, MacroNode);
   };
};
function ZAssertNode_DeSugar(self, Generator){ return DeSugar__2qo0(self, Generator); }

function ZBinaryNode__5qos(self, ParentNode, SourceToken, Left, Pattern) {
   ZNode__4qwo(self, ParentNode, SourceToken, 2);
   Set__3qwo(self, 0, Left);
   console.assert(Pattern != null, "(libzen/libzen.zen:3452)");
   self.Pattern = Pattern;
   return self;
};

function IsRightJoin__2qos(self, Node) {
   if ((Node).constructor.name == (ZBinaryNode).name) {
      return IsRightJoin__2qy7(self.Pattern, (Node).Pattern);
   };
   return false;
};
function ZBinaryNode_IsRightJoin(self, Node){ return IsRightJoin__2qos(self, Node); }

function RightJoin__3qos(self, ParentNode, RightNode) {
   var RightLeftNode = RightNode.AST[0];
   if (IsRightJoin__2qos(self, RightLeftNode)) {
      Set__3qwo(RightNode, 0, ZNode_RightJoin(self, ParentNode, RightLeftNode));
   } else {
      Set__3qwo(RightNode, 0, self);
      Set__3qwo(self, 1, RightLeftNode);
   };
   return RightNode;
};
function ZBinaryNode_RightJoin(self, ParentNode, RightNode){ return RightJoin__3qos(self, ParentNode, RightNode); }

function AppendParsedRightNode__3qos(self, ParentNode, TokenContext) {
   var RightNode = ZNode_ParsePattern(TokenContext, ParentNode, "$Expression$", true);
   if (IsErrorNode__1qwo(RightNode)) {
      return RightNode;
   };
   if (IsRightJoin__2qos(self, RightNode)) {
      return ZNode_RightJoin(self, ParentNode, RightNode);
   };
   Set__3qwo(self, 1, RightNode);
   return self;
};
function ZBinaryNode_AppendParsedRightNode(self, ParentNode, TokenContext){ return AppendParsedRightNode__3qos(self, ParentNode, TokenContext); }

function TryMacroNode__2qos(self, Generator) {
   if (!ZType_GetAstType(self, 0).IsVarType(ZType_GetAstType(self, 0)) && !ZType_GetAstType(self, 1).IsVarType(ZType_GetAstType(self, 1))) {
      var Op = GetText__1qw3(self.SourceToken);
      var Func = ZFunc_GetDefinedFunc(Generator, Op, ZType_GetAstType(self, 0), 2);
      if ((Func).constructor.name == (ZMacroFunc).name) {
         var MacroNode = ZMacroNode__4q06(new ZMacroNode(), self.ParentNode, self.SourceToken, Func);
         Append__2quv(MacroNode, self.AST[0]);
         Append__2quv(MacroNode, self.AST[1]);
         return MacroNode;
      };
   };
   return self;
};
function ZBinaryNode_TryMacroNode(self, Generator){ return TryMacroNode__2qos(self, Generator); }

function Accept__2qos(self, Visitor) {
   Visitor.VisitBinaryNode(Visitor, self);
   return;
};
function ZBinaryNode_Accept(self, Visitor){ return Accept__2qos(self, Visitor); }

function ZBreakNode__2qol(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 0);
   return self;
};

function Accept__2qol(self, Visitor) {
   Visitor.VisitBreakNode(Visitor, self);
   return;
};
function ZBreakNode_Accept(self, Visitor){ return Accept__2qol(self, Visitor); }

function ZCastNode__4qo6(self, ParentNode, CastType, Node) {
   ZNode__4qwo(self, ParentNode, null, 1);
   self.Type = CastType;
   if (Node != null) {
      Set__3qwo(self, 0, Node);
   };
   return self;
};

function Accept__2qo6(self, Visitor) {
   Visitor.VisitCastNode(Visitor, self);
   return;
};
function ZCastNode_Accept(self, Visitor){ return Accept__2qo6(self, Visitor); }

function ToFuncCallNode__2qo6(self, Func) {
   if ((Func).constructor.name == (ZMacroFunc).name) {
      var FuncNode = ZMacroNode__4q06(new ZMacroNode(), self.ParentNode, self.SourceToken, Func);
      Append__2quv(FuncNode, self.AST[0]);
      return FuncNode;
   } else {
      var FuncNode = ZFuncCallNode__4q4e(new ZFuncCallNode(), self.ParentNode, Func.FuncName, ZFuncType_GetFuncType(Func));
      FuncNode.SourceToken = self.SourceToken;
      Append__2quv(FuncNode, self.AST[0]);
      return FuncNode;
   };
};
function ZCastNode_ToFuncCallNode(self, Func){ return ToFuncCallNode__2qo6(self, Func); }

function ZCatchNode__2qov(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 1);
   return self;
};

function SetTypeInfo__3qov(self, TypeToken, Type) {
   self.ExceptionType = Type;
   return;
};
function ZCatchNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3qov(self, TypeToken, Type); }

function SetNameInfo__3qov(self, NameToken, Name) {
   self.ExceptionName = Name;
   self.NameToken = NameToken;
   return;
};
function ZCatchNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qov(self, NameToken, Name); }

function ZComparatorNode__5qo7(self, ParentNode, SourceToken, Left, Pattern) {
   ZBinaryNode__5qos(self, ParentNode, SourceToken, Left, Pattern);
   return self;
};

function Accept__2qo7(self, Visitor) {
   Visitor.VisitComparatorNode(Visitor, self);
   return;
};
function ZComparatorNode_Accept(self, Visitor){ return Accept__2qo7(self, Visitor); }

function ZConstNode_CreateDefaultValueNode__3qwo(ParentNode, Type, FieldName) {
   if (IsIntType__1qwg(Type)) {
      return ZIntNode__4q0o(new ZIntNode(), ParentNode, null, 0);
   } else if (IsBooleanType__1qwg(Type)) {
      return ZBooleanNode__4qa5(new ZBooleanNode(), ParentNode, null, false);
   } else if (IsFloatType__1qwg(Type)) {
      return ZFloatNode__4qp4(new ZFloatNode(), ParentNode, null, 0.0);
   };
   return ZNullNode__3q4d(new ZNullNode(), ParentNode, null);
};
function ZNode_ZConstNode_CreateDefaultValueNode(ParentNode, Type, FieldName){ return ZConstNode_CreateDefaultValueNode__3qwo(ParentNode, Type, FieldName); }

function ZConstNode__3qo2(self, ParentNode, SourceToken) {
   ZNode__4qwo(self, ParentNode, SourceToken, 0);
   return self;
};

function ZEmptyNode__3qpw(self, ParentNode, Token) {
   ZNode__4qwo(self, ParentNode, Token, 0);
   return self;
};

function ZErrorNode__4qpr(self, ParentNode, SourceToken, ErrorMessage) {
   ZConstNode__3qo2(self, ParentNode, SourceToken);
   self.ErrorMessage = ErrorMessage;
   return self;
};

function ZErrorNode__3qpr(self, Node, ErrorMessage) {
   ZConstNode__3qo2(self, Node.ParentNode, Node.SourceToken);
   self.ErrorMessage = ErrorMessage;
   return self;
};

function Accept__2qpr(self, Visitor) {
   Visitor.VisitErrorNode(Visitor, self);
   return;
};
function ZErrorNode_Accept(self, Visitor){ return Accept__2qpr(self, Visitor); }

function ZFieldNode__2qpi(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 1);
   return self;
};

function SetTypeInfo__3qpi(self, TypeToken, Type) {
   self.DeclType = Type;
   return;
};
function ZFieldNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3qpi(self, TypeToken, Type); }

function SetNameInfo__3qpi(self, NameToken, Name) {
   self.FieldName = Name;
   self.NameToken = NameToken;
   return;
};
function ZFieldNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qpi(self, NameToken, Name); }

function ZFloatNode__4qp4(self, ParentNode, Token, Value) {
   ZConstNode__3qo2(self, ParentNode, Token);
   self.Type = ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null));
   self.FloatValue = Value;
   return self;
};

function Accept__2qp4(self, Visitor) {
   Visitor.VisitFloatNode(Visitor, self);
   return;
};
function ZFloatNode_Accept(self, Visitor){ return Accept__2qp4(self, Visitor); }

function ZGetIndexNode__3qpd(self, ParentNode, RecvNode) {
   ZNode__4qwo(self, ParentNode, null, 2);
   self.AST[0] = ZNode_SetChild(self, RecvNode);
   return self;
};

function Accept__2qpd(self, Visitor) {
   Visitor.VisitGetIndexNode(Visitor, self);
   return;
};
function ZGetIndexNode_Accept(self, Visitor){ return Accept__2qpd(self, Visitor); }

function ZGetNameNode__4qph(self, ParentNode, Token, NativeName) {
   ZNode__4qwo(self, ParentNode, Token, 0);
   self.VarName = NativeName;
   return self;
};

function ZGetNameNode__3qph(self, ParentNode, ResolvedFunc) {
   ZNode__4qwo(self, ParentNode, null, 0);
   self.VarName = ResolvedFunc.FuncName;
   self.Type = ZFuncType_GetFuncType(ResolvedFunc);
   return self;
};

function Accept__2qph(self, Visitor) {
   Visitor.VisitGetNameNode(Visitor, self);
   return;
};
function ZGetNameNode_Accept(self, Visitor){ return Accept__2qph(self, Visitor); }

function ToGlobalNameNode__1qph(self) {
   return ZGlobalNameNode__6qpv(new ZGlobalNameNode(), self.ParentNode, self.SourceToken, self.Type, self.VarName, false);
};
function ZGetNameNode_ToGlobalNameNode(self){ return ToGlobalNameNode__1qph(self); }

function ZGetterNode__3qp1(self, ParentNode, RecvNode) {
   ZNode__4qwo(self, ParentNode, null, 1);
   Set__3qwo(self, 0, RecvNode);
   return self;
};

function SetNameInfo__3qp1(self, NameToken, Name) {
   self.FieldName = Name;
   self.NameToken = NameToken;
   return;
};
function ZGetterNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qp1(self, NameToken, Name); }

function Accept__2qp1(self, Visitor) {
   Visitor.VisitGetterNode(Visitor, self);
   return;
};
function ZGetterNode_Accept(self, Visitor){ return Accept__2qp1(self, Visitor); }

function IsStaticField__1qp1(self) {
   return (self.AST[0]).constructor.name == (ZTypeNode).name;
};
function ZGetterNode_IsStaticField(self){ return IsStaticField__1qp1(self); }

function ZGlobalNameNode__6qpv(self, ParentNode, SourceToken, Type, GlobalName, IsStaticFuncName) {
   ZNode__4qwo(self, ParentNode, SourceToken, 0);
   self.GlobalName = GlobalName;
   self.Type = Type;
   self.IsStaticFuncName = IsStaticFuncName;
   return self;
};

function IsGivenName__1qpv(self) {
   return (!self.IsStaticFuncName);
};
function ZGlobalNameNode_IsGivenName(self){ return IsGivenName__1qpv(self); }

function Accept__2qpv(self, Visitor) {
   Visitor.VisitGlobalNameNode(Visitor, self);
   return;
};
function ZGlobalNameNode_Accept(self, Visitor){ return Accept__2qpv(self, Visitor); }

function ZGroupNode__2qp7(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 1);
   return self;
};

function Accept__2qp7(self, Visitor) {
   Visitor.VisitGroupNode(Visitor, self);
   return;
};
function ZGroupNode_Accept(self, Visitor){ return Accept__2qp7(self, Visitor); }

function ZIfNode__2qp2(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 3);
   return self;
};

function Accept__2qp2(self, Visitor) {
   Visitor.VisitIfNode(Visitor, self);
   return;
};
function ZIfNode_Accept(self, Visitor){ return Accept__2qp2(self, Visitor); }

function ZImportNode__2q0w(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 0);
   return self;
};

function SetNameInfo__3q0w(self, NameToken, Name) {
   if (self.ResourcePath == null) {
      self.ResourcePath = Name;
      self.ResourceToken = NameToken;
   } else {
      self.Alias = Name;
   };
   return;
};
function ZImportNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3q0w(self, NameToken, Name); }

function ZInstanceOfNode__4q0t(self, ParentNode, Token, LeftNode) {
   ZNode__4qwo(self, ParentNode, Token, 1);
   Set__3qwo(self, 0, LeftNode);
   return self;
};

function SetTypeInfo__3q0t(self, TypeToken, Type) {
   self.TargetType = Type;
   return;
};
function ZInstanceOfNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3q0t(self, TypeToken, Type); }

function Accept__2q0t(self, Visitor) {
   Visitor.VisitInstanceOfNode(Visitor, self);
   return;
};
function ZInstanceOfNode_Accept(self, Visitor){ return Accept__2q0t(self, Visitor); }

function ZIntNode__4q0o(self, ParentNode, Token, Value) {
   ZConstNode__3qo2(self, ParentNode, Token);
   self.Type = ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null));
   self.IntValue = Value;
   return self;
};

function Accept__2q0o(self, Visitor) {
   Visitor.VisitIntNode(Visitor, self);
   return;
};
function ZIntNode_Accept(self, Visitor){ return Accept__2q0o(self, Visitor); }

function ZLetNode__2q04(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 1);
   return self;
};

function SetNameInfo__3q04(self, NameToken, Name) {
   self.Symbol = Name;
   self.SymbolToken = NameToken;
   return;
};
function ZLetNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3q04(self, NameToken, Name); }

function SetTypeInfo__3q04(self, TypeToken, Type) {
   self.SymbolType = Type;
   return;
};
function ZLetNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3q04(self, TypeToken, Type); }

function Accept__2q04(self, Visitor) {
   Visitor.VisitLetNode(Visitor, self);
   return;
};
function ZLetNode_Accept(self, Visitor){ return Accept__2q04(self, Visitor); }

function ToGlobalNameNode__1q04(self) {
   return ZGlobalNameNode__6qpv(new ZGlobalNameNode(), null, self.SymbolToken, ZType_GetAstType(self, 0), self.GlobalName, false);
};
function ZLetNode_ToGlobalNameNode(self){ return ToGlobalNameNode__1q04(self); }

function ZListNode__4quv(self, ParentNode, SourceToken, Size) {
   ZNode__4qwo(self, ParentNode, SourceToken, Size);
   self.ListStartIndex = Size;
   return self;
};

function Append__2quv(self, Node) {
   if (self.AST == null) {
      self.AST = LibZen.NewNodeArray(1);
      Set__3qwo(self, 0, Node);
   } else {
      var newAST = LibZen.NewNodeArray((self.AST).length + 1);
      LibZen.ArrayCopy(self.AST, 0, newAST, 0, (self.AST).length);
      self.AST = newAST;
      Set__3qwo(self, (self.AST).length - 1, Node);
   };
   return;
};
function ZListNode_Append(self, Node){ return Append__2quv(self, Node); }

function GetListSize__1quv(self) {
   return GetAstSize__1qwo(self) - self.ListStartIndex;
};
function ZListNode_GetListSize(self){ return GetListSize__1quv(self); }

function GetListAt__2quv(self, Index) {
   return self.AST[self.ListStartIndex + Index];
};
function ZListNode_GetListAt(self, Index){ return GetListAt__2quv(self, Index); }

function SetListAt__3quv(self, Index, Node) {
   Set__3qwo(self, Index + self.ListStartIndex, Node);
   return;
};
function ZListNode_SetListAt(self, Index, Node){ return SetListAt__3quv(self, Index, Node); }

function InsertListAt__3quv(self, Index, Node) {
   if (self.AST == null || Index < 0 || (self.AST).length == Index) {
      Append__2quv(self, Node);
   } else {
      var newAST = LibZen.NewNodeArray((self.AST).length + 1);
      Index = self.ListStartIndex + Index;
      LibZen.ArrayCopy(self.AST, 0, newAST, 0, Index);
      Set__3qwo(self, Index, Node);
      LibZen.ArrayCopy(self.AST, Index, newAST, Index + 1, (self.AST).length - Index);
      self.AST = newAST;
   };
   return;
};
function ZListNode_InsertListAt(self, Index, Node){ return InsertListAt__3quv(self, Index, Node); }

function RemoveListAt__2quv(self, Index) {
   var Removed = ZNode_GetListAt(self, Index);
   var newAST = LibZen.NewNodeArray((self.AST).length - 1);
   var RemovedIndex = self.ListStartIndex + Index;
   LibZen.ArrayCopy(self.AST, 0, newAST, 0, RemovedIndex);
   LibZen.ArrayCopy(self.AST, RemovedIndex + 1, newAST, RemovedIndex, (self.AST).length - (RemovedIndex + 1));
   self.AST = newAST;
   return Removed;
};
function ZListNode_RemoveListAt(self, Index){ return RemoveListAt__2quv(self, Index); }

function ClearListAfter__2quv(self, Size) {
   if (Size < GetListSize__1quv(self)) {
      var newsize = self.ListStartIndex + Size;
      if (newsize == 0) {
         self.AST = null;
      } else {
         var newAST = LibZen.NewNodeArray(newsize);
         LibZen.ArrayCopy(self.AST, 0, newAST, 0, newsize);
         self.AST = newAST;
      };
   };
   return;
};
function ZListNode_ClearListAfter(self, Size){ return ClearListAfter__2quv(self, Size); }

function ZMacroNode__4q06(self, ParentNode, SourceToken, MacroFunc) {
   ZListNode__4quv(self, ParentNode, SourceToken, 0);
   self.MacroFunc = MacroFunc;
   console.assert(MacroFunc != null, "(libzen/libzen.zen:3822)");
   return self;
};

function GetFuncType__1q06(self) {
   return ZFuncType_GetFuncType(self.MacroFunc);
};
function ZMacroNode_GetFuncType(self){ return GetFuncType__1q06(self); }

function GetMacroText__1q06(self) {
   var Func = self.MacroFunc;
   if ((Func).constructor.name == (ZSourceMacro).name) {
      return (Func).Macro;
   };
   return "";
};
function ZMacroNode_GetMacroText(self){ return GetMacroText__1q06(self); }

function Accept__2q06(self, Visitor) {
   Visitor.VisitMacroNode(Visitor, self);
   return;
};
function ZMacroNode_Accept(self, Visitor){ return Accept__2q06(self, Visitor); }

function ZMapEntryNode__2q0b(self, ParentNode) {
   ZNode__4qwo(self, ParentNode, null, 2);
   return self;
};

function ZMapLiteralNode__2q0m(self, ParentNode) {
   ZListNode__4quv(self, ParentNode, null, 0);
   return self;
};

function GetMapEntryNode__2q0m(self, Index) {
   var Node = ZNode_GetListAt(self, Index);
   if ((Node).constructor.name == (ZMapEntryNode).name) {
      return Node;
   };
   return null;
};
function ZMapLiteralNode_GetMapEntryNode(self, Index){ return GetMapEntryNode__2q0m(self, Index); }

function Accept__2q0m(self, Visitor) {
   Visitor.VisitMapLiteralNode(Visitor, self);
   return;
};
function ZMapLiteralNode_Accept(self, Visitor){ return Accept__2q0m(self, Visitor); }

function ZMethodCallNode__3q02(self, ParentNode, RecvNode) {
   ZListNode__4quv(self, ParentNode, null, 1);
   Set__3qwo(self, 0, RecvNode);
   return self;
};

function SetNameInfo__3q02(self, NameToken, Name) {
   self.MethodName = Name;
   self.MethodToken = NameToken;
   return;
};
function ZMethodCallNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3q02(self, NameToken, Name); }

function Accept__2q02(self, Visitor) {
   Visitor.VisitMethodCallNode(Visitor, self);
   return;
};
function ZMethodCallNode_Accept(self, Visitor){ return Accept__2q02(self, Visitor); }

function ToGetterFuncCall__1q02(self) {
   var Getter = ZGetterNode__3qp1(new ZGetterNode(), null, self.AST[0]);
   Getter.SetNameInfo(Getter, self.MethodToken, self.MethodName);
   var FuncNode = ZFuncCallNode__3q4e(new ZFuncCallNode(), self.ParentNode, Getter);
   FuncNode.SourceToken = self.SourceToken;
   Append__2quv(FuncNode, self.AST[0]);
   var i = 0;
   while (i < GetListSize__1quv(self)) {
      Append__2quv(FuncNode, ZNode_GetListAt(self, i));
      i = i + 1;
   };
   return FuncNode;
};
function ZMethodCallNode_ToGetterFuncCall(self){ return ToGetterFuncCall__1q02(self); }

function ToFuncCallNode__2q02(self, Func) {
   if ((Func).constructor.name == (ZMacroFunc).name) {
      var MacroNode = ZMacroNode__4q06(new ZMacroNode(), self.ParentNode, self.MethodToken, Func);
      Append__2quv(MacroNode, self.AST[0]);
      var i = 0;
      while (i < GetListSize__1quv(self)) {
         Append__2quv(MacroNode, ZNode_GetListAt(self, i));
         i = i + 1;
      };
      return MacroNode;
   } else {
      var FuncNode = ZFuncCallNode__4q4e(new ZFuncCallNode(), self.ParentNode, Func.FuncName, ZFuncType_GetFuncType(Func));
      FuncNode.SourceToken = self.MethodToken;
      Append__2quv(FuncNode, self.AST[0]);
      var i = 0;
      while (i < GetListSize__1quv(self)) {
         Append__2quv(FuncNode, ZNode_GetListAt(self, i));
         i = i + 1;
      };
      return FuncNode;
   };
};
function ZMethodCallNode_ToFuncCallNode(self, Func){ return ToFuncCallNode__2q02(self, Func); }

function ZNewArrayNode__4q4y(self, ParentNode, Type, Token) {
   ZListNode__4quv(self, ParentNode, null, 0);
   return self;
};

function ZNewObjectNode__2q4i(self, ParentNode) {
   ZListNode__4quv(self, ParentNode, null, 0);
   return self;
};

function Accept__2q4i(self, Visitor) {
   Visitor.VisitNewObjectNode(Visitor, self);
   return;
};
function ZNewObjectNode_Accept(self, Visitor){ return Accept__2q4i(self, Visitor); }

function ToFuncCallNode__2q4i(self, Func) {
   var FuncNode = null;
   if ((Func).constructor.name == (ZMacroFunc).name) {
      FuncNode = ZMacroNode__4q06(new ZMacroNode(), self.ParentNode, self.SourceToken, Func);
   } else {
      FuncNode = ZFuncCallNode__4q4e(new ZFuncCallNode(), self.ParentNode, Func.FuncName, ZFuncType_GetFuncType(Func));
      FuncNode.SourceToken = self.SourceToken;
   };
   Append__2quv(FuncNode, self);
   var i = 0;
   while (i < GetListSize__1quv(self)) {
      Append__2quv(FuncNode, ZNode_GetListAt(self, i));
      i = i + 1;
   };
   ClearListAfter__2quv(self, 0);
   return FuncNode;
};
function ZNewObjectNode_ToFuncCallNode(self, Func){ return ToFuncCallNode__2q4i(self, Func); }

function ZNotNode__3q44(self, ParentNode, Token) {
   ZUnaryNode__3qyp(self, ParentNode, Token);
   return self;
};

function Accept__2q44(self, Visitor) {
   Visitor.VisitNotNode(Visitor, self);
   return;
};
function ZNotNode_Accept(self, Visitor){ return Accept__2q44(self, Visitor); }

function ZNullNode__3q4d(self, ParentNode, SourceToken) {
   ZConstNode__3qo2(self, ParentNode, SourceToken);
   return self;
};

function Accept__2q4d(self, Visitor) {
   Visitor.VisitNullNode(Visitor, self);
   return;
};
function ZNullNode_Accept(self, Visitor){ return Accept__2q4d(self, Visitor); }

function ZOrNode__5q4h(self, ParentNode, Token, Left, Pattern) {
   ZBinaryNode__5qos(self, ParentNode, Token, Left, Pattern);
   return self;
};

function Accept__2q4h(self, Visitor) {
   Visitor.VisitOrNode(Visitor, self);
   return;
};
function ZOrNode_Accept(self, Visitor){ return Accept__2q4h(self, Visitor); }

function ZPrototypeNode__2q4l(self, ParentNode) {
   ZListNode__4quv(self, ParentNode, null, 0);
   return self;
};

function SetTypeInfo__3q4l(self, TypeToken, Type) {
   self.ReturnType = Type;
   return;
};
function ZPrototypeNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3q4l(self, TypeToken, Type); }

function SetNameInfo__3q4l(self, NameToken, Name) {
   self.FuncName = Name;
   self.NameToken = NameToken;
   return;
};
function ZPrototypeNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3q4l(self, NameToken, Name); }

function GetParamNode__2q4l(self, Index) {
   var Node = ZNode_GetListAt(self, Index);
   if ((Node).constructor.name == (ZParamNode).name) {
      return Node;
   };
   return null;
};
function ZPrototypeNode_GetParamNode(self, Index){ return GetParamNode__2q4l(self, Index); }

function GetFuncType__1q4l(self) {
   var TypeList = [];
   TypeList.push(ZType_null(self.ReturnType));
   var i = 0;
   while (i < GetListSize__1quv(self)) {
      var Node = ZParamNode_GetParamNode(self, i);
      var ParamType = ZType_null(Node.Type);
      TypeList.push(ParamType);
      i = i + 1;
   };
   return ZFuncType_ZTypePool_LookupFuncType(TypeList);
};
function ZPrototypeNode_GetFuncType(self){ return GetFuncType__1q4l(self); }

function ZStringNode__4q4c(self, ParentNode, Token, Value) {
   ZConstNode__3qo2(self, ParentNode, Token);
   self.Type = ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null));
   self.StringValue = Value;
   return self;
};

function Accept__2q4c(self, Visitor) {
   Visitor.VisitStringNode(Visitor, self);
   return;
};
function ZStringNode_Accept(self, Visitor){ return Accept__2q4c(self, Visitor); }

function ZStupidCastErrorNode__3q4n(self, Node, ErrorMessage) {
   ZErrorNode__3qpr(self, Node, ErrorMessage);
   self.ErrorNode = Node;
   return self;
};

function ZTypeNode__4qu4(self, ParentNode, SourceToken, ParsedType) {
   ZConstNode__3qo2(self, ParentNode, SourceToken);
   self.Type = ParsedType;
   return self;
};

function ZGenerator__3qw4(self, LanguageExtension, TargetVersion) {
   self.RootNameSpace = ZNameSpace__3qwt(new ZNameSpace(), self, null);
   self.GrammarInfo = "";
   self.LanguageExtention = LanguageExtension;
   self.TargetVersion = TargetVersion;
   self.OutputFile = null;
   self.Logger = new ZLogger();
   self.StoppedVisitor = false;
   return self;
};

function ImportLocalGrammar__2qw4(self, NameSpace) {
   return;
};
function ZGenerator_ImportLocalGrammar(self, NameSpace){ return ImportLocalGrammar__2qw4(self, NameSpace); }

function WriteTo__2qw4(self, FileName) {
   return;
};
function ZGenerator_WriteTo(self, FileName){ return WriteTo__2qw4(self, FileName); }

function GetSourceText__1qw4(self) {
   return null;
};
function ZGenerator_GetSourceText(self){ return GetSourceText__1qw4(self); }

function NameOutputFile__2qw4(self, FileName) {
   if (FileName != null) {
      return (FileName + ".") + self.LanguageExtention;
   };
   return FileName;
};
function ZGenerator_NameOutputFile(self, FileName){ return NameOutputFile__2qw4(self, FileName); }

function EnableVisitor__1qw4(self) {
   self.StoppedVisitor = false;
   return;
};
function ZGenerator_EnableVisitor(self){ return EnableVisitor__1qw4(self); }

function StopVisitor__1qw4(self) {
   self.StoppedVisitor = true;
   return;
};
function ZGenerator_StopVisitor(self){ return StopVisitor__1qw4(self); }

function IsVisitable__1qw4(self) {
   return !self.StoppedVisitor;
};
function ZGenerator_IsVisitable(self){ return IsVisitable__1qw4(self); }

function GetGrammarInfo__1qw4(self) {
   return self.GrammarInfo;
};
function ZGenerator_GetGrammarInfo(self){ return GetGrammarInfo__1qw4(self); }

function AppendGrammarInfo__2qw4(self, GrammarInfo) {
   self.GrammarInfo = (self.GrammarInfo + GrammarInfo) + " ";
   return;
};
function ZGenerator_AppendGrammarInfo(self, GrammarInfo){ return AppendGrammarInfo__2qw4(self, GrammarInfo); }

function GetTargetLangInfo__1qw4(self) {
   return self.LanguageExtention + self.TargetVersion;
};
function ZGenerator_GetTargetLangInfo(self){ return GetTargetLangInfo__1qw4(self); }

function GetFieldType__3qw4(self, BaseType, Name) {
   return ZType__4qwg(new ZType(), 1 << 16, "var", null);
};
function ZGenerator_GetFieldType(self, BaseType, Name){ return GetFieldType__3qw4(self, BaseType, Name); }

function GetSetterType__3qw4(self, BaseType, Name) {
   return ZType__4qwg(new ZType(), 1 << 16, "var", null);
};
function ZGenerator_GetSetterType(self, BaseType, Name){ return GetSetterType__3qw4(self, BaseType, Name); }

function GetConstructorFuncType__3qw4(self, ClassType, List) {
   return ZFuncType__3qe0(new ZFuncType(), "Func", null);
};
function ZGenerator_GetConstructorFuncType(self, ClassType, List){ return GetConstructorFuncType__3qw4(self, ClassType, List); }

function GetMethodFuncType__4qw4(self, RecvType, MethodName, List) {
   return ZFuncType__3qe0(new ZFuncType(), "Func", null);
};
function ZGenerator_GetMethodFuncType(self, RecvType, MethodName, List){ return GetMethodFuncType__4qw4(self, RecvType, MethodName, List); }

function GetUniqueNumber__1qw4(self) {
   var UniqueNumber = self.UniqueNumber;
   self.UniqueNumber = self.UniqueNumber + 1;
   return UniqueNumber;
};
function ZGenerator_GetUniqueNumber(self){ return GetUniqueNumber__1qw4(self); }

function NameGlobalSymbol__2qw4(self, Symbol) {
   return (Symbol + "_Z") + (GetUniqueNumber__1qw4(self)).toString();
};
function ZGenerator_NameGlobalSymbol(self, Symbol){ return NameGlobalSymbol__2qw4(self, Symbol); }

function NameClass__2qw4(self, ClassType) {
   return (ClassType.ShortName + "") + (ClassType.TypeId).toString();
};
function ZGenerator_NameClass(self, ClassType){ return NameClass__2qw4(self, ClassType); }

function SetDefinedFunc__2qw4(self, Func) {
   self.DefinedFuncMap[GetSignature__1qep(Func)] = Func;
   return;
};
function ZGenerator_SetDefinedFunc(self, Func){ return SetDefinedFunc__2qw4(self, Func); }

function SetPrototype__4qw4(self, Node, FuncName, FuncType) {
   var Func = ZFunc_GetDefinedFunc(self, FuncName, FuncType);
   if (Func != null) {
      if (!Equals__2qwg(FuncType, ZFuncType_GetFuncType(Func))) {
         ZLogger_LogError__2qw3(Node.SourceToken, "function has been defined diffrently: " + toString__1qwg(ZFuncType_GetFuncType(Func)));
         return null;
      };
      if ((Func).constructor.name == (ZPrototype).name) {
         return Func;
      };
      ZLogger_LogError__2qw3(Node.SourceToken, "function has been defined as macro" + toString__1qep(Func));
      return null;
   };
   var Proto = ZPrototype__5qry(new ZPrototype(), 0, FuncName, FuncType, Node.SourceToken);
   self.DefinedFuncMap[GetSignature__1qep(Proto)] = Proto;
   return Proto;
};
function ZGenerator_SetPrototype(self, Node, FuncName, FuncType){ return SetPrototype__4qw4(self, Node, FuncName, FuncType); }

function GetDefinedFunc__2qw4(self, GlobalName) {
   var Func = self.DefinedFuncMap[GlobalName];
   if (Func == null && LibZen.IsLetter(LibZen.GetChar(GlobalName, 0))) {
      Func = self.DefinedFuncMap[LibZen.AnotherName(GlobalName)];
   };
   return Func;
};
function ZGenerator_GetDefinedFunc(self, GlobalName){ return GetDefinedFunc__2qw4(self, GlobalName); }

function GetDefinedFunc__3qw4(self, FuncName, FuncType) {
   return ZFunc_GetDefinedFunc(self, StringfySignature__2qe0(FuncType, FuncName));
};
function ZGenerator_GetDefinedFunc(self, FuncName, FuncType){ return GetDefinedFunc__3qw4(self, FuncName, FuncType); }

function GetDefinedFunc__4qw4(self, FuncName, RecvType, FuncParamSize) {
   return ZFunc_GetDefinedFunc(self, ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, RecvType));
};
function ZGenerator_GetDefinedFunc(self, FuncName, RecvType, FuncParamSize){ return GetDefinedFunc__4qw4(self, FuncName, RecvType, FuncParamSize); }

function LookupFunc__4qw4(self, FuncName, RecvType, FuncParamSize) {
   var Func = ZFunc_GetDefinedFunc(self, ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, RecvType));
   while (Func == null) {
      RecvType = ZType_null(RecvType);
      if (RecvType == null) {
         break;
      };
      Func = ZFunc_GetDefinedFunc(self, ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, RecvType));
   };
   return Func;
};
function ZGenerator_LookupFunc(self, FuncName, RecvType, FuncParamSize){ return LookupFunc__4qw4(self, FuncName, RecvType, FuncParamSize); }

function GetMacroFunc__4qw4(self, FuncName, RecvType, FuncParamSize) {
   var Func = ZFunc_GetDefinedFunc(self, ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, RecvType));
   if ((Func).constructor.name == (ZMacroFunc).name) {
      return (Func);
   };
   return null;
};
function ZGenerator_GetMacroFunc(self, FuncName, RecvType, FuncParamSize){ return GetMacroFunc__4qw4(self, FuncName, RecvType, FuncParamSize); }

function NameConverterFunc__3qw4(self, FromType, ToType) {
   return (GetUniqueName__1qwg(FromType) + "T") + GetUniqueName__1qwg(ToType);
};
function ZGenerator_NameConverterFunc(self, FromType, ToType){ return NameConverterFunc__3qw4(self, FromType, ToType); }

function SetConverterFunc__4qw4(self, FromType, ToType, Func) {
   self.DefinedFuncMap[NameConverterFunc__3qw4(self, FromType, ToType)] = Func;
   return;
};
function ZGenerator_SetConverterFunc(self, FromType, ToType, Func){ return SetConverterFunc__4qw4(self, FromType, ToType, Func); }

function LookupConverterFunc__3qw4(self, FromType, ToType) {
   while (FromType != null) {
      var Func = self.DefinedFuncMap[NameConverterFunc__3qw4(self, FromType, ToType)];
      if (Func != null) {
         return Func;
      };
      FromType = FromType.GetSuperType(FromType);
   };
   return null;
};
function ZGenerator_LookupConverterFunc(self, FromType, ToType){ return LookupConverterFunc__3qw4(self, FromType, ToType); }

function GetCoercionFunc__3qw4(self, FromType, ToType) {
   while (FromType != null) {
      var Func = self.DefinedFuncMap[NameConverterFunc__3qw4(self, FromType, ToType)];
      if (Func != null && IsCoercionFunc__1qep(Func)) {
         return Func;
      };
      FromType = FromType.GetSuperType(FromType);
   };
   return null;
};
function ZGenerator_GetCoercionFunc(self, FromType, ToType){ return GetCoercionFunc__3qw4(self, FromType, ToType); }

function VisitExtendedNode__2qw4(self, Node) {
   var DeNode = Node.DeSugar(Node, self);
   DeNode.Accept(DeNode, self);
   return;
};
function ZGenerator_VisitExtendedNode(self, Node){ return VisitExtendedNode__2qw4(self, Node); }

function VisitSugarNode__2qw4(self, Node) {
   Node.AST[0].Accept(Node.AST[0], self);
   return;
};
function ZGenerator_VisitSugarNode(self, Node){ return VisitSugarNode__2qw4(self, Node); }

function ZIndentToken__4qak(self, Source, StartIndex, EndIndex) {
   ZToken__4qw3(self, Source, StartIndex, EndIndex);
   return self;
};

function ZPatternToken__5qa9(self, Source, StartIndex, EndIndex, PresetPattern) {
   ZToken__4qw3(self, Source, StartIndex, EndIndex);
   self.PresetPattern = PresetPattern;
   return self;
};

function ZSourceEngine__3qws(self, TypeChecker, Generator) {
   self.TypeChecker = TypeChecker;
   self.Generator = Generator;
   self.Logger = Generator.Logger;
   return self;
};

function IsVisitable__1qws(self) {
   return self.IsVisitableFlag;
};
function ZSourceEngine_IsVisitable(self){ return IsVisitable__1qws(self); }

function EnableVisitor__1qws(self) {
   self.IsVisitableFlag = true;
   return;
};
function ZSourceEngine_EnableVisitor(self){ return EnableVisitor__1qws(self); }

function StopVisitor__1qws(self) {
   self.IsVisitableFlag = false;
   return;
};
function ZSourceEngine_StopVisitor(self){ return StopVisitor__1qws(self); }

function Eval2__2qws(self, Node) {
   if (self.IsVisitable(self)) {
      Node.Accept(Node, self);
   };
   return;
};
function ZSourceEngine_Eval2(self, Node){ return Eval2__2qws(self, Node); }

function VisitPrototypeNode__2qws(self, Node) {
   var FuncType = ZFuncType_GetFuncType(Node);
   ZPrototype_SetPrototype(self.Generator, Node, Node.FuncName, FuncType);
   return;
};
function ZSourceEngine_VisitPrototypeNode(self, Node){ return VisitPrototypeNode__2qws(self, Node); }

function VisitImportNode__2qws(self, Node) {
   Node.Import(Node);
   return;
};
function ZSourceEngine_VisitImportNode(self, Node){ return VisitImportNode__2qws(self, Node); }

function Exec2__3qws(self, Node, IsInteractive) {
   self.InteractiveContext = IsInteractive;
   self.EnableVisitor(self);
   if ((Node).constructor.name == (ZPrototypeNode).name) {
      VisitPrototypeNode__2qws(self, Node);
   } else if ((Node).constructor.name == (ZImportNode).name) {
      VisitImportNode__2qws(self, Node);
   } else {
      Node = ZNode_CheckType(self.TypeChecker, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
      Eval2__2qws(self, Node);
   };
   return;
};
function ZSourceEngine_Exec2(self, Node, IsInteractive){ return Exec2__3qws(self, Node, IsInteractive); }

function Translate__4qws(self, ScriptText, FileName, LineNumber) {
   var TopBlockNode = ZBlockNode__2qtp(new ZBlockNode(), self.Generator.RootNameSpace);
   var TokenContext = ZTokenContext__6qwp(new ZTokenContext(), self.Generator, self.Generator.RootNameSpace, FileName, LineNumber, ScriptText);
   SkipEmptyStatement__1qwp(TokenContext);
   var SkipToken = ZToken_GetToken(TokenContext);
   while (HasNext__1qwp(TokenContext)) {
      SetParseFlag__2qwp(TokenContext, false);
      ClearListAfter__2quv(TopBlockNode, 0);
      SkipToken = ZToken_GetToken(TokenContext);
      var ParsedNode = ZNode_ParsePattern(TokenContext, TopBlockNode, "$Statement$", true);
      if (IsErrorNode__1qwo(ParsedNode)) {
         SkipError__2qwp(TokenContext, SkipToken);
      };
      Exec2__3qws(self, ParsedNode, false);
      SkipEmptyStatement__1qwp(TokenContext);
      Vacume__1qwp(TokenContext);
   };
   return self.Generator.GetSourceText(self.Generator);
};
function ZSourceEngine_Translate(self, ScriptText, FileName, LineNumber){ return Translate__4qws(self, ScriptText, FileName, LineNumber); }

function Unsupported__2qws(self, Node) {
   if (self.InteractiveContext) {
      self.Generator.StartCodeGeneration(self.Generator, Node, self.InteractiveContext);
   } else {
      ZLogger_LogError__2qw3(Node.SourceToken, "unsupported at top level");
      self.StopVisitor(self);
   };
   return;
};
function ZSourceEngine_Unsupported(self, Node){ return Unsupported__2qws(self, Node); }

function VisitNullNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitNullNode(self, Node){ return VisitNullNode__2qws(self, Node); }

function VisitBooleanNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitBooleanNode(self, Node){ return VisitBooleanNode__2qws(self, Node); }

function VisitIntNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitIntNode(self, Node){ return VisitIntNode__2qws(self, Node); }

function VisitFloatNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitFloatNode(self, Node){ return VisitFloatNode__2qws(self, Node); }

function VisitStringNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitStringNode(self, Node){ return VisitStringNode__2qws(self, Node); }

function VisitArrayLiteralNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitArrayLiteralNode(self, Node){ return VisitArrayLiteralNode__2qws(self, Node); }

function VisitMapLiteralNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitMapLiteralNode(self, Node){ return VisitMapLiteralNode__2qws(self, Node); }

function VisitNewObjectNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitNewObjectNode(self, Node){ return VisitNewObjectNode__2qws(self, Node); }

function VisitGlobalNameNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitGlobalNameNode(self, Node){ return VisitGlobalNameNode__2qws(self, Node); }

function VisitGetNameNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitGetNameNode(self, Node){ return VisitGetNameNode__2qws(self, Node); }

function VisitSetNameNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitSetNameNode(self, Node){ return VisitSetNameNode__2qws(self, Node); }

function VisitGroupNode__2qws(self, Node) {
   Eval2__2qws(self, Node.AST[0]);
   return;
};
function ZSourceEngine_VisitGroupNode(self, Node){ return VisitGroupNode__2qws(self, Node); }

function VisitGetterNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitGetterNode(self, Node){ return VisitGetterNode__2qws(self, Node); }

function VisitSetterNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitSetterNode(self, Node){ return VisitSetterNode__2qws(self, Node); }

function VisitGetIndexNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitGetIndexNode(self, Node){ return VisitGetIndexNode__2qws(self, Node); }

function VisitSetIndexNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitSetIndexNode(self, Node){ return VisitSetIndexNode__2qws(self, Node); }

function VisitMacroNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitMacroNode(self, Node){ return VisitMacroNode__2qws(self, Node); }

function VisitFuncCallNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitFuncCallNode(self, Node){ return VisitFuncCallNode__2qws(self, Node); }

function VisitMethodCallNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitMethodCallNode(self, Node){ return VisitMethodCallNode__2qws(self, Node); }

function VisitUnaryNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitUnaryNode(self, Node){ return VisitUnaryNode__2qws(self, Node); }

function VisitNotNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitNotNode(self, Node){ return VisitNotNode__2qws(self, Node); }

function VisitCastNode__2qws(self, Node) {
   if (IsVoidType__1qwg(Node.Type)) {
      Eval2__2qws(self, Node.AST[0]);
      Node.Type = Node.AST[0].Type;
   } else {
      Unsupported__2qws(self, Node);
   };
   return;
};
function ZSourceEngine_VisitCastNode(self, Node){ return VisitCastNode__2qws(self, Node); }

function VisitInstanceOfNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitInstanceOfNode(self, Node){ return VisitInstanceOfNode__2qws(self, Node); }

function VisitBinaryNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitBinaryNode(self, Node){ return VisitBinaryNode__2qws(self, Node); }

function VisitComparatorNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitComparatorNode(self, Node){ return VisitComparatorNode__2qws(self, Node); }

function VisitAndNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitAndNode(self, Node){ return VisitAndNode__2qws(self, Node); }

function VisitOrNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitOrNode(self, Node){ return VisitOrNode__2qws(self, Node); }

function VisitBlockNode__2qws(self, Node) {
   var i = 1;
   while (i < GetListSize__1quv(Node) && self.IsVisitable(self)) {
      var StmtNode = ZNode_GetListAt(Node, i);
      Eval2__2qws(self, StmtNode);
      if (StmtNode.IsBreakingBlock(StmtNode)) {
         break;
      };
   };
   return;
};
function ZSourceEngine_VisitBlockNode(self, Node){ return VisitBlockNode__2qws(self, Node); }

function VisitVarNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitVarNode(self, Node){ return VisitVarNode__2qws(self, Node); }

function VisitIfNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitIfNode(self, Node){ return VisitIfNode__2qws(self, Node); }

function VisitReturnNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitReturnNode(self, Node){ return VisitReturnNode__2qws(self, Node); }

function VisitWhileNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitWhileNode(self, Node){ return VisitWhileNode__2qws(self, Node); }

function VisitBreakNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitBreakNode(self, Node){ return VisitBreakNode__2qws(self, Node); }

function VisitThrowNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitThrowNode(self, Node){ return VisitThrowNode__2qws(self, Node); }

function VisitTryNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitTryNode(self, Node){ return VisitTryNode__2qws(self, Node); }

function VisitLetNode__2qws(self, Node) {
   if (HasUntypedNode__1qwo(Node)) {
      LibZen.PrintDebug((("HasUntypedNode: " + HasUntypedNode__1qwo(Node)) + "\n") + toString__1qwo(Node));
   };
   self.Generator.StartCodeGeneration(self.Generator, Node, self.InteractiveContext);
   return;
};
function ZSourceEngine_VisitLetNode(self, Node){ return VisitLetNode__2qws(self, Node); }

function VisitFunctionNode__2qws(self, Node) {
   if (HasUntypedNode__1qwo(Node)) {
      LibZen.PrintDebug((("HasUntypedNode: " + HasUntypedNode__1qwo(Node)) + "\nLAZY: ") + toString__1qwo(Node));
   };
   self.Generator.StartCodeGeneration(self.Generator, Node, self.InteractiveContext);
   return;
};
function ZSourceEngine_VisitFunctionNode(self, Node){ return VisitFunctionNode__2qws(self, Node); }

function VisitClassNode__2qws(self, Node) {
   if (HasUntypedNode__1qwo(Node)) {
      LibZen.PrintDebug((("HasUntypedNode: " + HasUntypedNode__1qwo(Node)) + "\n") + toString__1qwo(Node));
   };
   self.Generator.StartCodeGeneration(self.Generator, Node, self.InteractiveContext);
   return;
};
function ZSourceEngine_VisitClassNode(self, Node){ return VisitClassNode__2qws(self, Node); }

function VisitErrorNode__2qws(self, Node) {
   ZLogger_LogError__2qw3(Node.SourceToken, Node.ErrorMessage);
   self.StopVisitor(self);
   return;
};
function ZSourceEngine_VisitErrorNode(self, Node){ return VisitErrorNode__2qws(self, Node); }

function VisitTypeNode__2qws(self, Node) {
   Unsupported__2qws(self, Node);
   return;
};
function ZSourceEngine_VisitTypeNode(self, Node){ return VisitTypeNode__2qws(self, Node); }

function VisitExtendedNode__2qws(self, Node) {
   if ((Node).constructor.name == (ZTypeNode).name) {
      VisitTypeNode__2qws(self, Node);
   } else {
      var SugarNode = Node.DeSugar(Node, self.Generator);
      SugarNode.Accept(SugarNode, self);
   };
   return;
};
function ZSourceEngine_VisitExtendedNode(self, Node){ return VisitExtendedNode__2qws(self, Node); }

function VisitSugarNode__2qws(self, Node) {
   Eval2__2qws(self, Node.AST[0]);
   return;
};
function ZSourceEngine_VisitSugarNode(self, Node){ return VisitSugarNode__2qws(self, Node); }

function WriteTo__2qws(self, OutputFile) {
   self.Generator.WriteTo(self.Generator, OutputFile);
   ShowErrors__1qrk(self.Generator.Logger);
   return;
};
function ZSourceEngine_WriteTo(self, OutputFile){ return WriteTo__2qws(self, OutputFile); }

function ZSourceGenerator__3quk(self, TargetCode, TargetVersion) {
   ZGenerator__3qw4(self, TargetCode, TargetVersion);
   self.InitBuilderList(self);
   self.LineFeed = "\n";
   self.Tab = "   ";
   self.LineComment = "//";
   self.BeginComment = "/*";
   self.EndComment = "*/";
   self.Camma = ", ";
   self.SemiColon = ";";
   self.TrueLiteral = "true";
   self.FalseLiteral = "false";
   self.NullLiteral = "null";
   self.AndOperator = "&&";
   self.OrOperator = "||";
   self.NotOperator = "!";
   self.TopType = "var";
   return self;
};

function InitBuilderList__1quk(self) {
   self.CurrentBuilder = null;
   Array<ZSourceBuilder>_clear(0);
   self.HeaderBuilder = ZSourceBuilder_AppendNewSourceBuilder(self);
   self.CurrentBuilder = ZSourceBuilder_AppendNewSourceBuilder(self);
   return;
};
function ZSourceGenerator_InitBuilderList(self){ return InitBuilderList__1quk(self); }

function GetEngine__1quk(self) {
   LibZen.PrintLine("FIXME: Overide GetEngine in each generator!!");
   return ZSourceEngine__3qws(new ZSourceEngine(), ZenTypeSafer__2qga(new ZenTypeSafer(), self), self);
};
function ZSourceGenerator_GetEngine(self){ return GetEngine__1quk(self); }

function AppendNewSourceBuilder__1quk(self) {
   var Builder = ZSourceBuilder__3qq2(new ZSourceBuilder(), self, self.CurrentBuilder);
   self.BuilderList.push(Builder);
   return Builder;
};
function ZSourceGenerator_AppendNewSourceBuilder(self){ return AppendNewSourceBuilder__1quk(self); }

function InsertNewSourceBuilder__1quk(self) {
   var Builder = ZSourceBuilder__3qq2(new ZSourceBuilder(), self, self.CurrentBuilder);
   var i = 0;
   while (i < (self.BuilderList).length) {
      if (self.BuilderList[i] == self.CurrentBuilder) {
         Array<ZSourceBuilder>_add(i, Builder);
         return Builder;
      };
      i = i + 1;
   };
   self.BuilderList.push(Builder);
   return Builder;
};
function ZSourceGenerator_InsertNewSourceBuilder(self){ return InsertNewSourceBuilder__1quk(self); }

function SetNativeType__3quk(self, Type, TypeName) {
   var Key = "" + (Type.TypeId).toString();
   self.NativeTypeMap[Key] = TypeName;
   return;
};
function ZSourceGenerator_SetNativeType(self, Type, TypeName){ return SetNativeType__3quk(self, Type, TypeName); }

function GetNativeTypeName__2quk(self, Type) {
   var Key = "" + (Type.TypeId).toString();
   var TypeName = self.NativeTypeMap[Key];
   if (TypeName == null) {
      return Type.ShortName;
   };
   return TypeName;
};
function ZSourceGenerator_GetNativeTypeName(self, Type){ return GetNativeTypeName__2quk(self, Type); }

function SetReservedName__3quk(self, Keyword, AnotherName) {
   if (AnotherName == null) {
      AnotherName = "_" + Keyword;
   };
   self.ReservedNameMap[Keyword] = AnotherName;
   return;
};
function ZSourceGenerator_SetReservedName(self, Keyword, AnotherName){ return SetReservedName__3quk(self, Keyword, AnotherName); }

function SafeName__3quk(self, Name, Index) {
   if (Index == 0) {
      var SafeName = self.ReservedNameMap[Name];
      if (SafeName == null) {
         SafeName = Name;
      };
      return SafeName;
   };
   return (Name + "__") + (Index).toString();
};
function ZSourceGenerator_SafeName(self, Name, Index){ return SafeName__3quk(self, Name, Index); }

function SetMacro__4quk(self, FuncName, Macro, ReturnType) {
   var FuncType = ZFuncType_ZTypePool_LookupFuncType(ReturnType);
   SetDefinedFunc__2qw4(self, ZSourceMacro__4qit(new ZSourceMacro(), FuncName, FuncType, Macro));
   return;
};
function ZSourceGenerator_SetMacro(self, FuncName, Macro, ReturnType){ return SetMacro__4quk(self, FuncName, Macro, ReturnType); }

function SetMacro__5quk(self, FuncName, Macro, ReturnType, P1) {
   var FuncType = ZFuncType_ZTypePool_LookupFuncType(ReturnType, P1);
   SetDefinedFunc__2qw4(self, ZSourceMacro__4qit(new ZSourceMacro(), FuncName, FuncType, Macro));
   return;
};
function ZSourceGenerator_SetMacro(self, FuncName, Macro, ReturnType, P1){ return SetMacro__5quk(self, FuncName, Macro, ReturnType, P1); }

function SetMacro__6quk(self, FuncName, Macro, ReturnType, P1, P2) {
   var FuncType = ZFuncType_ZTypePool_LookupFuncType(ReturnType, P1, P2);
   SetDefinedFunc__2qw4(self, ZSourceMacro__4qit(new ZSourceMacro(), FuncName, FuncType, Macro));
   return;
};
function ZSourceGenerator_SetMacro(self, FuncName, Macro, ReturnType, P1, P2){ return SetMacro__6quk(self, FuncName, Macro, ReturnType, P1, P2); }

function SetMacro__7quk(self, FuncName, Macro, ReturnType, P1, P2, P3) {
   var FuncType = ZFuncType_ZTypePool_LookupFuncType(ReturnType, P1, P2, P3);
   SetDefinedFunc__2qw4(self, ZSourceMacro__4qit(new ZSourceMacro(), FuncName, FuncType, Macro));
   return;
};
function ZSourceGenerator_SetMacro(self, FuncName, Macro, ReturnType, P1, P2, P3){ return SetMacro__7quk(self, FuncName, Macro, ReturnType, P1, P2, P3); }

function SetConverterMacro__4quk(self, Macro, ReturnType, P1) {
   var FuncType = ZFuncType_ZTypePool_LookupFuncType(ReturnType, P1);
   SetConverterFunc__4qw4(self, P1, ReturnType, ZSourceMacro__4qit(new ZSourceMacro(), "to" + NameClass__2qw4(self, ReturnType), FuncType, Macro));
   return;
};
function ZSourceGenerator_SetConverterMacro(self, Macro, ReturnType, P1){ return SetConverterMacro__4quk(self, Macro, ReturnType, P1); }

function WriteTo__2quk(self, FileName) {
   LibZen.WriteTo(self.NameOutputFile(self, FileName), self.BuilderList);
   self.InitBuilderList(self);
   return;
};
function ZSourceGenerator_WriteTo(self, FileName){ return WriteTo__2quk(self, FileName); }

function GetSourceText__1quk(self) {
   var sb = ZSourceBuilder__3qq2(new ZSourceBuilder(), self, null);
   var i = 0;
   while (i < (self.BuilderList).length) {
      var Builder = self.BuilderList[i];
      Append__2qq2(sb, toString__1qq2(Builder));
      Clear__1qq2(Builder);
      AppendLineFeed__1qq2(sb);
      AppendLineFeed__1qq2(sb);
      i = i + 1;
   };
   self.InitBuilderList(self);
   return LibZen.SourceBuilderToString(sb);
};
function ZSourceGenerator_GetSourceText(self){ return GetSourceText__1quk(self); }

function StartCodeGeneration__3quk(self, Node, IsInteractive) {
   Node.Accept(Node, self);
   if (IsInteractive) {
      var i = 0;
      LibZen.PrintLine("---");
      while (i < (self.BuilderList).length) {
         var Builder = self.BuilderList[i];
         LibZen.PrintLine(toString__1qq2(Builder));
         Clear__1qq2(Builder);
         i = i + 1;
      };
      self.InitBuilderList(self);
   };
   return true;
};
function ZSourceGenerator_StartCodeGeneration(self, Node, IsInteractive){ return StartCodeGeneration__3quk(self, Node, IsInteractive); }

function GenerateCode__3quk(self, ContextType, Node) {
   Node.Accept(Node, self);
   return;
};
function ZSourceGenerator_GenerateCode(self, ContextType, Node){ return GenerateCode__3quk(self, ContextType, Node); }

function IsNeededSurroud__2quk(self, Node) {
   if ((Node).constructor.name == (ZBinaryNode).name) {
      return true;
   };
   return false;
};
function ZSourceGenerator_IsNeededSurroud(self, Node){ return IsNeededSurroud__2quk(self, Node); }

function GenerateSurroundCode__2quk(self, Node) {
   if (IsNeededSurroud__2quk(self, Node)) {
      Append__2qq2(self.CurrentBuilder, "(");
      self.GenerateCode(self, null, Node);
      Append__2qq2(self.CurrentBuilder, ")");
   } else {
      self.GenerateCode(self, null, Node);
   };
   return;
};
function ZSourceGenerator_GenerateSurroundCode(self, Node){ return GenerateSurroundCode__2quk(self, Node); }

function AppendCode__2quk(self, RawSource) {
   Append__2qq2(self.CurrentBuilder, RawSource);
   return;
};
function ZSourceGenerator_AppendCode(self, RawSource){ return AppendCode__2quk(self, RawSource); }

function VisitStmtList__2quk(self, BlockNode) {
   var i = 0;
   while (i < GetListSize__1quv(BlockNode)) {
      var SubNode = ZNode_GetListAt(BlockNode, i);
      AppendLineFeed__1qq2(self.CurrentBuilder);
      AppendIndent__1qq2(self.CurrentBuilder);
      self.GenerateCode(self, null, SubNode);
      i = i + 1;
      if (i < GetListSize__1quv(BlockNode)) {
         Append__2qq2(self.CurrentBuilder, self.SemiColon);
      };
   };
   return;
};
function ZSourceGenerator_VisitStmtList(self, BlockNode){ return VisitStmtList__2quk(self, BlockNode); }

function VisitBlockNode__2quk(self, Node) {
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, "{");
   Indent__1qq2(self.CurrentBuilder);
   VisitStmtList__2quk(self, Node);
   if (GetListSize__1quv(Node) > 0) {
      Append__2qq2(self.CurrentBuilder, self.SemiColon);
   };
   UnIndent__1qq2(self.CurrentBuilder);
   AppendLineFeed__1qq2(self.CurrentBuilder);
   AppendIndent__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, "}");
   return;
};
function ZSourceGenerator_VisitBlockNode(self, Node){ return VisitBlockNode__2quk(self, Node); }

function VisitNullNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, self.NullLiteral);
   return;
};
function ZSourceGenerator_VisitNullNode(self, Node){ return VisitNullNode__2quk(self, Node); }

function VisitBooleanNode__2quk(self, Node) {
   if (Node.BooleanValue) {
      Append__2qq2(self.CurrentBuilder, self.TrueLiteral);
   } else {
      Append__2qq2(self.CurrentBuilder, self.FalseLiteral);
   };
   return;
};
function ZSourceGenerator_VisitBooleanNode(self, Node){ return VisitBooleanNode__2quk(self, Node); }

function VisitIntNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "" + ((Node.IntValue)).toString());
   return;
};
function ZSourceGenerator_VisitIntNode(self, Node){ return VisitIntNode__2quk(self, Node); }

function VisitFloatNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "" + ((Node.FloatValue)).toString());
   return;
};
function ZSourceGenerator_VisitFloatNode(self, Node){ return VisitFloatNode__2quk(self, Node); }

function VisitStringNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, LibZen.QuoteString(Node.StringValue));
   return;
};
function ZSourceGenerator_VisitStringNode(self, Node){ return VisitStringNode__2quk(self, Node); }

function VisitArrayLiteralNode__2quk(self, Node) {
   VisitListNode__4quk(self, "[", Node, "]");
   return;
};
function ZSourceGenerator_VisitArrayLiteralNode(self, Node){ return VisitArrayLiteralNode__2quk(self, Node); }

function VisitMapLiteralNode__2quk(self, Node) {
   return;
};
function ZSourceGenerator_VisitMapLiteralNode(self, Node){ return VisitMapLiteralNode__2quk(self, Node); }

function VisitNewObjectNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "new");
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   GenerateTypeName__2quk(self, Node.Type);
   VisitListNode__4quk(self, "(", Node, ")");
   return;
};
function ZSourceGenerator_VisitNewObjectNode(self, Node){ return VisitNewObjectNode__2quk(self, Node); }

function VisitGroupNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "(");
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, ")");
   return;
};
function ZSourceGenerator_VisitGroupNode(self, Node){ return VisitGroupNode__2quk(self, Node); }

function VisitGetIndexNode__2quk(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, "[");
   self.GenerateCode(self, null, Node.AST[1]);
   Append__2qq2(self.CurrentBuilder, "]");
   return;
};
function ZSourceGenerator_VisitGetIndexNode(self, Node){ return VisitGetIndexNode__2quk(self, Node); }

function VisitSetIndexNode__2quk(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, "[");
   self.GenerateCode(self, null, Node.AST[1]);
   Append__2qq2(self.CurrentBuilder, "]");
   AppendToken__2qq2(self.CurrentBuilder, "=");
   self.GenerateCode(self, null, Node.AST[2]);
   return;
};
function ZSourceGenerator_VisitSetIndexNode(self, Node){ return VisitSetIndexNode__2quk(self, Node); }

function VisitGlobalNameNode__2quk(self, Node) {
   if (IsUntyped__1qwo(Node)) {
      ZLogger_LogError__2qw3(Node.SourceToken, "undefined symbol: " + Node.GlobalName);
   };
   if (Node.IsStaticFuncName) {
      Append__2qq2(self.CurrentBuilder, StringfySignature__2qwg(Node.Type, Node.GlobalName));
   } else {
      Append__2qq2(self.CurrentBuilder, Node.GlobalName);
   };
   return;
};
function ZSourceGenerator_VisitGlobalNameNode(self, Node){ return VisitGlobalNameNode__2quk(self, Node); }

function VisitGetNameNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, SafeName__3quk(self, Node.VarName, Node.VarIndex));
   return;
};
function ZSourceGenerator_VisitGetNameNode(self, Node){ return VisitGetNameNode__2quk(self, Node); }

function VisitSetNameNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, SafeName__3quk(self, Node.VarName, Node.VarIndex));
   AppendToken__2qq2(self.CurrentBuilder, "=");
   self.GenerateCode(self, null, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitSetNameNode(self, Node){ return VisitSetNameNode__2quk(self, Node); }

function VisitGetterNode__2quk(self, Node) {
   GenerateSurroundCode__2quk(self, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, ".");
   Append__2qq2(self.CurrentBuilder, Node.FieldName);
   return;
};
function ZSourceGenerator_VisitGetterNode(self, Node){ return VisitGetterNode__2quk(self, Node); }

function VisitSetterNode__2quk(self, Node) {
   GenerateSurroundCode__2quk(self, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, ".");
   Append__2qq2(self.CurrentBuilder, Node.FieldName);
   AppendToken__2qq2(self.CurrentBuilder, "=");
   self.GenerateCode(self, null, Node.AST[1]);
   return;
};
function ZSourceGenerator_VisitSetterNode(self, Node){ return VisitSetterNode__2quk(self, Node); }

function VisitMethodCallNode__2quk(self, Node) {
   GenerateSurroundCode__2quk(self, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, ".");
   Append__2qq2(self.CurrentBuilder, Node.MethodName);
   VisitListNode__4quk(self, "(", Node, ")");
   return;
};
function ZSourceGenerator_VisitMethodCallNode(self, Node){ return VisitMethodCallNode__2quk(self, Node); }

function VisitMacroNode__2quk(self, Node) {
   var Macro = GetMacroText__1q06(Node);
   var FuncType = ZFuncType_GetFuncType(Node);
   var fromIndex = 0;
   var BeginNum = String_indexOf("$[", fromIndex);
   while (BeginNum != -1) {
      var EndNum = String_indexOf("]", BeginNum + 2);
      if (EndNum == -1) {
         break;
      };
      Append__2qq2(self.CurrentBuilder, String_substring(fromIndex, BeginNum));
      var Index = LibZen_ParseInt(String_substring(BeginNum + 2, EndNum));
      if (HasAst__2qwo(Node, Index)) {
         self.GenerateCode(self, ZType_GetFuncParamType(FuncType, Index), Node.AST[Index]);
      };
      fromIndex = EndNum + 1;
      BeginNum = String_indexOf("$[", fromIndex);
   };
   Append__2qq2(self.CurrentBuilder, String_substring(fromIndex));
   return;
};
function ZSourceGenerator_VisitMacroNode(self, Node){ return VisitMacroNode__2quk(self, Node); }

function VisitFuncCallNode__2quk(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   VisitListNode__4quk(self, "(", Node, ")");
   return;
};
function ZSourceGenerator_VisitFuncCallNode(self, Node){ return VisitFuncCallNode__2quk(self, Node); }

function VisitUnaryNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, GetText__1qw3(Node.SourceToken));
   self.GenerateCode(self, null, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitUnaryNode(self, Node){ return VisitUnaryNode__2quk(self, Node); }

function VisitNotNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, self.NotOperator);
   GenerateSurroundCode__2quk(self, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitNotNode(self, Node){ return VisitNotNode__2quk(self, Node); }

function VisitCastNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "(");
   GenerateTypeName__2quk(self, Node.Type);
   Append__2qq2(self.CurrentBuilder, ")");
   GenerateSurroundCode__2quk(self, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitCastNode(self, Node){ return VisitCastNode__2quk(self, Node); }

function VisitInstanceOfNode__2quk(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   AppendToken__2qq2(self.CurrentBuilder, "instanceof");
   GenerateTypeName__2quk(self, Node.AST[1].Type);
   return;
};
function ZSourceGenerator_VisitInstanceOfNode(self, Node){ return VisitInstanceOfNode__2quk(self, Node); }

function VisitBinaryNode__2quk(self, Node) {
   if ((Node.ParentNode).constructor.name == (ZBinaryNode).name) {
      Append__2qq2(self.CurrentBuilder, "(");
   };
   self.GenerateCode(self, null, Node.AST[0]);
   AppendToken__2qq2(self.CurrentBuilder, GetText__1qw3(Node.SourceToken));
   self.GenerateCode(self, null, Node.AST[1]);
   if ((Node.ParentNode).constructor.name == (ZBinaryNode).name) {
      Append__2qq2(self.CurrentBuilder, ")");
   };
   return;
};
function ZSourceGenerator_VisitBinaryNode(self, Node){ return VisitBinaryNode__2quk(self, Node); }

function VisitComparatorNode__2quk(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   AppendToken__2qq2(self.CurrentBuilder, GetText__1qw3(Node.SourceToken));
   self.GenerateCode(self, null, Node.AST[1]);
   return;
};
function ZSourceGenerator_VisitComparatorNode(self, Node){ return VisitComparatorNode__2quk(self, Node); }

function VisitAndNode__2quk(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   AppendToken__2qq2(self.CurrentBuilder, self.AndOperator);
   self.GenerateCode(self, null, Node.AST[1]);
   return;
};
function ZSourceGenerator_VisitAndNode(self, Node){ return VisitAndNode__2quk(self, Node); }

function VisitOrNode__2quk(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   AppendToken__2qq2(self.CurrentBuilder, self.OrOperator);
   self.GenerateCode(self, null, Node.AST[1]);
   return;
};
function ZSourceGenerator_VisitOrNode(self, Node){ return VisitOrNode__2quk(self, Node); }

function VisitIfNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "if (");
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, ")");
   self.GenerateCode(self, null, Node.AST[1]);
   if (Node.AST[2] != null) {
      AppendToken__2qq2(self.CurrentBuilder, "else");
      self.GenerateCode(self, null, Node.AST[2]);
   };
   return;
};
function ZSourceGenerator_VisitIfNode(self, Node){ return VisitIfNode__2quk(self, Node); }

function VisitReturnNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "return");
   if (Node.AST[0] != null) {
      AppendWhiteSpace__1qq2(self.CurrentBuilder);
      self.GenerateCode(self, null, Node.AST[0]);
   };
   return;
};
function ZSourceGenerator_VisitReturnNode(self, Node){ return VisitReturnNode__2quk(self, Node); }

function VisitWhileNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "while (");
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, ")");
   self.GenerateCode(self, null, Node.AST[1]);
   return;
};
function ZSourceGenerator_VisitWhileNode(self, Node){ return VisitWhileNode__2quk(self, Node); }

function VisitBreakNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "break");
   return;
};
function ZSourceGenerator_VisitBreakNode(self, Node){ return VisitBreakNode__2quk(self, Node); }

function VisitThrowNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "throw");
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   self.GenerateCode(self, null, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitThrowNode(self, Node){ return VisitThrowNode__2quk(self, Node); }

function VisitTryNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "try");
   self.GenerateCode(self, null, Node.AST[0]);
   if (Node.AST[1] != null) {
      self.GenerateCode(self, null, Node.AST[1]);
   };
   if (Node.AST[2] != null) {
      Append__2qq2(self.CurrentBuilder, "finally");
      self.GenerateCode(self, null, Node.AST[2]);
   };
   return;
};
function ZSourceGenerator_VisitTryNode(self, Node){ return VisitTryNode__2quk(self, Node); }

function VisitCatchNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "catch (");
   Append__2qq2(self.CurrentBuilder, Node.ExceptionName);
   VisitTypeAnnotation__2quk(self, Node.ExceptionType);
   Append__2qq2(self.CurrentBuilder, ")");
   self.GenerateCode(self, null, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitCatchNode(self, Node){ return VisitCatchNode__2quk(self, Node); }

function VisitVarNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "var");
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, SafeName__3quk(self, Node.NativeName, Node.VarIndex));
   VisitTypeAnnotation__2quk(self, Node.DeclType);
   AppendToken__2qq2(self.CurrentBuilder, "=");
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, self.SemiColon);
   VisitStmtList__2quk(self, Node);
   return;
};
function ZSourceGenerator_VisitVarNode(self, Node){ return VisitVarNode__2quk(self, Node); }

function VisitTypeAnnotation__2quk(self, Type) {
   Append__2qq2(self.CurrentBuilder, ": ");
   GenerateTypeName__2quk(self, Type);
   return;
};
function ZSourceGenerator_VisitTypeAnnotation(self, Type){ return VisitTypeAnnotation__2quk(self, Type); }

function VisitLetNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "let");
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, Node.GlobalName);
   AppendToken__2qq2(self.CurrentBuilder, "=");
   self.GenerateCode(self, null, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitLetNode(self, Node){ return VisitLetNode__2quk(self, Node); }

function VisitParamNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, SafeName__3quk(self, Node.Name, Node.ParamIndex));
   VisitTypeAnnotation__2quk(self, Node.Type);
   return;
};
function ZSourceGenerator_VisitParamNode(self, Node){ return VisitParamNode__2quk(self, Node); }

function VisitFunctionNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "function");
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   if (Node.FuncName != null) {
      Append__2qq2(self.CurrentBuilder, Node.FuncName);
   };
   VisitListNode__4quk(self, "(", Node, ")");
   VisitTypeAnnotation__2quk(self, Node.ReturnType);
   self.GenerateCode(self, null, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitFunctionNode(self, Node){ return VisitFunctionNode__2quk(self, Node); }

function VisitClassNode__2quk(self, Node) {
   Append__2qq2(self.CurrentBuilder, "class");
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, Node.ClassName);
   if (Node.SuperType != null) {
      AppendToken__2qq2(self.CurrentBuilder, "extends");
      GenerateTypeName__2quk(self, Node.SuperType);
   };
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, "{");
   Indent__1qq2(self.CurrentBuilder);
   var i = 0;
   while (i < GetListSize__1quv(Node)) {
      var FieldNode = ZFieldNode_GetFieldNode(Node, i);
      AppendLineFeed__1qq2(self.CurrentBuilder);
      AppendIndent__1qq2(self.CurrentBuilder);
      Append__2qq2(self.CurrentBuilder, "var");
      AppendWhiteSpace__1qq2(self.CurrentBuilder);
      Append__2qq2(self.CurrentBuilder, FieldNode.FieldName);
      VisitTypeAnnotation__2quk(self, FieldNode.DeclType);
      if (HasAst__2qwo(FieldNode, 0)) {
         AppendToken__2qq2(self.CurrentBuilder, "=");
         self.GenerateCode(self, null, FieldNode.AST[0]);
      };
      Append__2qq2(self.CurrentBuilder, self.SemiColon);
      i = i + 1;
   };
   UnIndent__1qq2(self.CurrentBuilder);
   AppendLineFeed__1qq2(self.CurrentBuilder);
   AppendIndent__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, "}");
   return;
};
function ZSourceGenerator_VisitClassNode(self, Node){ return VisitClassNode__2quk(self, Node); }

function VisitErrorNode__2quk(self, Node) {
   ZLogger_LogError__2qw3(Node.SourceToken, Node.ErrorMessage);
   Append__2qq2(self.CurrentBuilder, "ThrowError(");
   Append__2qq2(self.CurrentBuilder, LibZen.QuoteString(Node.ErrorMessage));
   Append__2qq2(self.CurrentBuilder, ")");
   return;
};
function ZSourceGenerator_VisitErrorNode(self, Node){ return VisitErrorNode__2quk(self, Node); }

function VisitExtendedNode__2quk(self, Node) {
   if ((Node).constructor.name == (ZParamNode).name) {
      VisitParamNode__2quk(self, Node);
   } else {
      var SugarNode = Node.DeSugar(Node, self);
      self.VisitSugarNode(self, SugarNode);
   };
   return;
};
function ZSourceGenerator_VisitExtendedNode(self, Node){ return VisitExtendedNode__2quk(self, Node); }

function VisitSugarNode__2quk(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   return;
};
function ZSourceGenerator_VisitSugarNode(self, Node){ return VisitSugarNode__2quk(self, Node); }

function GenerateTypeName__2quk(self, Type) {
   Append__2qq2(self.CurrentBuilder, GetNativeTypeName__2quk(self, Type.GetRealType(Type)));
   return;
};
function ZSourceGenerator_GenerateTypeName(self, Type){ return GenerateTypeName__2quk(self, Type); }

function VisitListNode__5quk(self, OpenToken, VargNode, DelimToken, CloseToken) {
   Append__2qq2(self.CurrentBuilder, OpenToken);
   var i = 0;
   while (i < GetListSize__1quv(VargNode)) {
      var ParamNode = ZNode_GetListAt(VargNode, i);
      if (i > 0) {
         Append__2qq2(self.CurrentBuilder, DelimToken);
      };
      self.GenerateCode(self, null, ParamNode);
      i = i + 1;
   };
   Append__2qq2(self.CurrentBuilder, CloseToken);
   return;
};
function ZSourceGenerator_VisitListNode(self, OpenToken, VargNode, DelimToken, CloseToken){ return VisitListNode__5quk(self, OpenToken, VargNode, DelimToken, CloseToken); }

function VisitListNode__4quk(self, OpenToken, VargNode, CloseToken) {
   VisitListNode__5quk(self, OpenToken, VargNode, ", ", CloseToken);
   return;
};
function ZSourceGenerator_VisitListNode(self, OpenToken, VargNode, CloseToken){ return VisitListNode__4quk(self, OpenToken, VargNode, CloseToken); }

function ZTypeChecker__2qrc(self, Generator) {
   self.Generator = Generator;
   self.Logger = Generator.Logger;
   self.StackedContextType = null;
   self.ReturnedNode = null;
   self.StoppedVisitor = false;
   self.VarScope = ZVarScope__4qrj(new ZVarScope(), null, self.Logger, null);
   return self;
};

function EnableVisitor__1qrc(self) {
   self.StoppedVisitor = false;
   return;
};
function ZTypeChecker_EnableVisitor(self){ return EnableVisitor__1qrc(self); }

function StopVisitor__1qrc(self) {
   self.StoppedVisitor = true;
   return;
};
function ZTypeChecker_StopVisitor(self){ return StopVisitor__1qrc(self); }

function IsVisitable__1qrc(self) {
   return !self.StoppedVisitor;
};
function ZTypeChecker_IsVisitable(self){ return IsVisitable__1qrc(self); }

function GetContextType__1qrc(self) {
   return self.StackedContextType;
};
function ZTypeChecker_GetContextType(self){ return GetContextType__1qrc(self); }

function VisitTypeChecker__3qrc(self, Node, ContextType) {
   var ParentNode = Node.ParentNode;
   self.StackedContextType = ContextType;
   self.ReturnedNode = null;
   Node.Accept(Node, self);
   if (self.ReturnedNode == null) {
      LibZen.PrintDebug("!! returns no value: " + toString__1qwo(Node));
   } else {
      Node = self.ReturnedNode;
   };
   if (ParentNode != Node.ParentNode && ParentNode != null) {
      ZNode_SetChild(ParentNode, Node);
   };
   CheckVarNode__3qrj(self.VarScope, ContextType, Node);
   return Node;
};
function ZTypeChecker_VisitTypeChecker(self, Node, ContextType){ return VisitTypeChecker__3qrc(self, Node, ContextType); }

function CreateStupidCastNode__3qrc(self, Requested, Node) {
   var ErrorNode = ZStupidCastErrorNode__3q4n(new ZStupidCastErrorNode(), Node, (("type error: requested=" + toString__1qwg(Requested)) + ", given=") + toString__1qwg(Node.Type));
   ErrorNode.Type = Requested;
   return ErrorNode;
};
function ZTypeChecker_CreateStupidCastNode(self, Requested, Node){ return CreateStupidCastNode__3qrc(self, Requested, Node); }

function EnforceNodeType__3qrc(self, Node, EnforcedType) {
   var Func = ZFunc_LookupConverterFunc(self.Generator, Node.Type, EnforcedType);
   if (Func == null && IsStringType__1qwg(EnforcedType)) {
      Func = ZFunc_LookupFunc(self.Generator, "toString", Node.Type, 1);
   };
   if ((Func).constructor.name == (ZMacroFunc).name) {
      var MacroNode = ZMacroNode__4q06(new ZMacroNode(), Node.ParentNode, null, Func);
      Append__2quv(MacroNode, Node);
      MacroNode.Type = EnforcedType;
      return MacroNode;
   } else if (Func != null) {
      var MacroNode = ZFuncCallNode__4q4e(new ZFuncCallNode(), Node.ParentNode, Func.FuncName, ZFuncType_GetFuncType(Func));
      Append__2quv(MacroNode, Node);
      MacroNode.Type = EnforcedType;
      return MacroNode;
   };
   return ZNode_CreateStupidCastNode(self, EnforcedType, Node);
};
function ZTypeChecker_EnforceNodeType(self, Node, EnforcedType){ return EnforceNodeType__3qrc(self, Node, EnforcedType); }

function TypeCheckImpl__4qrc(self, Node, ContextType, TypeCheckPolicy) {
   if (IsErrorNode__1qwo(Node)) {
      if (!ContextType.IsVarType(ContextType)) {
         Node.Type = ContextType;
      };
      return Node;
   };
   if (IsUntyped__1qwo(Node) || ContextType.IsVarType(ContextType) || LibZen.IsFlag(TypeCheckPolicy, 1)) {
      return Node;
   };
   if (Node.Type == ContextType || Accept__2qwg(ContextType, Node.Type)) {
      return Node;
   };
   if (IsVoidType__1qwg(ContextType) && !IsVoidType__1qwg(Node.Type)) {
      return ZCastNode__4qo6(new ZCastNode(), Node.ParentNode, ZType__4qwg(new ZType(), 1 << 16, "void", null), Node);
   };
   if (IsFloatType__1qwg(ContextType) && IsIntType__1qwg(Node.Type)) {
      return ZNode_EnforceNodeType(self, Node, ContextType);
   };
   if (IsIntType__1qwg(ContextType) && IsFloatType__1qwg(Node.Type)) {
      return ZNode_EnforceNodeType(self, Node, ContextType);
   };
   return ZNode_CreateStupidCastNode(self, ContextType, Node);
};
function ZTypeChecker_TypeCheckImpl(self, Node, ContextType, TypeCheckPolicy){ return TypeCheckImpl__4qrc(self, Node, ContextType, TypeCheckPolicy); }

function VisitTypeChecker__4qrc(self, Node, ContextType, TypeCheckPolicy) {
   if (self.IsVisitable(self) && Node != null) {
      if (HasUntypedNode__1qwo(Node)) {
         Node = ZNode_VisitTypeChecker(Node, self, ContextType);
      };
      Node = ZNode_TypeCheckImpl(self, Node, ContextType, TypeCheckPolicy);
      CheckVarNode__3qrj(self.VarScope, ContextType, Node);
   };
   self.ReturnedNode = null;
   return Node;
};
function ZTypeChecker_VisitTypeChecker(self, Node, ContextType, TypeCheckPolicy){ return VisitTypeChecker__4qrc(self, Node, ContextType, TypeCheckPolicy); }

function TryType__3qrc(self, Node, ContextType) {
   return ZNode_VisitTypeChecker(self, Node, ContextType, 1);
};
function ZTypeChecker_TryType(self, Node, ContextType){ return TryType__3qrc(self, Node, ContextType); }

function TryTypeAt__4qrc(self, Node, Index, ContextType) {
   Set__3qwo(Node, Index, ZNode_VisitTypeChecker(self, Node.AST[Index], ContextType, 1));
   return;
};
function ZTypeChecker_TryTypeAt(self, Node, Index, ContextType){ return TryTypeAt__4qrc(self, Node, Index, ContextType); }

function CheckType__3qrc(self, Node, ContextType) {
   return ZNode_VisitTypeChecker(self, Node, ContextType, 0);
};
function ZTypeChecker_CheckType(self, Node, ContextType){ return CheckType__3qrc(self, Node, ContextType); }

function CheckTypeAt__4qrc(self, Node, Index, ContextType) {
   Set__3qwo(Node, Index, ZNode_VisitTypeChecker(self, Node.AST[Index], ContextType, 0));
   return;
};
function ZTypeChecker_CheckTypeAt(self, Node, Index, ContextType){ return CheckTypeAt__4qrc(self, Node, Index, ContextType); }

function TypeCheckNodeList__2qrc(self, List) {
   if (self.IsVisitable(self)) {
      var AllTyped = true;
      var i = 0;
      while (i < GetListSize__1quv(List)) {
         var SubNode = ZNode_GetListAt(List, i);
         SubNode = ZNode_CheckType(self, SubNode, ZType__4qwg(new ZType(), 1 << 16, "var", null));
         SetListAt__3quv(List, i, SubNode);
         if (IsUntyped__1qwo(SubNode)) {
            AllTyped = false;
         };
         i = i + 1;
      };
      return AllTyped;
   };
   return false;
};
function ZTypeChecker_TypeCheckNodeList(self, List){ return TypeCheckNodeList__2qrc(self, List); }

function Return__2qrc(self, Node) {
   if (self.ReturnedNode != null) {
      LibZen.PrintDebug("previous returned node " + toString__1qwo(Node));
   };
   self.ReturnedNode = Node;
   return;
};
function ZTypeChecker_Return(self, Node){ return Return__2qrc(self, Node); }

function TypedNode__3qrc(self, Node, Type) {
   Node.Type = ZType_null(Type);
   if (self.ReturnedNode != null) {
      LibZen.PrintDebug("previous returned node " + toString__1qwo(Node));
   };
   self.ReturnedNode = Node;
   return;
};
function ZTypeChecker_TypedNode(self, Node, Type){ return TypedNode__3qrc(self, Node, Type); }

function ReturnErrorNode__4qrc(self, Node, ErrorToken, Message) {
   if (ErrorToken == null) {
      ErrorToken = Node.SourceToken;
   };
   Return__2qrc(self, ZErrorNode__4qpr(new ZErrorNode(), Node.ParentNode, ErrorToken, Message));
   return;
};
function ZTypeChecker_ReturnErrorNode(self, Node, ErrorToken, Message){ return ReturnErrorNode__4qrc(self, Node, ErrorToken, Message); }

function VisitErrorNode__2qrc(self, Node) {
   var ContextType = ZType_GetContextType(self);
   if (!ContextType.IsVarType(ContextType)) {
      TypedNode__3qrc(self, Node, ContextType);
   } else {
      Return__2qrc(self, Node);
   };
   return;
};
function ZTypeChecker_VisitErrorNode(self, Node){ return VisitErrorNode__2qrc(self, Node); }

function VisitExtendedNode__2qrc(self, Node) {
   var ContextType = ZType_GetContextType(self);
   var DeNode = Node.DeSugar(Node, self.Generator);
   if (!IsErrorNode__1qwo(DeNode)) {
      Return__2qrc(self, ZNode_CheckType(self, DeNode, ContextType));
   } else {
      TypedNode__3qrc(self, DeNode, ContextType);
   };
   return;
};
function ZTypeChecker_VisitExtendedNode(self, Node){ return VisitExtendedNode__2qrc(self, Node); }

function VisitSugarNode__2qrc(self, Node) {
   var ContextType = ZType_GetContextType(self);
   CheckTypeAt__4qrc(self, Node, 0, ContextType);
   TypedNode__3qrc(self, Node, ZType_GetAstType(Node, 0));
   return;
};
function ZTypeChecker_VisitSugarNode(self, Node){ return VisitSugarNode__2qrc(self, Node); }

function ZenTypeSafer__2qga(self, Generator) {
   ZTypeChecker__2qrc(self, Generator);
   return self;
};

function IsTopLevel__1qga(self) {
   return (self.CurrentFunctionNode == null);
};
function ZenTypeSafer_IsTopLevel(self){ return IsTopLevel__1qga(self); }

function InFunctionScope__1qga(self) {
   return (self.CurrentFunctionNode != null);
};
function ZenTypeSafer_InFunctionScope(self){ return InFunctionScope__1qga(self); }

function VisitNullNode__2qga(self, Node) {
   var Type = ZType_GetContextType(self);
   TypedNode__3qrc(self, Node, Type);
   return;
};
function ZenTypeSafer_VisitNullNode(self, Node){ return VisitNullNode__2qga(self, Node); }

function VisitBooleanNode__2qga(self, Node) {
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitBooleanNode(self, Node){ return VisitBooleanNode__2qga(self, Node); }

function VisitIntNode__2qga(self, Node) {
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitIntNode(self, Node){ return VisitIntNode__2qga(self, Node); }

function VisitFloatNode__2qga(self, Node) {
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitFloatNode(self, Node){ return VisitFloatNode__2qga(self, Node); }

function VisitStringNode__2qga(self, Node) {
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitStringNode(self, Node){ return VisitStringNode__2qga(self, Node); }

function VisitArrayLiteralNode__2qga(self, Node) {
   var ArrayType = ZType_GetContextType(self);
   if (IsMapType__1qwg(ArrayType) && GetListSize__1quv(Node) == 0) {
      TypedNode__3qrc(self, ZMapLiteralNode__2q0m(new ZMapLiteralNode(), Node.ParentNode), ArrayType);
      return;
   };
   var ElementType = ZType__4qwg(new ZType(), 1 << 16, "var", null);
   if (IsArrayType__1qwg(ArrayType)) {
      ElementType = ZType_null(ArrayType, 0);
   };
   var i = 0;
   while (i < GetListSize__1quv(Node)) {
      var SubNode = ZNode_GetListAt(Node, i);
      SubNode = ZNode_CheckType(self, SubNode, ElementType);
      SetListAt__3quv(Node, i, SubNode);
      if (ElementType.IsVarType(ElementType)) {
         ElementType = SubNode.Type;
      };
      i = i + 1;
   };
   if (!ElementType.IsVarType(ElementType)) {
      TypedNode__3qrc(self, Node, ZType_ZTypePool_GetGenericType1(ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), ElementType));
   } else {
      TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   return;
};
function ZenTypeSafer_VisitArrayLiteralNode(self, Node){ return VisitArrayLiteralNode__2qga(self, Node); }

function VisitMapLiteralNode__2qga(self, Node) {
   var ContextType = ZType_GetContextType(self);
   var EntryType = ZType__4qwg(new ZType(), 1 << 16, "var", null);
   if (IsMapType__1qwg(ContextType)) {
      EntryType = ZType_null(ContextType, 0);
   };
   var i = 0;
   while (i < GetListSize__1quv(Node)) {
      var EntryNode = ZMapEntryNode_GetMapEntryNode(Node, i);
      if (EntryNode.Name == null) {
         EntryNode.Name = GetText__1qw3(EntryNode.AST[0].SourceToken);
      };
      if (IsUntyped__1qwo(EntryNode)) {
         CheckTypeAt__4qrc(self, EntryNode, 1, EntryType);
         if (EntryType.IsVarType(EntryType)) {
            EntryType = ZType_GetAstType(EntryNode, 1);
         };
      };
      i = i + 1;
   };
   if (!EntryType.IsVarType(EntryType)) {
      TypedNode__3qrc(self, Node, ZType_ZTypePool_GetGenericType1(ZGenericType__5qev(new ZGenericType(), 1 << 16, "Map", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), EntryType));
      return;
   } else {
      TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   return;
};
function ZenTypeSafer_VisitMapLiteralNode(self, Node){ return VisitMapLiteralNode__2qga(self, Node); }

function VisitGlobalNameNode__2qga(self, Node) {
   Return__2qrc(self, Node);
   return;
};
function ZenTypeSafer_VisitGlobalNameNode(self, Node){ return VisitGlobalNameNode__2qga(self, Node); }

function VisitGetNameNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   var VarInfo = ZVariable_GetLocalVariable(NameSpace, Node.VarName);
   if (VarInfo != null) {
      Node.VarName = VarInfo.VarName;
      Node.VarIndex = VarInfo.VarUniqueIndex;
      Node.IsCaptured = IsCaptured__2quu(VarInfo, self.CurrentFunctionNode);
      TypedNode__3qrc(self, Node, VarInfo.VarType);
   } else {
      var SymbolNode = ZNode_GetSymbolNode(NameSpace, Node.VarName);
      if (SymbolNode == null) {
         SymbolNode = ZNode_ToGlobalNameNode(Node);
      };
      TypedNode__3qrc(self, SymbolNode, SymbolNode.Type);
   };
   return;
};
function ZenTypeSafer_VisitGetNameNode(self, Node){ return VisitGetNameNode__2qga(self, Node); }

function VisitSetNameNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   var VarInfo = ZVariable_GetLocalVariable(NameSpace, Node.VarName);
   if (VarInfo == null) {
      ReturnErrorNode__4qrc(self, Node, Node.SourceToken, "undefined variable");
      return;
   };
   Node.VarName = VarInfo.VarName;
   Node.VarIndex = VarInfo.VarUniqueIndex;
   Node.IsCaptured = IsCaptured__2quu(VarInfo, self.CurrentFunctionNode);
   if (Node.IsCaptured) {
      ReturnErrorNode__4qrc(self, Node, Node.SourceToken, "readonly variable");
      return;
   };
   CheckTypeAt__4qrc(self, Node, 0, VarInfo.VarType);
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitSetNameNode(self, Node){ return VisitSetNameNode__2qga(self, Node); }

function GetIndexType__3qga(self, NameSpace, RecvType) {
   if (IsArrayType__1qwg(RecvType) || IsStringType__1qwg(RecvType)) {
      return ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   if (IsMapType__1qwg(RecvType)) {
      return ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   return ZType__4qwg(new ZType(), 1 << 16, "var", null);
};
function ZenTypeSafer_GetIndexType(self, NameSpace, RecvType){ return GetIndexType__3qga(self, NameSpace, RecvType); }

function GetElementType__3qga(self, NameSpace, RecvType) {
   if (IsArrayType__1qwg(RecvType) || IsMapType__1qwg(RecvType)) {
      return RecvType.GetParamType(RecvType, 0);
   };
   if (IsStringType__1qwg(RecvType)) {
      return ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   return ZType__4qwg(new ZType(), 1 << 16, "var", null);
};
function ZenTypeSafer_GetElementType(self, NameSpace, RecvType){ return GetElementType__3qga(self, NameSpace, RecvType); }

function VisitGetIndexNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   CheckTypeAt__4qrc(self, Node, 1, ZType_GetIndexType(self, NameSpace, Node.AST[0].Type));
   TypedNode__3qrc(self, Node, ZType_GetElementType(self, NameSpace, Node.AST[0].Type));
   return;
};
function ZenTypeSafer_VisitGetIndexNode(self, Node){ return VisitGetIndexNode__2qga(self, Node); }

function VisitSetIndexNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   CheckTypeAt__4qrc(self, Node, 1, ZType_GetIndexType(self, NameSpace, Node.AST[0].Type));
   CheckTypeAt__4qrc(self, Node, 2, ZType_GetElementType(self, NameSpace, Node.AST[0].Type));
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitSetIndexNode(self, Node){ return VisitSetIndexNode__2qga(self, Node); }

function VisitGroupNode__2qga(self, Node) {
   var ContextType = ZType_GetContextType(self);
   CheckTypeAt__4qrc(self, Node, 0, ContextType);
   TypedNode__3qrc(self, Node, ZType_GetAstType(Node, 0));
   return;
};
function ZenTypeSafer_VisitGroupNode(self, Node){ return VisitGroupNode__2qga(self, Node); }

function VisitListNodeAsFuncCall__3qga(self, FuncNode, FuncType) {
   var i = 0;
   var Greek = ZGreekType_NewGreekTypes(null);
   while (i < GetListSize__1quv(FuncNode)) {
      var SubNode = ZNode_GetListAt(FuncNode, i);
      var ParamType = ZType_null(FuncType, i + 1);
      SubNode = ZNode_TryType(self, SubNode, ParamType);
      if (!IsUntyped__1qwo(SubNode) || !ParamType.IsVarType(ParamType)) {
         if (!ParamType.AcceptValueType(ParamType, SubNode.Type, false, Greek)) {
            SubNode = ZNode_CreateStupidCastNode(self, ZType_null(ParamType, Greek), SubNode);
         };
      };
      SetListAt__3quv(FuncNode, i, SubNode);
      i = i + 1;
   };
   TypedNode__3qrc(self, FuncNode, ZType_null(ZType_GetReturnType(FuncType), Greek));
   return;
};
function ZenTypeSafer_VisitListNodeAsFuncCall(self, FuncNode, FuncType){ return VisitListNodeAsFuncCall__3qga(self, FuncNode, FuncType); }

function VisitMacroNode__2qga(self, FuncNode) {
   VisitListNodeAsFuncCall__3qga(self, FuncNode, ZFuncType_GetFuncType(FuncNode));
   return;
};
function ZenTypeSafer_VisitMacroNode(self, FuncNode){ return VisitMacroNode__2qga(self, FuncNode); }

function VisitFuncCallNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   TypeCheckNodeList__2qrc(self, Node);
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   var FuncNode = Node.AST[0];
   var FuncNodeType = ZType_GetAstType(Node, 0);
   if ((FuncNodeType).constructor.name == (ZFuncType).name) {
      VisitListNodeAsFuncCall__3qga(self, Node, FuncNodeType);
   } else if ((FuncNode).constructor.name == (ZTypeNode).name) {
      var FuncName = FuncNode.Type.ShortName;
      var Func = ZFunc_LookupFunc(self, NameSpace, FuncName, FuncNode.Type, GetListSize__1quv(Node));
      if (Func != null) {
         Set__3qwo(Node, 0, ZGlobalNameNode__6qpv(new ZGlobalNameNode(), Node, FuncNode.SourceToken, ZFuncType_GetFuncType(Func), FuncName, true));
         VisitListNodeAsFuncCall__3qga(self, Node, ZFuncType_GetFuncType(Func));
         return;
      };
   } else if (FuncNodeType.IsVarType(FuncNodeType)) {
      var FuncName = GetFuncName__1q4e(Node);
      if (FuncName != null) {
         var Func = ZFunc_LookupFunc(self, NameSpace, FuncName, ZType_GetRecvType(Node), GetListSize__1quv(Node));
         if ((Func).constructor.name == (ZMacroFunc).name) {
            var MacroNode = ZMacroNode_ToMacroNode(Node, Func);
            VisitListNodeAsFuncCall__3qga(self, MacroNode, ZFuncType_GetFuncType(Func));
            return;
         } else if (Func != null) {
            var NameNode = Node.AST[0];
            NameNode.Type = ZFuncType_GetFuncType(Func);
            NameNode.IsStaticFuncName = true;
            VisitListNodeAsFuncCall__3qga(self, Node, ZFuncType_GetFuncType(Func));
            return;
         };
      };
      TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   } else {
      Return__2qrc(self, ZErrorNode__3qpr(new ZErrorNode(), Node, (("not function: " + toString__1qwg(FuncNodeType)) + " of node ") + toString__1qwo(Node.AST[0])));
   };
   return;
};
function ZenTypeSafer_VisitFuncCallNode(self, Node){ return VisitFuncCallNode__2qga(self, Node); }

function LookupFieldType__4qga(self, NameSpace, ClassType, FieldName) {
   ClassType = ClassType.GetRealType(ClassType);
   if ((ClassType).constructor.name == (ZClassType).name) {
      return ZType_GetFieldType((ClassType), FieldName, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   };
   return NameSpace.Generator.GetFieldType(NameSpace.Generator, ClassType, FieldName);
};
function ZenTypeSafer_LookupFieldType(self, NameSpace, ClassType, FieldName){ return LookupFieldType__4qga(self, NameSpace, ClassType, FieldName); }

function LookupSetterType__4qga(self, NameSpace, ClassType, FieldName) {
   ClassType = ClassType.GetRealType(ClassType);
   if ((ClassType).constructor.name == (ZClassType).name) {
      return ZType_GetFieldType((ClassType), FieldName, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   };
   return NameSpace.Generator.GetSetterType(NameSpace.Generator, ClassType, FieldName);
};
function ZenTypeSafer_LookupSetterType(self, NameSpace, ClassType, FieldName){ return LookupSetterType__4qga(self, NameSpace, ClassType, FieldName); }

function UndefinedFieldNode__3qga(self, Node, Name) {
   return ZErrorNode__3qpr(new ZErrorNode(), Node, (("undefined field: " + Name) + " of ") + toString__1qwg(ZType_GetAstType(Node, 0)));
};
function ZenTypeSafer_UndefinedFieldNode(self, Node, Name){ return UndefinedFieldNode__3qga(self, Node, Name); }

function VisitGetterNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   if (!IsUntyped__1qwo(Node.AST[0])) {
      var FieldType = ZType_LookupFieldType(self, NameSpace, ZType_GetAstType(Node, 0), Node.FieldName);
      if (IsVoidType__1qwg(FieldType)) {
         Return__2qrc(self, ZNode_UndefinedFieldNode(self, Node, Node.FieldName));
         return;
      };
      TypedNode__3qrc(self, Node, FieldType);
   } else {
      TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   return;
};
function ZenTypeSafer_VisitGetterNode(self, Node){ return VisitGetterNode__2qga(self, Node); }

function VisitSetterNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   if (!IsUntyped__1qwo(Node.AST[0])) {
      var FieldType = ZType_LookupSetterType(self, NameSpace, ZType_GetAstType(Node, 0), Node.FieldName);
      if (IsVoidType__1qwg(FieldType)) {
         Return__2qrc(self, ZNode_UndefinedFieldNode(self, Node, Node.FieldName));
         return;
      };
      CheckTypeAt__4qrc(self, Node, 1, FieldType);
      TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   } else {
      TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   return;
};
function ZenTypeSafer_VisitSetterNode(self, Node){ return VisitSetterNode__2qga(self, Node); }

function VisitListAsNativeMethod__5qga(self, Node, RecvType, MethodName, List) {
   var FuncType = self.Generator.GetMethodFuncType(self.Generator, RecvType, MethodName, List);
   if (FuncType != null) {
      if (!FuncType.IsVarType(FuncType)) {
         var i = 0;
         var StaticShift = FuncType.GetParamSize(FuncType) - GetListSize__1quv(List);
         while (i < GetListSize__1quv(List)) {
            var SubNode = ZNode_GetListAt(List, i);
            SubNode = ZNode_CheckType(self, SubNode, FuncType.GetParamType(FuncType, i + StaticShift));
            SetListAt__3quv(List, i, SubNode);
            i = i + 1;
         };
      };
      TypedNode__3qrc(self, Node, ZType_GetReturnType(FuncType));
      return;
   };
   var Message = null;
   if (MethodName == null) {
      Message = "undefined constructor: " + toString__1qwg(RecvType);
   } else {
      Message = (("undefined method: " + MethodName) + " of ") + toString__1qwg(RecvType);
   };
   ReturnErrorNode__4qrc(self, Node, null, Message);
   return;
};
function ZenTypeSafer_VisitListAsNativeMethod(self, Node, RecvType, MethodName, List){ return VisitListAsNativeMethod__5qga(self, Node, RecvType, MethodName, List); }

function VisitMethodCallNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   if (!IsUntyped__1qwo(Node.AST[0])) {
      var FieldType = ZType_LookupFieldType(self, NameSpace, ZType_GetAstType(Node, 0), Node.MethodName);
      if ((FieldType).constructor.name == (ZFuncType).name) {
         var FuncCall = ZFuncCallNode_ToGetterFuncCall(Node);
         VisitListNodeAsFuncCall__3qga(self, FuncCall, FieldType);
         return;
      };
      var FuncParamSize = GetListSize__1quv(Node) + 1;
      var Func = ZFunc_LookupFunc(self, NameSpace, Node.MethodName, ZType_GetAstType(Node, 0), FuncParamSize);
      if (Func != null) {
         var FuncCall = ZListNode_ToFuncCallNode(Node, Func);
         VisitListNodeAsFuncCall__3qga(self, FuncCall, ZFuncType_GetFuncType(Func));
      } else {
         VisitListAsNativeMethod__5qga(self, Node, ZType_GetAstType(Node, 0), Node.MethodName, Node);
      };
   } else {
      TypeCheckNodeList__2qrc(self, Node);
      TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   return;
};
function ZenTypeSafer_VisitMethodCallNode(self, Node){ return VisitMethodCallNode__2qga(self, Node); }

function VisitNewObjectNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   var ContextType = ZType_GetContextType(self);
   TypeCheckNodeList__2qrc(self, Node);
   if (Node.Type.IsVarType(Node.Type)) {
      if (ContextType.IsVarType(ContextType)) {
         TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "var", null));
         return;
      };
      Node.Type = ContextType;
   };
   var FuncParamSize = GetListSize__1quv(Node) + 1;
   var Func = ZFunc_LookupFunc(self, NameSpace, Node.Type.ShortName, Node.Type, FuncParamSize);
   if (Func != null) {
      var FuncCall = ZListNode_ToFuncCallNode(Node, Func);
      VisitListNodeAsFuncCall__3qga(self, FuncCall, ZFuncType_GetFuncType(Func));
      return;
   };
   VisitListAsNativeMethod__5qga(self, Node, Node.Type, null, Node);
   return;
};
function ZenTypeSafer_VisitNewObjectNode(self, Node){ return VisitNewObjectNode__2qga(self, Node); }

function VisitUnaryNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   TypedNode__3qrc(self, Node, Node.AST[0].Type);
   return;
};
function ZenTypeSafer_VisitUnaryNode(self, Node){ return VisitUnaryNode__2qga(self, Node); }

function VisitNotNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, ZNotNode_Recv, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitNotNode(self, Node){ return VisitNotNode__2qga(self, Node); }

function VisitCastNode__2qga(self, Node) {
   TryTypeAt__4qrc(self, Node, 0, Node.Type);
   var ExprType = Node.AST[0].Type;
   if (Equals__2qwg(ExprType, Node.Type)) {
      Return__2qrc(self, Node.AST[0]);
   };
   var Func = ZFunc_GetCoercionFunc(self.Generator, ExprType, Node.Type);
   if (Func != null) {
      TypedNode__3qrc(self, ZListNode_ToFuncCallNode(Node, Func), Node.Type);
   };
   TypedNode__3qrc(self, Node, Node.Type);
   return;
};
function ZenTypeSafer_VisitCastNode(self, Node){ return VisitCastNode__2qga(self, Node); }

function VisitInstanceOfNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitInstanceOfNode(self, Node){ return VisitInstanceOfNode__2qga(self, Node); }

function GuessBinaryLeftType__3qga(self, Op, ContextType) {
   if (EqualsText__2qw3(Op, "|") || EqualsText__2qw3(Op, "&") || EqualsText__2qw3(Op, "<<") || EqualsText__2qw3(Op, ">>") || EqualsText__2qw3(Op, "^")) {
      return ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null));
   };
   if (EqualsText__2qw3(Op, "+") || EqualsText__2qw3(Op, "-") || EqualsText__2qw3(Op, "*") || EqualsText__2qw3(Op, "/") || EqualsText__2qw3(Op, "%")) {
      if (IsNumberType__1qwg(ContextType)) {
         return ContextType;
      };
   };
   return ZType__4qwg(new ZType(), 1 << 16, "var", null);
};
function ZenTypeSafer_GuessBinaryLeftType(self, Op, ContextType){ return GuessBinaryLeftType__3qga(self, Op, ContextType); }

function UnifyBinaryNodeType__3qga(self, Node, Type) {
   if (Equals__2qwg(ZType_GetAstType(Node, 0), Type)) {
      CheckTypeAt__4qrc(self, Node, 1, Type);
      return;
   };
   if (Equals__2qwg(ZType_GetAstType(Node, 1), Type)) {
      CheckTypeAt__4qrc(self, Node, 0, Type);
   };
   return;
};
function ZenTypeSafer_UnifyBinaryNodeType(self, Node, Type){ return UnifyBinaryNodeType__3qga(self, Node, Type); }

function UnifyBinaryEnforcedType__3qga(self, Node, Type) {
   if (Equals__2qwg(ZType_GetAstType(Node, 0), Type)) {
      Set__3qwo(Node, 1, ZNode_EnforceNodeType(self, Node.AST[1], Type));
      return;
   };
   if (Equals__2qwg(ZType_GetAstType(Node, 1), Type)) {
      Set__3qwo(Node, 0, ZNode_EnforceNodeType(self, Node.AST[0], Type));
   };
   return;
};
function ZenTypeSafer_UnifyBinaryEnforcedType(self, Node, Type){ return UnifyBinaryEnforcedType__3qga(self, Node, Type); }

function VisitBinaryNode__2qga(self, Node) {
   var ContextType = ZType_GetContextType(self);
   var LeftType = ZType_GuessBinaryLeftType(self, Node.SourceToken, ContextType);
   var RightType = ZType_GuessBinaryLeftType(self, Node.SourceToken, ContextType);
   CheckTypeAt__4qrc(self, Node, 0, LeftType);
   CheckTypeAt__4qrc(self, Node, 1, RightType);
   if (!Equals__2qwg(ZType_GetAstType(Node, 0), ZType_GetAstType(Node, 1))) {
      if (EqualsText__2qw3(Node.SourceToken, "+")) {
         UnifyBinaryEnforcedType__3qga(self, Node, ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
      };
      UnifyBinaryNodeType__3qga(self, Node, ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
      CheckTypeAt__4qrc(self, Node, 0, ZType_GetAstType(Node, 1));
   };
   TypedNode__3qrc(self, ZNode_TryMacroNode(Node, self.Generator), ZType_GetAstType(Node, 0));
   return;
};
function ZenTypeSafer_VisitBinaryNode(self, Node){ return VisitBinaryNode__2qga(self, Node); }

function VisitComparatorNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   TryTypeAt__4qrc(self, Node, 1, ZType_GetAstType(Node, 0));
   UnifyBinaryNodeType__3qga(self, Node, ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitComparatorNode(self, Node){ return VisitComparatorNode__2qga(self, Node); }

function VisitAndNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   CheckTypeAt__4qrc(self, Node, 1, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitAndNode(self, Node){ return VisitAndNode__2qga(self, Node); }

function VisitOrNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   CheckTypeAt__4qrc(self, Node, 1, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   return;
};
function ZenTypeSafer_VisitOrNode(self, Node){ return VisitOrNode__2qga(self, Node); }

function VisitBlockNode__2qga(self, Node) {
   var i = 0;
   while (i < GetListSize__1quv(Node)) {
      var SubNode = ZNode_GetListAt(Node, i);
      SubNode = ZNode_CheckType(self, SubNode, ZType__4qwg(new ZType(), 1 << 16, "void", null));
      SetListAt__3quv(Node, i, SubNode);
      if (SubNode.IsBreakingBlock(SubNode)) {
         ClearListAfter__2quv(Node, i + 1);
         break;
      };
      i = i + 1;
   };
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitBlockNode(self, Node){ return VisitBlockNode__2qga(self, Node); }

function VisitVarNode__2qga(self, Node) {
   if (!InFunctionScope__1qga(self)) {
      ReturnErrorNode__4qrc(self, Node, Node.SourceToken, "only available inside function");
      return;
   };
   CheckTypeAt__4qrc(self, Node, 0, Node.DeclType);
   if (!((Node.DeclType).constructor.name == (ZVarType).name)) {
      Node.DeclType = ZType_NewVarType(self.VarScope, Node.DeclType, Node.NativeName, Node.SourceToken);
      Node.VarIndex = SetLocalVariable__5qwt(Node.NameSpace, self.CurrentFunctionNode, Node.DeclType, Node.NativeName, Node.SourceToken);
   };
   if (GetListSize__1quv(Node) == 0) {
      ZLogger_LogWarning__2qw3(Node.SourceToken, "unused variable: " + Node.NativeName);
   };
   self.VisitBlockNode(self, Node);
   return;
};
function ZenTypeSafer_VisitVarNode(self, Node){ return VisitVarNode__2qga(self, Node); }

function VisitIfNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   CheckTypeAt__4qrc(self, Node, 1, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   if (HasAst__2qwo(Node, 2)) {
      CheckTypeAt__4qrc(self, Node, 2, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   };
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitIfNode(self, Node){ return VisitIfNode__2qga(self, Node); }

function VisitReturnNode__2qga(self, Node) {
   if (!InFunctionScope__1qga(self)) {
      ReturnErrorNode__4qrc(self, Node, Node.SourceToken, "only available inside function");
      return;
   };
   var ReturnType = self.CurrentFunctionNode.ReturnType;
   if (HasAst__2qwo(Node, 0) && IsVoidType__1qwg(ReturnType)) {
      Node.AST[0] = null;
   } else if (!HasAst__2qwo(Node, 0) && !ReturnType.IsVarType(ReturnType) && !IsVoidType__1qwg(ReturnType)) {
      ZLogger_LogWarning__2qw3(Node.SourceToken, "returning default value of " + toString__1qwg(ReturnType));
      Set__3qwo(Node, 0, ZNode_ZConstNode_CreateDefaultValueNode(Node, ReturnType, null));
   };
   if (HasAst__2qwo(Node, 0)) {
      CheckTypeAt__4qrc(self, Node, 0, ReturnType);
   } else {
      if ((ReturnType).constructor.name == (ZVarType).name) {
         Infer__3qrl((ReturnType), ZType__4qwg(new ZType(), 1 << 16, "void", null), Node.SourceToken);
      };
   };
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitReturnNode(self, Node){ return VisitReturnNode__2qga(self, Node); }

function VisitWhileNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   CheckTypeAt__4qrc(self, Node, 1, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitWhileNode(self, Node){ return VisitWhileNode__2qga(self, Node); }

function VisitBreakNode__2qga(self, Node) {
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitBreakNode(self, Node){ return VisitBreakNode__2qga(self, Node); }

function VisitThrowNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "var", null));
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitThrowNode(self, Node){ return VisitThrowNode__2qga(self, Node); }

function VisitTryNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   if (HasAst__2qwo(Node, 1)) {
      CheckTypeAt__4qrc(self, Node, 1, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   };
   if (HasAst__2qwo(Node, 2)) {
      CheckTypeAt__4qrc(self, Node, 2, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   };
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitTryNode(self, Node){ return VisitTryNode__2qga(self, Node); }

function VisitLetNode__2qga(self, Node) {
   CheckTypeAt__4qrc(self, Node, 0, Node.SymbolType);
   if (!ZType_GetAstType(Node, 0).IsVarType(ZType_GetAstType(Node, 0))) {
      Node.GlobalName = NameGlobalSymbol__2qw4(self.Generator, Node.Symbol);
      ZSymbolEntry_SetLocalSymbol(ZNameSpace_GetNameSpace(Node), Node.Symbol, Node.AST[0]);
   };
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitLetNode(self, Node){ return VisitLetNode__2qga(self, Node); }

function HasReturn__2qga(self, Node) {
   if ((Node).constructor.name == (ZBlockNode).name) {
      var BlockNode = Node;
      var i = 0;
      var StmtNode = null;
      while (i < GetListSize__1quv(BlockNode)) {
         StmtNode = ZNode_GetListAt(BlockNode, i);
         if ((StmtNode).constructor.name == (ZReturnNode).name) {
            return true;
         };
         i = i + 1;
      };
      Node = StmtNode;
   };
   if ((Node).constructor.name == (ZReturnNode).name) {
      return true;
   };
   if ((Node).constructor.name == (ZIfNode).name) {
      var IfNode = Node;
      if (HasAst__2qwo(IfNode, 2)) {
         return HasReturn__2qga(self, IfNode.AST[1]) && HasReturn__2qga(self, IfNode.AST[2]);
      };
      return false;
   };
   if ((Node).constructor.name == (ZBlockNode).name) {
      return HasReturn__2qga(self, Node);
   };
   return false;
};
function ZenTypeSafer_HasReturn(self, Node){ return HasReturn__2qga(self, Node); }

function DefineFunction__3qga(self, FunctionNode, Enforced) {
   if (FunctionNode.FuncName != null && FunctionNode.ResolvedFuncType == null) {
      var FuncType = ZFuncType_GetFuncType(FunctionNode, null);
      if (Enforced || !FuncType.IsVarType(FuncType)) {
         var NameSpace = ZNameSpace_GetNameSpace(FunctionNode);
         var Func = ZPrototype_SetPrototype(NameSpace.Generator, FunctionNode, FunctionNode.FuncName, FuncType);
         if (Func != null) {
            Defined__1qry(Func);
            if (Func.DefinedCount > 1) {
               ZLogger_LogError__2qw3(FunctionNode.SourceToken, "redefinition of function: " + toString__1qep(Func));
            };
         };
      };
   };
   return;
};
function ZenTypeSafer_DefineFunction(self, FunctionNode, Enforced){ return DefineFunction__3qga(self, FunctionNode, Enforced); }

function PushFunctionNode__4qga(self, NameSpace, FunctionNode, ContextType) {
   var FuncType = null;
   if ((ContextType).constructor.name == (ZFuncType).name) {
      FuncType = ContextType;
   };
   self.CurrentFunctionNode = ZFunctionNode_Push(FunctionNode, self.CurrentFunctionNode);
   self.VarScope = ZVarScope__4qrj(new ZVarScope(), self.VarScope, self.Logger, null);
   var i = 0;
   while (i < GetListSize__1quv(FunctionNode)) {
      var ParamNode = ZParamNode_GetParamNode(FunctionNode, i);
      ParamNode.ParamIndex = i;
      ParamNode.Type = ZType_NewVarType(self.VarScope, ParamNode.Type, ParamNode.Name, ParamNode.SourceToken);
      if (FuncType != null) {
         Maybe__3qwg(ParamNode.Type, ZType_null(FuncType, i + 1), null);
      };
      SetLocalVariable__5qwt(NameSpace, self.CurrentFunctionNode, ParamNode.Type, ParamNode.Name, null);
      i = i + 1;
   };
   FunctionNode.ReturnType = ZType_NewVarType(self.VarScope, FunctionNode.ReturnType, "return", FunctionNode.SourceToken);
   if (FuncType != null) {
      Maybe__3qwg(FunctionNode.Type, ZType_null(FuncType, 0), null);
   };
   return;
};
function ZenTypeSafer_PushFunctionNode(self, NameSpace, FunctionNode, ContextType){ return PushFunctionNode__4qga(self, NameSpace, FunctionNode, ContextType); }

function PopFunctionNode__2qga(self, NameSpace) {
   self.CurrentFunctionNode = ZFunctionNode_Pop(self.CurrentFunctionNode);
   self.VarScope = self.VarScope.Parent;
   return;
};
function ZenTypeSafer_PopFunctionNode(self, NameSpace){ return PopFunctionNode__2qga(self, NameSpace); }

function VisitFunctionNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node.AST[0]);
   var ContextType = ZType_GetContextType(self);
   if (IsUntyped__1qwo(Node)) {
      Node.Type = ContextType;
   };
   if (IsVoidType__1qwg(Node.Type)) {
      if (Node.FuncName == null) {
         Node.Type = ZType__4qwg(new ZType(), 1 << 16, "var", null);
      };
      if (!IsTopLevel__1qga(self)) {
         var VarNode = ZVarNode__2qsc(new ZVarNode(), Node.ParentNode);
         VarNode.SetNameInfo(VarNode, null, Node.FuncName);
         Set__3qwo(VarNode, 0, Node);
         var Block = ZBlockNode_GetScopeBlockNode(Node);
         var Index = IndexOf__2qtp(Block, Node);
         CopyTo__3qtp(Block, Index + 1, VarNode);
         ClearListAfter__2quv(Block, Index + 1);
         self.VisitVarNode(self, VarNode);
         return;
      };
   };
   if (!HasReturn__2qga(self, Node.AST[0])) {
      Set__3qwo(Node.AST[0], -4, ZReturnNode__2qtj(new ZReturnNode(), Node));
   };
   PushFunctionNode__4qga(self, NameSpace, Node, ContextType);
   TypeCheckFuncBlock__3qrj(self.VarScope, self, Node);
   PopFunctionNode__2qga(self, NameSpace);
   if (!IsVoidType__1qwg(Node.Type)) {
      Node.Type = ZFuncType_GetFuncType(Node, ContextType);
   };
   Return__2qrc(self, Node);
   return;
};
function ZenTypeSafer_VisitFunctionNode(self, Node){ return VisitFunctionNode__2qga(self, Node); }

function VisitClassNode__2qga(self, Node) {
   var NameSpace = ZNameSpace_GetNameSpace(Node);
   var ClassType = ZType_GetType(NameSpace, Node.ClassName, Node.SourceToken);
   if ((ClassType).constructor.name == (ZClassType).name) {
      if (!IsOpenType__1qwg(ClassType)) {
         Return__2qrc(self, ZErrorNode__3qpr(new ZErrorNode(), Node, Node.ClassName + " has been defined."));
         return;
      };
      Node.ClassType = ClassType;
   } else {
      Return__2qrc(self, ZErrorNode__3qpr(new ZErrorNode(), Node, Node.ClassName + " is not a Zen class."));
      return;
   };
   if (Node.SuperType != null) {
      if ((Node.SuperType).constructor.name == (ZClassType).name && !IsOpenType__1qwg(Node.SuperType)) {
         ResetSuperType__2qeq(Node.ClassType, Node.SuperType);
      } else {
         Return__2qrc(self, ZErrorNode__4qpr(new ZErrorNode(), Node.ParentNode, Node.SuperToken, ("" + toString__1qwg(Node.SuperType)) + " cannot be extended."));
         return;
      };
   };
   var i = 0;
   while (i < GetListSize__1quv(Node)) {
      var FieldNode = ZFieldNode_GetFieldNode(Node, i);
      if (!HasAst__2qwo(FieldNode, 0)) {
         Set__3qwo(FieldNode, 0, ZNode_ZConstNode_CreateDefaultValueNode(FieldNode, FieldNode.DeclType, FieldNode.FieldName));
      };
      if (!HasField__2qeq(Node.ClassType, FieldNode.FieldName)) {
         FieldNode.ClassType = Node.ClassType;
         CheckTypeAt__4qrc(self, FieldNode, 0, FieldNode.DeclType);
         if (FieldNode.DeclType.IsVarType(FieldNode.DeclType)) {
            FieldNode.DeclType = FieldNode.AST[0].Type;
         };
         if (FieldNode.DeclType.IsVarType(FieldNode.DeclType)) {
            ZLogger_LogError__2qw3(FieldNode.SourceToken, ("type of " + FieldNode.FieldName) + " is unspecific");
         } else {
            ZClassField_AppendField(Node.ClassType, FieldNode.DeclType, FieldNode.FieldName, FieldNode.SourceToken);
         };
      } else {
         ZLogger_LogError__2qw3(FieldNode.SourceToken, "duplicated field: " + FieldNode.FieldName);
      };
      FieldNode.Type = ZType__4qwg(new ZType(), 1 << 16, "void", null);
      i = i + 1;
   };
   Node.ClassType.TypeFlag = LibZen.UnsetFlag(Node.ClassType.TypeFlag, 1 << 9);
   TypedNode__3qrc(self, Node, ZType__4qwg(new ZType(), 1 << 16, "void", null));
   return;
};
function ZenTypeSafer_VisitClassNode(self, Node){ return VisitClassNode__2qga(self, Node); }

function LookupFunc__5qga(self, NameSpace, FuncName, RecvType, FuncParamSize) {
   var Signature = ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, RecvType);
   var Func = ZFunc_GetDefinedFunc(self.Generator, Signature);
   if (Func != null) {
      return Func;
   };
   if (IsIntType__1qwg(RecvType)) {
      Signature = ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
      Func = ZFunc_GetDefinedFunc(self.Generator, Signature);
      if (Func != null) {
         return Func;
      };
   };
   if (IsFloatType__1qwg(RecvType)) {
      Signature = ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
      Func = ZFunc_GetDefinedFunc(self.Generator, Signature);
      if (Func != null) {
         return Func;
      };
   };
   RecvType = ZType_null(RecvType);
   while (RecvType != null) {
      Signature = ZFunc_StringfySignature__3qqy(FuncName, FuncParamSize, RecvType);
      Func = ZFunc_GetDefinedFunc(self.Generator, Signature);
      if (Func != null) {
         return Func;
      };
      if (RecvType.IsVarType(RecvType)) {
         break;
      };
      RecvType = ZType_null(RecvType);
   };
   return null;
};
function ZenTypeSafer_LookupFunc(self, NameSpace, FuncName, RecvType, FuncParamSize){ return LookupFunc__5qga(self, NameSpace, FuncName, RecvType, FuncParamSize); }

function ZAndNode__5qs1(self, ParentNode, Token, Left, Pattern) {
   ZBinaryNode__5qos(self, ParentNode, Token, Left, Pattern);
   return self;
};

function Accept__2qs1(self, Visitor) {
   Visitor.VisitAndNode(Visitor, self);
   return;
};
function ZAndNode_Accept(self, Visitor){ return Accept__2qs1(self, Visitor); }

function ZArrayLiteralNode__2qsw(self, ParentNode) {
   ZListNode__4quv(self, ParentNode, null, 0);
   return self;
};

function Accept__2qsw(self, Visitor) {
   Visitor.VisitArrayLiteralNode(Visitor, self);
   return;
};
function ZArrayLiteralNode_Accept(self, Visitor){ return Accept__2qsw(self, Visitor); }

function ZBlockNode__2qtp(self, NameSpace) {
   ZListNode__4quv(self, null, null, 0);
   self.NameSpace = NameSpace;
   return self;
};

function ZBlockNode__3qtp(self, ParentNode, Init) {
   ZListNode__4quv(self, ParentNode, null, Init);
   self.NameSpace = ZNameSpace_CreateSubNameSpace(ZNameSpace_GetNameSpace(ParentNode));
   return self;
};

function Accept__2qtp(self, Visitor) {
   Visitor.VisitBlockNode(Visitor, self);
   return;
};
function ZBlockNode_Accept(self, Visitor){ return Accept__2qtp(self, Visitor); }

function ToReturnNode__1qtp(self) {
   if (GetListSize__1quv(self) == 1) {
      return ZReturnNode_ToReturnNode(ZNode_GetListAt(self, 0));
   };
   return null;
};
function ZBlockNode_ToReturnNode(self){ return ToReturnNode__1qtp(self); }

function IndexOf__2qtp(self, ChildNode) {
   var i = 0;
   while (i < GetListSize__1quv(self)) {
      if (ZNode_GetListAt(self, i) == ChildNode) {
         return i;
      };
      i = i + 1;
   };
   return -1;
};
function ZBlockNode_IndexOf(self, ChildNode){ return IndexOf__2qtp(self, ChildNode); }

function CopyTo__3qtp(self, Index, BlockNode) {
   var i = Index;
   while (i < GetListSize__1quv(self)) {
      Append__2quv(BlockNode, ZNode_GetListAt(self, i));
      i = i + 1;
   };
   return;
};
function ZBlockNode_CopyTo(self, Index, BlockNode){ return CopyTo__3qtp(self, Index, BlockNode); }

function ZBooleanNode__4qa5(self, ParentNode, Token, Value) {
   ZConstNode__3qo2(self, ParentNode, Token);
   self.Type = ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null));
   self.BooleanValue = Value;
   return self;
};

function Accept__2qa5(self, Visitor) {
   Visitor.VisitBooleanNode(Visitor, self);
   return;
};
function ZBooleanNode_Accept(self, Visitor){ return Accept__2qa5(self, Visitor); }

function ZClassNode__2qdq(self, ParentNode) {
   ZListNode__4quv(self, ParentNode, null, 0);
   return self;
};

function SetTypeInfo__3qdq(self, TypeToken, Type) {
   self.SuperType = Type;
   self.SuperToken = TypeToken;
   return;
};
function ZClassNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3qdq(self, TypeToken, Type); }

function SetNameInfo__3qdq(self, NameToken, Name) {
   self.ClassName = Name;
   self.NameToken = NameToken;
   return;
};
function ZClassNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qdq(self, NameToken, Name); }

function GetFieldNode__2qdq(self, Index) {
   var Node = ZNode_GetListAt(self, Index);
   if ((Node).constructor.name == (ZFieldNode).name) {
      return Node;
   };
   return null;
};
function ZClassNode_GetFieldNode(self, Index){ return GetFieldNode__2qdq(self, Index); }

function Accept__2qdq(self, Visitor) {
   Visitor.VisitClassNode(Visitor, self);
   return;
};
function ZClassNode_Accept(self, Visitor){ return Accept__2qdq(self, Visitor); }

function ZFuncCallNode__3q4e(self, ParentNode, FuncNode) {
   ZListNode__4quv(self, ParentNode, null, 1);
   Set__3qwo(self, 0, FuncNode);
   return self;
};

function ZFuncCallNode__4q4e(self, ParentNode, FuncName, FuncType) {
   ZListNode__4quv(self, ParentNode, null, 1);
   var FuncNode = ZGlobalNameNode__6qpv(new ZGlobalNameNode(), self, null, FuncType, FuncName, true);
   Set__3qwo(self, 0, FuncNode);
   return self;
};

function Accept__2q4e(self, Visitor) {
   Visitor.VisitFuncCallNode(Visitor, self);
   return;
};
function ZFuncCallNode_Accept(self, Visitor){ return Accept__2q4e(self, Visitor); }

function GetRecvType__1q4e(self) {
   if (GetListSize__1quv(self) > 0) {
      return ZNode_GetListAt(self, 0).Type.GetRealType(ZNode_GetListAt(self, 0).Type);
   };
   return ZType__4qwg(new ZType(), 1 << 16, "void", null);
};
function ZFuncCallNode_GetRecvType(self){ return GetRecvType__1q4e(self); }

function GetFuncName__1q4e(self) {
   var FNode = self.AST[0];
   if ((FNode).constructor.name == (ZGlobalNameNode).name) {
      return (FNode).GlobalName;
   };
   return null;
};
function ZFuncCallNode_GetFuncName(self){ return GetFuncName__1q4e(self); }

function GetFuncType__1q4e(self) {
   var FType = self.AST[0].Type;
   if ((FType).constructor.name == (ZFuncType).name) {
      return FType;
   };
   return null;
};
function ZFuncCallNode_GetFuncType(self){ return GetFuncType__1q4e(self); }

function ToMacroNode__2q4e(self, MacroFunc) {
   var MacroNode = ZMacroNode__4q06(new ZMacroNode(), self.ParentNode, self.AST[0].SourceToken, MacroFunc);
   var i = 0;
   while (i < GetListSize__1quv(self)) {
      Append__2quv(MacroNode, ZNode_GetListAt(self, i));
      i = i + 1;
   };
   return MacroNode;
};
function ZFuncCallNode_ToMacroNode(self, MacroFunc){ return ToMacroNode__2q4e(self, MacroFunc); }

function ZFunctionNode__2qrb(self, ParentNode) {
   ZListNode__4quv(self, ParentNode, null, 1);
   return self;
};

function SetTypeInfo__3qrb(self, TypeToken, Type) {
   self.ReturnType = Type;
   return;
};
function ZFunctionNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3qrb(self, TypeToken, Type); }

function SetNameInfo__3qrb(self, NameToken, Name) {
   self.FuncName = Name;
   self.NameToken = NameToken;
   return;
};
function ZFunctionNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qrb(self, NameToken, Name); }

function Accept__2qrb(self, Visitor) {
   Visitor.VisitFunctionNode(Visitor, self);
   return;
};
function ZFunctionNode_Accept(self, Visitor){ return Accept__2qrb(self, Visitor); }

function GetParamNode__2qrb(self, Index) {
   var Node = ZNode_GetListAt(self, Index);
   if ((Node).constructor.name == (ZParamNode).name) {
      return Node;
   };
   return null;
};
function ZFunctionNode_GetParamNode(self, Index){ return GetParamNode__2qrb(self, Index); }

function GetFuncType__2qrb(self, ContextType) {
   if (self.ResolvedFuncType == null) {
      var FuncType = null;
      if ((ContextType).constructor.name == (ZFuncType).name) {
         FuncType = ContextType;
      };
      var TypeList = [];
      if (self.ReturnType.IsVarType(self.ReturnType) && FuncType != null) {
         self.ReturnType = ZType_null(FuncType, 0);
      };
      TypeList.push(ZType_null(self.ReturnType));
      var i = 0;
      while (i < GetListSize__1quv(self)) {
         var Node = ZParamNode_GetParamNode(self, i);
         var ParamType = ZType_null(Node.Type);
         if (ParamType.IsVarType(ParamType) && FuncType != null) {
            ParamType = ZType_null(FuncType, i + 1);
         };
         TypeList.push(ParamType);
         i = i + 1;
      };
      FuncType = ZFuncType_ZTypePool_LookupFuncType(TypeList);
      if (!FuncType.IsVarType(FuncType)) {
         self.ResolvedFuncType = FuncType;
      };
      return FuncType;
   };
   return self.ResolvedFuncType;
};
function ZFunctionNode_GetFuncType(self, ContextType){ return GetFuncType__2qrb(self, ContextType); }

function GetSignature__2qrb(self, Generator) {
   var FuncType = ZFuncType_GetFuncType(self, null);
   if (self.FuncName == null) {
      self.FuncName = "f_Z" + (GetUniqueNumber__1qw4(Generator)).toString();
   };
   return StringfySignature__2qe0(FuncType, self.FuncName);
};
function ZFunctionNode_GetSignature(self, Generator){ return GetSignature__2qrb(self, Generator); }

function Push__2qrb(self, Parent) {
   self.ParentFunctionNode = Parent;
   return self;
};
function ZFunctionNode_Push(self, Parent){ return Push__2qrb(self, Parent); }

function Pop__1qrb(self) {
   return self.ParentFunctionNode;
};
function ZFunctionNode_Pop(self){ return Pop__1qrb(self); }

function IsTopLevel__1qrb(self) {
   return self.ParentFunctionNode == null;
};
function ZFunctionNode_IsTopLevel(self){ return IsTopLevel__1qrb(self); }

function GetVarIndex__1qrb(self) {
   var Index = self.VarIndex;
   self.VarIndex = self.VarIndex + 1;
   return Index;
};
function ZFunctionNode_GetVarIndex(self){ return GetVarIndex__1qrb(self); }

function ZVarNode__2qsc(self, ParentNode) {
   ZBlockNode__3qtp(self, ParentNode, 1);
   return self;
};

function SetNameInfo__3qsc(self, NameToken, Name) {
   self.NativeName = Name;
   self.NameToken = NameToken;
   return;
};
function ZVarNode_SetNameInfo(self, NameToken, Name){ return SetNameInfo__3qsc(self, NameToken, Name); }

function SetTypeInfo__3qsc(self, TypeToken, Type) {
   self.DeclType = Type;
   self.TypeToken = TypeToken;
   return;
};
function ZVarNode_SetTypeInfo(self, TypeToken, Type){ return SetTypeInfo__3qsc(self, TypeToken, Type); }

function Accept__2qsc(self, Visitor) {
   Visitor.VisitVarNode(Visitor, self);
   return;
};
function ZVarNode_Accept(self, Visitor){ return Accept__2qsc(self, Visitor); }

var AndPattern_Z82 = (function(ParentNode, TokenContext, LeftNode) {
   var BinaryNode = ZAndNode__5qs1(new ZAndNode(), ParentNode, ZToken_GetToken(TokenContext, true), LeftNode, ZSyntax_GetApplyingSyntax(TokenContext));
   return ZNode_AppendParsedRightNode(BinaryNode, ParentNode, TokenContext);
});
var AnnotationPattern_Z83 = (function(ParentNode, TokenContext, LeftNode) {
   return null;
});
var ApplyPattern_Z84 = (function(ParentNode, TokenContext, LeftNode) {
   var ApplyNode = ZFuncCallNode__3q4e(new ZFuncCallNode(), ParentNode, LeftNode);
   ApplyNode = ZNode_MatchNtimes(TokenContext, ApplyNode, "(", "$Expression$", ",", ")");
   return ApplyNode;
});
var ArrayLiteralPattern_Z85 = (function(ParentNode, TokenContext, LeftNode) {
   var LiteralNode = ZArrayLiteralNode__2qsw(new ZArrayLiteralNode(), ParentNode);
   LiteralNode = ZNode_MatchNtimes(TokenContext, LiteralNode, "[", "$Expression$", ",", "]");
   return LiteralNode;
});
var AssertPattern_Z86 = (function(ParentNode, TokenContext, LeftNode) {
   var AssertNode = ZAssertNode__2qo0(new ZAssertNode(), ParentNode);
   AssertNode = ZNode_MatchToken(TokenContext, AssertNode, "assert", true);
   AssertNode = ZNode_MatchToken(TokenContext, AssertNode, "(", true);
   AssertNode = ZNode_MatchPattern(TokenContext, AssertNode, 0, "$Expression$", true, true);
   AssertNode = ZNode_MatchToken(TokenContext, AssertNode, ")", true);
   return AssertNode;
});
var Assig_Z87 = (function(ParentNode, TokenContext, LeftNode) {
   return null;
});
var BinaryPattern_Z88 = (function(ParentNode, TokenContext, LeftNode) {
   var Token = ZToken_GetToken(TokenContext, true);
   var BinaryNode = ZBinaryNode__5qos(new ZBinaryNode(), ParentNode, Token, LeftNode, ZSyntax_GetApplyingSyntax(TokenContext));
   return ZNode_AppendParsedRightNode(BinaryNode, ParentNode, TokenContext);
});
var BlockComment_Z89 = (function(SourceContext) {
   var StartIndex = GetPosition__1qwu(SourceContext);
   var NextChar = GetCharAtFromCurrentPosition__2qwu(SourceContext, +1);
   if (NextChar != "/" && NextChar != "*") {
      return false;
   };
   if (NextChar == "/") {
      while (HasChar__1qwu(SourceContext)) {
         var ch = GetCurrentChar__1qwu(SourceContext);
         if (ch == "\n") {
            break;
         };
         MoveNext__1qwu(SourceContext);
      };
      return true;
   };
   var NestedLevel = 0;
   var PrevChar = "0";
   while (HasChar__1qwu(SourceContext)) {
      NextChar = GetCurrentChar__1qwu(SourceContext);
      if (PrevChar == "*" && NextChar == "/") {
         NestedLevel = NestedLevel - 1;
         if (NestedLevel == 0) {
            MoveNext__1qwu(SourceContext);
            return true;
         };
      };
      if (PrevChar == "/" && NextChar == "*") {
         NestedLevel = NestedLevel + 1;
      };
      MoveNext__1qwu(SourceContext);
      PrevChar = NextChar;
   };
   LogWarning__3qwu(SourceContext, StartIndex, "unfound */");
   return true;
});
var BlockPattern_Z90 = (function(ParentNode, TokenContext, LeftNode) {
   var BlockNode = ZBlockNode__3qtp(new ZBlockNode(), ParentNode, 0);
   var SkipToken = ZToken_GetToken(TokenContext);
   BlockNode = ZNode_MatchToken(TokenContext, BlockNode, "{", true);
   if (!IsErrorNode__1qwo(BlockNode)) {
      var Remembered = SetParseFlag__2qwp(TokenContext, true);
      var NestedBlockNode = BlockNode;
      while (HasNext__1qwp(TokenContext)) {
         if (MatchToken__2qwp(TokenContext, "}")) {
            break;
         };
         NestedBlockNode = ZNode_MatchPattern(TokenContext, NestedBlockNode, -5, "$Statement$", true);
         if (IsErrorNode__1qwo(NestedBlockNode)) {
            SkipError__2qwp(TokenContext, SkipToken);
            MatchToken__2qwp(TokenContext, "}");
            break;
         };
      };
      SetParseFlag__2qwp(TokenContext, Remembered);
   };
   return BlockNode;
});
var BreakPattern_Z91 = (function(ParentNode, TokenContext, LeftNode) {
   var BreakNode = ZBreakNode__2qol(new ZBreakNode(), ParentNode);
   BreakNode = ZNode_MatchToken(TokenContext, BreakNode, "break", true);
   return BreakNode;
});
var CLin_Z92 = (function(SourceContext) {
   return false;
});
var CastPattern_Z93 = (function(ParentNode, TokenContext, LeftNode) {
   var CastNode = ZCastNode__4qo6(new ZCastNode(), ParentNode, ZType__4qwg(new ZType(), 1 << 16, "var", null), null);
   CastNode = ZNode_MatchToken(TokenContext, CastNode, "(", true);
   CastNode = ZNode_MatchPattern(TokenContext, CastNode, -3, "$Type$", true);
   CastNode = ZNode_MatchToken(TokenContext, CastNode, ")", true);
   CastNode = ZNode_MatchPattern(TokenContext, CastNode, 0, "$RightExpression$", true);
   return CastNode;
});
var CatchPattern_Z94 = (function(ParentNode, TokenContext, LeftNode) {
   var CatchNode = ZCatchNode__2qov(new ZCatchNode(), ParentNode);
   CatchNode = ZNode_MatchToken(TokenContext, CatchNode, "catch", true);
   CatchNode = ZNode_MatchToken(TokenContext, CatchNode, "(", true);
   CatchNode = ZNode_MatchPattern(TokenContext, CatchNode, -2, "$Name$", true);
   CatchNode = ZNode_MatchToken(TokenContext, CatchNode, ")", true);
   CatchNode = ZNode_MatchPattern(TokenContext, CatchNode, 0, "$Block$", true);
   return CatchNode;
});
var ClassPattern_Z95 = (function(ParentNode, TokenContext, LeftNode) {
   var ClassNode = ZClassNode__2qdq(new ZClassNode(), ParentNode);
   ClassNode = ZNode_MatchToken(TokenContext, ClassNode, "class", true);
   ClassNode = ZNode_MatchPattern(TokenContext, ClassNode, -2, "$Name$", true);
   if (MatchNewLineToken__2qwp(TokenContext, "extends")) {
      ClassNode = ZNode_MatchPattern(TokenContext, ClassNode, -3, "$Type$", true);
   };
   ClassNode = ZNode_MatchNtimes(TokenContext, ClassNode, "{", "$FieldDecl$", null, "}");
   return ClassNode;
});
var ComparatorPattern_Z96 = (function(ParentNode, TokenContext, LeftNode) {
   var Token = ZToken_GetToken(TokenContext, true);
   var BinaryNode = ZComparatorNode__5qo7(new ZComparatorNode(), ParentNode, Token, LeftNode, ZSyntax_GetApplyingSyntax(TokenContext));
   return ZNode_AppendParsedRightNode(BinaryNode, ParentNode, TokenContext);
});
function ExpressionPatternFunction_GetRightPattern__2qwt(NameSpace, TokenContext) {
   var Token = ZToken_GetToken(TokenContext);
   if (Token != ZToken__4qw3(new ZToken(), null, 0, 0)) {
      var Pattern = ZSyntax_GetRightSyntaxPattern(NameSpace, GetText__1qw3(Token));
      return Pattern;
   };
   return null;
};
function ZNameSpace_ExpressionPatternFunction_GetRightPattern(NameSpace, TokenContext){ return ExpressionPatternFunction_GetRightPattern__2qwt(NameSpace, TokenContext); }

function ExpressionPatternFunction_DispatchPattern__5qwo(ParentNode, TokenContext, LeftNode, AllowStatement, AllowBinary) {
   var Token = ZToken_GetToken(TokenContext);
   var Pattern = null;
   var NameSpace = ZNameSpace_GetNameSpace(ParentNode);
   if ((Token).constructor.name == (ZPatternToken).name) {
      Pattern = (Token).PresetPattern;
   } else {
      Pattern = ZSyntax_GetSyntaxPattern(NameSpace, GetText__1qw3(Token));
   };
   if (Pattern != null) {
      if (Pattern.IsStatement && !AllowStatement) {
         return ZErrorNode__4qpr(new ZErrorNode(), ParentNode, Token, GetText__1qw3(Token) + " statement is not here");
      };
      LeftNode = ZNode_ApplyMatchPattern(TokenContext, ParentNode, LeftNode, Pattern, true);
   } else {
      if (IsNameSymbol__1qw3(Token)) {
         if (AllowStatement) {
            Pattern = ZSyntax_GetSyntaxPattern(NameSpace, "$SymbolStatement$");
         } else {
            Pattern = ZSyntax_GetSyntaxPattern(NameSpace, "$SymbolExpression$");
         };
         LeftNode = ZNode_ApplyMatchPattern(TokenContext, ParentNode, LeftNode, Pattern, true);
      } else {
         if (AllowStatement) {
            return ZNode_CreateExpectedErrorNode(TokenContext, Token, "statement");
         } else {
            return ZNode_CreateExpectedErrorNode(TokenContext, Token, "expression");
         };
      };
   };
   if (!Pattern.IsStatement) {
      while (LeftNode != null && !IsErrorNode__1qwo(LeftNode)) {
         var RightPattern = ZSyntax_ExpressionPatternFunction_GetRightPattern(NameSpace, TokenContext);
         if (RightPattern == null) {
            break;
         };
         if (!AllowBinary && IsBinaryOperator__1qy7(RightPattern)) {
            break;
         };
         LeftNode = ZNode_ApplyMatchPattern(TokenContext, ParentNode, LeftNode, RightPattern, true);
      };
   };
   return LeftNode;
};
function ZNode_ExpressionPatternFunction_DispatchPattern(ParentNode, TokenContext, LeftNode, AllowStatement, AllowBinary){ return ExpressionPatternFunction_DispatchPattern__5qwo(ParentNode, TokenContext, LeftNode, AllowStatement, AllowBinary); }

var ExpressionPattern_Z97 = (function(ParentNode, TokenContext, LeftNode) {
   return ZNode_ExpressionPatternFunction_DispatchPattern(ParentNode, TokenContext, LeftNode, false, true);
});
var FalsePattern_Z98 = (function(ParentNode, TokenContext, LeftNode) {
   return ZBooleanNode__4qa5(new ZBooleanNode(), ParentNode, ZToken_GetToken(TokenContext, true), false);
});
var FieldPattern_Z99 = (function(ParentNode, TokenContext, LeftNode) {
   var Rememberd = SetParseFlag__2qwp(TokenContext, false);
   var FieldNode = ZFieldNode__2qpi(new ZFieldNode(), ParentNode);
   FieldNode = ZNode_MatchToken(TokenContext, FieldNode, "var", true);
   FieldNode = ZNode_MatchPattern(TokenContext, FieldNode, -2, "$Name$", true);
   FieldNode = ZNode_MatchPattern(TokenContext, FieldNode, -3, "$TypeAnnotation$", false);
   if (MatchToken__2qwp(TokenContext, "=")) {
      FieldNode = ZNode_MatchPattern(TokenContext, FieldNode, 0, "$Expression$", true);
   };
   FieldNode = ZNode_MatchPattern(TokenContext, FieldNode, -1, ";", true);
   SetParseFlag__2qwp(TokenContext, Rememberd);
   return FieldNode;
});
var FloatLiteralPattern_Z100 = (function(ParentNode, TokenContext, LeftNode) {
   var Token = ZToken_GetToken(TokenContext, true);
   return ZFloatNode__4qp4(new ZFloatNode(), ParentNode, Token, LibZen.ParseFloat(GetText__1qw3(Token)));
});
var FunctionPattern_Z101 = (function(ParentNode, TokenContext, LeftNode) {
   var FuncNode = ZFunctionNode__2qrb(new ZFunctionNode(), ParentNode);
   FuncNode = ZNode_MatchToken(TokenContext, FuncNode, "function", true);
   FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, -2, "$Name$", false);
   FuncNode = ZNode_MatchNtimes(TokenContext, FuncNode, "(", "$Param$", ",", ")");
   FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, -3, "$TypeAnnotation$", false);
   FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, 0, "$Block$", true);
   return FuncNode;
});
var GetIndexPattern_Z102 = (function(ParentNode, TokenContext, LeftNode) {
   var IndexerNode = ZGetIndexNode__3qpd(new ZGetIndexNode(), ParentNode, LeftNode);
   IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "[", true);
   IndexerNode = ZNode_MatchPattern(TokenContext, IndexerNode, 1, "$Expression$", true, true);
   IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "]", true);
   return IndexerNode;
});
var GetterPattern_Z103 = (function(ParentNode, TokenContext, LeftNode) {
   var GetterNode = ZGetterNode__3qp1(new ZGetterNode(), ParentNode, LeftNode);
   GetterNode = ZNode_MatchToken(TokenContext, GetterNode, ".", true);
   GetterNode = ZNode_MatchPattern(TokenContext, GetterNode, -2, "$Name$", true);
   return GetterNode;
});
var GroupPattern_Z104 = (function(ParentNode, TokenContext, LeftNode) {
   var GroupNode = ZGroupNode__2qp7(new ZGroupNode(), ParentNode);
   GroupNode = ZNode_MatchToken(TokenContext, GroupNode, "(", true);
   GroupNode = ZNode_MatchPattern(TokenContext, GroupNode, 0, "$Expression$", true, true);
   GroupNode = ZNode_MatchToken(TokenContext, GroupNode, ")", true);
   return GroupNode;
});
var IfPattern_Z105 = (function(ParentNode, TokenContext, LeftNode) {
   var IfNode = ZIfNode__2qp2(new ZIfNode(), ParentNode);
   IfNode = ZNode_MatchToken(TokenContext, IfNode, "if", true);
   IfNode = ZNode_MatchToken(TokenContext, IfNode, "(", true);
   IfNode = ZNode_MatchPattern(TokenContext, IfNode, 0, "$Expression$", true, true);
   IfNode = ZNode_MatchToken(TokenContext, IfNode, ")", true);
   IfNode = ZNode_MatchPattern(TokenContext, IfNode, 1, "$Block$", true);
   if (MatchNewLineToken__2qwp(TokenContext, "else")) {
      var PatternName = "$Block$";
      if (IsNewLineToken__2qwp(TokenContext, "if")) {
         PatternName = "if";
      };
      IfNode = ZNode_MatchPattern(TokenContext, IfNode, 2, PatternName, true);
   };
   return IfNode;
});
var InstanceOfPattern_Z106 = (function(ParentNode, TokenContext, LeftNode) {
   var BinaryNode = ZInstanceOfNode__4q0t(new ZInstanceOfNode(), ParentNode, ZToken_GetToken(TokenContext, true), LeftNode);
   BinaryNode = ZNode_MatchPattern(TokenContext, BinaryNode, -3, "$Type$", true);
   return BinaryNode;
});
var IntLiteralPattern_Z107 = (function(ParentNode, TokenContext, LeftNode) {
   var Token = ZToken_GetToken(TokenContext, true);
   return ZIntNode__4q0o(new ZIntNode(), ParentNode, Token, LibZen.ParseInt(GetText__1qw3(Token)));
});
var LetPattern_Z108 = (function(ParentNode, TokenContext, LeftNode) {
   var LetNode = ZLetNode__2q04(new ZLetNode(), ParentNode);
   LetNode = ZNode_MatchToken(TokenContext, LetNode, "let", true);
   LetNode = ZNode_MatchPattern(TokenContext, LetNode, -2, "$Name$", true);
   LetNode = ZNode_MatchPattern(TokenContext, LetNode, -3, "$TypeAnnotation$", false);
   LetNode = ZNode_MatchToken(TokenContext, LetNode, "=", true);
   LetNode = ZNode_MatchPattern(TokenContext, LetNode, 0, "$Expression$", true);
   return LetNode;
});
var MapEntryPattern_Z109 = (function(ParentNode, TokenContext, LeftNode) {
   var LiteralNode = ZMapEntryNode__2q0b(new ZMapEntryNode(), ParentNode);
   LiteralNode = ZNode_MatchPattern(TokenContext, LiteralNode, 0, "$Expression$", true);
   LiteralNode = ZNode_MatchToken(TokenContext, LiteralNode, ":", true);
   LiteralNode = ZNode_MatchPattern(TokenContext, LiteralNode, 1, "$Expression$", true);
   return LiteralNode;
});
var MapLiteralPattern_Z110 = (function(ParentNode, TokenContext, LeftNode) {
   var LiteralNode = ZMapLiteralNode__2q0m(new ZMapLiteralNode(), ParentNode);
   LiteralNode = ZNode_MatchNtimes(TokenContext, LiteralNode, "{", "$MapEntry$", ",", "}");
   return LiteralNode;
});
var MethodCallPattern_Z111 = (function(ParentNode, TokenContext, LeftNode) {
   var MethodCallNode = ZMethodCallNode__3q02(new ZMethodCallNode(), ParentNode, LeftNode);
   MethodCallNode = ZNode_MatchToken(TokenContext, MethodCallNode, ".", true);
   MethodCallNode = ZNode_MatchPattern(TokenContext, MethodCallNode, -2, "$Name$", true);
   MethodCallNode = ZNode_MatchNtimes(TokenContext, MethodCallNode, "(", "$Expression$", ",", ")");
   return MethodCallNode;
});
var NamePattern_Z112 = (function(ParentNode, TokenContext, LeftNode) {
   var Token = ZToken_GetToken(TokenContext, true);
   if (LibZen.IsSymbol(GetChar__1qw3(Token))) {
      return ZGetNameNode__4qph(new ZGetNameNode(), ParentNode, Token, GetText__1qw3(Token));
   };
   return ZErrorNode__4qpr(new ZErrorNode(), ParentNode, Token, ("illegal name: \"" + GetText__1qw3(Token)) + "\"");
});
var NameToken_Z113 = (function(SourceContext) {
   var StartIndex = GetPosition__1qwu(SourceContext);
   while (HasChar__1qwu(SourceContext)) {
      var ch = GetCurrentChar__1qwu(SourceContext);
      if (!LibZen.IsSymbol(ch) && !LibZen.IsDigit(ch)) {
         break;
      };
      MoveNext__1qwu(SourceContext);
   };
   Tokenize__3qwu(SourceContext, StartIndex, GetPosition__1qwu(SourceContext));
   return true;
});
var NewLineToken_Z114 = (function(SourceContext) {
   var StartIndex = GetPosition__1qwu(SourceContext) + 1;
   MoveNext__1qwu(SourceContext);
   SkipWhiteSpace__1qwu(SourceContext);
   FoundIndent__3qwu(SourceContext, StartIndex, GetPosition__1qwu(SourceContext));
   return true;
});
var NewObjectPattern_Z115 = (function(ParentNode, TokenContext, LeftNode) {
   var LiteralNode = ZNewObjectNode__2q4i(new ZNewObjectNode(), ParentNode);
   LiteralNode = ZNode_MatchToken(TokenContext, LiteralNode, "new", true);
   LiteralNode = ZNode_MatchPattern(TokenContext, LiteralNode, -3, "$Type$", false);
   LiteralNode = ZNode_MatchNtimes(TokenContext, LiteralNode, "(", "$Expression$", ",", ")");
   return LiteralNode;
});
var NotPattern_Z116 = (function(ParentNode, TokenContext, LeftNode) {
   var UnaryNode = ZNotNode__3q44(new ZNotNode(), ParentNode, ZToken_GetToken(TokenContext, true));
   UnaryNode = ZNode_MatchPattern(TokenContext, UnaryNode, 0, "$RightExpression$", true);
   return UnaryNode;
});
var NullPattern_Z117 = (function(ParentNode, TokenContext, LeftNode) {
   return ZNullNode__3q4d(new ZNullNode(), ParentNode, ZToken_GetToken(TokenContext, true));
});
function NumberLiteralTokenFunction_ParseDigit__1qwu(SourceContext) {
   var ch = "0";
   while (HasChar__1qwu(SourceContext)) {
      ch = GetCurrentChar__1qwu(SourceContext);
      if (!LibZen.IsDigit(ch)) {
         break;
      };
      MoveNext__1qwu(SourceContext);
   };
   return ch;
};
function ZSourceContext_NumberLiteralTokenFunction_ParseDigit(SourceContext){ return NumberLiteralTokenFunction_ParseDigit__1qwu(SourceContext); }

var NumberLiteralToken_Z118 = (function(SourceContext) {
   var StartIndex = GetPosition__1qwu(SourceContext);
   var ch = NumberLiteralTokenFunction_ParseDigit__1qwu(SourceContext);
   if (ch == ".") {
      MoveNext__1qwu(SourceContext);
      ch = NumberLiteralTokenFunction_ParseDigit__1qwu(SourceContext);
      if (ch == "e" || ch == "E") {
         MoveNext__1qwu(SourceContext);
         if (HasChar__1qwu(SourceContext)) {
            ch = GetCurrentChar__1qwu(SourceContext);
            if (ch == "+" || ch == "-") {
               MoveNext__1qwu(SourceContext);
            };
         };
         NumberLiteralTokenFunction_ParseDigit__1qwu(SourceContext);
      };
      Tokenize__4qwu(SourceContext, "$FloatLiteral$", StartIndex, GetPosition__1qwu(SourceContext));
   } else {
      Tokenize__4qwu(SourceContext, "$IntegerLiteral$", StartIndex, GetPosition__1qwu(SourceContext));
   };
   return true;
});
var OperatorToken_Z119 = (function(SourceContext) {
   TokenizeDefinedSymbol__2qwu(SourceContext, GetPosition__1qwu(SourceContext));
   return true;
});
var OrPattern_Z120 = (function(ParentNode, TokenContext, LeftNode) {
   var BinaryNode = ZOrNode__5q4h(new ZOrNode(), ParentNode, ZToken_GetToken(TokenContext, true), LeftNode, ZSyntax_GetApplyingSyntax(TokenContext));
   return ZNode_AppendParsedRightNode(BinaryNode, ParentNode, TokenContext);
});
var ParamPattern_Z121 = (function(ParentNode, TokenContext, LeftNode) {
   var ParamNode = ZParamNode__2qtl(new ZParamNode(), ParentNode);
   ParamNode = ZNode_MatchPattern(TokenContext, ParamNode, -2, "$Name$", true);
   ParamNode = ZNode_MatchPattern(TokenContext, ParamNode, -3, "$TypeAnnotation$", false);
   return ParamNode;
});
var PrototypePattern_Z122 = (function(ParentNode, TokenContext, LeftNode) {
   var FuncNode = ZPrototypeNode__2q4l(new ZPrototypeNode(), ParentNode);
   FuncNode = ZNode_MatchToken(TokenContext, FuncNode, "function", true);
   FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, -2, "$Name$", true);
   FuncNode = ZNode_MatchNtimes(TokenContext, FuncNode, "(", "$Param$", ",", ")");
   FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, -3, "$TypeAnnotation$", true);
   return FuncNode;
});
var ReturnPattern_Z123 = (function(ParentNode, TokenContext, LeftNode) {
   var ReturnNode = ZReturnNode__2qtj(new ZReturnNode(), ParentNode);
   ReturnNode = ZNode_MatchToken(TokenContext, ReturnNode, "return", true);
   ReturnNode = ZNode_MatchPattern(TokenContext, ReturnNode, 0, "$Expression$", false);
   return ReturnNode;
});
var RightExpressionPattern_Z124 = (function(ParentNode, TokenContext, LeftNode) {
   return ZNode_ExpressionPatternFunction_DispatchPattern(ParentNode, TokenContext, LeftNode, false, false);
});
var RightTypePattern_Z125 = (function(ParentNode, TokenContext, LeftTypeNode) {
   var SourceToken = ZToken_GetToken(TokenContext);
   if (LeftTypeNode.Type.GetParamSize(LeftTypeNode.Type) > 0) {
      if (MatchToken__2qwp(TokenContext, "<")) {
         var TypeList = [];
         while (!StartsWithToken__2qwp(TokenContext, ">")) {
            if ((TypeList).length > 0 && !MatchToken__2qwp(TokenContext, ",")) {
               return null;
            };
            var ParamTypeNode = ZNode_ParsePattern(TokenContext, ParentNode, "$Type$", false);
            if (ParamTypeNode == null) {
               return LeftTypeNode;
            };
            TypeList.push(ParamTypeNode.Type);
         };
         LeftTypeNode = ZTypeNode__4qu4(new ZTypeNode(), ParentNode, SourceToken, ZType_ZTypePool_GetGenericType(LeftTypeNode.Type, TypeList, true));
      };
   };
   while (MatchToken__2qwp(TokenContext, "[")) {
      if (!MatchToken__2qwp(TokenContext, "]")) {
         return null;
      };
      LeftTypeNode = ZTypeNode__4qu4(new ZTypeNode(), ParentNode, SourceToken, ZType_ZTypePool_GetGenericType1(ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), LeftTypeNode.Type));
   };
   return LeftTypeNode;
});
var SetIndexPattern_Z126 = (function(ParentNode, TokenContext, LeftNode) {
   var IndexerNode = ZSetIndexNode__3qtc(new ZSetIndexNode(), ParentNode, LeftNode);
   IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "[", true);
   IndexerNode = ZNode_MatchPattern(TokenContext, IndexerNode, 1, "$Expression$", true, true);
   IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "]", true);
   IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "=", true);
   IndexerNode = ZNode_MatchPattern(TokenContext, IndexerNode, 2, "$Expression$", true);
   return IndexerNode;
});
var SetterPattern_Z127 = (function(ParentNode, TokenContext, LeftNode) {
   var SetterNode = ZSetterNode__3qt5(new ZSetterNode(), ParentNode, LeftNode);
   SetterNode = ZNode_MatchToken(TokenContext, SetterNode, ".", true);
   SetterNode = ZNode_MatchPattern(TokenContext, SetterNode, -2, "$Name$", true);
   SetterNode = ZNode_MatchToken(TokenContext, SetterNode, "=", true);
   SetterNode = ZNode_MatchPattern(TokenContext, SetterNode, 1, "$Expression$", true);
   return SetterNode;
});
var StatementEndPattern_Z128 = (function(ParentNode, TokenContext, LeftNode) {
   var ContextAllowance = SetParseFlag__2qwp(TokenContext, false);
   var Token = null;
   if (HasNext__1qwp(TokenContext)) {
      Token = ZToken_GetToken(TokenContext);
      if (!EqualsText__2qw3(Token, ";") && !IsIndent__1qw3(Token)) {
         SetParseFlag__2qwp(TokenContext, ContextAllowance);
         return ZNode_CreateExpectedErrorNode(TokenContext, Token, ";");
      };
      MoveNext__1qwp(TokenContext);
      while (HasNext__1qwp(TokenContext)) {
         Token = ZToken_GetToken(TokenContext);
         if (!EqualsText__2qw3(Token, ";") && !IsIndent__1qw3(Token)) {
            break;
         };
         MoveNext__1qwp(TokenContext);
      };
   };
   SetParseFlag__2qwp(TokenContext, ContextAllowance);
   return ZEmptyNode__3qpw(new ZEmptyNode(), ParentNode, Token);
});
var StatementPattern_Z129 = (function(ParentNode, TokenContext, LeftNode) {
   var Rememberd = SetParseFlag__2qwp(TokenContext, true);
   SetParseFlag__2qwp(TokenContext, false);
   var StmtNode = ZNode_ExpressionPatternFunction_DispatchPattern(ParentNode, TokenContext, null, true, true);
   StmtNode = ZNode_MatchPattern(TokenContext, StmtNode, -1, ";", true);
   SetParseFlag__2qwp(TokenContext, Rememberd);
   return StmtNode;
});
var StringLiteralPattern_Z130 = (function(ParentNode, TokenContext, LeftNode) {
   var Token = ZToken_GetToken(TokenContext, true);
   return ZStringNode__4q4c(new ZStringNode(), ParentNode, Token, LibZen.UnquoteString(GetText__1qw3(Token)));
});
var StringLiteralToken_Z131 = (function(SourceContext) {
   var StartIndex = GetPosition__1qwu(SourceContext);
   MoveNext__1qwu(SourceContext);
   while (HasChar__1qwu(SourceContext)) {
      var ch = GetCurrentChar__1qwu(SourceContext);
      if (ch == "\"") {
         MoveNext__1qwu(SourceContext);
         Tokenize__4qwu(SourceContext, "$StringLiteral$", StartIndex, GetPosition__1qwu(SourceContext));
         return true;
      };
      if (ch == "\n") {
         break;
      };
      if (ch == "\\") {
         MoveNext__1qwu(SourceContext);
      };
      MoveNext__1qwu(SourceContext);
   };
   LogWarning__3qwu(SourceContext, StartIndex, "unclosed \"");
   Tokenize__4qwu(SourceContext, "$StringLiteral$", StartIndex, GetPosition__1qwu(SourceContext));
   return false;
});
var SymbolExpressionPattern_Z132 = (function(ParentNode, TokenContext, LeftNode) {
   var NameToken = ZToken_GetToken(TokenContext, true);
   if (IsToken__2qwp(TokenContext, "=")) {
      return ZErrorNode__4qpr(new ZErrorNode(), ParentNode, ZToken_GetToken(TokenContext), "assignment is not en expression");
   } else {
      return ZGetNameNode__4qph(new ZGetNameNode(), ParentNode, NameToken, GetText__1qw3(NameToken));
   };
});
var SymbolStatementPattern_Z133 = (function(ParentNode, TokenContext, LeftNode) {
   var NameToken = ZToken_GetToken(TokenContext, true);
   if (MatchToken__2qwp(TokenContext, "=")) {
      var AssignedNode = ZSetNameNode__4qtn(new ZSetNameNode(), ParentNode, NameToken, GetText__1qw3(NameToken));
      AssignedNode = ZNode_MatchPattern(TokenContext, AssignedNode, 0, "$Expression$", true);
      return AssignedNode;
   } else {
      return ZGetNameNode__4qph(new ZGetNameNode(), ParentNode, NameToken, GetText__1qw3(NameToken));
   };
});
var ThrowPattern_Z134 = (function(ParentNode, TokenContext, LeftNode) {
   var ThrowNode = ZThrowNode__2qyr(new ZThrowNode(), ParentNode);
   ThrowNode = ZNode_MatchToken(TokenContext, ThrowNode, "throw", true);
   ThrowNode = ZNode_MatchPattern(TokenContext, ThrowNode, 0, "$Expression$", true);
   return ThrowNode;
});
var TruePattern_Z135 = (function(ParentNode, TokenContext, LeftNode) {
   return ZBooleanNode__4qa5(new ZBooleanNode(), ParentNode, ZToken_GetToken(TokenContext, true), true);
});
var TryPattern_Z136 = (function(ParentNode, TokenContext, LeftNode) {
   var TryNode = ZTryNode__2qyu(new ZTryNode(), ParentNode);
   TryNode = ZNode_MatchToken(TokenContext, TryNode, "try", true);
   TryNode = ZNode_MatchPattern(TokenContext, TryNode, 0, "$Block$", true);
   var count = 0;
   if (IsNewLineToken__2qwp(TokenContext, "catch")) {
      TryNode = ZNode_MatchPattern(TokenContext, TryNode, 1, "$Catch$", true);
      count = count + 1;
   };
   if (MatchNewLineToken__2qwp(TokenContext, "finally")) {
      TryNode = ZNode_MatchPattern(TokenContext, TryNode, 2, "$Block$", true);
      count = count + 1;
   };
   if (count == 0 && !IsErrorNode__1qwo(TryNode)) {
      return TryNode.AST[0];
   };
   return TryNode;
});
var TypeAnnotationPattern_Z137 = (function(ParentNode, TokenContext, LeftNode) {
   if (MatchToken__2qwp(TokenContext, ":")) {
      return ZNode_ParsePattern(TokenContext, ParentNode, "$Type$", true);
   };
   return null;
});
var TypePattern_Z138 = (function(ParentNode, TokenContext, LeftNode) {
   var Token = ZToken_GetToken(TokenContext, true);
   var TypeNode = ZTypeNode_GetTypeNode(ZNameSpace_GetNameSpace(ParentNode), GetText__1qw3(Token), Token);
   if (TypeNode != null) {
      return ZNode_ParsePatternAfter(TokenContext, ParentNode, TypeNode, "$TypeRight$", false);
   };
   return null;
});
var UnaryPattern_Z139 = (function(ParentNode, TokenContext, LeftNode) {
   var UnaryNode = ZUnaryNode__3qyp(new ZUnaryNode(), ParentNode, ZToken_GetToken(TokenContext, true));
   return ZNode_MatchPattern(TokenContext, UnaryNode, 0, "$RightExpression$", true);
});
var VarPattern_Z140 = (function(ParentNode, TokenContext, LeftNode) {
   var VarNode = ZVarNode__2qsc(new ZVarNode(), ParentNode);
   VarNode = ZNode_MatchToken(TokenContext, VarNode, "var", true);
   VarNode = ZNode_MatchPattern(TokenContext, VarNode, -2, "$Name$", true);
   VarNode = ZNode_MatchPattern(TokenContext, VarNode, -3, "$TypeAnnotation$", false);
   VarNode = ZNode_MatchToken(TokenContext, VarNode, "=", true);
   VarNode = ZNode_MatchPattern(TokenContext, VarNode, 0, "$Expression$", true);
   return VarNode;
});
var WhilePattern_Z141 = (function(ParentNode, TokenContext, LeftNode) {
   var WhileNode = ZWhileNode__2qya(new ZWhileNode(), ParentNode);
   WhileNode = ZNode_MatchToken(TokenContext, WhileNode, "while", true);
   WhileNode = ZNode_MatchToken(TokenContext, WhileNode, "(", true);
   WhileNode = ZNode_MatchPattern(TokenContext, WhileNode, 0, "$Expression$", true, true);
   WhileNode = ZNode_MatchToken(TokenContext, WhileNode, ")", true);
   WhileNode = ZNode_MatchPattern(TokenContext, WhileNode, 1, "$Block$", true);
   return WhileNode;
});
var WhiteSpaceToken_Z142 = (function(SourceContext) {
   SkipWhiteSpace__1qwu(SourceContext);
   return true;
});
var ZenGrammar = (function() {
   function ZenGrammar(){
   }
   return ZenGrammar;
})();

var ZenPrecedence = (function() {
   function ZenPrecedence(){
   }
   return ZenPrecedence;
})();

var ZenPrecedence_BinaryOperator_Z143 = 1;
var ZenPrecedence_LeftJoin_Z144 = 1 << 1;
var ZenPrecedence_PrecedenceShift_Z145 = 3;
var ZenPrecedence_CStyleMUL_Z146 = (100 << 3) | 1;
var ZenPrecedence_CStyleADD_Z147 = (200 << 3) | 1;
var ZenPrecedence_CStyleSHIFT_Z148 = (300 << 3) | 1;
var ZenPrecedence_CStyleCOMPARE_Z149 = (400 << 3) | 1;
var ZenPrecedence_Instanceof_Z150 = (400 << 3) | 1;
var ZenPrecedence_CStyleEquals_Z151 = (500 << 3) | 1;
var ZenPrecedence_CStyleBITAND_Z152 = (600 << 3) | 1;
var ZenPrecedence_CStyleBITXOR_Z153 = (700 << 3) | 1;
var ZenPrecedence_CStyleBITOR_Z154 = (800 << 3) | 1;
var ZenPrecedence_CStyleAND_Z155 = (900 << 3) | 1;
var ZenPrecedence_CStyleOR_Z156 = (1000 << 3) | 1;
var ZenPrecedence_CStyleTRINARY_Z157 = (1100 << 3) | 1;
var ZenPrecedence_CStyleAssign_Z158 = (1200 << 3) | 1;
var ZenPrecedence_CStyleCOMMA_Z159 = (1300 << 3) | 1;
function ImportGrammar__1qwt(NameSpace) {
   SetTypeName__3qwt(NameSpace, ZType__4qwg(new ZType(), 1 << 16, "void", null), null);
   SetTypeName__3qwt(NameSpace, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)), null);
   SetTypeName__3qwt(NameSpace, ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), null);
   SetTypeName__3qwt(NameSpace, ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)), null);
   SetTypeName__3qwt(NameSpace, ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), null);
   SetTypeName__3qwt(NameSpace, ZType__4qwg(new ZType(), 1 << 16, "Type", ZType__4qwg(new ZType(), 1 << 16, "var", null)), null);
   SetTypeName__3qwt(NameSpace, ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), null);
   SetTypeName__3qwt(NameSpace, ZGenericType__5qev(new ZGenericType(), 1 << 16, "Map", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), null);
   SetTypeName__3qwt(NameSpace, ZFuncType__3qe0(new ZFuncType(), "Func", null), null);
   AppendTokenFunc__3qwt(NameSpace, " \t", (function(SourceContext) {
      SkipWhiteSpace__1qwu(SourceContext);
      return true;
   }));
   AppendTokenFunc__3qwt(NameSpace, "\n", (function(SourceContext) {
      var StartIndex = GetPosition__1qwu(SourceContext) + 1;
      MoveNext__1qwu(SourceContext);
      SkipWhiteSpace__1qwu(SourceContext);
      FoundIndent__3qwu(SourceContext, StartIndex, GetPosition__1qwu(SourceContext));
      return true;
   }));
   AppendTokenFunc__3qwt(NameSpace, "{}()[]<>.,;?:+-*/%=&|!@~^$", (function(SourceContext) {
      TokenizeDefinedSymbol__2qwu(SourceContext, GetPosition__1qwu(SourceContext));
      return true;
   }));
   AppendTokenFunc__3qwt(NameSpace, "/", (function(SourceContext) {
      var StartIndex = GetPosition__1qwu(SourceContext);
      var NextChar = GetCharAtFromCurrentPosition__2qwu(SourceContext, +1);
      if (NextChar != "/" && NextChar != "*") {
         return false;
      };
      if (NextChar == "/") {
         while (HasChar__1qwu(SourceContext)) {
            var ch = GetCurrentChar__1qwu(SourceContext);
            if (ch == "\n") {
               break;
            };
            MoveNext__1qwu(SourceContext);
         };
         return true;
      };
      var NestedLevel = 0;
      var PrevChar = "0";
      while (HasChar__1qwu(SourceContext)) {
         NextChar = GetCurrentChar__1qwu(SourceContext);
         if (PrevChar == "*" && NextChar == "/") {
            NestedLevel = NestedLevel - 1;
            if (NestedLevel == 0) {
               MoveNext__1qwu(SourceContext);
               return true;
            };
         };
         if (PrevChar == "/" && NextChar == "*") {
            NestedLevel = NestedLevel + 1;
         };
         MoveNext__1qwu(SourceContext);
         PrevChar = NextChar;
      };
      LogWarning__3qwu(SourceContext, StartIndex, "unfound */");
      return true;
   }));
   AppendTokenFunc__3qwt(NameSpace, "Aa_", (function(SourceContext) {
      var StartIndex = GetPosition__1qwu(SourceContext);
      while (HasChar__1qwu(SourceContext)) {
         var ch = GetCurrentChar__1qwu(SourceContext);
         if (!LibZen.IsSymbol(ch) && !LibZen.IsDigit(ch)) {
            break;
         };
         MoveNext__1qwu(SourceContext);
      };
      Tokenize__3qwu(SourceContext, StartIndex, GetPosition__1qwu(SourceContext));
      return true;
   }));
   AppendTokenFunc__3qwt(NameSpace, "\"", (function(SourceContext) {
      var StartIndex = GetPosition__1qwu(SourceContext);
      MoveNext__1qwu(SourceContext);
      while (HasChar__1qwu(SourceContext)) {
         var ch = GetCurrentChar__1qwu(SourceContext);
         if (ch == "\"") {
            MoveNext__1qwu(SourceContext);
            Tokenize__4qwu(SourceContext, "$StringLiteral$", StartIndex, GetPosition__1qwu(SourceContext));
            return true;
         };
         if (ch == "\n") {
            break;
         };
         if (ch == "\\") {
            MoveNext__1qwu(SourceContext);
         };
         MoveNext__1qwu(SourceContext);
      };
      LogWarning__3qwu(SourceContext, StartIndex, "unclosed \"");
      Tokenize__4qwu(SourceContext, "$StringLiteral$", StartIndex, GetPosition__1qwu(SourceContext));
      return false;
   }));
   AppendTokenFunc__3qwt(NameSpace, "1", (function(SourceContext) {
      var StartIndex = GetPosition__1qwu(SourceContext);
      var ch = NumberLiteralTokenFunction_ParseDigit__1qwu(SourceContext);
      if (ch == ".") {
         MoveNext__1qwu(SourceContext);
         ch = NumberLiteralTokenFunction_ParseDigit__1qwu(SourceContext);
         if (ch == "e" || ch == "E") {
            MoveNext__1qwu(SourceContext);
            if (HasChar__1qwu(SourceContext)) {
               ch = GetCurrentChar__1qwu(SourceContext);
               if (ch == "+" || ch == "-") {
                  MoveNext__1qwu(SourceContext);
               };
            };
            NumberLiteralTokenFunction_ParseDigit__1qwu(SourceContext);
         };
         Tokenize__4qwu(SourceContext, "$FloatLiteral$", StartIndex, GetPosition__1qwu(SourceContext));
      } else {
         Tokenize__4qwu(SourceContext, "$IntegerLiteral$", StartIndex, GetPosition__1qwu(SourceContext));
      };
      return true;
   }));
   var MatchUnary = (function(ParentNode, TokenContext, LeftNode) {
      var UnaryNode = ZUnaryNode__3qyp(new ZUnaryNode(), ParentNode, ZToken_GetToken(TokenContext, true));
      return ZNode_MatchPattern(TokenContext, UnaryNode, 0, "$RightExpression$", true);
   });
   var MatchBinary = (function(ParentNode, TokenContext, LeftNode) {
      var Token = ZToken_GetToken(TokenContext, true);
      var BinaryNode = ZBinaryNode__5qos(new ZBinaryNode(), ParentNode, Token, LeftNode, ZSyntax_GetApplyingSyntax(TokenContext));
      return ZNode_AppendParsedRightNode(BinaryNode, ParentNode, TokenContext);
   });
   var MatchComparator = (function(ParentNode, TokenContext, LeftNode) {
      var Token = ZToken_GetToken(TokenContext, true);
      var BinaryNode = ZComparatorNode__5qo7(new ZComparatorNode(), ParentNode, Token, LeftNode, ZSyntax_GetApplyingSyntax(TokenContext));
      return ZNode_AppendParsedRightNode(BinaryNode, ParentNode, TokenContext);
   });
   DefineExpression__3qwt(NameSpace, "null", (function(ParentNode, TokenContext, LeftNode) {
      return ZNullNode__3q4d(new ZNullNode(), ParentNode, ZToken_GetToken(TokenContext, true));
   }));
   DefineExpression__3qwt(NameSpace, "true", (function(ParentNode, TokenContext, LeftNode) {
      return ZBooleanNode__4qa5(new ZBooleanNode(), ParentNode, ZToken_GetToken(TokenContext, true), true);
   }));
   DefineExpression__3qwt(NameSpace, "false", (function(ParentNode, TokenContext, LeftNode) {
      return ZBooleanNode__4qa5(new ZBooleanNode(), ParentNode, ZToken_GetToken(TokenContext, true), false);
   }));
   DefineExpression__3qwt(NameSpace, "+", MatchUnary);
   DefineExpression__3qwt(NameSpace, "-", MatchUnary);
   DefineExpression__3qwt(NameSpace, "~", MatchUnary);
   DefineExpression__3qwt(NameSpace, "!", (function(ParentNode, TokenContext, LeftNode) {
      var UnaryNode = ZNotNode__3q44(new ZNotNode(), ParentNode, ZToken_GetToken(TokenContext, true));
      UnaryNode = ZNode_MatchPattern(TokenContext, UnaryNode, 0, "$RightExpression$", true);
      return UnaryNode;
   }));
   DefineRightExpression__4qwt(NameSpace, "* / %", (100 << 3) | 1, MatchBinary);
   DefineRightExpression__4qwt(NameSpace, "+ -", (200 << 3) | 1, MatchBinary);
   DefineRightExpression__4qwt(NameSpace, "< <= > >=", (400 << 3) | 1, MatchComparator);
   DefineRightExpression__4qwt(NameSpace, "== !=", (500 << 3) | 1, MatchComparator);
   DefineRightExpression__4qwt(NameSpace, "<< >>", (300 << 3) | 1, MatchBinary);
   DefineRightExpression__4qwt(NameSpace, "&", (600 << 3) | 1, MatchBinary);
   DefineRightExpression__4qwt(NameSpace, "|", (800 << 3) | 1, MatchBinary);
   DefineRightExpression__4qwt(NameSpace, "^", (700 << 3) | 1, MatchBinary);
   DefineRightExpression__4qwt(NameSpace, "&&", (900 << 3) | 1, (function(ParentNode, TokenContext, LeftNode) {
      var BinaryNode = ZAndNode__5qs1(new ZAndNode(), ParentNode, ZToken_GetToken(TokenContext, true), LeftNode, ZSyntax_GetApplyingSyntax(TokenContext));
      return ZNode_AppendParsedRightNode(BinaryNode, ParentNode, TokenContext);
   }));
   DefineRightExpression__4qwt(NameSpace, "||", (1000 << 3) | 1, (function(ParentNode, TokenContext, LeftNode) {
      var BinaryNode = ZOrNode__5q4h(new ZOrNode(), ParentNode, ZToken_GetToken(TokenContext, true), LeftNode, ZSyntax_GetApplyingSyntax(TokenContext));
      return ZNode_AppendParsedRightNode(BinaryNode, ParentNode, TokenContext);
   }));
   DefineExpression__3qwt(NameSpace, "$Type$", (function(ParentNode, TokenContext, LeftNode) {
      var Token = ZToken_GetToken(TokenContext, true);
      var TypeNode = ZTypeNode_GetTypeNode(ZNameSpace_GetNameSpace(ParentNode), GetText__1qw3(Token), Token);
      if (TypeNode != null) {
         return ZNode_ParsePatternAfter(TokenContext, ParentNode, TypeNode, "$TypeRight$", false);
      };
      return null;
   }));
   DefineExpression__3qwt(NameSpace, "$TypeRight$", (function(ParentNode, TokenContext, LeftTypeNode) {
      var SourceToken = ZToken_GetToken(TokenContext);
      if (LeftTypeNode.Type.GetParamSize(LeftTypeNode.Type) > 0) {
         if (MatchToken__2qwp(TokenContext, "<")) {
            var TypeList = [];
            while (!StartsWithToken__2qwp(TokenContext, ">")) {
               if ((TypeList).length > 0 && !MatchToken__2qwp(TokenContext, ",")) {
                  return null;
               };
               var ParamTypeNode = ZNode_ParsePattern(TokenContext, ParentNode, "$Type$", false);
               if (ParamTypeNode == null) {
                  return LeftTypeNode;
               };
               TypeList.push(ParamTypeNode.Type);
            };
            LeftTypeNode = ZTypeNode__4qu4(new ZTypeNode(), ParentNode, SourceToken, ZType_ZTypePool_GetGenericType(LeftTypeNode.Type, TypeList, true));
         };
      };
      while (MatchToken__2qwp(TokenContext, "[")) {
         if (!MatchToken__2qwp(TokenContext, "]")) {
            return null;
         };
         LeftTypeNode = ZTypeNode__4qu4(new ZTypeNode(), ParentNode, SourceToken, ZType_ZTypePool_GetGenericType1(ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), LeftTypeNode.Type));
      };
      return LeftTypeNode;
   }));
   DefineExpression__3qwt(NameSpace, "$TypeAnnotation$", (function(ParentNode, TokenContext, LeftNode) {
      if (MatchToken__2qwp(TokenContext, ":")) {
         return ZNode_ParsePattern(TokenContext, ParentNode, "$Type$", true);
      };
      return null;
   }));
   DefineExpression__3qwt(NameSpace, "$StringLiteral$", (function(ParentNode, TokenContext, LeftNode) {
      var Token = ZToken_GetToken(TokenContext, true);
      return ZStringNode__4q4c(new ZStringNode(), ParentNode, Token, LibZen.UnquoteString(GetText__1qw3(Token)));
   }));
   DefineExpression__3qwt(NameSpace, "$IntegerLiteral$", (function(ParentNode, TokenContext, LeftNode) {
      var Token = ZToken_GetToken(TokenContext, true);
      return ZIntNode__4q0o(new ZIntNode(), ParentNode, Token, LibZen.ParseInt(GetText__1qw3(Token)));
   }));
   DefineExpression__3qwt(NameSpace, "$FloatLiteral$", (function(ParentNode, TokenContext, LeftNode) {
      var Token = ZToken_GetToken(TokenContext, true);
      return ZFloatNode__4qp4(new ZFloatNode(), ParentNode, Token, LibZen.ParseFloat(GetText__1qw3(Token)));
   }));
   DefineRightExpression__4qwt(NameSpace, ".", 0, (function(ParentNode, TokenContext, LeftNode) {
      var GetterNode = ZGetterNode__3qp1(new ZGetterNode(), ParentNode, LeftNode);
      GetterNode = ZNode_MatchToken(TokenContext, GetterNode, ".", true);
      GetterNode = ZNode_MatchPattern(TokenContext, GetterNode, -2, "$Name$", true);
      return GetterNode;
   }));
   DefineRightExpression__4qwt(NameSpace, ".", 0, (function(ParentNode, TokenContext, LeftNode) {
      var SetterNode = ZSetterNode__3qt5(new ZSetterNode(), ParentNode, LeftNode);
      SetterNode = ZNode_MatchToken(TokenContext, SetterNode, ".", true);
      SetterNode = ZNode_MatchPattern(TokenContext, SetterNode, -2, "$Name$", true);
      SetterNode = ZNode_MatchToken(TokenContext, SetterNode, "=", true);
      SetterNode = ZNode_MatchPattern(TokenContext, SetterNode, 1, "$Expression$", true);
      return SetterNode;
   }));
   DefineRightExpression__4qwt(NameSpace, ".", 0, (function(ParentNode, TokenContext, LeftNode) {
      var MethodCallNode = ZMethodCallNode__3q02(new ZMethodCallNode(), ParentNode, LeftNode);
      MethodCallNode = ZNode_MatchToken(TokenContext, MethodCallNode, ".", true);
      MethodCallNode = ZNode_MatchPattern(TokenContext, MethodCallNode, -2, "$Name$", true);
      MethodCallNode = ZNode_MatchNtimes(TokenContext, MethodCallNode, "(", "$Expression$", ",", ")");
      return MethodCallNode;
   }));
   DefineExpression__3qwt(NameSpace, "(", (function(ParentNode, TokenContext, LeftNode) {
      var GroupNode = ZGroupNode__2qp7(new ZGroupNode(), ParentNode);
      GroupNode = ZNode_MatchToken(TokenContext, GroupNode, "(", true);
      GroupNode = ZNode_MatchPattern(TokenContext, GroupNode, 0, "$Expression$", true, true);
      GroupNode = ZNode_MatchToken(TokenContext, GroupNode, ")", true);
      return GroupNode;
   }));
   DefineExpression__3qwt(NameSpace, "(", (function(ParentNode, TokenContext, LeftNode) {
      var CastNode = ZCastNode__4qo6(new ZCastNode(), ParentNode, ZType__4qwg(new ZType(), 1 << 16, "var", null), null);
      CastNode = ZNode_MatchToken(TokenContext, CastNode, "(", true);
      CastNode = ZNode_MatchPattern(TokenContext, CastNode, -3, "$Type$", true);
      CastNode = ZNode_MatchToken(TokenContext, CastNode, ")", true);
      CastNode = ZNode_MatchPattern(TokenContext, CastNode, 0, "$RightExpression$", true);
      return CastNode;
   }));
   DefineRightExpression__4qwt(NameSpace, "(", 0, (function(ParentNode, TokenContext, LeftNode) {
      var ApplyNode = ZFuncCallNode__3q4e(new ZFuncCallNode(), ParentNode, LeftNode);
      ApplyNode = ZNode_MatchNtimes(TokenContext, ApplyNode, "(", "$Expression$", ",", ")");
      return ApplyNode;
   }));
   DefineRightExpression__4qwt(NameSpace, "[", 0, (function(ParentNode, TokenContext, LeftNode) {
      var IndexerNode = ZGetIndexNode__3qpd(new ZGetIndexNode(), ParentNode, LeftNode);
      IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "[", true);
      IndexerNode = ZNode_MatchPattern(TokenContext, IndexerNode, 1, "$Expression$", true, true);
      IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "]", true);
      return IndexerNode;
   }));
   DefineRightExpression__4qwt(NameSpace, "[", 0, (function(ParentNode, TokenContext, LeftNode) {
      var IndexerNode = ZSetIndexNode__3qtc(new ZSetIndexNode(), ParentNode, LeftNode);
      IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "[", true);
      IndexerNode = ZNode_MatchPattern(TokenContext, IndexerNode, 1, "$Expression$", true, true);
      IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "]", true);
      IndexerNode = ZNode_MatchToken(TokenContext, IndexerNode, "=", true);
      IndexerNode = ZNode_MatchPattern(TokenContext, IndexerNode, 2, "$Expression$", true);
      return IndexerNode;
   }));
   DefineExpression__3qwt(NameSpace, "[", (function(ParentNode, TokenContext, LeftNode) {
      var LiteralNode = ZArrayLiteralNode__2qsw(new ZArrayLiteralNode(), ParentNode);
      LiteralNode = ZNode_MatchNtimes(TokenContext, LiteralNode, "[", "$Expression$", ",", "]");
      return LiteralNode;
   }));
   DefineExpression__3qwt(NameSpace, "$MapEntry$", (function(ParentNode, TokenContext, LeftNode) {
      var LiteralNode = ZMapEntryNode__2q0b(new ZMapEntryNode(), ParentNode);
      LiteralNode = ZNode_MatchPattern(TokenContext, LiteralNode, 0, "$Expression$", true);
      LiteralNode = ZNode_MatchToken(TokenContext, LiteralNode, ":", true);
      LiteralNode = ZNode_MatchPattern(TokenContext, LiteralNode, 1, "$Expression$", true);
      return LiteralNode;
   }));
   DefineExpression__3qwt(NameSpace, "{", (function(ParentNode, TokenContext, LeftNode) {
      var LiteralNode = ZMapLiteralNode__2q0m(new ZMapLiteralNode(), ParentNode);
      LiteralNode = ZNode_MatchNtimes(TokenContext, LiteralNode, "{", "$MapEntry$", ",", "}");
      return LiteralNode;
   }));
   DefineExpression__3qwt(NameSpace, "new", (function(ParentNode, TokenContext, LeftNode) {
      var LiteralNode = ZNewObjectNode__2q4i(new ZNewObjectNode(), ParentNode);
      LiteralNode = ZNode_MatchToken(TokenContext, LiteralNode, "new", true);
      LiteralNode = ZNode_MatchPattern(TokenContext, LiteralNode, -3, "$Type$", false);
      LiteralNode = ZNode_MatchNtimes(TokenContext, LiteralNode, "(", "$Expression$", ",", ")");
      return LiteralNode;
   }));
   DefineStatement__3qwt(NameSpace, ";", (function(ParentNode, TokenContext, LeftNode) {
      var ContextAllowance = SetParseFlag__2qwp(TokenContext, false);
      var Token = null;
      if (HasNext__1qwp(TokenContext)) {
         Token = ZToken_GetToken(TokenContext);
         if (!EqualsText__2qw3(Token, ";") && !IsIndent__1qw3(Token)) {
            SetParseFlag__2qwp(TokenContext, ContextAllowance);
            return ZNode_CreateExpectedErrorNode(TokenContext, Token, ";");
         };
         MoveNext__1qwp(TokenContext);
         while (HasNext__1qwp(TokenContext)) {
            Token = ZToken_GetToken(TokenContext);
            if (!EqualsText__2qw3(Token, ";") && !IsIndent__1qw3(Token)) {
               break;
            };
            MoveNext__1qwp(TokenContext);
         };
      };
      SetParseFlag__2qwp(TokenContext, ContextAllowance);
      return ZEmptyNode__3qpw(new ZEmptyNode(), ParentNode, Token);
   }));
   DefineExpression__3qwt(NameSpace, "$Block$", (function(ParentNode, TokenContext, LeftNode) {
      var BlockNode = ZBlockNode__3qtp(new ZBlockNode(), ParentNode, 0);
      var SkipToken = ZToken_GetToken(TokenContext);
      BlockNode = ZNode_MatchToken(TokenContext, BlockNode, "{", true);
      if (!IsErrorNode__1qwo(BlockNode)) {
         var Remembered = SetParseFlag__2qwp(TokenContext, true);
         var NestedBlockNode = BlockNode;
         while (HasNext__1qwp(TokenContext)) {
            if (MatchToken__2qwp(TokenContext, "}")) {
               break;
            };
            NestedBlockNode = ZNode_MatchPattern(TokenContext, NestedBlockNode, -5, "$Statement$", true);
            if (IsErrorNode__1qwo(NestedBlockNode)) {
               SkipError__2qwp(TokenContext, SkipToken);
               MatchToken__2qwp(TokenContext, "}");
               break;
            };
         };
         SetParseFlag__2qwp(TokenContext, Remembered);
      };
      return BlockNode;
   }));
   DefineExpression__3qwt(NameSpace, "$Annotation$", (function(ParentNode, TokenContext, LeftNode) {
      return null;
   }));
   DefineExpression__3qwt(NameSpace, "$SymbolExpression$", (function(ParentNode, TokenContext, LeftNode) {
      var NameToken = ZToken_GetToken(TokenContext, true);
      if (IsToken__2qwp(TokenContext, "=")) {
         return ZErrorNode__4qpr(new ZErrorNode(), ParentNode, ZToken_GetToken(TokenContext), "assignment is not en expression");
      } else {
         return ZGetNameNode__4qph(new ZGetNameNode(), ParentNode, NameToken, GetText__1qw3(NameToken));
      };
   }));
   DefineExpression__3qwt(NameSpace, "$SymbolStatement$", (function(ParentNode, TokenContext, LeftNode) {
      var NameToken = ZToken_GetToken(TokenContext, true);
      if (MatchToken__2qwp(TokenContext, "=")) {
         var AssignedNode = ZSetNameNode__4qtn(new ZSetNameNode(), ParentNode, NameToken, GetText__1qw3(NameToken));
         AssignedNode = ZNode_MatchPattern(TokenContext, AssignedNode, 0, "$Expression$", true);
         return AssignedNode;
      } else {
         return ZGetNameNode__4qph(new ZGetNameNode(), ParentNode, NameToken, GetText__1qw3(NameToken));
      };
   }));
   DefineExpression__3qwt(NameSpace, "$Statement$", (function(ParentNode, TokenContext, LeftNode) {
      var Rememberd = SetParseFlag__2qwp(TokenContext, true);
      SetParseFlag__2qwp(TokenContext, false);
      var StmtNode = ZNode_ExpressionPatternFunction_DispatchPattern(ParentNode, TokenContext, null, true, true);
      StmtNode = ZNode_MatchPattern(TokenContext, StmtNode, -1, ";", true);
      SetParseFlag__2qwp(TokenContext, Rememberd);
      return StmtNode;
   }));
   DefineExpression__3qwt(NameSpace, "$Expression$", (function(ParentNode, TokenContext, LeftNode) {
      return ZNode_ExpressionPatternFunction_DispatchPattern(ParentNode, TokenContext, LeftNode, false, true);
   }));
   DefineExpression__3qwt(NameSpace, "$RightExpression$", (function(ParentNode, TokenContext, LeftNode) {
      return ZNode_ExpressionPatternFunction_DispatchPattern(ParentNode, TokenContext, LeftNode, false, false);
   }));
   DefineStatement__3qwt(NameSpace, "if", (function(ParentNode, TokenContext, LeftNode) {
      var IfNode = ZIfNode__2qp2(new ZIfNode(), ParentNode);
      IfNode = ZNode_MatchToken(TokenContext, IfNode, "if", true);
      IfNode = ZNode_MatchToken(TokenContext, IfNode, "(", true);
      IfNode = ZNode_MatchPattern(TokenContext, IfNode, 0, "$Expression$", true, true);
      IfNode = ZNode_MatchToken(TokenContext, IfNode, ")", true);
      IfNode = ZNode_MatchPattern(TokenContext, IfNode, 1, "$Block$", true);
      if (MatchNewLineToken__2qwp(TokenContext, "else")) {
         var PatternName = "$Block$";
         if (IsNewLineToken__2qwp(TokenContext, "if")) {
            PatternName = "if";
         };
         IfNode = ZNode_MatchPattern(TokenContext, IfNode, 2, PatternName, true);
      };
      return IfNode;
   }));
   DefineStatement__3qwt(NameSpace, "return", (function(ParentNode, TokenContext, LeftNode) {
      var ReturnNode = ZReturnNode__2qtj(new ZReturnNode(), ParentNode);
      ReturnNode = ZNode_MatchToken(TokenContext, ReturnNode, "return", true);
      ReturnNode = ZNode_MatchPattern(TokenContext, ReturnNode, 0, "$Expression$", false);
      return ReturnNode;
   }));
   DefineStatement__3qwt(NameSpace, "while", (function(ParentNode, TokenContext, LeftNode) {
      var WhileNode = ZWhileNode__2qya(new ZWhileNode(), ParentNode);
      WhileNode = ZNode_MatchToken(TokenContext, WhileNode, "while", true);
      WhileNode = ZNode_MatchToken(TokenContext, WhileNode, "(", true);
      WhileNode = ZNode_MatchPattern(TokenContext, WhileNode, 0, "$Expression$", true, true);
      WhileNode = ZNode_MatchToken(TokenContext, WhileNode, ")", true);
      WhileNode = ZNode_MatchPattern(TokenContext, WhileNode, 1, "$Block$", true);
      return WhileNode;
   }));
   DefineStatement__3qwt(NameSpace, "break", (function(ParentNode, TokenContext, LeftNode) {
      var BreakNode = ZBreakNode__2qol(new ZBreakNode(), ParentNode);
      BreakNode = ZNode_MatchToken(TokenContext, BreakNode, "break", true);
      return BreakNode;
   }));
   DefineExpression__3qwt(NameSpace, "$Name$", (function(ParentNode, TokenContext, LeftNode) {
      var Token = ZToken_GetToken(TokenContext, true);
      if (LibZen.IsSymbol(GetChar__1qw3(Token))) {
         return ZGetNameNode__4qph(new ZGetNameNode(), ParentNode, Token, GetText__1qw3(Token));
      };
      return ZErrorNode__4qpr(new ZErrorNode(), ParentNode, Token, ("illegal name: \"" + GetText__1qw3(Token)) + "\"");
   }));
   DefineStatement__3qwt(NameSpace, "var", (function(ParentNode, TokenContext, LeftNode) {
      var VarNode = ZVarNode__2qsc(new ZVarNode(), ParentNode);
      VarNode = ZNode_MatchToken(TokenContext, VarNode, "var", true);
      VarNode = ZNode_MatchPattern(TokenContext, VarNode, -2, "$Name$", true);
      VarNode = ZNode_MatchPattern(TokenContext, VarNode, -3, "$TypeAnnotation$", false);
      VarNode = ZNode_MatchToken(TokenContext, VarNode, "=", true);
      VarNode = ZNode_MatchPattern(TokenContext, VarNode, 0, "$Expression$", true);
      return VarNode;
   }));
   DefineExpression__3qwt(NameSpace, "$Param$", (function(ParentNode, TokenContext, LeftNode) {
      var ParamNode = ZParamNode__2qtl(new ZParamNode(), ParentNode);
      ParamNode = ZNode_MatchPattern(TokenContext, ParamNode, -2, "$Name$", true);
      ParamNode = ZNode_MatchPattern(TokenContext, ParamNode, -3, "$TypeAnnotation$", false);
      return ParamNode;
   }));
   DefineExpression__3qwt(NameSpace, "function", (function(ParentNode, TokenContext, LeftNode) {
      var FuncNode = ZPrototypeNode__2q4l(new ZPrototypeNode(), ParentNode);
      FuncNode = ZNode_MatchToken(TokenContext, FuncNode, "function", true);
      FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, -2, "$Name$", true);
      FuncNode = ZNode_MatchNtimes(TokenContext, FuncNode, "(", "$Param$", ",", ")");
      FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, -3, "$TypeAnnotation$", true);
      return FuncNode;
   }));
   DefineExpression__3qwt(NameSpace, "function", (function(ParentNode, TokenContext, LeftNode) {
      var FuncNode = ZFunctionNode__2qrb(new ZFunctionNode(), ParentNode);
      FuncNode = ZNode_MatchToken(TokenContext, FuncNode, "function", true);
      FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, -2, "$Name$", false);
      FuncNode = ZNode_MatchNtimes(TokenContext, FuncNode, "(", "$Param$", ",", ")");
      FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, -3, "$TypeAnnotation$", false);
      FuncNode = ZNode_MatchPattern(TokenContext, FuncNode, 0, "$Block$", true);
      return FuncNode;
   }));
   DefineStatement__3qwt(NameSpace, "let", (function(ParentNode, TokenContext, LeftNode) {
      var LetNode = ZLetNode__2q04(new ZLetNode(), ParentNode);
      LetNode = ZNode_MatchToken(TokenContext, LetNode, "let", true);
      LetNode = ZNode_MatchPattern(TokenContext, LetNode, -2, "$Name$", true);
      LetNode = ZNode_MatchPattern(TokenContext, LetNode, -3, "$TypeAnnotation$", false);
      LetNode = ZNode_MatchToken(TokenContext, LetNode, "=", true);
      LetNode = ZNode_MatchPattern(TokenContext, LetNode, 0, "$Expression$", true);
      return LetNode;
   }));
   AppendGrammarInfo__2qw4(NameSpace.Generator, "zen-0.1");
   DefineStatement__3qwt(NameSpace, "try", (function(ParentNode, TokenContext, LeftNode) {
      var TryNode = ZTryNode__2qyu(new ZTryNode(), ParentNode);
      TryNode = ZNode_MatchToken(TokenContext, TryNode, "try", true);
      TryNode = ZNode_MatchPattern(TokenContext, TryNode, 0, "$Block$", true);
      var count = 0;
      if (IsNewLineToken__2qwp(TokenContext, "catch")) {
         TryNode = ZNode_MatchPattern(TokenContext, TryNode, 1, "$Catch$", true);
         count = count + 1;
      };
      if (MatchNewLineToken__2qwp(TokenContext, "finally")) {
         TryNode = ZNode_MatchPattern(TokenContext, TryNode, 2, "$Block$", true);
         count = count + 1;
      };
      if (count == 0 && !IsErrorNode__1qwo(TryNode)) {
         return TryNode.AST[0];
      };
      return TryNode;
   }));
   DefineExpression__3qwt(NameSpace, "$Catch$", (function(ParentNode, TokenContext, LeftNode) {
      var CatchNode = ZCatchNode__2qov(new ZCatchNode(), ParentNode);
      CatchNode = ZNode_MatchToken(TokenContext, CatchNode, "catch", true);
      CatchNode = ZNode_MatchToken(TokenContext, CatchNode, "(", true);
      CatchNode = ZNode_MatchPattern(TokenContext, CatchNode, -2, "$Name$", true);
      CatchNode = ZNode_MatchToken(TokenContext, CatchNode, ")", true);
      CatchNode = ZNode_MatchPattern(TokenContext, CatchNode, 0, "$Block$", true);
      return CatchNode;
   }));
   DefineStatement__3qwt(NameSpace, "throw", (function(ParentNode, TokenContext, LeftNode) {
      var ThrowNode = ZThrowNode__2qyr(new ZThrowNode(), ParentNode);
      ThrowNode = ZNode_MatchToken(TokenContext, ThrowNode, "throw", true);
      ThrowNode = ZNode_MatchPattern(TokenContext, ThrowNode, 0, "$Expression$", true);
      return ThrowNode;
   }));
   AppendGrammarInfo__2qw4(NameSpace.Generator, "zen-trycatch-0.1");
   DefineRightExpression__4qwt(NameSpace, "instanceof", (400 << 3) | 1, (function(ParentNode, TokenContext, LeftNode) {
      var BinaryNode = ZInstanceOfNode__4q0t(new ZInstanceOfNode(), ParentNode, ZToken_GetToken(TokenContext, true), LeftNode);
      BinaryNode = ZNode_MatchPattern(TokenContext, BinaryNode, -3, "$Type$", true);
      return BinaryNode;
   }));
   DefineStatement__3qwt(NameSpace, "class", (function(ParentNode, TokenContext, LeftNode) {
      var ClassNode = ZClassNode__2qdq(new ZClassNode(), ParentNode);
      ClassNode = ZNode_MatchToken(TokenContext, ClassNode, "class", true);
      ClassNode = ZNode_MatchPattern(TokenContext, ClassNode, -2, "$Name$", true);
      if (MatchNewLineToken__2qwp(TokenContext, "extends")) {
         ClassNode = ZNode_MatchPattern(TokenContext, ClassNode, -3, "$Type$", true);
      };
      ClassNode = ZNode_MatchNtimes(TokenContext, ClassNode, "{", "$FieldDecl$", null, "}");
      return ClassNode;
   }));
   DefineExpression__3qwt(NameSpace, "$FieldDecl$", (function(ParentNode, TokenContext, LeftNode) {
      var Rememberd = SetParseFlag__2qwp(TokenContext, false);
      var FieldNode = ZFieldNode__2qpi(new ZFieldNode(), ParentNode);
      FieldNode = ZNode_MatchToken(TokenContext, FieldNode, "var", true);
      FieldNode = ZNode_MatchPattern(TokenContext, FieldNode, -2, "$Name$", true);
      FieldNode = ZNode_MatchPattern(TokenContext, FieldNode, -3, "$TypeAnnotation$", false);
      if (MatchToken__2qwp(TokenContext, "=")) {
         FieldNode = ZNode_MatchPattern(TokenContext, FieldNode, 0, "$Expression$", true);
      };
      FieldNode = ZNode_MatchPattern(TokenContext, FieldNode, -1, ";", true);
      SetParseFlag__2qwp(TokenContext, Rememberd);
      return FieldNode;
   }));
   AppendGrammarInfo__2qw4(NameSpace.Generator, "zen-class-0.1");
   DefineStatement__3qwt(NameSpace, "assert", (function(ParentNode, TokenContext, LeftNode) {
      var AssertNode = ZAssertNode__2qo0(new ZAssertNode(), ParentNode);
      AssertNode = ZNode_MatchToken(TokenContext, AssertNode, "assert", true);
      AssertNode = ZNode_MatchToken(TokenContext, AssertNode, "(", true);
      AssertNode = ZNode_MatchPattern(TokenContext, AssertNode, 0, "$Expression$", true, true);
      AssertNode = ZNode_MatchToken(TokenContext, AssertNode, ")", true);
      return AssertNode;
   }));
   return;
};
function ZNameSpace_ImportGrammar(NameSpace){ return ImportGrammar__1qwt(NameSpace); }

var CSourceGenerator = (function(_super) {
   __extends(CSourceGenerator, _super);
   function CSourceGenerator(){
      _super.call(this);
   }
   return CSourceGenerator;
})(ZSourceGenerator);

function CSourceGenerator__1q94(self) {
   ZSourceGenerator__3quk(self, "c", "C99");
   self.LineFeed = "\n";
   self.Tab = "\t";
   self.Camma = ", ";
   self.SemiColon = ";";
   self.TrueLiteral = "1/*true*/";
   self.FalseLiteral = "0/*false*/";
   self.NullLiteral = "NULL";
   self.TopType = "void *";
   SetNativeType__3quk(self, ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)), "int");
   SetNativeType__3quk(self, ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), "long");
   SetNativeType__3quk(self, ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)), "double");
   SetNativeType__3quk(self, ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), "const char *");
   SetMacro__6quk(self, "assert", "LibZen_Assert($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "void", null), ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__5quk(self, "print", "LibZen_Print($[0])", ZType__4qwg(new ZType(), 1 << 16, "void", null), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__5quk(self, "println", "LibZen_PrintLine($[0])", ZType__4qwg(new ZType(), 1 << 16, "void", null), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetConverterMacro__4quk(self, "(double)($[0])", ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetConverterMacro__4quk(self, "(long)($[0])", ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetConverterMacro__4quk(self, "LibZen_BooleanToString($[0])", ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetConverterMacro__4quk(self, "LibZen_IntToString($[0])", ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetConverterMacro__4quk(self, "LibZen_FloatToString($[0])", ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "float", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__6quk(self, "+", "LibZen_StrCat($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__5quk(self, "size", "LibZen_StringSize($[0])", ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__6quk(self, "substring", "LibZen_SubString($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__7quk(self, "substring", "LibZen_SubString2($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__6quk(self, "indexOf", "LibZen_IndexOf($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__7quk(self, "indexOf", "LibZen_IndexOf2($[0], $[1], $[2])", ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__6quk(self, "equals", "LibZen_EqualsString($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__6quk(self, "startsWith", "LibZen_StartsWith($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__6quk(self, "endsWith", "LibZen_EndWidth($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "boolean", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "String", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__5quk(self, "size", "LibZen_ArraySize($[0])", ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__6quk(self, "clear", "LibZen_ArrayClear($[0])", ZType__4qwg(new ZType(), 1 << 16, "void", null), ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)));
   SetMacro__6quk(self, "add", "LibZen_ArrayAdd($[0], $[1])", ZType__4qwg(new ZType(), 1 << 16, "void", null), ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "var", null));
   SetMacro__7quk(self, "add", "LibZen_ArrayAdd2($[0], $[1], $[2])", ZType__4qwg(new ZType(), 1 << 16, "void", null), ZGenericType__5qev(new ZGenericType(), 1 << 16, "Array", null, ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "int", ZType__4qwg(new ZType(), 1 << 16, "var", null)), ZType__4qwg(new ZType(), 1 << 16, "var", null));
   return self;
};

function GetEngine__1q94(self) {
   return ZSourceEngine__3qws(new ZSourceEngine(), ZenTypeSafer__2qga(new ZenTypeSafer(), self), self);
};
function CSourceGenerator_GetEngine(self){ return GetEngine__1q94(self); }

function GenerateCode__3q94(self, ContextType, Node) {
   if (IsUntyped__1qwo(Node) && !IsErrorNode__1qwo(Node) && !((Node).constructor.name == (ZGlobalNameNode).name)) {
      Append__2qq2(self.CurrentBuilder, "/*untyped*/" + self.NullLiteral);
      ZLogger_LogError__2qw3(Node.SourceToken, "untyped error: " + toString__1qwo(Node));
   } else {
      if (ContextType != null && Node.Type != ContextType) {
         Append__2qq2(self.CurrentBuilder, "(");
         GenerateTypeName__2q94(self, ContextType);
         Append__2qq2(self.CurrentBuilder, ")");
      };
      Node.Accept(Node, self);
   };
   return;
};
function CSourceGenerator_GenerateCode(self, ContextType, Node){ return GenerateCode__3q94(self, ContextType, Node); }

function VisitArrayLiteralNode__2q94(self, Node) {
   var ParamType = Node.Type.GetParamType(Node.Type, 0);
   if (IsIntType__1qwg(ParamType) || IsBooleanType__1qwg(ParamType)) {
      Append__2qq2(self.CurrentBuilder, "LibZen_NewIntArray(");
   } else if (IsFloatType__1qwg(ParamType)) {
      Append__2qq2(self.CurrentBuilder, "LibZen_NewFloatArray(");
   } else if (IsStringType__1qwg(ParamType)) {
      Append__2qq2(self.CurrentBuilder, "LibZen_NewStringArray(");
   } else {
      Append__2qq2(self.CurrentBuilder, "LibZen_NewArray(");
   };
   Append__2qq2(self.CurrentBuilder, "" + ((GetListSize__1quv(Node))).toString());
   if (GetListSize__1quv(Node) > 0) {
      Append__2qq2(self.CurrentBuilder, self.Camma);
   };
   VisitListNode__4quk(self, "", Node, ")");
   return;
};
function CSourceGenerator_VisitArrayLiteralNode(self, Node){ return VisitArrayLiteralNode__2q94(self, Node); }

function VisitMapLiteralNode__2q94(self, Node) {
   var ParamType = Node.Type.GetParamType(Node.Type, 0);
   if (IsIntType__1qwg(ParamType) || IsBooleanType__1qwg(ParamType)) {
      Append__2qq2(self.CurrentBuilder, "LibZen_NewIntMap(");
   } else if (IsFloatType__1qwg(ParamType)) {
      Append__2qq2(self.CurrentBuilder, "LibZen_NewFloatMap(");
   } else if (IsStringType__1qwg(ParamType)) {
      Append__2qq2(self.CurrentBuilder, "LibZen_NewStringMap(");
   } else {
      Append__2qq2(self.CurrentBuilder, "LibZen_NewMap(");
   };
   Append__2qq2(self.CurrentBuilder, "" + ((GetListSize__1quv(Node))).toString());
   if (GetListSize__1quv(Node) > 0) {
      Append__2qq2(self.CurrentBuilder, self.Camma);
   };
   VisitListNode__4quk(self, "", Node, ")");
   return;
};
function CSourceGenerator_VisitMapLiteralNode(self, Node){ return VisitMapLiteralNode__2q94(self, Node); }

function VisitNewObjectNode__2q94(self, Node) {
   Append__2qq2(self.CurrentBuilder, "_New" + NameClass__2qw4(self, Node.Type));
   VisitListNode__4quk(self, "(", Node, ")");
   return;
};
function CSourceGenerator_VisitNewObjectNode(self, Node){ return VisitNewObjectNode__2q94(self, Node); }

function BaseName__2q94(self, RecvType) {
   return GetAsciiName__1qwg(RecvType);
};
function CSourceGenerator_BaseName(self, RecvType){ return BaseName__2q94(self, RecvType); }

function VisitGetIndexNode__2q94(self, Node) {
   Append__2qq2(self.CurrentBuilder, BaseName__2q94(self, ZType_GetAstType(Node, 0)) + "GetIndex");
   Append__2qq2(self.CurrentBuilder, "(");
   self.GenerateCode(self, null, Node.AST[1]);
   Append__2qq2(self.CurrentBuilder, ")");
   return;
};
function CSourceGenerator_VisitGetIndexNode(self, Node){ return VisitGetIndexNode__2q94(self, Node); }

function VisitSetIndexNode__2q94(self, Node) {
   Append__2qq2(self.CurrentBuilder, BaseName__2q94(self, ZType_GetAstType(Node, 0)) + "SetIndex");
   Append__2qq2(self.CurrentBuilder, "(");
   self.GenerateCode(self, null, Node.AST[1]);
   Append__2qq2(self.CurrentBuilder, self.Camma);
   self.GenerateCode(self, null, Node.AST[2]);
   Append__2qq2(self.CurrentBuilder, ")");
   return;
};
function CSourceGenerator_VisitSetIndexNode(self, Node){ return VisitSetIndexNode__2q94(self, Node); }

function VisitGetNameNode__2q94(self, Node) {
   Append__2qq2(self.CurrentBuilder, SafeName__3quk(self, Node.VarName, Node.VarIndex));
   return;
};
function CSourceGenerator_VisitGetNameNode(self, Node){ return VisitGetNameNode__2q94(self, Node); }

function VisitSetNameNode__2q94(self, Node) {
   Append__2qq2(self.CurrentBuilder, SafeName__3quk(self, Node.VarName, Node.VarIndex));
   AppendToken__2qq2(self.CurrentBuilder, "=");
   self.GenerateCode(self, null, Node.AST[0]);
   return;
};
function CSourceGenerator_VisitSetNameNode(self, Node){ return VisitSetNameNode__2q94(self, Node); }

function VisitGetterNode__2q94(self, Node) {
   GenerateSurroundCode__2quk(self, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, "->");
   Append__2qq2(self.CurrentBuilder, Node.FieldName);
   return;
};
function CSourceGenerator_VisitGetterNode(self, Node){ return VisitGetterNode__2q94(self, Node); }

function VisitSetterNode__2q94(self, Node) {
   GenerateSurroundCode__2quk(self, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, "->");
   Append__2qq2(self.CurrentBuilder, Node.FieldName);
   AppendToken__2qq2(self.CurrentBuilder, "=");
   self.GenerateCode(self, null, Node.AST[1]);
   return;
};
function CSourceGenerator_VisitSetterNode(self, Node){ return VisitSetterNode__2q94(self, Node); }

function VisitMethodCallNode__2q94(self, Node) {
   return;
};
function CSourceGenerator_VisitMethodCallNode(self, Node){ return VisitMethodCallNode__2q94(self, Node); }

function VisitFuncCallNode__2q94(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   VisitListNode__4quk(self, "(", Node, ")");
   return;
};
function CSourceGenerator_VisitFuncCallNode(self, Node){ return VisitFuncCallNode__2q94(self, Node); }

function VisitThrowNode__2q94(self, Node) {
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, "longjump(1)");
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   return;
};
function CSourceGenerator_VisitThrowNode(self, Node){ return VisitThrowNode__2q94(self, Node); }

function VisitTryNode__2q94(self, Node) {
   return;
};
function CSourceGenerator_VisitTryNode(self, Node){ return VisitTryNode__2q94(self, Node); }

function VisitCatchNode__2q94(self, Node) {
   return;
};
function CSourceGenerator_VisitCatchNode(self, Node){ return VisitCatchNode__2q94(self, Node); }

function ParamTypeName__2q94(self, Type) {
   if (IsArrayType__1qwg(Type)) {
      return "ArrayOf" + ParamTypeName__2q94(self, Type.GetParamType(Type, 0));
   };
   if (IsMapType__1qwg(Type)) {
      return "MapOf" + ParamTypeName__2q94(self, Type.GetParamType(Type, 0));
   };
   if (IsFuncType__1qwg(Type)) {
      var s = ("FuncOf" + ParamTypeName__2q94(self, Type.GetParamType(Type, 0))) + "Of";
      var i = 0;
      while (i < Type.GetParamSize(Type)) {
         s = s + ParamTypeName__2q94(self, Type.GetParamType(Type, i));
         i = i + 1;
      };
      return s;
   };
   if (IsIntType__1qwg(Type)) {
      return "Int";
   };
   if (IsFloatType__1qwg(Type)) {
      return "Float";
   };
   if (IsVoidType__1qwg(Type)) {
      return "Void";
   };
   if (Type.IsVarType(Type)) {
      return "Var";
   };
   return Type.ShortName;
};
function CSourceGenerator_ParamTypeName(self, Type){ return ParamTypeName__2q94(self, Type); }

function GetCTypeName__2q94(self, Type) {
   var TypeName = null;
   if (IsArrayType__1qwg(Type) || IsMapType__1qwg(Type)) {
      TypeName = ParamTypeName__2q94(self, Type) + " *";
   };
   if ((Type).constructor.name == (ZClassType).name) {
      TypeName = ("struct " + NameClass__2qw4(self, Type)) + " *";
   };
   if (TypeName == null) {
      TypeName = GetNativeTypeName__2quk(self, Type);
   };
   return TypeName;
};
function CSourceGenerator_GetCTypeName(self, Type){ return GetCTypeName__2q94(self, Type); }

function GenerateFuncTypeName__3q94(self, Type, FuncName) {
   GenerateTypeName__2q94(self, Type.GetParamType(Type, 0));
   Append__2qq2(self.CurrentBuilder, (" (*" + FuncName) + ")");
   var i = 1;
   Append__2qq2(self.CurrentBuilder, "(");
   while (i < Type.GetParamSize(Type)) {
      if (i > 1) {
         Append__2qq2(self.CurrentBuilder, ",");
      };
      GenerateTypeName__2q94(self, Type.GetParamType(Type, i));
      i = i + 1;
   };
   Append__2qq2(self.CurrentBuilder, ")");
   return;
};
function CSourceGenerator_GenerateFuncTypeName(self, Type, FuncName){ return GenerateFuncTypeName__3q94(self, Type, FuncName); }

function GenerateTypeName__2q94(self, Type) {
   if (IsFuncType__1qwg(Type)) {
      GenerateFuncTypeName__3q94(self, Type, "");
   } else {
      Append__2qq2(self.CurrentBuilder, GetCTypeName__2q94(self, Type.GetRealType(Type)));
   };
   return;
};
function CSourceGenerator_GenerateTypeName(self, Type){ return GenerateTypeName__2q94(self, Type); }

function VisitVarNode__2q94(self, Node) {
   GenerateTypeName__2q94(self, Node.DeclType);
   Append__2qq2(self.CurrentBuilder, " ");
   Append__2qq2(self.CurrentBuilder, SafeName__3quk(self, Node.NativeName, Node.VarIndex));
   AppendToken__2qq2(self.CurrentBuilder, "=");
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, self.SemiColon);
   VisitStmtList__2quk(self, Node);
   return;
};
function CSourceGenerator_VisitVarNode(self, Node){ return VisitVarNode__2q94(self, Node); }

function VisitParamNode__2q94(self, Node) {
   if (IsFuncType__1qwg(Node.Type)) {
      GenerateFuncTypeName__3q94(self, Node.Type, Node.Name);
   } else {
      GenerateTypeName__2q94(self, Node.Type);
      Append__2qq2(self.CurrentBuilder, " ");
      Append__2qq2(self.CurrentBuilder, SafeName__3quk(self, Node.Name, Node.ParamIndex));
   };
   return;
};
function CSourceGenerator_VisitParamNode(self, Node){ return VisitParamNode__2q94(self, Node); }

function SetMethod__3q94(self, FuncName, FuncType) {
   var RecvType = ZType_GetRecvType(FuncType);
   if ((RecvType).constructor.name == (ZClassType).name && FuncName != null) {
      var ClassType = RecvType;
      var FieldType = ZType_GetFieldType(ClassType, FuncName, null);
      if (FieldType == null || !IsFuncType__1qwg(FieldType)) {
         FuncName = LibZen.AnotherName(FuncName);
         FieldType = ZType_GetFieldType(ClassType, FuncName, null);
         if (FieldType == null || !IsFuncType__1qwg(FieldType)) {
            return;
         };
      };
      if ((FieldType).constructor.name == (ZFuncType).name) {
         if (AcceptAsFieldFunc__2qe0((FieldType), FuncType)) {
            Append__2qq2(self.HeaderBuilder, (("#define _" + NameClass__2qw4(self, ClassType)) + "_") + FuncName);
            AppendLineFeed__1qq2(self.HeaderBuilder);
         };
      };
   };
   return;
};
function CSourceGenerator_SetMethod(self, FuncName, FuncType){ return SetMethod__3q94(self, FuncName, FuncType); }

function VisitInstanceOfNode__2q94(self, Node) {
   Append__2qq2(self.CurrentBuilder, "LibZen_Is(");
   self.GenerateCode(self, null, Node.AST[0]);
   Append__2qq2(self.CurrentBuilder, self.Camma);
   AppendInt__2qq2(self.CurrentBuilder, Node.TargetType.TypeId);
   Append__2qq2(self.CurrentBuilder, ")");
   return;
};
function CSourceGenerator_VisitInstanceOfNode(self, Node){ return VisitInstanceOfNode__2q94(self, Node); }

function GenerateCField__3q94(self, CType, FieldName) {
   AppendLineFeed__1qq2(self.CurrentBuilder);
   AppendIndent__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, CType);
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, FieldName);
   Append__2qq2(self.CurrentBuilder, self.SemiColon);
   return;
};
function CSourceGenerator_GenerateCField(self, CType, FieldName){ return GenerateCField__3q94(self, CType, FieldName); }

function GenerateField__3q94(self, DeclType, FieldName) {
   AppendLineFeedIndent__1qq2(self.CurrentBuilder);
   GenerateTypeName__2q94(self, DeclType);
   AppendWhiteSpace__1qq2(self.CurrentBuilder);
   Append__2qq2(self.CurrentBuilder, FieldName);
   Append__2qq2(self.CurrentBuilder, self.SemiColon);
   return;
};
function CSourceGenerator_GenerateField(self, DeclType, FieldName){ return GenerateField__3q94(self, DeclType, FieldName); }

function GenerateFields__3q94(self, ClassType, ThisType) {
   var SuperType = ThisType.GetSuperType(ThisType);
   if (!SuperType.IsVarType(SuperType)) {
      GenerateFields__3q94(self, ClassType, SuperType);
   };
   var i = 0;
   GenerateCField__3q94(self, "int", "_classId" + (ThisType.TypeId).toString());
   GenerateCField__3q94(self, "int", "_delta" + (ThisType.TypeId).toString());
   while (i < GetFieldSize__1qeq(ClassType)) {
      var ClassField = ZClassField_GetFieldAt(ClassType, i);
      if (ClassField.ClassType == ThisType) {
         GenerateField__3q94(self, ClassField.FieldType, ClassField.FieldName);
      };
      i = i + 1;
   };
   return;
};
function CSourceGenerator_GenerateFields(self, ClassType, ThisType){ return GenerateFields__3q94(self, ClassType, ThisType); }

function VisitErrorNode__2q94(self, Node) {
   ZLogger_LogError__2qw3(Node.SourceToken, Node.ErrorMessage);
   Append__2qq2(self.CurrentBuilder, "ThrowError(");
   Append__2qq2(self.CurrentBuilder, LibZen.QuoteString(Node.ErrorMessage));
   Append__2qq2(self.CurrentBuilder, ")");
   return;
};
function CSourceGenerator_VisitErrorNode(self, Node){ return VisitErrorNode__2q94(self, Node); }


