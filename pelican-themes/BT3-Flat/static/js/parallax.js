var ua = navigator.userAgent,
  isMobileWebkit = /WebKit/.test(ua) && /Mobile/.test(ua);

var iOS = /(iPad|iPhone|iPod)/g.test( navigator.userAgent );

function isIE() {
  return ((navigator.appName == 'Microsoft Internet Explorer') || ((navigator.appName == 'Netscape') && (new RegExp("Trident/.*rv:([0-9]{1,}[\.0-9]{0,})").exec(navigator.userAgent) != null)));
}

function createParallax(imagetype,speedVal) {
  $(imagetype).parallax({ speed: speedVal, axis: 'y' });
  $('.image-caption').parallaxDiv({ speed: -speedVal, axis: 'y' });
  $(imagetype).parallaxUpdate({ speed: speedVal, axis: 'y' });
}

(function(){

  if (isMobileWebkit) {
    // $('html').addClass('mobile');
  }

  if (iOS) {
    $("#ipadBG").css("display", "block");
    $(".fullscreen-img").css("display", "none");
  };

  $(function(){

    if (!isMobileWebkit) {

        if (!isIE()) {
          $("body").niceScroll();
        }

      }
  });

  // homemade parallax
  $.fn.parallax = function ( userSettings ) {
      var options = $.extend( {}, $.fn.parallax.defaults, userSettings );

      return this.each(function () {
          var $this = $(this),
              isX = options.axis === 'x',
              origPos = ( $this.css( 'background-position' ) || '' ).split(' '),
              origX = $this.css( 'background-position-x' ) || origPos[ 0 ],
              origY = $this.css( 'background-position-y' ) || origPos[ 1 ],
              dist = function () {
                  return -$( window )[ isX ? 'scrollLeft' : 'scrollTop' ]();
              };
          $this
              // .css( 'background-attachment', 'fixed' )
              .addClass( 'inview' );

          $this.bind('inview', function ( e, visible ) {
              $this[ visible ? 'addClass' : 'removeClass' ]( 'inview' );
          });

          $( window ).bind( 'scroll', function () {
              if ( !$this.hasClass( 'inview' )) { return; }
              var xPos = isX ? ( dist() * options.speed ) + 'px' : origX,
                  yPos = isX ? origY : ( dist() * options.speed ) + 'px';
              $this.css( 'background-position', xPos + ' calc(' + origY + ' + ' + yPos +')' );
          });
      });
  };

  // homemade parallax
  $.fn.parallaxUpdate = function ( userSettings ) {
      var options = $.extend( {}, $.fn.parallax.defaults, userSettings );

      return this.each(function () {
          var $this = $(this),
              isX = options.axis === 'x',
              origPos = ( $this.css( 'background-position' ) || '' ).split(' '),
              origX = $this.css( 'background-position-x' ) || origPos[ 0 ],
              origY = $this.css( 'background-position-y' ) || origPos[ 1 ],
              dist = function () {
                  return -$( window )[ isX ? 'scrollLeft' : 'scrollTop' ]();
              };
          $this
              // .css( 'background-attachment', 'fixed' )
              .addClass( 'inview' );

          $this.bind('inview', function ( e, visible ) {
              $this[ visible ? 'addClass' : 'removeClass' ]( 'inview' );
          });

          if ( !$this.hasClass( 'inview' )) { return; }
          var xPos = isX ? ( dist() * options.speed ) + 'px' : origX,
              yPos = isX ? origY : ( dist() * options.speed ) + 'px';
          $this.css( 'background-position', xPos + ' calc(' + origY + ' + ' + yPos +')' );
      });
  };

  $.fn.parallax.defaults = {
      start: 0,
      stop: $( document ).height(),
      speed: 1,
      axis: 'x'
  };

  $.fn.parallaxDiv = function ( userSettings ) {
      var options = $.extend( {}, $.fn.parallax.defaults, userSettings );

      return this.each(function () {
          var $this = $(this),
              isX = options.axis === 'x',
              origTopMargin = $this.css( 'margin-top' ) || origPos[ 1 ],
              dist = function () {
                  return -$( window )[ 'scrollTop' ]();
              };
          $this
              // .css( 'background-attachment', 'fixed' )
              .addClass( 'inview' );

          $this.bind('inview', function ( e, visible ) {
              $this[ visible ? 'addClass' : 'removeClass' ]( 'inview' );
          });

          $( window ).bind( 'scroll', function () {
              if ( !$this.hasClass( 'inview' )) { return; }
                var yPos = ( dist() * options.speed ) + 'px';
              $this.css( 'margin-top', ' calc(' + origTopMargin + ' + ' + yPos +')' );
          });
      });
  };

})();