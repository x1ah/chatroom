"use strict";

function login() {
  $(".login").click(function(){
    var username = $("#username").val();
    var password = $("#password").val();
    if (!username && !password) {
      alert("请填入用户名或密码");
      return false;
    }
    $.post("/login",
      {
        username:$("#username").val(),
        password: $("#password").val()
      });
  });
}

function redirectToRegister() {
  $(".registerPage").click(function(){
    window.location.href = "/register";
    return false;
  });
}

$(document).ready(function() {
  login();
  redirectToRegister();
});
