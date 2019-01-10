//globals
let lastTextID = null;
let book_page = 1; //page number from server
let maxLength; // max length per text post



//modal button
$("#info-btn").click(function () {
  $("#modal-id").addClass('active');
});

$(".btn-clear").click(function () {
	$("#modal-id").removeClass("active")
});

function randomIntFromInterval(min,max) // min and max included
{
    return Math.floor(Math.random()*(max-min+1)+min);
}

//toastr configuration
toastr.options = {
	"closeButton": true,
  "debug": false,
	"newestOnTop": true,
  "progressBar": true,
  "positionClass": "toast-top-center",
  "preventDuplicates": true,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

// Place the caret at the end of input contenteditable elem
function placeCaretAtEnd(el) {
	el.focus();
	if (typeof window.getSelection != "undefined" &&
    typeof document.createRange != "undefined") {
    var range = document.createRange();
    range.selectNodeContents(el);
    range.collapse(false);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  } else if (typeof document.body.createTextRange != "undefined") {
    var textRange = document.body.createTextRange();
    textRange.moveToElementText(el);
    textRange.collapse(false);
    textRange.select();
  }
}

// disable Enter
document.getElementById("9999999").addEventListener("keydown", function (e) {
  //play sound
  if(e.keyCode != 13){
      eval("type"+randint(3)+'.play()');
    }

  if (e.keyIdentifier == 'U+000A' || e.keyIdentifier == 'Enter' || e.keyCode == 13) {
    e.preventDefault();
    let lgnBtn = document.getElementById('submit-btn');
    if (lgnBtn.classList.contains('disabled')) {
      return false;
    } else {

      if (window.confirm(`Are you sure you want to post:\n \"${$('#9999999').text()}\" ?`)) {
        lgnBtn.click();
      }

    }
  }

})


// focus event for submit input
let focus_flag = true; //flag to run only once
document.getElementById('9999999').addEventListener("click", function () {
  if (focus_flag) {

    this.classList.add('trypewriter'); //add trypewriter font
    //$('#9999999').css('display', 'inline-block;');


		// this.textContent = '';
		this.innerHTML = '&nbsp;';

    this.contentEditable = true;
    this.focus()
    //this.innerHTML = '&nbsp;';


    //document.getElementById("9999999").focus() //focus the text filed
    focus_flag = false;
  }
})

// check for input text size
allow_char = /^[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\.\n\?\!,\s\n\"]*$/
notAllowCharRegex = /(?![abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\.\n\?\!,\s\n\"])./g

let first_flag = true;
document.getElementById('9999999').addEventListener("keyup", function (e) {

  // to fix the binking insit point when click in the input field
  if (first_flag) {
    let firstInput = this.textContent[0]
    this.textContent = firstInput
    this.focus()
    placeCaretAtEnd(document.getElementById("9999999"));
    $('#submit-btn-form').fadeIn(5000); //show submit btn
    first_flag = false
  }



  var c_left = lettersTyped($('#9999999'));

  if (notAllowCharRegex.test($('#9999999').text())) { // if find a not allow char in string
    let notAllowChars = ($('#9999999').text()).match(notAllowCharRegex).toString() //list of char not allowed

    $('#19999999').text(`  Char ${notAllowChars} ${function(){if (notAllowChars.length > 1){return 'are'}else{return 'is'}}()} not allowed!`); // shows with char is not allow
    $('#submit-btn').addClass('disabled'); // disable submit button
    document.getElementById('9999999').style.backgroundColor = '#fee7e7' // red background
    toastr["warning"]("Only ascii characters and !?,.\"\' are allowed", "Error.", {
      onHidden: function () {}
    });

  } else {
    if ((c_left - maxLength) < 0) {
      $('#19999999').text(`  ${maxLength-c_left} characters left`);
      document.getElementById('9999999').style.backgroundColor = 'transparent'
      $('#submit-btn').removeClass('disabled');
    } else if ((c_left - maxLength) > 0) {
      $('#19999999').text('  Limit exceeded!');
      document.getElementById('9999999').style.backgroundColor = '#fee7e7'
      $('#submit-btn').addClass('disabled');

    } else if ((c_left - maxLength) == 0) {
      $('#19999999').text(' ');
      document.getElementById('9999999').style.backgroundColor = 'transparent';
      $('#submit-btn').removeClass('disabled');

    }
  }
});

function lettersTyped(text) {
  var len = text.text().length;
  return len;
}


// focus if blur text input
document.getElementById('9999999').addEventListener('blur', function (event) {
  document.getElementById('9999999').focus();

})


// gihhtlight book texts
function mouseOver(elem) {
  $(elem).toggleClass('bg-secondary')
}
