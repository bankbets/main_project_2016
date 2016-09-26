$(document).ready(function(){

    $(window).click(function(){
        $(".form").fadeOut();
        $(".outside").fadeOut();
    });

    $('.form').click(function(e){
        e.stopPropagation();
    });

    $("#close_tray").click(function(e){
        e.stopPropagation();
        $(".form").fadeOut();
        $(".outside").fadeOut();
    });

    $("#display_login").click(function(e){
        e.stopPropagation();
        $(".form").fadeIn();
        $(".outside").fadeIn();
    });

    $('.form').find('input, textarea').on('keyup blur focus', function (e) {
      var $this = $(this),
          label = $this.prev('label');

          if (e.type === 'keyup') {
                if ($this.val() === '') {
              label.removeClass('active highlight');
            } else {
              label.addClass('active highlight');
            }
        } else if (e.type === 'blur') {
            if( $this.val() === '' ) {
                label.removeClass('active highlight');
                } else {
                label.removeClass('highlight');
                }
        } else if (e.type === 'focus') {

          if( $this.val() === '' ) {
                label.removeClass('highlight');
                }
          else if( $this.val() !== '' ) {
                label.addClass('highlight');
                }
        }

    });

    $('.tab a').on('click', function (e) {

      e.preventDefault();

      $(this).parent().addClass('active');
      $(this).parent().siblings().removeClass('active');

      target = $(this).attr('href');

      $('.tab-content > div').not(target).hide();

      $(target).fadeIn(600);

    });

    $("#register_form").submit(function(ev){
        ev.preventDefault();
        var frm = $("#register_form");
        $("#invalid_pass").hide();
        $("#short_pass").hide();
        $("#taken").hide();
        $("#short_user").hide();
        if($("#pass1").val() != $("#pass2").val()){
            $("#invalid_pass").show();
        }else if($("#pass1").val().length < 8){
            $("#short_pass").show();
        }else{
            $.ajax({
                type: 'POST',
                url: frm.attr('action'),
                data: frm.serialize(),
                success: function(data){
                    if(data == "taken"){
                        $("#taken").show();
                    }else if(data == "short"){
                        $("#short_user").show();
                    }else{
                        if(data == "done"){
                            $("#success_register").show();
                        }
                        frm.trigger('reset');
                        $("#make_bank").prop('disabled', true);
                        $("#username").prop('disabled', true);
                        $("#pass1").prop('disabled', true);
                        $("#pass2").prop('disabled', true);
                        $("#email").prop('disabled', true);
                    }
                }
            });
        }
    });

    $("#check_login").submit(function(ev){
        ev.preventDefault();
        var frm = $("#check_login");
        $("#invalid").hide();
        $.ajax({
            type: 'POST',
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function(data){
                if(data == "fail"){
                    $("#invalid").show();
                }else{
                    $("#success_login").show();
                }
            }
        });
    });

});




