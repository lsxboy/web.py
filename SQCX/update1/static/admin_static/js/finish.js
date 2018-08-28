var link = $.cookie("admin_user_name");
$('#modify1').text(link);
// 点击登陆或刷新页面时加载菜单内容
// call_hover_list();
// 登录后显示机构数据汇总页面
// read_file("机构数据汇总", "rightMain", "org_data.html", org_data_onload);

//get current organization
function get_current_organization() {
    $.ajax({
        type: "GET",
        url: gpath + "/admin/current_organization/get",
        dataType: "json",
        success: function (data) {
            if (data['resCode'] == 0) {
                var cur_org = data['currentOrganization'];
                var cur_id = data['currentOrganizationId'];
                // clickautohide(4, "当前机构： " + cur_org);
                var int = setInterval(frame, 1);
                function frame() {
                    if ($('#cur_org').text() != "") {
                        clearInterval(int);
                        $('#cur_org').val(cur_id);
                        //call_hover_list();
                    }
                }
            } else {
                clickautohide(1, data['resMsg']);
            }
        }
    });
}
//登录用户下所有绑定机构
$.ajax({
    type: "GET",
    url: gpath + "/admin/org_list",
    dataType: "json",
    // data: {
    //     userName: $('#modify1').text()
    // },
    success: function (data) {
        if (data.resCode == 0) {
            for (var i in data.organizationList) {
                var org_name = data.organizationList[i].orgName;
                var org_id = data.organizationList[i].orgId;
                var current_org = "<option value= " + org_id + ">" + org_name + "</option>";
                $('#cur_org').append(current_org);
                // $.cookie('orgname', $('#cur_org option:selected').val());
            }
            get_current_organization();
        } else {
            clickautohide(1, data['resMsg']);
        }

    }
});
function call_hover_list() {
    // alert('call_hover_list')
    listorg();
}

var nav_height = $(window).height() - $('#top').height();
$('.nav').css({
    'height': nav_height,
    'overflow-x': 'hidden',
    'overflow-y': 'scroll'
})
// nav收缩展开
$(document).on('click', '.nav-item>a',function () {
    if ($(this).next().css('display') == "none") {
        // 展开 未展开
        $(this).next().addClass('zk');
        if ($(this).children('span').text() != '机构配置' && $(this).children('span').text() != '管理员配置'){
            sub_category($(this).children('span').attr('id'), $(this).next());
        }
        
        $.cookie('big_category', $(this).children('span').attr('id'))
        // alert(222)
        $('.nav-item').children('ul').slideUp(300);
        $(this).next('ul').slideDown(300);
        $(this).parent('li').addClass('nav-show').siblings('li').removeClass('nav-show');
        
        $(this).parent('li').siblings('li').find('.open').removeClass('sub-show').find('.add-menu').css('display', 'none');

        $(this).parent('li').siblings('li').find('.open').removeClass('sub-show');
        switch ($(this).children('span').text()) {
            case '机构配置':
                listorg();
                break;
            case '管理员配置':
                listuser();
                break;
        }
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
$(document).on('click','.small', function () {
    // alert('open')
    if ($(this).next().css('display') == "none") {
        // 展开 未展开
        $(this).next().addClass('thing');
        $.cookie('editor', $(this).attr('id'));
        $('.open').children('ul').slideUp(300);
        $(this).next('ul').slideDown(300);
        $(this).parent('li').addClass('sub-show').siblings('li').removeClass('sub-show');
        business_list($(this).attr('id'), $(this).next());
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
// 其他节点
function otherNode() {
    //菜单跳转 
    $('.org a').on('click', function () {
        rightMain1($(this).text());
    });
    $('.detail_org a').on('click', function () {
        // alert('点击了'+$(this).text())
        $.cookie('click_org', $(this).attr('class'))
        rightMain1($(this).text());
        
    });
    $('.add_user a').on('click', function () {
        rightMain1($(this).text());
    });
    $('.user a').on('click', function () {
        // alert('点击了'+$(this).text())
        $.cookie('click_user', $(this).attr('class'))
        rightMain1($(this).text());
        
    })
};

$(document).on('click', '.add_big>a', function () {
    // alert($(this).text());
    rightMain1($(this).text());
    $(this).parent('li').siblings('.nav-item').removeClass('nav-show').find('ul').slideUp(300).find('li').removeClass('sub-show');
});

$(document).on('click', '.editor_big>a', function () {
    // alert('点击了编辑大类');
    // rightMain1($(this).attr('class'));
    // $.cookie('editor_big', $(this).attr('class'));
    rightMain1($(this).text());
});
$(document).on('click',".editor_small a", function () {
    // alert('点击了编辑小类');
    // rightMain1($(this).attr('class'));
    rightMain1($(this).text());
});
$(document).on('click', '.add_small a',function () {
    // alert('点击了添加小类');
    // rightMain1($(this).attr('class'));
    rightMain1($(this).text());
});
$(document).on('click', '.additions a', function () {
    // alert('点击了添加事项')
    // rightMain1($(this).attr('class'));
    rightMain1($(this).text());
});

$(document).on('click', '.detail_addition a',function () {
    // alert('点击了具体事项')
    $.cookie('detail_addition', $(this).attr('id'))
    rightMain1($(this).text());
})
