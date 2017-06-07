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

  $(".registerPage").click(function(){
    window.location.href = "/register";
  });

  $(".register").click(function(){
    $.post("/register",
      {
        username: $("#username").val(),
        password: $("#password").val()
      },
      function(result, status) {
        window.location.href = "/";
      });
  });

  $(function () {
    var socket = io();
    socket.on('connect', function() {
      socket.emit('message', {msg: 'user connected'});
      console.log('user connected');
    });

    socket.on('disconnect', function() {
      socket.emit('message', {msg: 'user disconnected'});
    });

    socket.on('response', function(msg){
      $('#messages').append($('<li>').text(msg));
      var empty_div = $('<div />');
      var send_div = $('<div />', {"class": "sender"});
      var avater = $('<img />', {"src": "chatTemplateExample2_files/cat.jpg"});
      avater.appendTo(empty_div);
      empty_div.appendTo(send_div);
      var empty_div = $('<div />');
      var chat_box = $('<div />', {"class": "left_triangle"});
      var chat_content = $('<span />').text(msg);
      chat_box.appendTo(empty_div);
      chat_content.appendTo(empty_div);
      empty_div.appendTo(send_div);
      var msghsty = $('.msgHistory');
      send_div.appendTo(msghsty);
    });
    $('form').submit(function(){
      socket.emit('message', {msg: $('#inputMsg').val()});
      $('#inputMsg').val('');
      return false;
    });
  });
});
