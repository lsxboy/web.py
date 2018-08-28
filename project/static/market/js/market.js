$(document).ready(function () {
    // http://127.0.0.1:8000/market/103606/
    var url = location.href;
    spanIdStr = "yellow" + url.split("/")[4];
    $yellowSpan = $(document.getElementById(spanIdStr));
    $yellowSpan.addClass("yellowSlide");


    //点击分类和排序
    $("#allTypeBtn").bind("click", function () {
        $("#typediv").toggle();
        $("#sortdiv").hide();
    });
    $("#allSortBtn").bind("click", function () {
        $("#sortdiv").toggle();
        $("#typediv").hide();
    });
    $("#typediv").bind("click", func);
    $("#sortdiv").bind("click", func);
    function func() {
        $(this).hide()
    }
    //给分类添加颜色
    var aIdStr = "type" + url.split("/")[5];
    var $a = $(document.getElementById(aIdStr));
    $a.addClass("abg");

     //添加购物车
    function changecart() {
        var flag = $(this).attr("flag");
        //获取 组id 子组id 商品ID
        var pid = $(this).attr("pid");
        var gid = $(this).attr("gid");
        var ppid = $(this).attr("ppid");
       //发起ajax请求，添加购物
        $.ajax({
           url:"/changecart/"+flag+'/',
           data:{"pid":pid,'gid':gid,'ppid':ppid},
           dataType:"json",
           type:"post",
           success:function (data,status) {
               // console.log(data);
                if (data.Succeed){
                    $(document.getElementById(pid)).html(data.Succeed)
               }
               if (data.Error){
                   location.href="http://127.0.0.1:8000/login/";
               }
                if (data.None ){
                    alert('请添加收货地址!');
                   location.href="http://127.0.0.1:8000/add/";
               }
               if (data.Null){
                   alert('库存不足！')
               }
                if (data.login){
                     alert('您没有登录我们无法保存您的信息哦');
                   location.href="http://127.0.0.1:8000/login/";
               }
               if (data.reload){
                    alert('你没有添加该商品！')
                   // location.href="http://127.0.0.1:8000/market/103606/0/0/";
               }

           }
       });
}

     $(".addBtn").bind("click",changecart);
     $(".subBtn").bind("click",changecart);



});




