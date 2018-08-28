$.ajax({
    type: "GET",
    url: gpath + "/detail/" + $.cookie('detail_cookie'),
    dataType: "json",
    success: function (suc) {
        // for (var s in suc.Data) {
        var li_one = '<li class="new_permit_li one"><h3>' + suc.Data.Name + '</h3></li>';
        $('.new_permit').append(li_one);
        var li_two = '<li class="new_permit_li two"><span class="com_department"> 主管部门</span><span class="bureau">' + suc.Data.DeptName + '</span></li >';
        $('.new_permit').append(li_two);
        // var li_three = '<li class="new_permit_li three"><h5> 办理依据</h5><p>' + suc.Data.PolicyRef + '</p></li >';

        if (suc.Data.PolicyRef.indexOf('\n') == -1) {
            var li_three = '<li class="new_permit_li three"><h5> 办理依据</h5><p>' + suc.Data.PolicyRef + '</p></li >';
            $('.new_permit').append(li_three);
        } else {
            var li_three = '<li class="new_permit_li three"><h5> 办理依据</h5></li >';
            $('.new_permit').append(li_three);
            var arry_yj = suc.Data.PolicyRef.split('\n');
            for (var a in arry_yj) {
                var po_li = '<p>' + arry_yj[a] + '</p>';
                $('.three').append(po_li)
            }
        }

        if (suc.Data.AppCondition.indexOf('\n') == -1) {
            var li_four = '<li class="new_permit_li four"><h5> 申办条件</h5><p>' + suc.Data.AppCondition + '</p></li >';
            $('.new_permit').append(li_four);
        } else {
            var li_four = '<li class="new_permit_li four"><h5> 申办条件</h5></li >';
            $('.new_permit').append(li_four);
            var arry_tj = suc.Data.AppCondition.split('\n');
            for (var b in arry_tj) {
                var ap_li = '<p>' + arry_tj[b] + '</p>';
                $('.four').append(ap_li);
            }
        }
        if (suc.Data.AppMaterial.indexOf('\n') == -1) {
            var li_five = '<li class="new_permit_li five"><h5> 申请材料</h5><p>' + suc.Data.AppMaterial + '</p></li >';
            $('.new_permit').append(li_five);
        } else {
            var li_five = '<li class="new_permit_li five"><h5> 申请材料</h5></li >';
            $('.new_permit').append(li_five);
            var arry_cl = suc.Data.AppMaterial.split('\n');
            for (var c in arry_cl) {
                var cl_li = '<p>' + arry_cl[c] + '</p>';
                $('.five').append(cl_li)
            }
        }
        if (suc.Data.OperationProcess.indexOf('\n') == -1) {
            var li_six = '<li class="new_permit_li six"><h5> 办理程序</h5><p>' + suc.Data.OperationProcess + '</p></li >';
            $('.new_permit').append(li_six);
        } else {
            var li_six = '<li class="new_permit_li six"><h5> 办理程序</h5></li >';
            $('.new_permit').append(li_six);
            var arry_cx = suc.Data.OperationProcess.split('\n');
            for (var d in arry_cx) {
                var cx_li = '<p>' + arry_cx[d] + '</p>';
                $('.six').append(cx_li)
            }
        }
        var li_seven = '<li class="new_permit_li seven"><h5> 收费标准</h5><p>' + suc.Data.ChargeDesc + '</p></li >';
        $('.new_permit').append(li_seven);
        var li_eight = '<li class="new_permit_li eight">温馨提示：为更好地向居民提供社区政务服务，社区事务受理服务中心实行“刷证办事”，请您办理事项时务必带好有效居民身份证原件或社保卡、居住证、医保卡原件，谢谢配合！</li>';
        $('.new_permit').append(li_eight);
        var btn = '<div class="btn"><a href = "javascript:;"> 打印</a></div>';
        $('.new_box').append(btn);
        // 点击打印按钮 打印本页面
        $(".btn a").click(function () {
            if (!$('.btn a').hasClass('printing')) {
                $('.btn a').addClass('printing');
                $('.btn a').text('打印中...');
                $(".print_con").printArea();
                setTimeout(function () { 
                    $('.btn a').removeClass('printing') ;
                    $('.btn a').text('打印');
                }, 2000);
            }    
        });
    }
});
// 上一页按钮
// 获取浏览器的高度
var win_height = $(window).height();
var back_position = ($(window).height()) / 2;
$('.back').css("top", back_position + 'px');
// 上下滚动按钮
$('.up_down').css("top", (back_position - 35) + 'px');
// 上下滚动屏幕
function scrool_up() {
    if ($('.new_box').scrollTop() != 0) {
        // console.log(up_height);
        var a = $('.new_box').scrollTop();
        $('.new_box').scrollTop(a-120)
        // $('.new_box').scrollTop('0')
    }

}
var win_top = $("body").height()
function scroll_down() {
    if ($('.new_box').scrollTop() != win_top) {
        var a = $('.new_box').scrollTop();
        $('.new_box').scrollTop(a+120)
    }
}
// 隐藏滚动条

$('.new_box').css({
    height: win_height + 'px'
})
