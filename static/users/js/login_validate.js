$(document).ready(function(){
	$('#loginform').on('submit', function(e){
		e.preventDefault();

		$('#loginform').children('p').each(function(){
				$(this).stop().slideUp("normal", function() {} );
			
		});

		$flag=false;
		$('#loginform').children('input').each(function(){
			if (!$(this).val()){
				if(!$(this).next().is('p')){
				$(this).after('<p type="notfilled" class="text-center text-warning" style="display: none">The above field is required.</p>');
				}
				$(this).next().stop().slideDown();
				$flag=true;
				}
		});
		if ($flag==true){return false;}

		$urlpath = $(location).attr('href');

		$.post($urlpath+"login_validate", $('#loginform').serializeArray(),  function(data){
			if (data == "true"){
				window.location.href = "http://"+window.location.host+"/redirect/?from="+$.url('?from');
				return true;
			}
			else if (data == "false"){
				if(!$('#loginform> button').next().is('p')){
				$('#loginform> button').after('<p type="wronginp" class="text-center text-warning" style="display: none">Incorrect username or password.</p>');
				}
				$('#loginform> button').next().stop().slideDown();
				return false;
			}
		});
	});

});




//	window.location.href = "http://example.com/Registration/Success/";
//		)