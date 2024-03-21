
$(document).ready(function(){
    // Function to handle filtering
    function filterReviews() {
      var url = $('.ajax_filter').data('url');
      console.log("change detected!");
        // Get the current values of the inputs
        var selectedRating = $('#ratingSelect').val();
        var albumName = $('#albumNameInput').val();  
        var artistName = $('#artistNameInput').val();

        $.ajax({
            url: url,
            data: {
                // Send the ratings and names as part of the request
                'rating': selectedRating,
                'album_name': albumName,
                'artist_name': artistName 
            },
            success: function(response) {
                $('.albumsDiv').html(response.html);  // Update the albums container
            }
        });
    }

    // Bind the filterReviews function to changes in both the rating select and the album name input
    $('#ratingSelect').change(filterReviews);
    $('#albumNameInput').on('input', filterReviews);  // Trigger filtering as the user types
    $('#artistNameInput').on('input', filterReviews);
});
