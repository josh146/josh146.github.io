$(document).ready(function () {
    
    $('a[href="' + this.location.pathname + '"]').parent().addClass('active');
    
    var socbarBig = document.getElementById("socialbarBIG");
    var socbarSmall = document.getElementById("socialbarSMALL");

    if ( $(window).width() > 767 ) {  
         document.getElementById("collapse").className="nav navbar-nav navbar-left";
         socbarSmall.style.display='none';
         socbarBig.style.display='inline';
    }  
    else {  
         document.getElementById("collapse").className="nav navbar-nav navbar-right";
         socbarSmall.style.display='inline';
         socbarBig.style.display='none';
    }

    //stick in the fixed 100% height behind the navbar but don't wrap it
    $('#slide-nav.navbar .container').append($('<div id="navbar-height-col"></div>'));

    // Enter your ids or classes
    var toggler = '.navbar-toggle';
    var toggler2 = '.navbar-brand';
    var toggler3 = '#scroll-home';
    var toggler4 = '#scroll-about';
    var toggler5 = '#scroll-work';
    var pagewrapper = '#page-content';
    var headwrapper = '#head-content';
    var navigationwrapper = '.navbar-left';
    var menuwidth = '400px'; // the menu inside the slide menu itself
    var slidewidth = '200px';
    var menuneg = '-400px';
    var slideneg = '-200px';


    $("#slide-nav").on("click", toggler, function (e) {

        var selected = $(this).hasClass('slide-active');


        $('#slidemenu').stop().animate({
            left: selected ? menuneg : '0px'
        });

        $('#navbar-height-col').stop().animate({
            left: selected ? slideneg : '0px'
        });

        $(pagewrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(headwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(navigationwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });


        $(this).toggleClass('slide-active', !selected);
        $('#slidemenu').toggleClass('slide-active');


        $('#head-content, #page-content, .navbar, body, .navbar-left, .navbar-brand').toggleClass('slide-active');

        // e.stopPropagation();
        // $('.dropdown-toggle').dropdown('toggle')

    });

    $("#slide-nav").on("click", toggler2, function (e) {

        var selected = $(this).hasClass('slide-active');

        $('#slidemenu').stop().animate({
            left: selected ? menuneg : '0px'
        });

        $('#navbar-height-col').stop().animate({
            left: selected ? slideneg : '0px'
        });

        $(pagewrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(headwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(navigationwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });


        $(this).toggleClass('slide-active', !selected);
        $('#slidemenu').toggleClass('slide-active');


        $('#head-content, #page-content, .navbar, body, .navbar-left, .navbar-toggle').toggleClass('slide-active');

        // e.stopPropagation();
        // $('.dropdown-toggle').dropdown('toggle')

    });

    $("#slide-nav").on("click", toggler3, function (e) {

        $('#slidemenu').stop().animate({
            left: selected ? menuneg : '0px'
        });

        $('#navbar-height-col').stop().animate({
            left: selected ? slideneg : '0px'
        });

        $(pagewrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(headwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(navigationwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });


        $('#head-content, #page-content, .navbar, body, .navbar-left, .navbar-toggle, .navbar-brand').toggleClass('slide-active');

        // e.stopPropagation();
        // $('.dropdown-toggle').dropdown('toggle')

    });

    $("#slide-nav").on("click", toggler4, function (e) {

        $('#slidemenu').stop().animate({
            left: selected ? menuneg : '0px'
        });

        $('#navbar-height-col').stop().animate({
            left: selected ? slideneg : '0px'
        });

        $(pagewrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(headwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(navigationwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });


        $('#head-content, #page-content, .navbar, body, .navbar-left, .navbar-toggle, .navbar-brand').toggleClass('slide-active');

        // e.stopPropagation();
        // $('.dropdown-toggle').dropdown('toggle')

    });

    $("#slide-nav").on("click", toggler5, function (e) {

        $('#slidemenu').stop().animate({
            left: selected ? menuneg : '0px'
        });

        $('#navbar-height-col').stop().animate({
            left: selected ? slideneg : '0px'
        });

        $(pagewrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(headwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });

        $(navigationwrapper).stop().animate({
            left: selected ? '0px' : slidewidth
        });


        $('#head-content, #page-content, .navbar, body, .navbar-left, .navbar-toggle, .navbar-brand').toggleClass('slide-active');

        // e.stopPropagation();
        // $('.dropdown-toggle').dropdown('toggle')

    });


    var selected = '#slidemenu, #page-content, #head-content, body, .navbar, .navbar-left';


    $(window).on("resize", function () {

        if ($(window).width() > 767 && $('.navbar-toggle').is(':hidden')) {
            $(selected).removeClass('slide-active');
            document.getElementById("collapse").className="nav navbar-nav navbar-left";
            socbarSmall.style.display='none';
            socbarBig.style.display='inline';
        }  
        else {  
             document.getElementById("collapse").className="nav navbar-nav navbar-right";
             socbarSmall.style.display='inline';
             socbarBig.style.display='none';
        }

    });

});