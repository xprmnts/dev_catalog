$(document).ready(function() {
	var movieDetails = {};
	$('.movie-search-form').on('submit', function(event) {
		movieDetails = {};
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
				$('.movie-add-form').show();
 				$('.movie-poster').attr("src", data.Poster);
				$('.embedded-trailer').attr("src", data.Trailer);
				$(".movie-data-list").empty();
				var items = [];
        		items.push( "<li>Title: "+data.Title+"</li>" );
        		items.push( "<li>Genre: "+data.Genre+"</li>" );
        		items.push( "<li>Year: "+data.Year+"</li>" );
        		items.push( "<li>Rated: "+data.Rated+"</li>" );
        		items.push( "<li>Director: "+data.Director+"</li>" );
        		items.push( "<li>IMDB Rating: "+data.imdbRating+"</li>" );
        		items.push( "<li>Plot: "+data.Plot+"</li>" );
        		for (var i = 0; i < items.length; i++) {
        		    $(".movie-data-list").append(items[i]);
        		}
        		$(".movie-data-list").append({
        		    html: items.join("")
        		});
				$('#errorAlert').hide();

				movieDetails = data;
			}

		});
		event.preventDefault();
	});

	$('.movie-add-form').on('submit', function(event){
		console.log(movieDetails);
		$.ajax({
			data : movieDetails,
			type : 'POST',
			url : '/newsearchedtrailer'
		}).done(function(data){
			if (data.error) {
				$('#addError').append(data.error).show();
				$('#addSuccess').hide();
			}
			else {
				$('#addSuccess').append(data.success).show();
				$('#addError').hide();
			}
		});
		event.preventDefault();
	});

});