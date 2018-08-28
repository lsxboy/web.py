// $(document).ready(function () {
//     $("#login").bind("click", function () {
//         data = {"phone":$("#phone").val(),'password':$('#password').val()};
//         $.ajax({
//             url:"/login/",
//             data:data,
//             dataType:"json",
//             type:"post",
//             success:function(data, status){
//                 if (data=='True'){
//                  alert("账号或者密码有误,请重新输入！");
//             }
//                 // $("#smsBtn").text('60秒后重新发送！');
//                 // alert("验证码已经发送！");
//                 // console.log(data);
//                 // console.log("ajax接受成功");
//             }
//         });
//     });
// });