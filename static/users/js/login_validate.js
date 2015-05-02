

function getUrlParameter(sParam)
	{
	    var sPageURL = window.location.search.substring(1);
	    var sURLVariables = sPageURL.split('&');
	    for (var i = 0; i < sURLVariables.length; i++) 
	    {
	        var sParameterName = sURLVariables[i].split('=');
	        if (sParameterName[0] == sParam) 
	        {
	            return sParameterName[1];
	        }
	    }
	} 


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

		var urlpath = window.location.href.split('?')[0];
		var sendpath = (urlpath.substr(urlpath.length - 1)=='/') ? urlpath+"login_validate" : urlpath+"/login_validate";

		$.post(sendpath, $('#loginform').serializeArray(),  function(data){
			if (data == "true"){
				var reder = getUrlParameter('red');
				if (reder == undefined){
					reder="user_pitch"
				}
				window.location.href = "http://"+window.location.host+"/redirect/?red="+reder;
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