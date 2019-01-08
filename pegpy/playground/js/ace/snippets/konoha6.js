define("ace/snippets/konoha6",["require","exports","module"], function(require, exports, module) {
"use strict";

exports.snippetText = "snippet #!\n\
	#!/usr/bin/env konoha6\n\
# New Function\n\
snippet assume\n\
	assume ${1:name}: ${2:type}\n\
# If\n\
snippet if\n\
	if ${1:condition}\n\
	then ${2:then}\n\
	else ${3:else}\n\
";
exports.scope = "konoha6";

});                (function() {
                    window.require(["ace/snippets/konoha6"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
