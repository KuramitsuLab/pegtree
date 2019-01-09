///<reference path='./typings/jquery/jquery.d.ts' />

var Playground;
(function (Playground) {
    function CreateEditor(query) {
        ace.require("ace/ext/language_tools");
        var editor = ace.edit(query);
        editor.setTheme("ace/theme/xcode");
        editor.getSession().setMode("ace/mode/text");
        editor.setFontSize(12);
        editor.setOptions({
            enableBasicAutocompletion: true,
            enableSnippets: true,
            enableLiveAutocompletion: true
        });
        return editor;
    }
    Playground.CreateEditor = CreateEditor;

    function ChangeSyntaxHighlight(editor, targetMode) {
        editor.getSession().setMode("ace/mode/" + targetMode);
    }
    Playground.ChangeSyntaxHighlight = ChangeSyntaxHighlight;
})(Playground || (Playground = {}));

var Debug = {};

$(function () {
    var zenEditor = Playground.CreateEditor("zen-editor");
    Debug.zenEditor = zenEditor;
    Playground.ChangeSyntaxHighlight(zenEditor, "konoha6");
    var outputViewer = Playground.CreateEditor("output-viewer");
    Debug.outputViewer = outputViewer;
    outputViewer.setReadOnly(true);

    var GenerateServer = function (ShowTopFlag) {
        let cmd = document.querySelector("form").elements.cmd.value;
        $.ajax({
            type: "POST",
            url: "/compile",
            data: JSON.stringify({ source: zenEditor.getValue() }),
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: function (data) {
                outputViewer.setValue(data.output);
                outputViewer.clearSelection();
                if (ShowTopFlag) {
                    outputViewer.gotoLine(0);
                }
                if (data.error != "") console.log(data.error);
            },
            error: function () {
                console.log("compile error");
            }
        });
    };

    var timer = null;
    zenEditor.on("change", function (cm, obj) {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
        timer = setTimeout(GenerateServer, 400);
    });

    $("#cmd").on("change", function (cm, obj) {
        let cmd = document.querySelector("form").elements.cmd.value;
        $.ajax({
            url: '/command',
            type: 'POST',
            data: JSON.stringify({ source: zenEditor.getValue(), cmd: cmd }),
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            timeout: 5000,
        })
        .done(function(data) {
            if (data.input != "") {
                zenEditor.setValue(data.input);
                zenEditor.clearSelection();
                zenEditor.gotoLine(0);
            }
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
            outputViewer.setValue(data.output);
            outputViewer.clearSelection();
            outputViewer.gotoLine(0);
            if (data.error != "") console.log(data.error);
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
            console.log("ajax通信に失敗しました");
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
        });
        //resetTarget();
    });

    /*var TargetNames = {
        origami: ['Python3', 'Niko', 'macaron'],
        macaron: ['macaron'],
        parse: ['TPEG'],
        json: ['JSON']
    };

    var TargetMode = {
        Python3: 'python',
        Niko: 'niko',
        macaron: 'macaron',
        TPEG: 'tpeg',
        JSON: 'json'
    }

    var bind = function (target) {
        var Target = $('#Target-' + target);
        Target.click(function () {
            $('li.active').removeClass("active");
            Target.parent().addClass("active");
            $('#active-lang').text(target);
            $('#active-lang').append('<b class="caret"></b>');
            //Playground.ChangeSyntaxHighlight(outputViewer, TargetMode[target]);
        });
    };

    var setTargets = function(targets) {
        $("#TargetCont").append(`<a id="active-lang" href="#" data-toggle="dropdown" class="dropdown-toggle">${targets[0]}<b class="caret"></b></a>`);
        $("#TargetCont").append('<ul id="Targets" class="dropdown-menu"></ul>');
        for (var i = 0; i < targets.length; i++) {
            $("#Targets").append(`<li id="Target-${targets[i]}-li"><a href="#" id="Target-${targets[i]}">${targets[i]}</a></li>`);
            bind(targets[i]);
        }
    }

    var removeTargets = function() {
        $("#active-lang").remove();
        $("#Targets").remove();
    };

    var resetTarget = function() {
        let cmd = document.querySelector("form").elements.cmd.value;
        removeTargets();
        mode = cmd.trim().split(' ')[0];
        if (Object.keys(TargetNames).indexOf(mode) !== -1) {
            setTargets(TargetNames[mode]);
        }
    }*/

    $('#closeButton').click(function () {
        window.open('about:blank','_self').close();
        $.ajax({
            type: "POST",
            url: "/close"
        });
    });

    $('#saveButton').click(function () {
        $.ajax({
            type: "POST",
            url: "/save",
            data: JSON.stringify({ source: zenEditor.getValue()}),
            contentType: "application/json; charset=utf-8",
        });
    });

    $.ajax({
        type: "POST",
        url: "/init",
        dataType: 'json',
        success: function (res) {
            document.querySelector("form").elements.cmd.value = res.cmd;
            zenEditor.setValue(res.input);
            zenEditor.clearSelection();
            zenEditor.gotoLine(0);
            //mode = res.cmd.trim().split(' ')[0];
            //if (Object.keys(TargetNames).indexOf(mode) !== -1)
            //    setTargets(TargetNames[mode]);
        },
        error: function () {
            console.log("error init");
        }
    });
});
