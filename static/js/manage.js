$(document).ready(function(){

   $("#pendingtable").DataTable();

   $("#pendingwithtable").DataTable();

   $("#rs3").on('input', function(e){
        var rs3Value = $("#rs3").val()
        if (rs3Value.match(/[a-z]/i)){
            $("#os").val("Invalid");
            return;
        }
        if(rs3Value == ""){
            $("#os").val("")
            $("#tokens").val("")
        }else{
            $("#os").val((parseFloat(rs3Value) / 5.0) + "")
            $("#tokens").val((parseFloat(rs3Value) * 10) + "")
        }
    });

    $("#os").on('input', function(e){
        var osValue = $("#os").val()
        if (osValue.match(/[a-z]/i)){
            $("#rs3").val("Invalid");
            return;
        }
        if(osValue == ""){
            $("#rs3").val("")
            $("#tokens").val("")
        }
        else{
            $("#rs3").val((parseFloat(osValue) * 5.0) + "")
            $("#tokens").val((parseFloat(osValue) * 50) + "")
        }
    });

    $("#tokens").on('input', function(e){
        var tokensValue = $("#tokens").val()
        if (tokensValue.match(/[a-z]/i)){
            $("#rs3").val("Invalid");
            return;
        }
        if(tokensValue == ""){
            $("#rs3").val("")
            $("#os").val("")
        }
        else{
            $("#rs3").val((parseFloat(tokensValue) / 10) + "")
            $("#os").val((parseFloat(tokensValue) / 50) + "")
        }
    });
});

function openReq(item){
    $.ajax({
            type: "GET",
            url: '/grab_info/' + item + '/d',
            success: function(response){
                $("#deposits").html(response);
            }
        });
}

function closeReq(item){
    $.ajax({
            type: "GET",
            url: '/grab_info/' + item + '/w',
            success: function(response){
                $("#withdraws").html(response);
            }
        });
}







