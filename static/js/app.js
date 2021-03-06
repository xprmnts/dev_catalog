/*
When the hamburger icon gets clicked animate the icon
and display the nav elements with animation
*/

$('#hamburger').click(function(){

  $('#hamburger').toggleClass('change');// the change class animates the hamburger
  $('li').toggleClass('responsive'); // the responsive class animates list elements in nav
  $('nav').toggleClass('show'); // the show class makes nav visible (could possibly use .show()?)

});

/*
When a nav element gets clicked within the expanded menu
animate the icon back to its original state
remove the responsive class from the elements to hide them

Need to monitor window size, or the class toggles go heywaire (there's probably a better way to do this)
*/

$(document).ready(function() {
    // run test on initial page load
    checkSize();
    // run test on resize of the window
    $(window).resize(checkSize);

});

function checkSize(){

  if ($(window).width() < 500){

    if($('li').hasClass('responsive')){

      $('li').removeClass('responsive');

    }

   $('.navlist-item').click(function(){

      $('#hamburger').toggleClass('change');
	    $('li').toggleClass('responsive');
	    $('nav').toggleClass('show');

   });
  }

  if ($(window).width() >= 500){

    if(!$('li').hasClass('responsive')){
      $('li').addClass('responsive');
    }

	}

}


