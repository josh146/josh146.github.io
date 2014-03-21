(function(){
  //set up iScroll and stellar
  var ua = navigator.userAgent,
    isMobileWebkit = /WebKit/.test(ua) && /Mobile/.test(ua);

  if (isMobileWebkit) {
    $('html').addClass('mobile');
  }

  $(function(){
    var iScrollInstance;

    if (isMobileWebkit) {
      iScrollInstance = new iScroll('wrapper');

      $('#scroller').stellar({
        scrollProperty: 'transform',
        positionProperty: 'transform',
        horizontalScrolling: false,
        verticalOffset: 50
      });
    } else {
      $.stellar({
        horizontalScrolling: false,
        verticalOffset: 50
      });
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