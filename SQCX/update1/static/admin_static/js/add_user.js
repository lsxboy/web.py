function add_user_onload(resource){
    $('#sys_user_name').focus();
    all_org_list();
}
function change_all_checkbox_input_status(chkname, status) {
    var chk = document.getElementsByName(chkname);
    for (var i = 0; i < chk.length; i++) {
        chk[i].checked = status;
    }
}
// 全选
function select_all_bind_org() {
    var select_all_tag_status = document.getElementById("select_all_bind_org_number");
    if (select_all_tag_status.checked == true) {
        change_all_checkbox_input_status("bind_org_number", true);
    } else {
        change_all_checkbox_input_status("bind_org_number", false);
    }
}
// selected and not select input
function get_bind_org_number_json(chkname) {
    var obj = {};
    var chk = document.getElementsByName(chkname);
    for (var i = 0; i < chk.length; i++) {
        obj[chk[i].value] = chk[i].checked;
    }
    return JSON.stringify(obj);
}
// 所有机构
function all_org_list() {
    //get current organization  list
    $.ajax({
        type: "GET",
        url: gpath + "/admin/org_list",
        dataType: "json",
        success: function (data) {
            for (var o in data.organizationList) {
                var org_name = data.organizationList[o].orgName;
                var org_id = data.organizationList[o].orgId;
                var input_temp = "<label class='lable-class2'>" + "<input type='checkbox' name='bind_org_number' id='bind_org_number" + org_id + "' value='" + org_id + "' />" + ' ' + org_name + "</label>";
                $("#bind_org").append(input_temp);
                if ((parseInt(o) + 1) % 10 == 0) {
                    $("#bind_org").append("<br />");
                }
            }
            var input_temp = "<label class='lable-class2'>" + "<input type='checkbox' onclick='select_all_bind_org()' name='select_all_bind_org_number' id='select_all_bind_org_number' /> 全选</label>";
            $("#bind_org").append(input_temp);
            // 如果每个窗口都选中，全选按钮也选中。有一个窗口没选中，全选按钮就不选中
            $("#bind_org input[name!=select_all_bind_org_number]").each(function () {
                $(this).click(function () {
                    // console.log($(this), $(this).is(':checked'));
                    if ($(this).is(':checked')) {
                        if ($("#bind_org input[name=bind_org_number]").length == $("#bind_org input[name=bind_org_number]:checked").length) {
                            if (!$("#select_all_bind_org_number").is(':checked')) {
                                $("#select_all_bind_org_number").prop('checked', true);
                                // console.log(2)
                            }
                        } else {
                            $("#bind_org input[name=select_all_bind_org_number]").prop("checked", false);
                            // console.log(3)
                        }
                    } else {
                        $("#bind_org input[name=select_all_bind_org_number]").prop("checked", null);
                        // console.log(5)
                    }
                });
            });
        }
    });
}
// 用户绑定的机构
function bind_org_list(bind_organization) {
    $.ajax({
        type: "GET",
        url: gpath + "/admin/org_list",
        dataType: "json",
        success: function (data) {
            for (var o in data.organizationList) {
                var org_name = data.organizationList[o].orgName;
                var org_id = data.organizationList[o].orgId;
                if (bind_organization.length != 0) {
                    for (var i in bind_organization) {
                        var input_temp = "";
                        if (org_name == bind_organization[i].orgName) {
                            input_temp = "<label class='lable-class2'>" + "<input type='checkbox' name='bind_org_number' id='bind_org_number" + org_id + "' value='" + org_id + "' checked='checked' />" + ' ' + org_name + "</label>";
                            break;
                        } if (org_name != bind_organization[i].orgName) {
                            input_temp = "<label class='lable-class2'>" + "<input type='checkbox' name='bind_org_number' id='bind_org_number" + org_id + "' value='" + org_id + "' />" + ' ' + org_name + "</label>";
                        }
                    }
                } else {
                    input_temp = "<label class='lable-class2'>" + "<input type='checkbox' name='bind_org_number' id='bind_org_number" + org_id + "' value='" + org_id + "' />" + ' ' + org_name + "</label>";
                }
                $("#bind_org").append(input_temp);
                if ((parseInt(o) + 1) % 10 == 0) {
                    $("#bind_org").append("<br />");
                    // break;
                }
            }
            var input_temp = "<label class='lable-class2'>" + "<input type='checkbox' onclick='select_all_bind_org()' name='select_all_bind_org_number' id='select_all_bind_org_number' /> 全选</label>";
            $("#bind_org").append(input_temp);
            // 如果每个窗口都选中，全选按钮也选中。有一个窗口没选中，全选按钮就不选中
            if ($("#bind_org input[name=bind_org_number]").length == $("#bind_org input[name=bind_org_number]:checked").length) {
                if (!$("#select_all_bind_org_number").is(':checked')) {
                    $("#select_all_bind_org_number").prop('checked', true);
                    // console.log(2)
                }
            } else {
                $("#bind_org input[name=select_all_bind_org_number]").prop("checked", false);
                // console.log(3)
            }
            $("#bind_org input[name!=select_all_bind_org_number]").each(function () {
                $(this).click(function () {
                    // console.log($(this), $(this).is(':checked'));
                    if ($(this).is(':checked')) {
                        if ($("#bind_org input[name=bind_org_number]").length == $("#bind_org input[name=bind_org_number]:checked").length) {
                            if (!$("#select_all_bind_org_number").is(':checked')) {
                                $("#select_all_bind_org_number").prop('checked', true);
                                // console.log(2)
                            }
                        } else {
                            $("#bind_org input[name=select_all_bind_org_number]").prop("checked", false);
                            // console.log(3)
                        }
                    } else {
                        $("#bind_org input[name=select_all_bind_org_number]").prop("checked", null);
                        // console.log(5)
                    }
                });
            });
        }
    });
}
// 添加和保存
function addSaveUser(){
    // 判断用户是否选择机构
    var chk = document.getElementsByName("bind_org_number");
    for (var i = 0; i < chk.length; i++) {
        var o = chk[i].checked;
        if (o == true) {
            var commit_button_value = $("#add_save_user").val();
            // alert(commit_button_value)
            switch (commit_button_value) {
                case "添加":
                    add_save_user();
                    break;
                case "保存":
                    save_user();
                    break;
            }
            break;
        }
    }
    if (o == false) {
        alert('绑定机构不能为空');
    }
}
// 添加
function add_save_user() {
    $.ajax({
        type: "POST",
        url: gpath + "/admin/user/post",
        dataType: "json",
        data: {
            username: $("#sys_user_name").val(),
            password: $("#sys_user_password").val(),
            // phone: $('#sys_user_phone').val(),
            bindOrganization: get_bind_org_number_json("bind_org_number")
        },
        success: function (data) {
            if (data.resCode == 0) {
                listuser();
                clickautohide(4, "添加成功！");
            } else {
                var error = "提示：" + data['resMsg'];
                clickautohide(1, error);
            }
        }
    })
}
// 保存
function save_user() {
    $.ajax({
        type: "PUT",
        url: gpath + "/admin/user/" + $('#sys_user_name').attr('name'),
        dataType: "json",
        data: {
            username: $("#sys_user_name").val(),
            password: $("#sys_user_password").val(),
            // phone: $('#sys_user_phone').val(),
            bindOrganization: get_bind_org_number_json("bind_org_number")
        },
        success: function (data) {
            if (data.resCode == 0) {
                listuser();
                clickautohide(4, "保存成功！");
                // if ($("#sys_user_name").val() == $("#modify1").text()) {
                //     $('#cur_org').empty();
                //     //登录用户下所有绑定机构
                //     $.ajax({
                //         type: "GET",
                //         url: gpath + "/get_user_bind_org",
                //         dataType: "json",
                //         data: {
                //             userName: $('#modify1').text()
                //         },
                //         success: function (data) {
                //             if (data.resCode == 0) {
                //                 for (var i in data.bindOrganization) {
                //                     var org_name = data.bindOrganization[i].orgName;
                //                     var org_id = data.bindOrganization[i].orgId;
                //                     var currentOrg = "<option value= " + org_id + ">" + org_name + "</option>";
                //                     $('#cur_org').append(currentOrg);
                //                 }
                //                 var cur_org = $("#cur_org option:selected").text();
                //                 $.ajax({
                //                     type: "PUT",
                //                     url: gpath + "/current_organization/" + cur_org,
                //                     dataType: "json",
                //                     success: function (data) {
                //                         if (data['resCode'] == 0) {
                //                             clickautohide(4, "当前机构： " + cur_org);
                //                         } else {
                //                             clickautohide(1, data['resMsg']);
                //                         }
                //                     }
                //                 })
                //             } else {
                //                 console.log(data.resMsg);
                //             }
                //         }
                //     });
                // }
            } else {
                var error = "提示：" + data['resMsg'];
                clickautohide(1, error);
            }
        }
    })
}
//删除
function remove_user() {
    var msg = "确认删除用户：" + $("#sys_user_name").val() + " ?";
    if (confirm(msg) == true) {
        $.ajax({
            type: "DELETE",
            url: gpath + "/admin/user/"+$('#sys_user_name').attr('name'),
            dataType: "json",
            success: function (data) {
                if (data['resCode'] == 0) {
                    listuser();
                    clickautohide(4, "删除用户成功！");
                    request_add_manager();
                } else {
                    var error = "提示: " + data['resMsg'];
                    clickautohide(1, error);
                }
            }
        });
    }
}
function request_add_manager() {
    read_file('添加管理员', "rightMain", "add_user.html", add_user_onload);
}
// 重置
function reset_user(){
    $('#sys_user_name').val("");
    $('#sys_user_password').val("");
    $('#sys_user_name').focus();
    change_all_checkbox_input_status("bind_org_number", false)
    if ($("#bind_org input[name=bind_org_number]").length == $("#bind_org input[name=bind_org_number]:checked").length) {
        if (!$("#select_all_bind_org_number").is(':checked')) {
            $("#select_all_bind_org_number").prop('checked', true);
        }
    } else {
        $("#bind_org input[name=select_all_bind_org_number]").prop("checked", false);
    }
}
// 示例
function user_example() {
    $('#sys_user_name').val("张三");
    change_all_checkbox_input_status('bind_org_number', true);
    if ($("#bind_org input[name=bind_org_number]").length == $("#bind_org input[name=bind_org_number]:checked").length) {
        if (!$("#select_all_bind_org_number").is(':checked')) {
            $("#select_all_bind_org_number").prop('checked', true);
        }
    } else {
        $("#bind_org input[name=select_all_bind_org_number]").prop("checked", false);
    }
    // $('#sys_user_password').val("123");
}
function user_onload(resource){

    $('#sys_user_name').focus();
    $('#add_save_user').val('保存');
    $.ajax({
        type: "GET",
        url: gpath + "/admin/user/"+$.cookie('click_user'),
        dataType: "json",
        success: function (data) {
            if (data.resCode == 0) {
                $('#sys_user_name').val(data.username);
                $('#sys_user_name').attr('name',$.cookie('click_user'));
                $('#sys_user_password').val(data.password);
                // $('#sys_user_phone').val(data.phone);
                // $('#add_save_user').val('保存');
                bind_org_list(data.bindOrganization)
            } else {
                var error = "提示：" + data.resMsg;
                clickautohide(1, error);
            }
        }

    })
}