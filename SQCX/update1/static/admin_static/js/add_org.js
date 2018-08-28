function add_org_onload() {
    $('#org_name').focus();
}
function detail_org_onload(resource) {
    $('#add_save_org').val('保存');
    $.ajax({
        type: "GET",
        url: gpath + "/admin/organization/" + $.cookie('click_org'),
        dataType: "json",
        success: function (data) {
            var org_name = data.orgName;
            var org_id = data.orgId;
            var org_intro = data.orgIntro;
            var org_phone = data.orgPhone;
            var org_traffic = data.orgTraffic;
            var org_worktime = data.orgWorktime;
            var org_traffic_image = data.orgTraffic_image;
            var org_intro_image = data.orgIntro_image;
            var org_url = data.orgUrl
            $('#org_id').val(org_id);
            $('#org_name').val(org_name);
            $('#org_intro').val(org_intro);
            $('#org_phone').val(org_phone);
            $('#org_traffic').val(org_traffic);
            $('#org_worktime').val(org_worktime);
            $('#org_url').val(org_url);
            $('#print').val(data.enablePrint);
            $('#tb_cont_org').attr('class', "screen_have_img");
            $('#tb_img_org').attr("src", org_intro_image);
            $('#button_normal_background_org_img').attr('class', "screen_have_img");
            $('#normal_background_img_org').attr("src", org_traffic_image);
        }
    })
}
// 添加和保存
function add_save_organization() {
    var org_id = $("#org_id").val();
    var org_name = $("#org_name").val();
    var org_intro = $("#org_intro").val(); //机构简介
    var org_traffic = $("#org_traffic").val();//周边交通
    var org_worktime= $ ("#org_worktime").val(); //工作时间
    var org_phone = $("#org_phone").val();//联系电话
    var org_url = $("#org_url").val();
    var print = $('#print option:selected').val();
    var cur_user = $("#modify1").text();
    var url = gpath;
    var request_type = "";
    var commit_op = $("#add_save_org").val();
    switch (commit_op) {
        case "添加":
            if ($("#org_name").val() == '机构名称不能为空') {
                clickautohide(1, "机构名称不能为空");
                return false;
            }
            url += "/admin/organization/" + org_name;
            request_type = "POST";
            break;

        case "保存":
            url += "/admin/organization/" + org_id;
            request_type = "PUT";
            break;
    }
    $.ajax({
        type: request_type,
        url: url,
        data:{
            orgName:org_name,
            orgIntro: org_intro,
            orgTraffic: org_traffic,
            orgWorktime: org_worktime,
            orgPhone: org_phone,
            orgUrl:org_url,
            enablePrint:print
        },
        dataType: "json",
        success: function (data) {
            switch (commit_op) {
                case "添加":
                    if (data['resCode'] == 0) {
                        // console.log(data);
                        listorg();
                        $('#cur_org').empty();
                        $('#org_id').val(data["orgId"]);
                        image_upload2($("#org_id"), "tb_form2", "/admin/organization_picture_upload/");
                        image_upload2($("#org_id"), "tp_form2", "/admin/organization_picture_upload/");

                        //登录用户下所有绑定机构
                        $.ajax({
                            type: "GET",
                            url: gpath + "/admin/org_list",
                            dataType: "json",
                            success: function (data) {
                                if (data.resCode == 0) {
                                    for (var i in data.organizationList) {
                                        var org_name = data.organizationList[i].orgName;
                                        var org_id = data.organizationList[i].orgId;
                                        var current_org = "<option value= " + org_id + ">" + org_name  +"</option>";
                                        $('#cur_org').append(current_org);
                                        $.cookie('orgname', $('#cur_org option:selected').val());
                                    }
                                    get_current_organization();
                                } else {
                                    clickautohide(1, data['resMsg']);
                                }

                            }
                        });
                    } else {
                        var error = "提示: " + data['resMsg'];
                        if (data['resCode'] == 1001) {
                            document.getElementById("org_name").focus();
                        }else if (data['resCode'] == 1002){
                            document.getElementById("org_abbr").focus();
                        }
                        clickautohide(1, error);
                    }
                    break;
                case "保存":
                    if (data['resCode'] == 0) {
                        clickautohide(4, "保存机构成功！");
                        listorg();
                        $('#cur_org').empty();
                        image_upload2($("#org_id"), "tb_form2", "/admin/organization_picture_upload/");
                        image_upload2($("#org_id"), "tp_form2", "/admin/organization_picture_upload/");
                        //登录用户下所有绑定机构
                        $.ajax({
                            type: "GET",
                            url: gpath + "/admin/org_list",
                            dataType: "json",
                            success: function (data) {
                                if (data.resCode == 0) {
                                    for (var i in data.organizationList) {
                                        var org_name = data.organizationList[i].orgName;
                                        var org_id = data.organizationList[i].orgId;
                                        var current_org = "<option value= " + org_id + ">" + org_name  +"</option>";

                                        $('#cur_org').append(current_org);
                                        $.cookie('orgname', $('#cur_org option:selected').val());

                                    }
                                    get_current_organization();
                                } else {
                                    clickautohide(1, data['resMsg']);
                                }

                            }
                        });
                    } else {
                        clickautohide(1, data['resMsg']);
                    }
                    break;
            }
        }
    });
}
//add organization request function
function request_add_organization() {
    read_file('添加机构', "rightMain", "add_org.html", add_org_onload);
}
// 删除
function remove_organization(){
    org_id = $("#org_id").val();
    org_name = $("#org_name").val();
    var msg = "确认删除机构：" + org_name + " ?";
    if (confirm(msg) == true) {
        $.ajax({
            type: "DELETE",
            url: gpath + "/admin/organization/" + org_id,
            dataType: "json",
            success: function (data) {
                if (data['resCode'] == 0) {
                    listorg();
                    request_add_organization();
                    clickautohide(4, "删除机构成功！");
                    $('#cur_org').empty();
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
                                    $.cookie('orgname', $('#cur_org option:selected').val());
                                }
                                get_current_organization();
                            } else {
                                clickautohide(1, data['resMsg']);
                            }

                        }
                    });

                } else {
                    var error = "提示: " + data['resMsg'];
                    clickautohide(1, error);
                }
            }
        });
    }
}
// 重置
function reset_organization() {
    $('#org_name').val("");
    $('#org_name').focus();
    $('#org_intro').val("");
    $('#org_intro').focus();
    $('#org_traffic').val("");
    $('#org_traffic').focus();
    $('#org_worktime').val("");
    $('#org_worktime').focus();
    $('#org_phone').val("");
    $('#org_phone').focus();
    $("#org_url").val("");
    $('#normal_background_img_org').attr('src',''); //交通图
    $('#tb_img_org').attr('src', '');  //机构简介图

}
// 示例
function example_org() {
    $('#org_name').val('周浦机构');
    $('#org_intro').val('机构简介'); //简介
    $('#org_traffic').val('周边交通');
    $('#org_worktime').val('工作时间');
    $('#org_phone').val('联系电话');
    $('#org_url').val('/query_static/introduce.html');
}

