$(document).ready(function(){
  $(".login").click(function(){
    $.post("/login",
      {
        username:$("#username").val(),
        password: $("#password").val()
      },
      function(result, status) {
        console.log(result, status);
        window.location.href = "/";
      });
    });
});
