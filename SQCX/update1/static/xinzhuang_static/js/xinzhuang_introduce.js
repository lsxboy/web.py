$(function($){
    //获取页面信息
    $.ajax({
        type: "GET",
        url: gpath+"/index_data",
        dataType: "json",
        success: function (result) {
            var traffic_image = result.data.trafficImage;
            var work_time = result.data.workTime;
            var phone = result.data.phone;
            var intro = result.data.intro;
            var traffic = result.data.traffic;
            var intro_image = result.data.introImage;
            // 生成html
            $('.top1').css("background-image", "url(" + intro_image + ")");

            var intro_p = '<p class="intro_font">' + intro + '</p>';
            $('.intro_jianjie').append(intro_p);

            // var intro_p ='<p class="intro_font">'+ intro+'</p>';
            // $('.intro_jianjie').append(intro_p);

            var traffic_p ='<p class="intro_font">'+traffic+'</p>';
            $('.traffic_zt').append(traffic_p);

            $('.traffic1').css('background-image', "url(" + traffic_image + ")");

            var work = '<p class="intro_font">' + work_time+'</p>';
            $('.time').append(work);

            var phone_list = phone.split(" ");
            for (var i in phone_list) {
                var phone = '<p class="intro_font">' + phone_list[i] + '</p>';
                $('.phone').append(phone);
            }
        }
    })
    var win_height = $(window).height();
    var back_position = ($(window).height()) / 2;
    $('.back').css("top", back_position + 'px');
    // 上下滚动按钮
    $('.up_down').css("top", (back_position - 35) + 'px');
    // 上下滚动屏幕
    
    $(document).on('click', '.click_top',function(){
        if ($('.intro_content').scrollTop() != 0) {
            var a = $('.intro_content').scrollTop();
            $('.intro_content').scrollTop(a - 120)
        }
    })
    var win_top = $("body").height();
    $(document).on('click', '.click_down', function () {
        var a = $('.intro_content').scrollTop();
        $('.intro_content').scrollTop(a + 120);
    })

    // 隐藏滚动条
    $('.intro_content').css({
        height: win_height + 'px'
    })
}(jQuery))
