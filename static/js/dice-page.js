$(document).ready(function(){

    $("#roll_dice").click(function(e){
        var amt = $("#wager_amt").val();
        var odds_amt = $("#odds_mult").val();
        console.log("Wagered: " + amt);
        var data = {
          "wager_amt": amt,
          "odds": odds_amt
        }
        $.ajax({
                type: 'POST',
                url: ('/roll_dice'),
                data: data,
                success: function(data){
                    if(data == "not_enough"){
                        $("#not_enough_bal").show();
                        console.log(data);
                    }else{
                        console.log(data);
                    }
                },
                error: function(err){
                    console.log("ERRROR");
                }
            });
    });

});




