// Function that changes the tags displayed based on an input filter string
function filterTagChange(filter,method) {
    // this finds all links in a list that contain the input,
    // and hide the ones not containing the input while showing the ones that do
    $('.list-of-tags').find("a:not(:Contains(" + filter + "))").parent().hide();
    $('.list-of-tags').find("a:Contains(" + filter + ")").parent().show();

    if(method=="slide"){
        $('#in-tags-contains').find("h2:not(:Contains(" + filter + "))").parent().slideUp();
        $('#in-tags-contains').find("h2:Contains(" + filter + ")").parent().slideDown();
    } else {
       $('#in-tags-contains').find("h2:not(:Contains(" + filter + "))").parent().hide();
       $('#in-tags-contains').find("h2:Contains(" + filter + ")").parent().show();
    }

    var numTags = $('.list-of-tags').find("a:Contains(" + filter + ")").length;
    if(numTags==0) {
        $('#notag').text('No tags found matching your filter');
    } else {
        $('#notag').text('');
    }
    $('#clearfilter').show();
}

// Document ready function
$(document).ready(function () {

    // clicking on tag buttons performs a filter
    $('.list-of-tags a').click(
        function(e){
            var elementId = $(this).attr("id");
            e.preventDefault();
            e.stopPropagation();

            if(elementId == 'clearfilterlink') {
                $('#filterinput').val('');    
                $('.list-of-tags').find("li").show();
                $('.articletag-container').slideDown();
                $('#notag').text('');
                $('#clearfilter').hide();
            } else {
                $('#filterinput').val($(this).data('name'));
                filterTagChange($(this).data('name'),'slide');             
            }
        }
    );

    // if there is a url hash, this expands all Bootstrap accordians
    location.hash && $(location.hash + '.collapse').collapse('show');

    // On Enter, show search results
    $('#st-search-input').keyup(function(e){
      if(e.keyCode == 13)
      {
         function complete() {
           $('#searchresults').fadeIn('slow');
        }
        $('#blog-content-area').fadeOut('slow',complete);
      }
    });

    // on Enter, show search results from the sidebar
    $('#st-search-input-mobile').keyup(function(e){
      if(e.keyCode == 13)
      {
         function complete() {
            $('html, body').animate({
                scrollTop: $("#searchresults").offset().top - 60
            });
           $('#searchresults').fadeIn('slow');
        }
        $('.navbar-toggle').trigger('click');
        $('#blog-content-area').fadeOut('slow',complete);
      }
    });

});