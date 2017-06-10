"use strict";

function register() {
  $(".register").click(function() {
    var username = $("#username").val();
    var password = $("#password").val();
    var repassword = $("#password_repeat").val();
    if (!username || !password || !repassword) {
      alert("请填写用户名或密码");
      return false;
    }
    if (password != repassword) {
      alert("密码不匹配");
      return false;
    }
    $.post("/register",
      {
        username: $("#username").val(),
        password: $("#password").val()
      });
    return true;
  });
}

$(document).ready(function() {
  register();
});
