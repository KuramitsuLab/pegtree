///<reference path='./typings/jquery/jquery.d.ts' />

var Playground;
(function (Playground) {
    Playground.CodeGenTarget = "js";

    function CreateEditor(query) {
        var editor = ace.edit(query);
        editor.setTheme("ace/theme/xcode");
        editor.getSession().setMode("ace/mode/javascript");
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
    Playground.ChangeSyntaxHighlight(zenEditor, "typescript");
    var outputViewer = Playground.CreateEditor("output-viewer");
    Debug.outputViewer = outputViewer;
    outputViewer.setReadOnly(true);

    //var Generate = () => {
    //    outputViewer.setValue(zenEditor.getValue());
    //    outputViewer.clearSelection();
    //};
    var GenerateServer = function (ShowTopFlag) {
        $.ajax({
            type: "POST",
            url: "/compile",
            data: JSON.stringify({ source: zenEditor.getValue(), option: Playground.CodeGenTarget }),
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: function (res) {
                outputViewer.setValue(res.source);
                outputViewer.clearSelection();
                if (ShowTopFlag) {
                    outputViewer.gotoLine(0);
                }
            },
            error: function () {
                console.log("error");
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
    var TargetOptions = ["py"];
    var TargetMode = ["python"];

    var bind = function (n) {
        var Target = $('#Target-' + TargetNames[n]);
        Target.click(function () {
            Playground.CodeGenTarget = TargetOptions[n];
            $('li.active').removeClass("active");
            Target.parent().addClass("active");
            $('#active-lang').text(TargetNames[n]);
            $('#active-lang').append('<b class="caret"></b>');
            Playground.ChangeSyntaxHighlight(outputViewer, TargetMode[n]);
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
            GenerateServer(true);
        });
    };

    for (var i = 0; i < TargetNames.length; i++) {
        $("#Targets").append('<li id="Target-' + TargetNames[i] + '-li"><a href="#" id="Target-' + TargetNames[i] + '">' + TargetNames[i] + '</a></li>');
        bind(i);
    }

    var Samples = ["function", "if", "while", "class", "fibo", "binarytrees"];

    var sample_bind = function (n) {
        $('#sample-' + Samples[n]).click(function () {
            zenEditor.setValue($("#" + Samples[n]).html());
            zenEditor.clearSelection();
            zenEditor.gotoLine(0);
            GenerateServer(true);
        });
    };

    for (var i = 0; i < Samples.length; i++) {
        $("#zen-sample").append('<li id="sample-' + Samples[i] + '-li"><a href="#" id="sample-' + Samples[i] + '">' + Samples[i] + '</a></li>');
        sample_bind(i);
    }

    $("#Target-JavaScript-li").addClass("active");
});
