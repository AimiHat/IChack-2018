
$(document).ready(function(){
    //First page
    $('a.primary-btn.d-inline-flex.align-items-center').click(function(){
        var text = '<a href="#" class="primary-btn gender d-inline-flex align-items-center"><span class="mr-10">'
        var text2 = '</span></a>';
        $(this).replaceWith(text+'Male'+text2+text+'Female'+text2);
        $('.mr-10').css('margin-right','0px');
        $('a.primary-btn.d-inline-flex.align-items-center').css('margin-right','10px');
        $('a.gender').click(function(){
        $.get('/camera', function(result) {
                $(".banner-area .container .row").html(result);
                $(".banner-area").css('background','transparent')
                $('.banner-area .container .row').removeClass("align-items-center")
            });
        })
    })
    

	var window_width 	 = $(window).width(),
	window_height 		 = window.innerHeight,
	header_height 		 = $(".default-header").height(),
	header_height_static = $(".site-header.static").outerHeight(),
	fitscreen 			 = window_height - header_height;


	$(".fullscreen").css("height", window_height)
	$(".fitscreen").css("height", fitscreen);

     
     // -------   Active Mobile Menu-----//

    $(".menu-bar").on('click', function(e){
        e.preventDefault();
        $("nav").toggleClass('hide');
        $("span", this).toggleClass("lnr-menu lnr-cross");
        $(".main-menu").addClass('mobile-menu');
    });
     
    $('select').niceSelect();
    $('.img-pop-up').magnificPopup({
        type: 'image',
        gallery:{
        enabled:true
        }
    });

    $('.active-works-carousel').owlCarousel({
        center: true,
        items:2,
        loop:true,
        margin: 100,
        dots: true,
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 1,
            },
            768: {
                items: 2,
            }
        }
    });
    // Add smooth scrolling to Menu links
    $(".main-menu li a, .smooth").on('click', function(event) {
            if (this.hash !== "") {
              event.preventDefault();
              var hash = this.hash;
              $('html, body').animate({
                scrollTop: $(hash).offset().top - (-10)
            }, 600, function(){
             
                window.location.hash = hash;
            });
        } 
    });

    $(document).ready(function() {
        $('#mc_embed_signup').find('form').ajaxChimp();
    });      

 });
