///<reference path='./typings/jquery/jquery.d.ts' />
declare var ace: any;

module Playground {
    export var CodeGenTarget = "js";

    export function CreateEditor(query: string): any {
        var editor = ace.edit(query);
        editor.setTheme("ace/theme/xcode");
        editor.getSession().setMode("ace/mode/javascript");
        return editor;
    }

    export function ChangeSyntaxHighlight(editor: any, targetMode: string): void {
        editor.getSession().setMode("ace/mode/" + targetMode);
    }
}

var Debug: any = {};

$(() => {
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

    var GenerateServer = (ShowTopFlag: boolean) => {
        $.ajax({
            type: "POST",
            url: "/compile",
            data: JSON.stringify({source: zenEditor.getValue(), option: Playground.CodeGenTarget}),
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: (res) => {
                outputViewer.setValue(res.source);
                outputViewer.clearSelection();
                if(ShowTopFlag) {
                    outputViewer.gotoLine(0);
                }
            },
            error: () => {
                console.log("error");
            }
        });
    }

    var timer: number = null;
    zenEditor.on("change", function(cm, obj) {
        if(timer){
            clearTimeout(timer);
            timer = null;
        }
        timer = setTimeout(GenerateServer, 400);
    });

    var TargetNames   = ["Python"];
    var TargetOptions = ["py"];
    var TargetMode    = ["python"];

    var bind = (n) => {
        var Target = $('#Target-' + TargetNames[n]);
        Target.click(function(){
            Playground.CodeGenTarget = TargetOptions[n];
            $('li.active').removeClass("active");
            Target.parent().addClass("active");
            $('#active-lang').text(TargetNames[n]);
            $('#active-lang').append('<b class="caret"></b>');
            Playground.ChangeSyntaxHighlight(outputViewer, TargetMode[n]);
            if(timer){
                clearTimeout(timer);
                timer = null;
            }
            GenerateServer(true);
        });
    };

    for(var i = 0; i < TargetNames.length; i++){
        $("#Targets").append('<li id="Target-'+TargetNames[i]+'-li"><a href="#" id="Target-'+TargetNames[i]+'">'+TargetNames[i]+'</a></li>');
        bind(i);
    }

    var Samples = ["function", "if", "while", "class", "fibo", "binarytrees"]

    var sample_bind = (n) => {
        $('#sample-'+Samples[n]).click(function(){
            zenEditor.setValue($("#"+ Samples[n]).html());
            zenEditor.clearSelection();
            zenEditor.gotoLine(0);
            GenerateServer(true);
        });
    };

    for(var i = 0; i < Samples.length; i++){
        $("#zen-sample").append('<li id="sample-'+Samples[i]+'-li"><a href="#" id="sample-'+Samples[i]+'">'+Samples[i]+'</a></li>');
        sample_bind(i);
    }


    $("#Target-JavaScript-li").addClass("active");
});
