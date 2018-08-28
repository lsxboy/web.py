// var gpath = "http://192.168.3.88:8080";
var gpath = "";
// var gpath = "http://192.168.3.52:8090";

// 设置翻页按钮大小
var win_width=$(window).width();
if (win_width >= 600 && win_width <= 768){
    $('.back i').css({
        'font-size':55+'px'
    })
    $('.up_down i').css({
        'font-size': 65 + 'px'
    })
}