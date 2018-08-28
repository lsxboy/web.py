$.ajax({
    type: "GET",
    url: gpath + "/affairs/" + $.cookie('name_cookie'),
    dataType: "json",
    success: function (res) {
        for (var i in res.Data) {
            for (var k in res.Data[i]) {
                // console.log(k)
                var tit = '<h4>' + k + '</h4>';
                // console.log(res.data[i][k])
                $('.police').append(tit);
                for (var m in res.Data[i][k]) {
                    // console.log(res.data[i][k][m])
                    var h = '<ul><li class="continer_li"><a>' + (+m + 1) + '. ' + res.Data[i][k][m] + '</a></li></ul>'
                    // console.log(res.data[i][k])
                    // $('.police ul').append(b);
                    $('.police').append(h);
                }
                
            }
        }
        var end_p = '<p>------结束</p>';
        $('.police').append(end_p);

        var police_a = $('.police ul').find('a');
        for (var p = 0; p < police_a.length; p++) {
            police_a.eq(p).on('click', function () {
                var detail_name = $(this).text().split(". ");
                $.cookie('detail_cookie', detail_name[1]);
                window.location.href = 'new_residence_permit.html';
            })
        }
    }
})
// 上一页按钮
// 获取浏览器的高度
var win_height = $(window).height();
var back_position = ($(window).height()) / 2;
$('.back').css("top", back_position + 'px');
// 上下滚动按钮
$('.up_down').css("top", (back_position - 35) + 'px');
// 上下滚动屏幕
function scrool_up() {
    var up_height = $(".police li").height()*10;
    if ( $('.police_index_box').scrollTop() != 0) {
        var a = $('.police_index_box').scrollTop();
        //  console.log(up_height);
        $('.police_index_box').scrollTop(a-up_height);
        // console.log(a-up_height)
    }
}
var win_top = $("body").height()
function scroll_down() {
    var up_height = $(".police li").height()*10;
    if ($('.police_index_box').scrollTop() != win_top) {
        var a = $('.police_index_box').scrollTop();
        $('.police_index_box').scrollTop(a+up_height);
    }
}
// 隐藏滚动条
$('.police_index_box').css({
    height: win_height+'px'
})