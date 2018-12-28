///<reference path='./typings/jquery/jquery.d.ts' />

var Playground;
(function (Playground) {
    function CreateEditor(query) {
        ace.require("ace/ext/language_tools");
        var editor = ace.edit(query);
        editor.setTheme("ace/theme/xcode");
        editor.getSession().setMode("ace/mode/text");
        editor.setFontSize(13);
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
            data: JSON.stringify({ source: zenEditor.getValue(), cmd: cmd}),
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: function (res) {
                outputViewer.setValue(res.source);
                outputViewer.clearSelection();
                if (ShowTopFlag) {
                    outputViewer.gotoLine(0);
                }
                if (res.error != "") console.log(res.error)
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

    var TargetNames = ["Python"];
    var TargetMode = ["python"];

    var bind = function (n) {
        var Target = $('#Target-' + TargetNames[n]);
        Target.click(function () {
            $('li.active').removeClass("active");
            Target.parent().addClass("active");
            $('#active-lang').text(TargetNames[n]);
            $('#active-lang').append('<b class="caret"></b>');
            Playground.ChangeSyntaxHighlight(outputViewer, TargetMode[n]);
        });
    };

    for (var i = 0; i < TargetNames.length; i++) {
        $("#Targets").append('<li id="Target-' + TargetNames[i] + '-li"><a href="#" id="Target-' + TargetNames[i] + '">' + TargetNames[i] + '</a></li>');
        bind(i);
    }

    var Samples = ["ifexpr", "fib"];

    var sample_bind = function (n) {
        $('#sample-' + Samples[n]).click(function () {
            url = '/sample/' + Samples[n]
            $.ajax({
                url: url,
                type: 'POST',
                timeout: 5000,
            })
            .done(function(data) {
                zenEditor.setValue(data);
                zenEditor.clearSelection();
                zenEditor.gotoLine(0);
                if (timer) {
                    clearTimeout(timer);
                    timer = null;
                }
                outputViewer.setValue('');
                GenerateServer(true);
            })
            .fail(function(XMLHttpRequest, textStatus, errorThrown) {
                console.log("ajax通信に失敗しました");
                console.log("XMLHttpRequest : " + XMLHttpRequest.status);
                console.log("textStatus     : " + textStatus);
                console.log("errorThrown    : " + errorThrown.message);
                // alert(errorThrown.message);
            });
        });
    };

    for (var i = 0; i < Samples.length; i++) {
        $("#zen-sample").append('<li id="sample-' + Samples[i] + '-li"><a href="#" id="sample-' + Samples[i] + '">' + Samples[i] + '</a></li>');
        sample_bind(i);
    }

    var SyntaxNames = ['Konoha6', 'NPL', 'Math', 'Python3', 'Java8', 'JavaScript', 'CSV', 'XML', 'JSON', 'UTF-8', 'EMail']
    var SyntaxFiles = ['konoha6.tpeg', 'npl.tpeg', 'math.tpeg', 'python3.tpeg', 'java8.tpeg', 'js.tpeg', 'csv.tpeg', 'xml.tpeg', 'json.tpeg', 'utf8.tpeg', 'email.tpeg']

    $('#saveButton').click(function () {
        let cmd = document.querySelector("form").elements.cmd.value;
        $.ajax({
            type: "POST",
            url: "/save",
            data: JSON.stringify({source: zenEditor.getValue(), cmd: cmd}),
            contentType: "application/json; charset=utf-8"
        })
        .done(function(data) {
        })
        .fail(function(XMLHttpRequest, textStatus, errorThrown) {
            console.log("ajax通信に失敗しました");
            console.log("XMLHttpRequest : " + XMLHttpRequest.status);
            console.log("textStatus     : " + textStatus);
            console.log("errorThrown    : " + errorThrown.message);
            // alert(errorThrown.message);
        });
    });

    $.ajax({
        url: '/sample/input',
        type: 'POST',
        timeout: 5000,
    })
    .done(function(data) {
        zenEditor.setValue(data);
        zenEditor.clearSelection();
        zenEditor.gotoLine(0);
    })
    .fail(function(XMLHttpRequest, textStatus, errorThrown) {
        console.log("ajax通信に失敗しました");
        console.log("XMLHttpRequest : " + XMLHttpRequest.status);
        console.log("textStatus     : " + textStatus);
        console.log("errorThrown    : " + errorThrown.message);
        // alert(errorThrown.message);
    });

    $.ajax({
        type: "POST",
        url: "/init",
        dataType: 'json',
        success: function (res) {
            document.querySelector("form").elements.cmd.value = res.cmd;
            GenerateServer(true);
        },
        error: function () {
            console.log("error init");
        }
    });
});
