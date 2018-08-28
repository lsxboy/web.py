// 加载
function add_small_onload() {
    $('.small_input').val('');
    $('.small_input').focus();
    var tit = '<i class="iconfont icon-shengqian"></i>添加';
    $('.config-title h1').empty().append(tit);
    $('.s').children('span').text('添加小类：');
    $('#add_small_catagory').val('添加小类');
    // $('.small_input').attr('class',resource);
}
function editor_small_onload(resource) {
    $('.small_input').focus();
    var tit = '<i class="iconfont icon-shengqian"></i>编辑';
    $('.config-title h1').empty().append(tit);
    $('.s').children('span').text('编辑小类：');
    $('#add_small_catagory').val('保存');
    $.ajax({
        type: "GET",
        dataType: 'json',
        url: gpath + "/general/sub_category/" + $.cookie('editor'),
        success: function (result) {
            if (result.resCode == 0) {
                $('.small_input').val(result.Data.sub_category_name);
                $('.small_input').attr('id', result.Data.sub_category_id);
            } else {
                var error = "提示: " + result['resMsg'];
                clickautohide(1, error);
            }
        }
    })
}
// 添加/保存小类
function catagory_commit_s() {
    var category_id = $.cookie('big_category');
    var sub_category_id = $('.small_input').attr('id');
    var name = $('.small_input').val();
    var url = gpath;
    var request_type = "";
    var btn = $('#add_small_catagory').val();
    switch (btn) {
        case "添加小类":
            if (name == '小类名称不能为空') {
                clickautohide(1, "大类名称不能为空");
                return false;
            }
            url += '/general/sub_category/post';
            request_type = "POST";
            break;
        case "保存":
            url += '/general/sub_category/' + sub_category_id;
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
            
            if (result.resCode == 0) {
                clickautohide(4, 'success');
                sub_category($.cookie('big_category'), $('.zk'));
                // a()
            } else {
                var error = "提示: " + result['resMsg'];
                clickautohide(1, error);
            }
        }
    })
}
// 删除
function remove_small() {
    var msg = "确认删除小类：" + $('.small_input').val() + " ?";
    if (confirm(msg) == true) {
        $.ajax({
            type: "DELETE",
            dataType: 'json',
            url: gpath + "/general/sub_category/" + $('.small_input').attr('id'),
            success: function (result) {
                if (result.resCode == 0) {
                    clickautohide(4, '删除小类成功');
                    request_add_small();
                    sub_category($.cookie('big_category'), $('.zk'));
                } else {
                    var error = "提示: " + result['resMsg'];
                    clickautohide(1, error);
                }
            }
        })
    }
}
function request_add_small() {
    add_small_onload();
}
// 重置
function reset_small() {
    $('.small_input').focus();
    $('.small_input').val('');
}
// 示例
function example_small() {
    $('.small_input').val('居住证');
}