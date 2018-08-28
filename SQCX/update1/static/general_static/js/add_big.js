// add_big init
function add_big_onload(resource){
    $(".tb_name_input").focus();
}
function editor_big_onload(resource) {
    $(".tb_name_input").focus();
    var tit = '<i class="iconfont icon-shengqian"></i>编辑';
    $('.config-title h1').empty().append(tit);
    $('#add_catagory').val('保存');
    $.ajax({
        type: "GET",
        dataType: 'json',
        url: gpath + '/general/category/' + $.cookie('big_category'),
        success: function (result) {
            if (result.resCode == 0) {
                $('#tb_id').val(result.Data.categoryId);
                $('.tb_name_input').val(result.Data.name);
                $('#xt_id').val(result.Data.id);
                if (result.Data.isChange == 0) {
                    $('.editor_btn').empty();
                }
                $('#tb_cont').attr('class', "screen_have_img");
                $('#tb_img').attr("src", result.Data.ico);
                $('#button_normal_background_img').attr('class', "screen_have_img");
                $('#normal_background_img').attr("src", result.Data.photo);
            }
        }
    })
}
// 重置
function reset_big(){
    $(".tb_name_input").focus();
    $('.tb_name_input').val('');
    $('#tb_id').val('');
}
// 示例
function example_big(){
    $('.tb_name_input').val('公安');
    $('#tb_id').val('1');
}
// add_big init
function add_big_onload(resource) {
    $(".tb_name_input").focus();
}

function big_list() {
    $.ajax({
        type: "GET",
        url: gpath + "/general/category_list",
        dataType: "json",
        success: function (result) {
            if (result.resCode == 0) {
                for (var i in result.Data) {
                    var nav_li = '<li class="nav-item"><a href = "javascript:;" class="big"><span class="fst-spn" id=' + result.Data[i].id + '>' + result.Data[i].name + '</span><i class="nav-more iconfont icon-xiangyou1"></i></a><ul class="nav-ul"><li class="open editor_big"><a href = "javascript:;" class=' + result.Data[i].id + '><span>编辑大类</span></a></li><li class="open add_small"><a href = "javascript:;" class=' + result.Data[i].id + 'small' + '><span>添加小类</span></a></li></ul></li>';
                    // console.log(nav_li)
                    $('.category').append(nav_li);
                }

            } else {
                clickautohide(1, '没有大类');
            }
        }
    });
}
// 添加和保存
function catagory_commit() {
    var category_id = $('#tb_id').val();
    var name = $('.tb_name_input').val();
    var id = $('#xt_id').val();
    var url = gpath;
    var request_type = "";
    var btn = $('#add_catagory').val();
    switch (btn) {
        case "添加大类":
            if (name == '大类名称不能为空') {
                clickautohide(1, "大类名称不能为空");
                return false;
            }
            url += '/general/category/post';
            request_type = "POST";
            break;
        case "保存":
            url += '/general/category/' + id;
            request_type = "PUT";
    }
    $.ajax({
        type: request_type,
        dataType: 'json',
        url: url,
        data: {
            categoryId: category_id,
            name: name
        },
        success: function (result) {
            /* switch (btn) {
                case "添加大类":
                    if (result.resCode == 0) {
                        clickautohide(4, 'success');
                        $('.category').empty();
                        big_list();
                    }
                    break;
                case "保存":
                    
            } */
            if (result.resCode == 0) {
                clickautohide(4, 'success');
                $('.category').empty();
                big_list();
                $('#xt_id').val(result.id);
                image_upload($("#xt_id"), "tb_form", "/general/category_picture_upload/");
                image_upload($("#xt_id"), "tp_form", "/general/category_picture_upload/");
            } else {
                var error = "提示: " + result['resMsg'];
                clickautohide(1, error);
            }
        }
    })
}
// 删除
function remove_catagory() {
    var msg = "确认删除大类：" + $('.tb_name_input').val() + " ?";
    if (confirm(msg) == true) {
        $.ajax({
            type: "DELETE",
            dataType: 'json',
            url: gpath + "/general/category/" + $('#xt_id').val(),
            success: function (result) {
                if (result.resCode == 0) {
                    clickautohide(4, '删除大类成功');
                    request_add_big();
                    $('.category').empty();
                    big_list();
                } else {
                    var error = "提示: " + result['resMsg'];
                    clickautohide(1, error);
                }
            }
        })
    }
}
function request_add_big() {
    read_file('添加大类', "rightMain", "add_big.html", add_big_onload);
}
// 重置
function reset_big() {
    $(".tb_name_input").focus();
    $('.tb_name_input').val('');
    $('#tb_id').val('');
}
// 示例
function example_big() {
    $('.tb_name_input').val('公安');
    $('#tb_id').val('1');
}
// 图标 图片
var clicked_filechange = function (event) {
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

        $("#tb_cont").attr("class", "have_img_button");
        $("#tb_img").attr("src", imgURL);
        // 使用下面这句可以在内存中释放对此 url 的伺服，跑了之后那个 URL 就无效了
        // URL.revokeObjectURL(imgURL);
    }
};
var normal_filechange = function (event) {
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

        $("#button_normal_background_img").attr("class", "have_img_button");
        $("#normal_background_img").attr("src", imgURL);
        // 使用下面这句可以在内存中释放对此 url 的伺服，跑了之后那个 URL 就无效了
        // URL.revokeObjectURL(imgURL);
    }
};
function button_clicked_bg_clicked() {
    $("#button_clicked_background").click();
}
function button_normal_bg_clicked() {
    $("#button_normal_background").click();
}
function image_upload(xt_id, image_element_id, image_upload_url) {
    var fd = new FormData(document.getElementById(image_element_id));
    // for (var i = 0; i < image_element_id.length; i++) {
    // 		file = document.getElementById(image_element_id[i]);
    // 		fd.append('file[]',file)
    // 	}
    $.ajax({
        type: "PUT",
        url: gpath + image_upload_url + $(xt_id).val(),
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

