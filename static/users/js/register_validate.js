$(document).ready(function(){

	$('#registerform').find('input').each(function(){
		if ($(this).attr('type')=="checkbox"){
			$(this).prettyCheckable();
		}
	});

	$('#username').keyup(function(){
		var inputUsername = $(this).val();
		if (inputUsername.val()!=""){
			$.post()
		}
	});
	var wipepass = function(){
		$('#password').val("");
		$('#confirmpassword').val("");
	};

	var rollup = function(){
		$('html, body').stop().animate({
				scrollTop: 0
			}, 700, function(){});
	}

	var checkpass = function(){
		if ($('#password').val() != $('#confirmpassword').val()  ){
			alert("afksdjh");
			$('#password, #confirmpassword').each(function(){
				$(this).after('<p type="notmatched" class="text-center text-warning" style="display: none">Passwords did not match.</p>');
				$(this).next().stop().slideDown();
			});
			wipepass();
			rollup();
			return false;
		}
	};

	checkpass();


	$('#registerform').on('submit', function(e){
		e.preventDefault();

		$('#registerform').find("p").each(function(){
				$(this).stop().slideUp("normal", function() { $(this).remove(); } );
			
		});

		$flag=false;
		$('#registerform').find("input, textarea").each(function(){
			if (!$(this).val() || $(this).val() == ""){
				$(this).after('<p type="notfilled" class="text-center text-warning" style="display: none"><i class="fa fa-close"></i> This field is required.</p>');
				$(this).next().stop().slideDown();
				$flag=true;
				}
			else{
				$(this).after('<i class="fa fa-check"></i>');
			}
		});

		if ($flag==true){
			wipepass();
			rollup();
			return false;}

		if (checkpass() == false) {return false;}

		$urlpath = $(location).attr('href');

		$.post($urlpath+"register_validate", $('#registerform').serializeArray(),  function(data){
			console.log(1);
			alert(data);
			if (data == "true"){
				window.location.href = $urlpath+"/registration_successful";
				return true;
			}
			else if (data == "username_taken"){
				$('#username').after('<p type="usertaken" class="text-center text-warning" style="display: none">This username is already taken.</p>');
				$('#username').next().stop().slideDown();
				wipepass();
				rollup();
				return false;
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

