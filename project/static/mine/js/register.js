$(document).ready(function () {
    $("#smsBtn").bind("click", function () {
        data = {"phone":$("#phone").val(),"password":$("#password").val()};
        $.ajax({
            url:"/register/",
            data:data,
            dataType:"json",
            type:"post",
            success:function(data, status){
                if(data.repetition){
                     alert("此账号已注册,将跳转到登录页面！");
                location.href='http://127.0.0.1:8000/login/';
                }else{
                     $("#smsBtn").text('60秒后重新发送！');
                    alert("验证码已经发送！");
                }
            }
        });
    });
});