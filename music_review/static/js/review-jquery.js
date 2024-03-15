$(document).ready(function() {
    $('.review_div').click(function() {
      var url = $(this).data('url');
      window.location.href = url;
    });
  });