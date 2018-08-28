function add_user_onload(){
    $('#sys_user_name').focus();
}
// 重置
function reset_user(){
    $('#sys_user_name').val("");
    $('#sys_user_password').val("");
    $('#sys_user_name').focus();
}
// 示例
function user_example() {
    $('#sys_user_name').val("张三");
    // $('#sys_user_password').val("123");
}
function user_onload(){
    $('#sys_user_name').focus();
    $('#add_save_user').val('保存');
}