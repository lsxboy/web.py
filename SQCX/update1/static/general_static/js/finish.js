var link = $.cookie("general_user_name");
$('#modify1').text(link);
$('#jg_id').text($.cookie('general_org_id'));
// 登录后显示机构数据汇总页面
// read_file("机构数据汇总", "rightMain", "org_data.html", org_data_onload);

var nav_height = $(window).height() - $('#top').height();
$('.nav').css({
    'height': nav_height,
    'overflow-x': 'hidden',
    'overflow-y': 'scroll'
})
// nav收缩展开
$(document).on('click', '.nav-item>a', a = function () {
    if ($(this).next().css('display') == "none") {
        // 展开 未展开
        $(this).next().addClass('zk');
        if ($(this).attr('id') == '0' && $(this).children('span').text() != '机构配置'){
            sub_change_category($(this).children('span').attr('id'), $(this).next());
        } else if ($(this).children('span').text() != '机构配置'){
            sub_category($(this).children('span').attr('id'), $(this).next());
        }
        switch ($(this).children('span').text()) {
            case '机构配置':
                listorg_general();
                break;
        }
        $.cookie('big_category', $(this).children('span').attr('id'));
       
        $('.nav-item').children('ul').slideUp(300);
        $(this).next('ul').slideDown(300);
        $(this).parent('li').addClass('nav-show').siblings('li').removeClass('nav-show');

        $(this).parent('li').siblings('li').find('.open').removeClass('sub-show').find('.add-menu').css('display', 'none');

        $(this).parent('li').siblings('li').find('.open').removeClass('sub-show');
        var nav_height = $(window).height() - $('#top').height();
        $('.nav').css({
            'height': nav_height,
            'overflow-x': 'hidden',
            'overflow-y': 'scroll'
        })
        // alert($('.nav').height())
    } else {
        // 收缩 已展开
        // alert('收起')
        $(this).next().removeClass('zk')
        $(this).next('ul').slideUp(300);
        $('.nav-item.nav-show').removeClass('nav-show');
        $(this).next().children('li').removeClass('sub-show').find('.add-menu').css('display', 'none');
        var nav_height = $(window).height() - $('#top').height();
        $('.nav').css({
            'height': nav_height,
            'overflow-x': 'hidden',
            'overflow-y': 'scroll'
        })
    }
});

//add-menu 收缩展开
$(document).on('click', '.small', function () {
    // alert('open')
    if ($(this).next().css('display') == "none") {
        // 展开 未展开
        $(this).next().addClass('thing');
        $.cookie('editor', $(this).attr('id'));
        $('.open').children('ul').slideUp(300);
        $(this).next('ul').slideDown(300);
        $(this).parent('li').addClass('sub-show').siblings('li').removeClass('sub-show');
        if ($(this).attr('name') == 'nochange'){
            business_nochange_list($(this).attr('id'), $(this).next());
        }else{
            business_list($(this).attr('id'), $(this).next());
        };
        var nav_height = $(window).height() - $('#top').height();
        $('.nav').css({
            'height': nav_height,
            'overflow-x': 'hidden',
            'overflow-y': 'scroll'
        });

    } else {
        // 收缩 已展开
        $(this).next().removeClass('thing');
        $(this).next('ul').slideUp(300);
        $(this).parent('li').siblings('li').find('ul').slideUp(300);
        $('.open.sub-show').removeClass('sub-show');
        $(this).next('ul').children('li').not(":eq(0)").empty();
        var nav_height = $(window).height() - $('#top').height();
        $('.nav').css({
            'height': nav_height,
            'overflow-x': 'hidden',
            'overflow-y': 'scroll'
        });
    }
})

$(document).on('click', '.add_big>a', function () {
    // alert($(this).text());
    rightMain1($(this).text());
    $(this).parent('li').siblings('.nav-item').removeClass('nav-show').find('ul').slideUp(300).find('li').removeClass('sub-show');
});

$(document).on('click', '.editor_big>a', function () {
    // alert('点击了编辑大类');
    rightMain1($(this).text());
   
});
$(document).on('click', ".editor_small a", function () {
    // alert('点击了编辑小类');
    rightMain1($(this).text());
});
$(document).on('click', '.add_small a', function () {
    // alert('点击了添加小类');
    rightMain1($(this).text());
});
$(document).on('click', '.additions a', function () {
    // alert('点击了添加事项')
    rightMain1($(this).text());
});

$(document).on('click', '.detail_addition a', function () {
    // alert('点击了具体事项')
    $.cookie('detail_addition2', $(this).attr('id'))
    rightMain1($(this).text());
});


//登录用户下所有绑定机构
/* $.ajax({
    type: "GET",
    url: gpath + "/general/get_user_bind_org",
    dataType: "json",
    data:{
        userName: $('#modify1').text()
    },
    success: function (data) {
        if (data.resCode == 0) {
                var org_name = data.bindOrganization[0].orgName;
                var org_id = data.bindOrganization[0].orgId;
                var org_li = '<li class="open detail_org_general"><a href = "javascript:;" class = ' + org_id + '><span>' + org_name + '</span></a ></li >';
                $('.org_ul').empty().append(org_li);
                    otherNode();
                listorg_general()
        } else {
            clickautohide(1, data['resMsg']);
        }
    }
}); */
//跳转
// 其他节点
function otherNode() {
    //菜单跳转
    $('.detail_org_general a').on('click', function () {
        $.cookie('detail_org_general', $(this).attr('class'))
        rightMain1($(this).text());

    });
};
