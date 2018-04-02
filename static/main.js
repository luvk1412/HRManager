

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



/*
 * Material Deesign Checkboxes non Polymer updated for use in bootstrap.
 * Tested and working in: IE9+, Chrome (Mobile + Desktop), Safari, Opera, Firefox.
 * @author Jason Mayes 2014, www.jasonmayes.com
 * @update Sergey Kupletsky 2014, www.design4net.ru
*/

var wskCheckbox = function() {
  var wskCheckboxes = [];
  var SPACE_KEY = 32;

  function addEventHandler(elem, eventType, handler) {
    if (elem.addEventListener) {
      elem.addEventListener (eventType, handler, false);
    }
    else if (elem.attachEvent) {
      elem.attachEvent ('on' + eventType, handler);
    }
  }

  function clickHandler(e) {
    e.stopPropagation();
    if (this.className.indexOf('checked') < 0) {
      this.className += ' checked';
    } else {
      this.className = 'chk-span';
    }
  }

  function keyHandler(e) {
    e.stopPropagation();
    if (e.keyCode === SPACE_KEY) {
      clickHandler.call(this, e);
      // Also update the checkbox state.

      var cbox = document.getElementById(this.parentNode.getAttribute('for'));
      cbox.checked = !cbox.checked;
    }
  }

  function clickHandlerLabel(e) {
    var id = this.getAttribute('for');
    var i = wskCheckboxes.length;
    while (i--) {
      if (wskCheckboxes[i].id === id) {
        if (wskCheckboxes[i].checkbox.className.indexOf('checked') < 0) {
          wskCheckboxes[i].checkbox.className += ' checked';
        } else {
          wskCheckboxes[i].checkbox.className = 'chk-span';
        }
        break;
      }
    }
  }

  function findCheckBoxes() {
    var labels =  document.getElementsByTagName('label');
    var i = labels.length;
    while (i--) {
      var posCheckbox = document.getElementById(labels[i].getAttribute('for'));
      if (posCheckbox !== null && posCheckbox.type === 'checkbox') {
        var text = labels[i].innerText;
        var span = document.createElement('span');
        span.className = 'chk-span';
        span.tabIndex = i;
        labels[i].insertBefore(span, labels[i].firstChild);
        addEventHandler(span, 'click', clickHandler);
        addEventHandler(span, 'keyup', keyHandler);
        addEventHandler(labels[i], 'click', clickHandlerLabel);
        wskCheckboxes.push({'checkbox': span,
            'id': labels[i].getAttribute('for')});
      }
    }
  }

  return {
    init: findCheckBoxes
  };
}();

wskCheckbox.init();