function additions_onload(){
    $('.one').children('input').focus();
    $('.sx input').val('');
    $('.one input').val('');
    $('.two input').val('');
    $('.three textarea').val('');
    $('.four textarea').val('');
    $('.five textarea').val('');
    $('.six textarea').val('');
    $('.seven textarea').val('');
}
function detail_addition_onload(resource) {
    var tit = '<i class="iconfont icon-shengqian"></i>事项';
    $('.config-title h1').empty().append(tit);
    $('#add_addition').val('保存事项');
    $.ajax({
        type: "GET",
        dataType: 'json',
        url: gpath + "/admin/business/" + $.cookie('detail_addition'),
        success: function (result) {
            if (result.resCode == 0) {
                $('.one input').attr('id', $.cookie('detail_addition'));
                $('.one input').val(result.businessData.name);
                $('.sx input').val(result.businessData.businessId);
                $('.two input').val(result.businessData.deptName);
                $('.three textarea').val(result.businessData.policyRef);
                $('.four textarea').val(result.businessData.appCondition);
                $('.five textarea').val(result.businessData.appMaterial);
                $('.six textarea').val(result.businessData.operationProcess);
                $('.seven textarea').val(result.businessData.chargeDesc);
            } else {
                var error = "提示: " + result['resMsg'];
                clickautohide(1, error);
            }
        }
    })
}
// 添加/保存
function add_addition(){
    var business_id = $('.sx input').val();
    var sub_category_id = $.cookie('editor');
    var name = $('.one input').val();
    var dept_name=$('.two input').val();
    var policy_ref = $('.three textarea').val();
    var app_condition = $('.four textarea').val();
    var app_material = $('.five textarea').val();
    var operation_process = $('.six textarea').val();
    var charge_desc = $('.seven textarea').val();
    var url = gpath;
    var request_type = "";
    var btn = $('#add_addition').val();
    switch (btn) {
        case "添加事项":
            url += '/admin/business/post';
            request_type = "POST";
            // alert(123)
            break;
        case "保存事项":
            url += '/admin/business/' + $('.one input').attr('id');
            request_type = "PUT";
    }
    $.ajax({
        type: request_type,
        dataType: 'json',
        url: url,
        data: {
            businessId: business_id,
            subCategoryId: sub_category_id,
            deptName: dept_name,
            policyRef:policy_ref,
            appMaterial: app_material,
            appCondition:app_condition,
            operationProcess: operation_process,
            chargeDesc: charge_desc,
            name: name
        },
        success: function (result) {
           
            if (result.resCode == 0) {
                clickautohide(4, 'success');
                $('.one input').attr('id',result.id);
                business_list($.cookie('editor'), $('.thing'));
            } else {
                var error = "提示: " + result['resMsg'];
                clickautohide(1, error);
            }
        }
    })
}
// 删除
function remove_addition(){
    var msg = "确认删除事项：" + $('.one input').val() + " ?";
    if (confirm(msg) == true) {
        $.ajax({
            type: "DELETE",
            dataType: 'json',
            url: gpath + "/admin/business/" + $('.one input').attr('id'),
            success: function (result) {
                if (result.resCode == 0) {
                    clickautohide(4, '删除事项成功');
                    additions_onload();
                    business_list($.cookie('editor'), $('.thing'));
                } else {
                    var error = "提示: " + result['resMsg'];
                    clickautohide(1, error);
                }
            }
        })
    }
}
// 重置
function reset_addition(){
    $('.new_permit_li input').val("");
    $('.new_permit_li textarea').val("");
}
// 示例
function example_addition(){
    $('.one input').val('居住证新办');
    $('.sx input').val('1');
    $('.two input').val('市公安局');
    $('.three textarea').val("《上海市居住证管理办法》（沪府令58号）； 《上海市居住证申办实施细则》（沪府发〔2017〕89号）。");
    $('.four textarea').val("1、离开常住户口所在地，在本市办理居住登记满半年； 2、符合有合法稳定就业、合法稳定住所、连续就读条件之一的。");
    $('.five textarea').val("1、申请人本人有效居民身份证正、反面复印件或户口簿复印件（验原件）； 2、《上海市居住证申请表》； 3、申请人现居住地址与居住登记地址不一致的，应当提供相应的在沪合法居住证明：居住在本人或近亲属自购住房的，提供相应的房地产权证明复印件（验原件）；居住在本人或近亲属租赁住房的，提供房屋管理部门出具的房屋租赁合同登记备案证明复印件（验原件）；居住在单位、学校集体宿舍的，提供单位、学校人事或者保卫部门出具的集体宿舍证明； 4、居住在近亲属自购或者租赁住房的，还应当提供相应的亲属关系证明。");
    $('.six textarea').val("1、申请人本人到居住地街道（乡镇）社区事务受理服务中心提交相关申办材料； 2、居住地街道（乡镇）社区事务受理服务中心指导申请人填写《上海市居住证申请表》并确认签字，核对材料； 3、对材料不齐全的，应当告知申请人需要补齐的内容，并将申请材料退还申请人； 4、对材料齐全的，应当在居住证信息系统中登记信息、拍照，并出具《上海市居住证受理回执》； 5、凭个人有效居民身份证原件和受理回执领取证件。");
    $('.seven textarea').val("首次新办免收工本费。 ");
} 