$(document).ready(function () {
    // $(".ischose").bind("click", function () {
    //     var cartid = $(this).attr("cartid");
    //     alert('-------------',cartid);
    //     //告诉后台把当前用户的当前购物车数据的ischeck更改
    //     $.post("/changecart2/", {"cartid":cartid}, function (data, status) {
    //         if (data.error == 0){
    //             if (data.flag){
    //                 $(document.getElementById(cartid)).html("√")
    //             } else {
    //                 $(document.getElementById(cartid)).html("")
    //             }
    //         }
    //     });
    // });

    //下订单
    // $("#ok").bind("click", function () {
    //     var f = confirm("确认下单？");
    //     if (f) {
    //         $.post("/qOrder/", function (data, status) {
    //             console.log("**********************", data);
    //             if (data.error == 0){
    //                 location.href = "http://127.0.0.1:8000/cart/"
    //             }
    //         });
    //     }
    // });

     function chengect() {
         var pid = $(this).attr("pid");
         var flag = $(this).attr("flag");
         var id = $(this).attr("add");
         // var$(document.getElementById(pid)).html(data.Succeed)

         // alert('接受请求',pid);
        $.ajax({
             url:"http://127.0.0.1:8000/changecart2/"+flag+"/",
           data:{"pid":pid,'flag':flag},
           dataType:"json",
           type:"post",
           success:function (data,status) {
              if(data.Num){
                $(document.getElementById(id)).html(data.Num)
             }
               if(data.Del){
                 location.href="http://127.0.0.1:8000/cart/";
             }
             if(data.Null){
                 alert('库存不足!')
             }
           }
        });
    }
    $(".addShopping").bind('click',chengect);
    $(".subShopping").bind('click',chengect);
});