//对照片的处理
// 图标 图片
var clicked_filechange2 = function (event) {
    var files = event.target.files,
        file;
    if (files && files.length > 0) {
        // 获取目前上传的文件
        file = files[0]; // 文件大小校验的动作
        if (file.size > 1024 * 1024 * 2) {
            alert('图片大小不能超过 2MB!');
            return false;
        }
        // 获取 window 的 URL 工具
        var URL = window.URL || window.webkitURL;
        // 通过 file 生成目标 url
        var imgURL = URL.createObjectURL(file);
        //用attr将img的src属性改成获得的url

        $("#tb_cont_org").attr("class", "have_img_button2");
        $("#tb_img_org").attr("src", imgURL);
        // 使用下面这句可以在内存中释放对此 url 的伺服，跑了之后那个 URL 就无效了
        // URL.revokeObjectURL(imgURL);
    }
};
var normal_filechange2 = function (event) {
    var files = event.target.files,
        file;
    if (files && files.length > 0) {
        // 获取目前上传的文件
        file = files[0]; // 文件大小校验的动作
        if (file.size > 1024 * 1024 * 2) {
            alert('图片大小不能超过 2MB!');
            return false;
        }
        // 获取 window 的 URL 工具
        var URL = window.URL || window.webkitURL;
        // 通过 file 生成目标 url
        var imgURL2 = URL.createObjectURL(file);
        //用attr将img的src属性改成获得的url

        $("#button_normal_background_org_img").attr("class", "have_img_button2");
        $("#normal_background_img_org").attr("src", imgURL2);
        // 使用下面这句可以在内存中释放对此 url 的伺服，跑了之后那个 URL 就无效了
        // URL.revokeObjectURL(imgURL);
    }
};
function button_clicked_bg_clicked2() {
    $("#button_clicked_background_org").click();
}
function button_normal_bg_clicked2() {
    $("#button_normal_background_org").click();
}
function image_upload2(org_id, image_element_id, image_upload2_url) {
    var fd = new FormData(document.getElementById(image_element_id));
    $.ajax({
        type: "PUT",
        url: gpath + image_upload2_url + $(org_id).val(),
        data: fd,
        contentType: false,
        processData: false,
        dataType: "json",
        success: function (data) {
            if (data['resCode'] == 0) {
                // clickautohide(4, "保存成功！");
            } else {
                var error = "提示: " + data['resMsg'];
                clickautohide(1, error);
            }
        },
        error: function (data, status, e) {
            clickautohide(1, e);
        }
    });
}
//check window_call_name input
//正则匹配，改变输入的值
function number_input_check(element) {
    var target_value = document.getElementById(element).value.replace(/[^0-9]+/, '');
    document.getElementById(element).value = target_value;
}
