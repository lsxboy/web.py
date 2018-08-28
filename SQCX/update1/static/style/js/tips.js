function clickme(i){
	var tip = "";
	switch(i){
		case 1:
			tip = "服务器繁忙，请稍后再试。";
		break;
		case 4:
			tip = "设置成功！";
		break;
		case 5:
			tip = "数据拉取失败";
		break;
		case 6:
			tip = "正在加载中，请稍后...";
		break;
	}
	ZENG.msgbox.show(tip, i);
}
function clickhide(){
	ZENG.msgbox._hide();
}
function clickautohide(i, tip0){
	var tip = "";
	switch(i){
		case 1:
			tip = tip0;
			//tip = "服务器繁忙，请稍后再试。";
		break;
		case 4:
			tip = tip0;
			//tip = "设置成功！";
		break;
		case 5:
			tip = tip0;
			//tip = "数据拉取失败";
		break;
		case 6:
			tip = tip0;
			//tip = "正在加载中，请稍后...";
		break;
	}
	ZENG.msgbox.show(tip, i, 1500);
}