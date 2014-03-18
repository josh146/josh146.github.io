// Document ready function
$(document).ready(function () {

    //Add Hover effect to menus
    $('ul.nav li.dropdown').hover(function() {
        $(this).find('.dropdown-menu').stop(true, true).delay(200).slideDown();
    }, function() {
        $(this).find('.dropdown-menu').stop(true, true).delay(200).slideUp();
    });

    var menubar = document.getElementById("collapse")

    if ( $(window).width() > 767 ) {  
        menubar.className="nav navbar-nav navbar-left";
    }  
    else {  
        menubar.className="nav navbar-nav navbar-right";
    };
    $('#collapse').show();

    // Show active section/page on the navbar
    $('a[href="' + this.location.pathname + '"]').parent().addClass('active');
    
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


    function toggleSlide(e) {
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


        $('#head-content, #page-content, .navbar, body, .navbar-left, .navbar-toggle, .navbar-brand').toggleClass('slide-active');

        // e.stopPropagation();
        // $('.dropdown-toggle').dropdown('toggle')
    }

    function openSlide(e) {
        $('#slidemenu').stop().animate({
            left: '0px'
        });

        $('#navbar-height-col').stop().animate({
            left: '0px'
        });

        $(pagewrapper).stop().animate({
            left: slidewidth
        });

        $(headwrapper).stop().animate({
            left: slidewidth
        });

        $(navigationwrapper).stop().animate({
            left: slidewidth
        });


        $('#slide-nav').toggleClass('slide-active', true);
        $('#slidemenu').toggleClass('slide-active',true);


        $('#head-content, #page-content, .navbar, body, .navbar-left, .navbar-brand, .navbar-toggle').toggleClass('slide-active',true);
    }

    function closeSlide(e) {
        $('#slidemenu').stop().animate({
            left: menuneg
        });

        $('#navbar-height-col').stop().animate({
            left: slideneg
        });

        $(pagewrapper).stop().animate({
            left: '0px'
        });

        $(headwrapper).stop().animate({
            left: '0px'
        });

        $(navigationwrapper).stop().animate({
            left: '0px'
        });


        $('#slide-nav').toggleClass('slide-active', false);
        $('#slidemenu').toggleClass('slide-active', false);


        $('#head-content, #page-content, .navbar, body, .navbar-left, .navbar-brand, .navbar-toggle').toggleClass('slide-active', false);
    }

    $(pagewrapper).on("click", function (e) {
        if ($(this).hasClass('slide-active')) {
            e.preventDefault();
            e.stopPropagation();
            closeSlide(e)
        };
    });

    $(headwrapper).on("click", function (e) {
        if ($(this).hasClass('slide-active')) {
            e.preventDefault();
            e.stopPropagation();
            closeSlide(e)
        };
    });

    $(navigationwrapper).on("click", function (e) {
        if ($('#slide-nav').hasClass('slide-active')) {
            e.preventDefault();
            e.stopPropagation();
            closeSlide(e)
        };
    });


    $("#slide-nav").on("click", '.navbar-toggle, .navbar-brand', function (e) {
        if (!$(this).hasClass('slide-active')) {
            openSlide(e);
        };
    });

    $("#slide-nav").on("click", '#scroll-home, #scroll-about, #scroll-work', closeSlide);


    var selected = '#slidemenu, #page-content, #head-content, body, .navbar, .navbar-left';


    $(window).on("resize", function () {

        if ($(window).width() > 767 && $('.navbar-toggle').is(':hidden')) {
            $(selected).removeClass('slide-active');
            document.getElementById("collapse").className="nav navbar-nav navbar-left";
        }  
        else {  
             document.getElementById("collapse").className="nav navbar-nav navbar-right";
        }

    });

});