$(document).ready(function() {
  $('.albumsDiv').on('click', '.clickable', function() {
      var url = $(this).data('url');
      window.location.href = url;
  });
});