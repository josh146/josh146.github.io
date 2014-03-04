$(document).ready(function() {
  // Activate zoom on content images in the main column and add an icon overlay (but ignore icons)

  // start image process only when loading is completed
  if (document.readyState != "complete") {
    //console.info('ready...');
    setTimeout(arguments.callee, 100);
    return;
  }
  var containter_width = null;
  if ($('#blog_main_area').width()) {
    containter_width = $('#blog_main_area').width();
  }
  else {
    containter_width = $('article.content').width();
  }

  $("section#blog img").each(function() {
    // Until we properly generate thumbnails and their links on Pelican's side, we just link an image to itself.
    if (this.width > containter_width) {
      if ($(this).parents('a').length === 0) {
        $(this).wrap(
          $('<a/>').attr('href', $(this).attr('src'))
        );
      }

      // Add a special class for images linking to videos
      var link_tag = $(this).closest('a');
      link_tag.magnificPopup({
        type: 'image',
        closeOnContentClick: true,
        midClick: true,
        mainClass: 'mfp-with-zoom',
        zoom: {
          enabled: true,
          duration: 300,
          easing: 'ease-in-out',
        },
      });
      $(this).css('max-width', containter_width);

      // // Add overlay zoom icon
      // $(this).mglass({opacity: 1,});
    }
  });
});

! function($) {
  $(function() {
    //   // Activate Bootstrap's tooltips
    //   $("[rel*=tooltip]").tooltip();

    // Add bootstrap table style to table elements
    $("article.content table").addClass('table').addClass('table-hover');

    // create tree
    $('.tree li:has(ul)').addClass('parent_li').find(' > span').attr('title', 'Collapse this branch');
    $('.tree li.parent_li > span').on('click', function(e) {
      // var children = $(this).siblings('ul:first').find('> li');
      var children = $(this).next('ul').find('> li');
      if (children.is(":visible")) {
        children.hide('fast');
        $(this).attr('title', 'Expand this branch').find(' > i').removeClass('fa fa-minus-square-o').addClass('fa fa-plus-square-o');
      }
      else {
        children.show('fast');
        $(this).attr('title', 'Collapse this branch').find(' > i').removeClass('fa fa-plus-square-o').addClass('fa fa-minus-square-o');
      }
      e.stopPropagation();
    });

    // static variable counter maker

    function makeCounter() {
      var count = 1;
      return function(a) {
        if (a === 0) {
          return count;
        }
        else {
          count = count + a;
          return count;
        }

      };
    }

    // ajax-like load blog index
    var counter = makeCounter();
    var index_num = counter(0);
    var POST_LIMIT = 3;
    var POST_COUNT = parseInt($('#blog_main_area').attr('count'), 10);
    $('#prev').on('click', function(e) {
      index_num -= 1;
      if (index_num === 0) {
        index_num = 1;
        $(this).addClass('disabled');
      }
      else {
        $('#next').removeClass('disabled');
        $('#blog_main_area div.item').each(function() {
          if ($(this).is(':visible')) {
            $(this).hide('slow');
          }
        });

        $('#blog_main_area div.item').slice((index_num - 1) * POST_LIMIT, (index_num) * POST_LIMIT).each(function() {
          $(this).show('slow');
        });

        if (index_num === 1) {
          $(this).addClass('disabled');
        }
      }

    });
    $('#next').on('click', function(e) {
      index_num += 1;
      $('#prev').removeClass('disabled');

      if (index_num * POST_LIMIT <= POST_COUNT + POST_LIMIT) {
        $('#blog_main_area div.item').each(function() {
          if ($(this).is(':visible')) {
            $(this).hide('slow');
          }
        });

        $('#blog_main_area div.item').slice((index_num - 1) * POST_LIMIT, (index_num) * POST_LIMIT).each(function() {
          $(this).show('slow');
        });
      }

      if (index_num * POST_LIMIT >= POST_COUNT) {
        $(this).addClass('disabled');
        index_num = Math.ceil(POST_COUNT / POST_LIMIT);
      }
    });




  });
}(window.jQuery);
