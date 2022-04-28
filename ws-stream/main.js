const timers = [];
// TODO: construct websocket for communication
let ws = new WebSocket("ws://127.0.0.1:8765/");
let name= randomString(3);//each websocket bind a random name
    function randomString(e) {
  e = e || 32;
  var t = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678",
  a = t.length,
  n = "";
  for (i = 0; i < e; i++) n += t.charAt(Math.floor(Math.random() * a));
  return n
}
function showa(){//refresh the chatbox
    ws.send(["",""]);
}setInterval(showa,50);

ws.onmessage = function(evt) {//if recieve message
    var t=$.parseJSON(evt.data);
    document.getElementById("logi").value=t['all'];
    if(t["type"]==="da"){addInterval(createDanmaku(t['content']));}//whether  there is a new danmaku to add
};
$(".send").on("click", function () {//if click the button,send the new danmaku to the back end.
    var text=document.getElementById("danmakutext").value;
  ws.send([name,text]);
});
// create a Dom object corresponding to a danmaku
function createDanmaku(text) {
    const jqueryDom = $("<div class='bullet'>" + text + "</div>");
    const fontColor = "rgb(255,255,255)";
    const fontSize = "20px";
    let top = Math.floor(Math.random() * 400) + "px";
    const left = $(".screen_container").width() + "px";
    jqueryDom.css({
        "position": 'absolute',
        "color": fontColor,
        "font-size": fontSize,
        "left": left,
        "top": top,
    });
    $(".screen_container").append(jqueryDom);
    return jqueryDom;
}
// add timer task to let the danmaku fly from right to left
function addInterval(jqueryDom) {
    let left = jqueryDom.offset().left - $(".screen_container").offset().left;
    const timer = setInterval(function () {
        left--;
        jqueryDom.css("left", left + "px");
        if (jqueryDom.offset().left + jqueryDom.width() < $(".screen_container").offset().left) {
            jqueryDom.remove();
            clearInterval(timer);
        }
    }, 5); // set delay as 5ms,which means the danmaku changes its position every 5ms
    timers.push(timer);
}