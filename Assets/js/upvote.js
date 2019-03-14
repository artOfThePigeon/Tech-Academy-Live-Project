$(function()){
  $(".upvote").click(function() {

    $.ajax({
      url: '/forum/upvote',
      type: 'POST',

    });
  });
};
