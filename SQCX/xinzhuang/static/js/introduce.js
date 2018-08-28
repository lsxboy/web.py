// 上一页按钮
// 获取浏览器的高度
var win_height = $(window).height();
var back_position = ($(window).height()) / 2;
$('.back').css("top", back_position + 'px');
// 上下滚动按钮
$('.up_down').css("top", (back_position - 35) + 'px');
// 上下滚动屏幕
function scrool_up() {
    if ($('.intro_content').scrollTop() != 0) {
        // console.log(up_height);
        var a = $('.intro_content').scrollTop();
        $('.intro_content').scrollTop(a - 120)
        // $('.intro_content').scrollTop('0')
    }

}
var win_top = $("body").height()
function scroll_down() {
    if ($('.intro_content').scrollTop() != win_top) {
        var a = $('.intro_content').scrollTop();
        $('.intro_content').scrollTop(a + 120)
    }
}
// 隐藏滚动条
$('.intro_content').css({
    height: win_height + 'px'
})
