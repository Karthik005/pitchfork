$(document).ready(function(){
	$flag = true;

	//icons
	var checker = '<i class="fa fa-check"></i>';
	var closer = '<i class="fa fa-close"></i>';

	//error messages
	var usernametaken='<p type="usertaken" class="text-center text-warning" style="display: none">This username is taken.</p>';
	var passwordsno = '<p type="notmatched" class="text-center text-warning" style="display: none">Passwords did not match.</p>';
	var invalidemail = '<p type="invalid" class="text-center text-warning" style="display: none">Invalid Email.</p>'
	var emailtaken = '<p type="emailtaken" class="text-center text-warning" style="display: none">This email id has been registered.</p>'
	var emptyfields = '<h4 id="emptyfields" type="emptyfields" class="text-center text-warning">All fields are required.</h4>'

//helper functions

	var wipepass = function(){
		$('#password').val("");
		$('#confirmpassword').val("");
	};

	var clear = function(obj){
		$(obj).siblings('p').stop().slideUp(function(){
			$(this).remove();
		});
		$(obj).siblings('i').remove();
	};

	var rollup = function(){
		$('html, body').stop().animate({
				scrollTop: 0
			}, 700, function(){});
	};

	var rolltothis = function(obj){
		$('html, body').animate({ scrollTop: $(obj).offset().top-100 }, 1000);
	};

	var checkpass = function(){
		if ($('#password').val() != $('#confirmpassword').val() && $('#confirmpassword') != ""){
			return false;
		}
		else {return true;}
	};

	var slidedown = function(obj){
		$(obj).siblings('p').slideDown();
	};

	var chekcdate = function(){

	}

//prettycheckable
	$('#registerform').find('input').each(function(){
		if ($(this).attr('type')=="checkbox"){
			$(this).prettyCheckable();
		}
	});

//datepicker
	$("#dob").datepicker({
		inline: true,
		changeMonth: true,
		changeYear: true,
	    maxDate: "-16Y",
	    minDate: "-100Y",
	    yearRange: "-100:-16",
	    dateFormat: 'dd/mm/yy'
	});


//urlpath to page
	$urlpath = $(location).attr('href');


//username availability check
	window.flag = false;

	$('#username').on('change', function(){
		clear($('#username'));
		var inputUsername = $(this).val();
		if (inputUsername!=""){
			//alert($(this).val());
			$.get($urlpath+"register_validate?username="+inputUsername,  function(data){
			if (data=="true"){
					$('#username').after(checker);
					window.user_flag = false;
				}
			else if (data == "false"){
					$('#username').after(usernametaken+closer);
					slidedown('#username');
					window.user_flag = true;
				}
			});
			}
		});


//email tester
	function IsEmail(email) {
	  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	  return regex.test(email);
	}

	var host = "http://"+window.location.hostname+":"+window.location.port;
	var emailcheck = function(){$("#email").on('change', function(){
		clear("#email");
		var inputmail = $(this).val();
		if (inputmail && !IsEmail(inputmail)){
			$(this).after(invalidemail+closer);
			slidedown("#email");
			window.mail_flag = true;
		}
		else if (inputmail) {
			$.get($urlpath+"register_validate?email="+inputmail,  function(data){
			if (data=="true"){
					$('#email').after(checker);
					window.mail_flag = false;
				}
			else if (data == "false"){
					$('#email').after(emailtaken+closer);
					slidedown('#email');
					window.mail_flag = true;
				}
			});
		}
	});
	};

	emailcheck();

//password matcher
	$("#confirmpassword").change(function(){
		clear("#confirmpassword");
		clear("#password");
		if (!checkpass()){
			wipepass();
			$(this).after(passwordsno+closer);
			slidedown("#confirmpassword");
			$('#password').after(passwordsno+closer);
			slidedown("#password");
			window.pswd_flag = true;
			}
		else{
			$(this).after(checker);
			$('#password').after(checker);
			window.pswd_flag = false;
		}
	});

//rest checker
	$("input, textarea").change(function(){
		if (!($(this).attr('id') == "username" || 
			$(this).attr('id') =="password"||
			$(this).attr('id') =="confirmpassword"||
			$(this).attr('id') =="email") &&
			$(this).attr('type')!="checkbox") {
		clear("#"+$(this).attr('id'));
		if ($(this).val()){
			$(this).after(checker);
		}
	}
	});


//final check and ajax submit

	$('#registerform').on('submit', function(e){
		e.preventDefault();

		$("#emptyfields").remove();

		var flag=false;

		$('#registerform').find("input, textarea").each(function(){
			if (!$(this).val() || $(this).val() == ""){
					clear("#"+$(this).attr('id'));
					$(this).after(closer);
					flag=true;
				}
		});

		if (flag == true){
			$('#registerform> button').before(emptyfields);
		}

		if (flag || window.user_flag || window.mail_flag || window.pswd_flag){
			wipepass();
			rollup();
			return false;}

		$.post($urlpath+"register_user", $('#registerform').serializeArray(),  function(data){
			if (data == "true"){
				$("")
				window.location.href = host+"/users/login";
				return true;
			}
			
			else if (data == "dberror"){
				$('#registerform> button').after('<p type="usertaken" class="text-center text-warning" style="display: none">Database error. Please try later.</p>');
				$('#registerform> button').next().stop().slideDown();
				wipepass();
				rollup();
				return false;
			}
		});
	});

});

