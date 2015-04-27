$(document).ready(function(){
	$flag = true;

	//icons
	var checker = '<i class="fa fa-check"></i>';
	var closer = '<i class="fa fa-close"></i>';

	//error messages
	var titletaken='<p type="usertaken" class="text-center text-warning" style="display: none">This title is taken.</p>';
	var devteamnumber='<p type="devteamnumber" class="text-center text-warning" style="display: none; margin-top: -2px; margin-bottom: 3px;">Value must range from 1-10.</p>';
// 	var invalidemail = '<p type="invalid" class="text-center text-warning" style="display: none">Invalid Email.</p>'
// 	var emailtaken = '<p type="emailtaken" class="text-center text-warning" style="display: none">This email id has been registered.</p>'
	var emptyfields = '<h4 id="emptyfields" type="emptyfields" class="text-center text-warning">Some required fields are empty.</h4>'

// //helper functions

	var clear = function(obj){
		$(obj).siblings('p').stop().slideUp(function(){
			$(this).remove();
		});
		$(obj).siblings('i').remove();
	};

	var slidedown = function(obj){
		$(obj).siblings('p').slideDown();
	};

//prettycheckable
	$('#pitchform').find('input').each(function(){
		if ($(this).attr('type')=="checkbox"){
			$(this).prettyCheckable();
		}
	});

//uploader
	$("[type=file]").on("change", function(){
	  // Name of file and placeholder
	  var file = this.files[0].name;
	  var dflt = $(this).attr("placeholder");
	  if($(this).val()!=""){
	    $(this).next().text(file);
	  } else {
	    $(this).next().text(dflt);
	  }
	});

//datepicker
	$.datepicker.setDefaults({
		inline: true,
		changeMonth: true,
		changeYear: true,
	    yearRange: "0:0",
	    dateFormat: 'dd/mm/yy'
	});

	$("#appclose").datepicker({
	    maxDate: "+1Y1M",
	    minDate: "+0Y10D",
	});

	$("#devstart").datepicker({
		maxDate: "+1Y3M",
	    minDate: "+1Y1M"
	});


//urlpath to page
	$urlpath = $(location).attr('href');


// //pitch title availability check
	window.flag = false;

	$('#title').on('change', function(){
		clear($('#title'));
		var inputTitle = $(this).val();
		if (inputTitle!=""){
			//alert($(this).val());
			$.get($urlpath+"pitch_validate?title="+ inputTitle,  function(data){
			if (data=="true"){
					$('#title').after(checker);
					window.title_flag = false;
				}
			else if (data == "false"){
					$('#title').after(titletaken+closer);
					slidedown('#title');
					window.title_flag = true;
				}
			});
			}
		});


//devteam tester
	
	var isnumber = function(num){
		var mynum = parseInt(num);
		if (mynum > 10 || mynum < 1){
			return false
		}
		else{
			return true;
		}
	};


	var devteamnumbercheck = function(){$("#numvol").on('change keyup', function(){
		clear("#numvol");
		//sanitize input
		  var sanitized = $(this).val().replace(/[^0-9]/g, '');
  		$(this).val(sanitized);
  		//endsanitizezd
  	});
  	$("#numvol").on('change', function(){
		var input = $(this).val();
		if (input && !isNaN(input) && !isnumber(input)){
			$(this).after(devteamnumber);
			slidedown("#numvol");
			window.devteam_flag = true;
		}

		else if (input) {
			window.devteam_flag = false;
		}
	});
	};

	devteamnumbercheck();	
// 	emailcheck();

// //password matcher
// 	$("#confirmpassword").change(function(){
// 		clear("#confirmpassword");
// 		clear("#password");
// 		if (!checkpass()){
// 			wipepass();
// 			$(this).after(passwordsno+closer);
// 			slidedown("#confirmpassword");
// 			$('#password').after(passwordsno+closer);
// 			slidedown("#password");
// 			window.pswd_flag = true;
// 			}
// 		else{
// 			$(this).after(checker);
// 			$('#password').after(checker);
// 			window.pswd_flag = false;
// 		}
// 	});

//rest checker
	$("input, textarea").change(function(){
		if (!($(this).attr('id') == "title" || 
			$(this).attr('id') =="numvol")) {
		clear("#"+$(this).attr('id'));
		if ($(this).val() && $(this).attr('type') != "checkbox"){
			$(this).after(checker);
		}
	}
	});


// //final check and ajax submit

	$('#pitchform').on('submit', function(e){
		e.preventDefault();

		$("#emptyfields").remove();

		var flag=false;

		$('#pitchform').find("input, textarea").each(function(){
			if ((!$(this).val() || $(this).val() == "") && ($(this).attr('id') != "file")) {
					clear("#"+$(this).attr('id'));
					$(this).after(closer);
					flag=true;
				}
		});

		if (flag == true){
			$('#pitchsubmit').before(emptyfields);
		}

		if (flag || window.title_flag || window.devteam_flag){
			return false;
		}

		$.post($urlpath, $('#pitchform').serializeArray(),  function(data){
			if (data == "true"){
				$("")
				window.location.href = $urlpath+"mypitches/";
				return true;
			}
			
			else if (data == "dberror"){
				$('#pitchform> button').after('<p type="usertaken" class="text-center text-warning" style="display: none">Database error. Please try later.</p>');
				$('#pitchform> button').next().stop().slideDown();
				return false;
			}
		});
	});

} );

