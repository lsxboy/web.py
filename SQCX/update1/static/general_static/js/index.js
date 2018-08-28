//when #cur_org select changed, change db curent organization

$(function () {
    $.ajaxSettings.beforeSend = function(xhr,request){
        token = $.cookie("general_token");
        org_id = $.cookie('general_org_id');
        // xhr.setRequestHeader("general_org_id", org_id);
        var link = $.cookie("general_user_name");
        if (link == null || link == '') {
            window.location.href = 'login.html';
        }
    };
    $.ajaxSettings.complete = function(event,xhr,options){
        // console.log(xhr)
        response_text = JSON.parse(event['responseText']);
        if (response_text['resCode'] == 999){
            window.location.href = 'login.html';
        }
    };
    var link = $.cookie("general_user_name");
    if (link == null || link == '') {
        window.location.href = 'login.html';
    }
}());

/**退出系统**/
function logout() {
    $.ajax({
        type: "PUT",
        url:"/general/logout",
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

// 加载大类列表
$.ajax({
    type: "GET",
    url: gpath + "/general/category_list",
    dataType: "json",
    success: function (result) {
        if (result.resCode == 0) {
            for (var i in result.Data) {
                if (result.Data[i].isChange == '0'){
                    var nav_li = '<li class="nav-item"><a href = "javascript:;" class="big" id=' + result.Data[i].isChange+'><span class="fst-spn" id=' + result.Data[i].id + '>' + result.Data[i].name + '</span><i class="nav-more iconfont icon-xiangyou1"></i></a><ul class="nav-ul"><li class="open editor_big"><a href = "javascript:;" class=' + result.Data[i].id + '><span>编辑大类</span></a></li></ul></li>';
                    $('.category').append(nav_li);
                }else{
                    var nav_li = '<li class="nav-item"><a href = "javascript:;" class="big" id=' + result.Data[i].isChange +'><span class="fst-spn" id=' + result.Data[i].id + '>' + result.Data[i].name + '</span><i class="nav-more iconfont icon-xiangyou1"></i></a><ul class="nav-ul"><li class="open editor_big"><a href = "javascript:;" class=' + result.Data[i].id + '><span>编辑大类</span></a></li><li class="open add_small"><a href = "javascript:;" class=' + result.Data[i].id + 'small' + '><span>添加小类</span></a></li></ul></li>';
                    $('.category').append(nav_li);
                }
            }
        } else {
            clickautohide(1, '没有大类');
        }
    }
});

// 小类列表
function sub_change_category(sub, ul) {
    // alert('a')
    ul.find('.open_li').empty();
    $.ajax({
        type: 'GET',
        url: gpath + "/general/sub_category_list/" + sub,
        dataType: "json",
        success: function (data) {
            for (var i in data.subCategoryList) {
                var sub_li = '<li class="open open_li"><a href = "javascript:;" id = ' + data.subCategoryList[i].id + ' class="small" name="nochange"><span>' + data.subCategoryList[i].name + '</span><i class="open-more iconfont icon-xiangyou1"></i></a><ul class="add-menu" id="addOrg"></ul></li>';
                // console.log(sub_li)
                ul.append(sub_li);
            }
        }
    });
};
function sub_category(sub, ul) {
    // alert('b')
    ul.find('.open_li').empty();
    $.ajax({
        type: 'GET',
        url: gpath + "/general/sub_category_list/" + sub,
        dataType: "json",
        success: function (data) {
            for (var i in data.subCategoryList) {
                var sub_li = '<li class="open open_li"><a href = "javascript:;" id = ' + data.subCategoryList[i].id + ' class="small"><span>' + data.subCategoryList[i].name + '</span><i class="open-more iconfont icon-xiangyou1"></i></a><ul class="add-menu" id="addOrg"><li class="editor_small"><a href="javascript:;" class=' + data.subCategoryList[i].id + '><span>编辑小类</span></a></li ><li class="additions"><a href = "javascript:;" class=' + data.subCategoryList[i].id + 'bus' + '><span>添加事项</span></a></li></ul></li>';
                // console.log(sub_li)
                ul.append(sub_li);
            }
        }
    });
};
// 事项列表
function business_nochange_list(bus, ul) {
    ul.find('.detail_addition').empty();
    $.ajax({
        type: "GET",
        url: gpath + "/general/business_list/" + bus,
        dataType: "json",
        success: function (result) {
            if (result.resCode == 0) {
                for (var i in result.businessList) {
                    var bus_li = '<li class="detail_addition"><a href = "javascript:;" title = ' + result.businessList[i].name + ' id=' + result.businessList[i].id + ' name="bus_nochange"><span>' + result.businessList[i].name + '</span></a></li>'
                    ul.append(bus_li);
                }
            } else {
                clickautohide(1, '没有事项');
            }
        }
    });
}
function business_list(bus, ul) {
    ul.find('.detail_addition').empty();
    $.ajax({
        type: "GET",
        url: gpath + "/general/business_list/" + bus,
        dataType: "json",
        success: function (result) {
            if (result.resCode == 0) {
                for (var i in result.businessList) {
                    var bus_li = '<li class="detail_addition"><a href = "javascript:;" title = ' + result.businessList[i].name + ' id=' + result.businessList[i].id + '><span>' + result.businessList[i].name + '</span></a></li>'
                    ul.append(bus_li);
                }
            } else {
                clickautohide(1, '没有事项');
            }
        }
    });
}

// 用户下所有机构列表(每个用户只能绑定一个机构)
function listorg_general() {
    //登录用户下所有绑定机构
    var org_li = '<li class="open detail_org_general"><a href = "javascript:;" class = "-1"><span>暂无管理机构</span></a ></li >';
    
    $('.org_ul').empty().append(org_li);
    $.ajax({
        type: "GET",
        url: gpath + "/general/get_user_bind_org",
        dataType: "json",
        data: {
            userName: $('#modify1').text()
        },
        success: function (data) {
            if (data.resCode == 0) {
                    var org_name = data.bindOrganization[0].orgName;
                    var org_id = data.bindOrganization[0].orgId;
                    var org_li = '<li class="open detail_org_general"><a href = "javascript:;" class = ' + org_id + '><span>' + org_name + '</span></a ></li >';
                    $('.org_ul').empty().append(org_li);
                    otherNode(); 
            } else {
                clickautohide(1, '未绑定机构');
            }
            
        }
    })
}


