
function cur_org_change(element_tag) {
    $.ajax({
        type: "PUT",
        url: gpath + "/admin/current_organization/" + $(element_tag).val(),
        dataType: "json",
        success: function (data) {
            if (data['resCode'] == 0) {
                clickautohide(4, "当前机构：" + $("#cur_org option:selected").text());
                listorg();
                listuser();
                $.ajax({
                    type: "GET",
                    url: gpath + "/admin/category_list",
                    dataType: "json",
                    success: function (result) {
                        $('.category').empty();
                        if (result.resCode == 0) {
                            for (var i in result.Data) {
                                var nav_li = '<li class="nav-item"><a href = "javascript:;" class="big"><span class="fst-spn" id=' + result.Data[i].id + '>' + result.Data[i].name + '</span><i class="nav-more iconfont icon-xiangyou1"></i></a><ul class="nav-ul"><li class="open editor_big"><a href = "javascript:;" class=' + result.Data[i].id + '><span>编辑大类</span></a></li><li class="open add_small"><a href = "javascript:;" class='+result.Data[i].id+'small'+'><span>添加小类</span></a></li></ul></li>';
                                // console.log(nav_li)
                                $('.category').append(nav_li);
                            }

                        } else {
                            clickautohide(1, '没有大类');
                        }
                    }
                });
            } else {
                clickautohide(1, data['resMsg']);
            }
        }
    });
}
$(function () {
    $.ajaxSettings.beforeSend = function(xhr,request){
        token = $.cookie("admin_token");
        org_id = $.cookie('admin_org_id');
        xhr.setRequestHeader("admin_org_id", org_id);
        var link = $.cookie("admin_user_name");
        if (link == null || link == '') {
            window.location.href = 'login.html';
        }
    // 在这里加上你的 token
    };
    $.ajaxSettings.complete = function(event,xhr,options){
        response_text = JSON.parse(event['responseText']);
        if (response_text['resCode'] == 999){
            window.location.href = 'login.html';
        }
    };
    var link = $.cookie("admin_user_name");
    if (link == null || link == '') {
        window.location.href = 'login.html';
    }
}());

/**退出系统**/
function logout() {
    $.ajax({
        type: "PUT",
        url:"/admin/logout",
        dataType: "json",
        success: function (data) {
            if (data.resCode == 0) {
                window.location.href = "login.html";
            } else {
                console.log(data.resMsg);
            }

        }
    });
}
/* *获得当前日期* */
function getDate01() {
    var time = new Date();
    var myYear = time.getFullYear();
    var myMonth = time.getMonth() + 1;
    var myDay = time.getDate();
    if (myMonth < 10) {
        myMonth = "0" + myMonth;
    }
    document.getElementById("today_day").innerHTML = myYear + "." + myMonth + "." + myDay;
}
// 用户下所有机构列表
function listorg() {
    //登录用户下所有绑定机构
    var org_li = '<li class="open org"><a href = "javascript:;"><span>添加机构</span></a></li >';
    $('.org_ul').empty().append(org_li);
    // if ($('.nav').hasClass('nav-mini')) {
    //     hover_node_first();
    // } else {
    //     otherNode();
    // }
    otherNode();
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
                    org_li += '<li class="open detail_org"><a href = "javascript:;" class = ' + org_id + '><span>' + org_name + '</span></a ></li >';
                }
                // console.log(123)
                $('.org_ul').empty().append(org_li);
                otherNode();
                // if ($('.nav').hasClass('nav-mini')) {
                //     hover_node_first();
                // } else {
                //     otherNode();
                // }
            } else {
                clickautohide(1, '未绑定机构');
            }
        }
    })
}

// 用户下的管理员
function listuser() {
    //登录用户下所有绑定机构
    var user_li = '<li class="open add_user"><a href = "javascript:;" id="0"><span>添加管理员</span></a></li >';
    $('.user_ul').empty().append(user_li);
    otherNode();
    // if ($('.nav').hasClass('nav-mini')) {
    //     hover_node_first();
    // } else {
    //     otherNode();
    // }
    $.ajax({
        type: "GET",
        url: gpath + "/admin/user_list",
        dataType: "json",
        // data: {
        //     userName: $('#modify1').text()
        // },
        success: function (data) {
            if (data.resCode == 0) {
                for (var i in data.userList) {
                    var username = data.userList[i].username;
                    var user_id = data.userList[i].userId;
                    user_li += '<li class="open user"><a href = "javascript:;" class = ' + user_id + '><span>' + username + '</span></a ></li >';
                }
                // console.log(123)
                $('.user_ul').empty().append(user_li);
                otherNode();
                // if ($('.nav').hasClass('nav-mini')) {
                //     hover_node_first();
                // } else {
                //     otherNode();
                // }
            } else {
                clickautohide(1, '无用户');
            }
        }
    });
}
// 加载大类列表
$.ajax({
    type: "GET",
    url: gpath + "/admin/category_list",
    dataType: "json",
    success: function (result) {
        if (result.resCode == 0) {
            for (var i in result.Data) {
                var nav_li = '<li class="nav-item"><a href = "javascript:;" class="big"><span class="fst-spn" id=' + result.Data[i].id + '>' + result.Data[i].name + '</span><i class="nav-more iconfont icon-xiangyou1"></i></a><ul class="nav-ul"><li class="open editor_big"><a href = "javascript:;" class=' + result.Data[i].id + '><span>编辑大类</span></a></li><li class="open add_small"><a href = "javascript:;" class='+result.Data[i].id+'small'+'><span>添加小类</span></a></li></ul></li>';
                // console.log(nav_li)
                $('.category').append(nav_li);
            }

        } else {
            clickautohide(1, '没有大类');
        }
    }
});

// 小类列表
function sub_category(sub,ul){
    ul.find('.open_li').empty();
    $.ajax({
        type: 'GET',
        url: gpath + "/admin/sub_category_list/" + sub,
        dataType:"json",
        success: function(data){
            for (var i in data.subCategoryList){
                var sub_li = '<li class="open open_li"><a href = "javascript:;" id = ' + data.subCategoryList[i].id + ' class="small"><span>' + data.subCategoryList[i].name + '</span><i class="open-more iconfont icon-xiangyou1"></i></a><ul class="add-menu" id="addOrg"><li class="editor_small"><a href="javascript:;" class=' + data.subCategoryList[i].id + '><span>编辑小类</span></a></li ><li class="additions"><a href = "javascript:;" class=' + data.subCategoryList[i].id +'bus'+'><span>添加事项</span></a></li></ul></li>';
                // console.log(sub_li)
                ul.append(sub_li);
            }   
        }
    })
};
// 事项列表
function business_list(bus,ul){
    ul.find('.detail_addition').empty();
    $.ajax({
    type: "GET",
        url: gpath + "/admin/business_list/" + bus,
    dataType: "json",
    success: function (result) {
        if (result.resCode == 0) {
            for (var i in result.businessList) {
                var bus_li = '<li class="detail_addition"><a href = "javascript:;" title = ' + result.businessList[i].name + ' id=' + result.businessList[i].id + '><span>' + result.businessList[i].name +'</span></a></li>'
                ul.append(bus_li);
            }
        } else {
            clickautohide(1, '没有事项');
        }
    }
});
}

// 刷新系统
function reload_systom(){
    $.ajax({
        type: "GET",
        url: gpath + "/admin/init",
        dataType: "json",
        success: function (data, textStatus, XMLHttpRequest) {
        }
    });
}

