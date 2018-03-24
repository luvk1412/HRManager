/*

UPDATED SO THAT IT WORKS BETTER. But I'm still useless at jQuery.

Found on this dribbble: http://dribbble.com/shots/1284939-2point0-CP-Login/attachments/177970

I know it's basic, I'm not good at this stuff...

*/
var username = false;
var password = false;

$("#username").on("input", function() {
  if ( $(this).val().length > 0) {
   username = true;
  } else {
    username = false;
  }
  if (username && password) {
    $('.login').css('background', '#14a03d');
    $('.login').addClass('buttonafter');
  } else {
    $('.login').css('background', '#a0a0a0');
    $('.login').removeClass('buttonafter');
  }
});

$("#password").on("input", function() {
 if ( $(this).val().length > 0){
   password = true;
  } else {
    password = false;
  }
  if (username && password) {
    $('.login').css('background', '#14a03d');
    $('.login').addClass('buttonafter');
  } else {
    $('.login').css('background', '#a0a0a0');
    $('.login').removeClass('buttonafter');
  }
});
