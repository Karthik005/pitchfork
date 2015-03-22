$(document).ready(function(){
	$('#loginform').on('submit', function(e){
		e.preventDefault();

		$('#loginform').children('p').each(function(){
				$(this).slideUp("normal", function() { $(this).remove(); } );
			
		});

		$flag=false;
		$('#loginform').children('input').each(function(){
			if (!$(this).val()){
				$(this).after('<p type="notfilled" class="text-center text-warning" style="display: none">The above field is required.</p>');
				$(this).next().slideDown();
				$flag=true;
				}
		});
		if ($flag==true){return false;}

		$urlpath = $(location).attr('href');

		$.post($urlpath+"login_validate", $('#loginform').serializeArray(),  function(data){
			if (data == "true"){
				window.location.href = "http://"+$.url('hostname')+"/redirect/"+$.url('?from');
				return true;
			}
			else if (data == "false"){
				$('#loginform> button').after('<p type="wronginp" class="text-center" style="display: none">Incorrect username or password.</p>');
				$('#loginform> button').next().slideDown();
			}
		});
	});

});




//	window.location.href = "http://example.com/Registration/Success/";
//		)