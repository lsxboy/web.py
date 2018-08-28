// 首页
$.ajax({
    type: "GET",
    // url: gpath + "/init",
    dataType: "json",
    success: function (data, textStatus, XMLHttpRequest) {
        // 获取id 和 name 办事指南
        $('#btn_box .fl').on('click', function () {
        //    console.log('点击了办事指南');
            window.location.href = 'department.html';
        });
        
    }
});
// 获取id 和 name 办事指南
$('#btn_box .fl').on('click', function () {
    //    console.log('点击了办事指南');
    window.location.href = 'department.html';
});
// 大厅简介
$('#btn_box .fr').on('click', function () {
    // console.log('点击了大厅简介');
    window.location.href = 'introduce.html';
});