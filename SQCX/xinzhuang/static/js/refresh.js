/**
 * Created by python on 18-7-5.
 */

function refresh_data() {
    $.ajax({
    type: "GET",
    url: gpath+ "/init",
    dataType: "json",
    success: function () {
        alert('刷新成功');
        }
    });
}
