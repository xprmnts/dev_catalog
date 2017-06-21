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
				console.log(data.posterURL);
				$('#trailerPoster').css("height","400px");
				$('#trailerPoster').css("background", "url('"+data.posterURL+"') no-repeat border-box center center");
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});