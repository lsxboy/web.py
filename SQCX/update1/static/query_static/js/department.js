// department.html页面中，图标下的文字
$(function ($) {
    // 获取id 和 name
    $.ajax({
        /* headers:{
            'Cookie':$.cookie('category')
        },
        xhrFields: {
            withCredentials: true
        }, */
        // crossDomain: true,
        type: "GET",
        // url: gpath + "/query/guide_to_affairs",
        dataType: "json",
        success: function (result) {
            for (var r in result.data) {
                var category_id = result.data[r].categoryID;
                var category_name = result.data[r].categoryName;
                var department_icon = +r + 1;
                var department_a = '<li class="flex_item"><img class="icon" src=' + result.data[r].ico +'><span id= "' + category_id + '">' + category_name + '</span></li>'
                $('.last').append(department_a);
            }
            // 获取列表 */
            var all_a = $('.depart_box .flex_item');
            for (var i = 0; i < all_a.length; i++) {
                all_a.eq(i).on('click', function () {
                    var depart_name = $(this).find('span').text();
                    $.cookie('name_cookie', depart_name);
                    window.location.href = 'xinzhuang_police.html';

                })
            }
        }
    })
    var win_height = $(window).height();
    if (win_height > 768) {
        $('.depart_box').css({
            height: 600 + 'px'
        })
    } else {
        $('.depart_box').css({
            height: win_height + 'px'
        })
    }

}(jQuery))