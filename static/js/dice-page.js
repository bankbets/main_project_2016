$(document).ready(function(){
    var betstable = $('#betstable').DataTable({
        "info":     false,
        "searching":   false
    } );

    $("#halfbutton").click(function(e){
        $("#wager_amt").val(Math.ceil(($("#wager_amt").val() / 2)));
        if(parseInt($("#wager_amt").val()) > parseInt($("#balance_new").html().substring(9))){
           $("#wager_amt").val($("#balance_new").html().substring(9));
        }
    });

    $("#doublebutton").click(function(e){
        $("#wager_amt").val(Math.ceil(($("#wager_amt").val() * 2)));
        if(parseInt($("#wager_amt").val()) > parseInt($("#balance_new").html().substring(9))){
           $("#wager_amt").val($("#balance_new").html().substring(9));
        }
    });

    $("#maxbutton").click(function(e){
        $("#wager_amt").val($("#balance_new").html().substring(9));
    });

    $("#roll_dice").click(function(e){
        $("#roll_dice").prop('disabled', true);
        var amt = $("#wager_amt").val();
        var odds_amt = $("#odds_mult").val();
        var client_seed = $("#client_seed").val();
        var data = {
          "wager_amt": amt,
          "odds": odds_amt,
          "client_seed": client_seed
        }
        $("#not_enough_bal").hide();
        $.ajax({
                type: 'POST',
                url: ('/roll_dice'),
                data: data,
                success: function(data){
                    if(data == "not_enough"){
                        $("#not_enough_bal").show();
                    }else{
                        $("#balance_new").html("Balance: " + data.newbal);
                        if(data.option > 0){
                            $("#prof").addClass("win").removeClass("lose");
                            betstable.row.add([data.bet, data.user, data.amt_total, "54", data.rolled, data.profit, data.s_seed]).order([0, 'desc']).draw(false).nodes().to$().addClass('win');
                            $("#prof").html("+" + data.option);
                        }else{
                            $("#prof").addClass("lose").removeClass("win");
                            betstable.row.add([data.bet, data.user, data.amt_total, "54", data.rolled, data.profit, data.s_seed]).order([0, 'desc']).draw(false).nodes().to$().addClass('lose');
                            $("#prof").html(data.option);
                        }
                    }
                    $("#roll_dice").prop('disabled', false);
                },
                error: function(err){
                    console.log("ERRROR");
                }
            });
    });
});




