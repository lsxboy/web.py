
//此函数使用ajax从本地读取Html文件并加载到页面中，并调用回调函数完成页面加载初始化
function read_file(resource, content_div, html_file, call_back_func) {
    var res = "";
    var xmlhttp;
    if (window.XMLHttpRequest) { // 兼容 IE7+, Firefox, Chrome, Opera, Safari 
        xmlhttp = new XMLHttpRequest();
    } else { // 兼容IE6, IE5 
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            //alert(xmlhttp.responseText);
            document.getElementById(content_div).innerHTML = xmlhttp.responseText;
            call_back_func(resource);
        }
    }
    xmlhttp.open("GET", html_file, true);
    xmlhttp.send();
}
// 菜单跳转
function rightMain1(resource){
    
    switch(resource){
        case $('.add_big a').text():
            // alert('调用了添加大类')
            read_file(resource, "rightMain", "add_big.html", add_big_onload);
            break;
        case $('.org a').text():
            // alert($('.org a').text())
            read_file(resource,"rightMain","add_org.html",add_org_onload);
            break;
        case $('.detail_org_general a').text():
            //general 绑定的机构
            // alert($('.detail_org_general a').text());
            read_file(resource, "rightMain", "add_org.html",detail_org_onload2);
            break;
        case $('.add_user a').text():
            read_file(resource, "rightMain", "add_user.html", add_user_onload);
            break;
    };
    var detail_org = $('.detail_org a');
    for(var i = 0;i<detail_org.length;i++){
        if (resource == detail_org.eq(i).text()){
            read_file(resource, "rightMain", "add_org.html", detail_org_onload);
            // alert('调用机构');
            break;
        }
    };
    var user = $('.user a');
    for(var i = 0;i<user.length;i++){
        if (resource == user.eq(i).text()){
            read_file(resource,"rightMain","add_user.html",user_onload);
            // alert('调用管理员');
            break;
        }
    };
    var editor_big = $('.editor_big a');
    for(var i=0;i<editor_big.length;i++){
        if (resource == editor_big.eq(i).text()){
            // alert('调用了编辑大类')
            read_file(resource, "rightMain", "add_big.html", editor_big_onload);
            break;
        }
    };
    var add_small = $('.nav-show .add_small a');
    for(var i = 0;i<add_small.length;i++){
        if (resource == add_small.eq(i).text()){
            // alert('调用了添加小类')
            read_file(resource, "rightMain", "add_small.html", add_small_onload);
            break;
        }
    };
    var editor_small=$('.editor_small a');
    for (var i = 0; i < editor_small.length;i++){
        if (resource == editor_small.eq(i).text()){
            // alert('调用了编辑小类')
            read_file(resource, "rightMain", "add_small.html", editor_small_onload);
            break;
        }
    };
    var additions=$('.additions a');
    for (var i = 0; i < additions.length; i++) {
        if (resource == additions.eq(i).text()) {
            // alert('调用了添加事项')
            read_file(resource, "rightMain", "additions.html", additions_onload);
            break;
        }
    };
    var detail_addition = $('.detail_addition a');
    for(var i=0; i<detail_addition.length;i++){
        if (resource == detail_addition.eq(i).text()){
            // read_file(resource, "rightMain", "additions.html", detail_addition_onload);
            if (detail_addition.eq(i).attr('name') == 'bus_nochange'){
                // alert('调用了具体事项1')
                read_file(resource, "rightMain", "additions.html", detail_nochange_addition_onload);
                break;
            } else {
                // alert('调用了具体事项2')
                read_file(resource, "rightMain", "additions.html", detail_addition_onload);
                break;
            }
        }
        
    };
}