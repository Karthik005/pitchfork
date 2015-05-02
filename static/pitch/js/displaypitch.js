$(document).ready(function(){



	var slidedown = function(obj){
		$(obj+"> p").slideDown();
	};

	var clear = function(obj){
		$(obj+'> p').stop().slideUp(function(){
			$(this).remove();
		});
	};

	var host = "http://"+window.location.hostname+":"+window.location.port;
	var arr = window.location.href.split("/");
	var pitch_id = arr[arr.length-2];

	$('#upvote').click(function (){
		var votes = parseInt($('#votes').html());
		var upvotes = parseInt($('#upvotes').html());
		var downvotes = parseInt($('#downvotes').html());
		$.get(host+"/pitch/vote/?pitch_id="+pitch_id+"&vote=1",  function(data){
			if (data=="true"){

					$('#upvotes').html(String(upvotes+1));
					$('#votes').html(String(votes+1));
					$('#upvote, #downvote').removeClass('pointer');
				}
			else if (data == "false"){
					$('#upvote, #downvote').removeClass('pointer');
					$('#overlay-voted').fadeIn();
				}
			});
	});

	$('#downvote').click(function () {
		var votes = parseInt($('#votes').html());
		var upvotes = parseInt($('#upvotes').html());
		var downvotes = parseInt($('#downvotes').html());
		$.get(host+"/pitch/vote/?pitch_id="+pitch_id+"&vote=-1",  function(data){
			if (data=="true"){
					$('#downvotes').html(String(downvotes+1));
					$('#votes').html(String(votes-1));
					$('#upvote, #downvote').removeClass('pointer');
				}
			else if (data == "false"){
					$('#upvote, #downvote').removeClass('pointer');
					$('#overlay-voted').fadeIn();
				}
			});
	});

	$('#okay').click(function(){
		$('#overlay-voted').fadeOut();
	});

	$('#remove').click(function(){
		$('#overlay-remove').fadeIn();
	});

	$('#remove_yes').click(function(){
		$.get(host+"/pitch/remove/?pitch_id="+pitch_id,  function(data){
			if (data=="true"){
					window.location.href = host+"/pitch/mypitches/";
				}
			else if (data == "false"){
					$('#overlay-remove').fadeOut();
				}
			});			
	});	

	$('#remove_no').click(function(){
			$('#overlay-remove').fadeOut();
	});

	$('#pitchin').click(function(){
		$('#overlay-pitchin').fadeIn();
	});

	$('#pitchin_yes').click(function(){
		$.get(host+"/pitch/pitchin/?pitch_id="+pitch_id,  function(data){
			if (data=="true"){
					window.location.href = host+"/pitch/pitchedinpitches/";
				}
			else if (data == "false"){
					$('#overlay-pitchin').fadeOut();
				}
			});			
	});	

	$('#pitchin_no').click(function(){
			$('#overlay-pitchin').fadeOut();
	});

	$('#pitched-in').click(function(){
		$('#overlay-pitchedin').fadeIn();
	});

	$('#okay_pitchedin').click(function(){
		$('#overlay-pitchedin').fadeOut();
	});

	$('#volunteerform').find('input').each(function(){
		if ($(this).attr('type')=="checkbox"){
			$(this).prettyCheckable();
		}
	});

	$('#submit_vol').click(function(){
		var flag = false
		$('#volunteerform').find("input").each(function(){
			if ($(this).is(":checked")){
				flag = true;
			}
			});

			if(!flag){
				$('#overlay-needed').fadeIn();
			}

			if (flag){
			console.log( $( '#volunteerform' ).serialize() );
			$.post(host+"/pitch/devteamadd/", $('#volunteerform').serializeArray(),  function(data){
				if (data == "true"){
					location.reload();
				}

			});
		}
	});

	$('#okay_needed').click(function(){
		$('#overlay-needed').fadeOut();
	});

	$('#commentform').on('submit', function(e){
		e.preventDefault();
		
		if ($('#comment').val().trim().length ==0 ){
			return false;
		}

		$.get(host+"/pitch/addcomment/?"+$('#commentform').serialize(),function(data){
			$(data).hide().insertAfter($('#commentform').prev()).fadeIn(1000);
			$('#comment').val("");
			return true;
		});
	});
});