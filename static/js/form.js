$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				year : $('#yearInput').val(),
				title : $('#titleInput').val()
			},
			type : 'POST',
			url : '/searchprocess'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').append(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').show();
				$('#trailerPoster').css("height","400px");
 				//$('#trailerPoster').append(data);
 				$('#trailerPoster').css("background", "url('"+data.Poster+"') no-repeat border-box center center");
				$('#trailerPoster').after("<iframe width='560' height='315' src="+data.Trailer+" frameborder='0' allowfullscreen></iframe>");
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});