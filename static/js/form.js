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
				$('#trailerPoster').append("<iframe width='560' height='315' src="+data.trailerURL+" frameborder='0' allowfullscreen></iframe>");
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});