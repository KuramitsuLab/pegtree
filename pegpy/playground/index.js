///<reference path='./typings/jquery/jquery.d.ts' />

var Playground;
(function (Playground) {
    Playground.CodeGenTarget = "common";
    Playground.Syntax = "konoha6.tpeg";
    Playground.Mode = "origami";

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
    Playground.ChangeSyntaxHighlight(zenEditor, "text");
    var outputViewer = Playground.CreateEditor("output-viewer");
    Playground.ChangeSyntaxHighlight(outputViewer, "text");
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
            data: JSON.stringify({ source: zenEditor.getValue(), target: Playground.CodeGenTarget, syntax: Playground.Syntax, mode: Playground.Mode}),
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
    var TargetOptions = ["common"];
    var TargetMode = ["python"];

    var setTarget = function () {
        var bind = function (n) {
            var Target = $('#Target-' + TargetNames[n]);
            Target.click(function () {
                Playground.CodeGenTarget = TargetOptions[n];
                $('li.active').removeClass("active");
                Target.parent().addClass("active");
                $('#active-lang').text(TargetNames[n]);
                $('#active-lang').append('<b class="caret"></b>');
                //Playground.ChangeSyntaxHighlight(outputViewer, TargetMode[n]);
                if (timer) {
                    clearTimeout(timer);
                    timer = null;
                }
                outputViewer.setValue('');
                GenerateServer(true);
            });
        };

        $("#TargetCont").append('<a id="active-lang" href="#" data-toggle="dropdown" class="dropdown-toggle">Python<b class="caret"></b></a>');
        $("#TargetCont").append('<ul id="Targets" class="dropdown-menu"></ul>');

        for (var i = 0; i < TargetNames.length; i++) {
            $("#Targets").append('<li id="Target-' + TargetNames[i] + '-li"><a href="#" id="Target-' + TargetNames[i] + '">' + TargetNames[i] + '</a></li>');
            bind(i);
        }
    };

    var removeTarget = function() {
        $("#active-lang").remove();
        $("#Targets").remove();
        //for (var i = 0; i < TargetNames.length; i++) {
        //    $("#Target-" + TargetNames[i]).remove();
        //}
    };

    var Samples = ["ifexpr"];

    var setSample = function() {
        var sample_bind = function (n) {
            $('#sample-' + Samples[n]).click(function () {
                url = 'sample/' + Samples[n]
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

        $("#SampleCont").append('<a id="SampleText" href="#" data-toggle="dropdown" class="dropdown-toggle">Sample<b class="caret"></b></a>')
        $("#SampleCont").append('<ul id="zen-sample" class="dropdown-menu"></ul>')

        for (var i = 0; i < Samples.length; i++) {
            $("#zen-sample").append('<li id="sample-' + Samples[i] + '-li"><a href="#" id="sample-' + Samples[i] + '">' + Samples[i] + '</a></li>');
            sample_bind(i);
        }
    };

    var removeSample = function () {
        $("#SampleText").remove()
        $("#zen-sample").remove()
        //for (var i = 0; i < Samples.length; i++) {
        //    $("#sample-" + Samples[i]).remove();
        //}
    };

    var ModePEG = ["parse", "json"]
    var ModeOrigami = ["origami"]
    var ModeNPL = ["macaron", "niko"]

    var setMode = function (Modes) {
        var mode_bind = function (n) {
            var Mode = $("#Mode-" + Modes[n]);
            Mode.click(function () {
                Playground.Mode = Modes[n];
                $('li.active').removeClass("active");
                Mode.parent().addClass("active");
                $('#active-mode').text(Modes[n]);
                $('#active-mode').append('<b class="caret"></b>');
                if (timer) {
                    clearTimeout(timer);
                    timer = null;
                }
                outputViewer.setValue('');
                GenerateServer(true);
            });
        };

        $("#ModeCont").append('<a id="active-mode" href="#" data-toggle="dropdown" class="dropdown-toggle">parse<b class="caret"></b></a>')
        $("#ModeCont").append('<ul id="Modes" class="dropdown-menu"></ul>')

        for (var i = 0; i < Modes.length; i++) {
            $("#Modes").append('<li id="Mode-' + Modes[i] + '-li"><a href="#" id="Mode-' + Modes[i] + '">' + Modes[i] + '</a></li>');
            mode_bind(i);
        }
    };

    var removeMode = function () {
        $("#active-mode").remove()
        $("#Modes").remove()
        //for (var i = 0; i < Modes.length; i++) {
        //    $("#Mode-" + Modes[i]).remove();
        //}
    };


    var SyntaxNames = ['Konoha6', 'NPL', 'Math', 'Python3', 'Java8', 'JavaScript', 'CSV', 'XML', 'JSON', 'UTF-8', 'EMail']
    var SyntaxFiles = ['konoha6.tpeg', 'npl.tpeg', 'math.tpeg', 'python3.tpeg', 'java8.tpeg', 'js.tpeg', 'csv.tpeg', 'xml.tpeg', 'json.tpeg', 'utf8.tpeg', 'email.tpeg']
    var ModeS = [ModePEG.concat(ModeOrigami), ModePEG.concat(ModeNPL), ModePEG, ModePEG, ModePEG, ModePEG, ModePEG, ModePEG, ModePEG, ModePEG, ModePEG]

    var setSyntax = function () {
        var syntax_bind = function (n) {
            var Syntax = $('#Syntax-' + SyntaxNames[n]);
            Syntax.click(function () {
                Playground.Syntax = SyntaxFiles[n];
                $('li.active').removeClass("active");
                Syntax.parent().addClass("active");
                $('#active-syntax').text(SyntaxNames[n]);
                $('#active-syntax').append('<b class="caret"></b>');
                //zenEditor.ChangeSyntaxHighlight(outputViewer, TargetMode[n]);
                if (timer) {
                    clearTimeout(timer);
                    timer = null;
                }
                removeTarget()
                removeSample()
                removeMode()
                setMode(ModeS[n])
                if (n == 0) {
                    setTarget()
                    setSample()
                }
                outputViewer.setValue('');
                GenerateServer(true);
            });
        };

        for (var i = 0; i < SyntaxNames.length; i++) {
            $("#Syntaxs").append('<li id="Syntax-' + SyntaxNames[i] + '-li"><a href="#" id="Syntax-' + SyntaxNames[i] + '">' + SyntaxNames[i] + '</a></li>');
            syntax_bind(i);
        }
    };

    setSyntax();

    $.ajax({
        url: 'sample/input',
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
            Playground.Syntax = res.syntax;//syntac_bind click
            Playground.Mode = res.mode;
            //Playground.CodeGenTarget = res.target

            var n = SyntaxFiles.indexOf(res.syntax);
            $('li.active').removeClass("active");
            var Syntax = $('#Syntax-' + SyntaxNames[n]);
            Syntax.parent().addClass("active");
            $('#active-syntax').text(SyntaxNames[n]);
            $('#active-syntax').append('<b class="caret"></b>');

            removeTarget()
            removeSample()
            removeMode()
            setMode(ModeS[n])
            if (n == 0) {
                setTarget()
                setSample()
            }

            var Mode = $("#Mode-" + res.mode);
            $('li.active').removeClass("active");
            Mode.parent().addClass("active");
            $('#active-mode').text(res.mode);
            $('#active-mode').append('<b class="caret"></b>');
            //zenEditor.ChangeSyntaxHighlight(outputViewer, TargetMode[n]);
            GenerateServer(true);
        },
        error: function () {
            console.log("error init");
        }
    });
});
