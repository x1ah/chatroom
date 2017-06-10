function chat() {
    var socket = io();
    socket.on('connect', function() {
      socket.emit('user_connect');
    });

    socket.on('disconnect', function() {
      socket.emit('user_disconnect');
    });

    socket.on('init', function(msg) {
      if (!current_user) {
        current_user = msg['user'];
      };
      appendGroupMessage(msg['msg'], '系统消息', 'left');
    });

    socket.on('response', function(msg){
      if (msg['user'] == current_user) {
        appendGroupMessage(msg['msg'],msg['user_nickname'], 'right');
      } else {
        appendGroupMessage(msg['msg'], msg['user_nickname'], 'left');
      }
    });
}

function submitMsg() {
    $('form').submit(function(){
      if ($('#inputMsg').val() != "") {
        socket.emit('message', {msg: $('#inputMsg').val()});
        $('#inputMsg').val('');
      }
      return false;
    });
}

function appendGroupMessage(msg_content, nickname, position) {
  var empty_div = $('<div />');
  if (position == 'left') {
    var send_div = $('<div />', {"class": "sender"});
    // 群消息显示成员昵称
    var nickname = $('<p />', {"class": "nickname_left"}).text(nickname);
  } else {
    var send_div = $('<div />', {"class": "receiver"});
    // 群消息显示成员昵称
    var nickname = $('<p />', {"class": "nickname_right"}).text(nickname);
  }
  var avater = $('<img />', {"src": '/static/images/github.png'});
  avater.appendTo(empty_div);
  empty_div.appendTo(send_div);
  nickname.appendTo(send_div);
  var empty_div = $('<div />');
  if (position == 'left') {
    var chat_box = $('<div />', {"class": "left_triangle"});
  } else {
    var chat_box = $('<div />', {"class": "right_triangle"});
  }
  var chat_content = $('<span />').text(msg_content);
  chat_box.appendTo(empty_div);
  chat_content.appendTo(empty_div);
  empty_div.appendTo(send_div);
  var msghsty = $('.msgHistory');
  send_div.appendTo(msghsty);
  var recevier = document.getElementsByClassName("msgHistory");
  scrollToBottom();
}

function scrollToBottom() {
  // 每个消息框内容都是 span 标签
  var msg = document.getElementsByTagName("span");
  if (msg.length > 0) {
    msg[msg.length-1].scrollIntoView();
  };
}


$(document).ready(function() {
  current_user = '';
  chat();
  submitMsg();
});
