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
 				//$('#trailerPoster').append(data);
 				$('.movie-poster').attr("src", data.Poster);
				$('.embedded-trailer').attr("src", data.Trailer);
				$("ul").empty();
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

				movieDetails.Title = data.Title;
				movieDetails.Genre = data.Genre;
				movieDetails.Year = data.Year;
				movieDetails.Rated = data.Rated;
				movieDetails.Director = data.Director;
				movieDetails.imdbRating = data.imdbRating;
				movieDetails.Plot = data.Plot;
				movieDetails.Poster = data.Poster;
				movieDetails.Trailer = data.Trailer;
				movieDetails.imdbID = data.imdbID;
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
				$('#addSuccess').append(data.error).show();
				$('#addError').hide();
			}
		});
		event.preventDefault();
	});



});