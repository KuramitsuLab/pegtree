var JavaScriptGlobal = Function("return this")();

Object.prototype.IsVarType = function (self) {
   return self.HasUnknownType;
};
Object.prototype.IsGreekType = function (self) {
   return self.HasGreekType;
};

var LibZen = {};
LibZen.AnotherName = (function(s){
	var ch = s.charAt(0);
	var chAnother = ch.toLowerCase();
	if(ch == chAnother){
		ch = ch.toUpperCase();
	}
	return ch + s.substring(1);
});

LibZen.NullChar			= 0;
LibZen.UndefinedChar	= 1;
LibZen.DigitChar		= 2;
LibZen.UpperAlphaChar	= 3;
LibZen.LowerAlphaChar	= 4;
LibZen.UnderBarChar		= 5;
LibZen.NewLineChar		= 6;
LibZen.TabChar			= 7;
LibZen.SpaceChar		= 8;
LibZen.OpenParChar		= 9;
LibZen.CloseParChar		= 10;
LibZen.OpenBracketChar	= 11;
LibZen.CloseBracketChar	= 12;
LibZen.OpenBraceChar	= 13;
LibZen.CloseBraceChar	= 14;
LibZen.LessThanChar		= 15;
LibZen.GreaterThanChar	= 16;
LibZen.QuoteChar		= 17;
LibZen.DoubleQuoteChar	= 18;
LibZen.BackQuoteChar	= 19;
LibZen.SurprisedChar	= 20;
LibZen.SharpChar		= 21;
LibZen.DollarChar		= 22;
LibZen.PercentChar		= 23;
LibZen.AndChar			= 24;
LibZen.StarChar			= 25;
LibZen.PlusChar			= 26;
LibZen.CommaChar		= 27;
LibZen.MinusChar		= 28;
LibZen.DotChar			= 29;
LibZen.SlashChar		= 30;
LibZen.ColonChar		= 31;
LibZen.SemiColonChar	= 32;
LibZen.EqualChar		= 33;
LibZen.QuestionChar		= 34;
LibZen.AtmarkChar		= 35;
LibZen.VarChar			= 36;
LibZen.ChilderChar		= 37;
LibZen.BackSlashChar	= 38;
LibZen.HatChar			= 39;
LibZen.UnicodeChar		= 40;
LibZen.MaxSizeOfChars	= 41;

LibZen.ApplyMatchFunc = (function(MatchFunc, ParentNode, TokenContext, LeftNode){
	return MatchFunc.call(ParentNode, TokenContext, LeftNode);
});

LibZen.ApplyTokenFunc = (function(TokenFunc, SourceContext){
	return TokenFunc.call(SourceContext);
});

LibZen.ArrayCopy = (function(src, sIndex, dst, dIndex, length){
	for(var i = 0; i < length; i++){
		dst[dIndex + i] = src[sIndex + i];
	}
});

LibZen.Assert = (function(TestResult){
	if (!TestResult) {
		throw new Error("ASSERTION FAILED");
	}
});

LibZen.GetChar = (function(Text, Pos){
	return Text.charCodeAt(Pos);
});

LibZen.GetClassName = (function(Value){
	return Value.constructor.name;
});

LibZen.GetTokenMatrixIndex = (function(c){
	if(c < 128) {
		return LibZen.CharMatrix[c];
	}
	return LibZen.UnicodeChar;
});

LibZen.IsDigit = (function(ch){
	return 48/*0*/ <= ch && ch <= 57/*9*/;
});

LibZen.IsFlag = (function(flag, flag2){
	return ((flag & flag2) == flag2);
});

LibZen.IsLetter = (function(ch){
	if(ch > 90){
		ch -= 0x20;
	}
	return 65/*A*/ <= ch && ch <= 90/*Z*/;
});

LibZen.IsSymbol = (function(ch){
	return LibZen.IsLetter(ch) || ch == 95/*_*/ || ch > 255;
});

LibZen.JoinStrings = (function(Unit, Times){
	var Builder = [];
	for(var i = 0; i < Times; i++){
		Builder.push(Unit);
	}
	return Builder.join("");
});

LibZen.NewNodeArray = (function(Size){
	var a = [];
	a[Size - 1] = null;
	return a;
});

LibZen.NewTokenMatrix = (function(){
	var a = [];
	a[LibZen.MaxSizeOfChars - 1] = null;
	return a;
});

LibZen.NewTypeArray = (function(Size){
	var a = [];
	a[Size - 1] = null;
	return a;
});

LibZen.ParseFloat = (function(Text){
	return parseFloat(Text);
});

LibZen.ParseInt = (function(Text){
	return parseInt(Text);
});

LibZen.PrintDebug = (function(){
	console.log(msg);
});

LibZen.PrintLine = (function(msg){
	console.log(msg);
});

LibZen.QuoteString = (function(Text){
	var sb = [];
	sb.push('"');
	for(var i = 0; i < Text.length(); i = i + 1) {
		var ch = Text.charAt(i);
		if(ch == '\n') {
			sb.push("\\n");
		}
		else if(ch == '\t') {
			sb.push("\\t");
		}
		else if(ch == '"') {
			sb.push("\\\"");
		}
		else if(ch == '\\') {
			sb.push("\\\\");
		}
		else {
			sb.push(ch);
		}
	}
	sb.push('"');
	return sb.join("");
});

LibZen.SourceBuilderToString = (function(Builder, BeginIndex, EndIndex){
	var builder = [];
	if(BeginIndex == undefined){
		BeginIndex = 0;
	}
	if(EndIndex == undefined){
		EndIndex = Builder.SourceList.length();
	}
	for(var i = BeginIndex; i < EndIndex; i = i + 1) {
		builder.push(Builder.SourceList.ArrayValues[i]);
	}
	return builder.join("");
});

LibZen.StringMatrix = [
		"q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "0", "4",
		"a", "s", "d", "f", "g", "h", "j", "k", "l", "9", "1", "6",
		"z", "x", "c", "v", "b", "n", "m", "7", "5", "3", "2", "8"
	];

LibZen.Stringfy = (function(number){
	var l = LibZen.StringMatrix.length;
	var d = number % l;
	number = number / l;
	var c = number % l;
	number = number / l;
	return LibZen.StringMatrix[number] + LibZen.StringMatrix[c] + LibZen.StringMatrix[d];
});

LibZen.UnquoteString = (function(Text){
	var sb = []
	var quote = Text.charAt(0);
	var i = 0;
	var Length = Text.length;
	if(quote == '"' || quote == '\'') {
		i = 1;
		Length -= 1;
	}
	else {
		quote = '\0';
	}
	for(; i < Length; i += 1) {
		var ch = Text.charAt(i);
		if(ch == '\\') {
			i++;
			var next = Text.charAt(i);
			switch (next) {
			case 't':
				ch = '\t';
				break;
			case 'n':
				ch = '\n';
				break;
			case '"':
				ch = '"';
				break;
			case '\'':
				ch = '\'';
				break;
			case '\\':
				ch = '\\';
				break;
			default:
				ch = next;
				break;
			}
		}
		sb.push(ch);
	}
	return sb.join("");
});

LibZen.WriteTo = (function(FileName, List){
	if(FileName == null) {
		for(var i = 0; i < List.size(); i++) {
			var Builder = List.ArrayValues[i];
			console.log(Builder.toString());
			Builder.Clear();
		}
	}else{
		throw new Error("Not impremented");
	}
});
