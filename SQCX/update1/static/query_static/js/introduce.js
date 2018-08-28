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
            $.cookie('enable_print', result.data.enablePrint);
            
            // 生成html
            $('.intro_top').css("background-image", "url(" + intro_image + ")");

            var intro_p = '<p class="intro_font">' + intro + '</p>';
            $('.intro_jianjie').append(intro_p);

            var traffic_p = '<p class="intro_font">' + traffic + '</p>';
            $('.traffic_zt').append(traffic_p);

            $('.traffic_img').css('background-image', "url(" + traffic_image + ")");

            var work = '<p class="intro_font">' + work_time + '</p>';
            $('.time').append(work);

            var phone_list = phone.split(" ");
            for (var i in phone_list) {
                var phone = '<p class="intro_font">' + phone_list[i] + '</p>';
                $('.phone').append(phone);
            }
        }
    })
    // 获取图标
    $.ajax({
        type: "GET",
        url: gpath + "/query/guide_to_affairs",
        dataType: "json",
        success: function (result) {
            for (var r in result.data) {
                var category_id = result.data[r].categoryID;
                var img_id = result.data[r].id
                var category_name = result.data[r].categoryName;
                var department_a = '<li class="flex_item"><img class="icon" src=' + result.data[r].ico + '><span id= "' + category_id + '">' + category_name + '</span></li>'
                $('.last').append(department_a);
            }
            // 获取列表 */
            var all_a = $('.depart_box .flex_item');
            for (var i = 0; i < all_a.length; i++) {
                all_a.eq(i).on('click', function () {
                    var depart_name = $(this).find('span').text();
                    $.cookie('name_cookie', depart_name);
                    window.location.href = 'police_index.html';

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
    var win_top = $("body").height();
    $(document).on('click', '.scroll_up',function(){
        if ($('.intro_content').scrollTop() != 0) {
            var a = $('.intro_content').scrollTop();
            $('.intro_content').scrollTop(a - 120)
        }
    });
    $(document).on('click', '.scroll_down',function(){
        var a = $('.intro_content').scrollTop();
        $('.intro_content').scrollTop(a + 120)
    })
    // 隐藏滚动条
    $('.intro_content').css({
        height: win_height + 'px'
    })
}(jQuery))

