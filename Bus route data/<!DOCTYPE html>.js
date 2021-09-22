<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>覆盖物鼠标事件</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <style>
    body,
    html,
    #container {
        overflow: hidden;
        width: 100%;
        height: 100%;
        margin: 0;
        font-family: "微软雅黑";
    }
    </style>
    <script src="//api.map.baidu.com/api?type=webgl&v=1.0&ak=您的密钥"></script>
</head>
<body>
    <div id="container"></div>
</body>
</html>
<script>
var map = new BMapGL.Map('container');
var point = new BMapGL.Point(116.404, 39.915);
map.centerAndZoom(point, 15);
map.enableScrollWheelZoom(true);

// 绘制点
var marker = new BMapGL.Marker(point);
map.addOverlay(marker);

// 绘制面
var polygon = new BMapGL.Polygon([
    new BMapGL.Point(116.387112, 39.920977),
    new BMapGL.Point(116.385243, 39.913063),
    new BMapGL.Point(116.394226, 39.917988),
    new BMapGL.Point(116.401772, 39.921364),
    new BMapGL.Point(116.41248, 39.927893)
], {
    strokeColor: 'blue',
    strokeWeight: 2,
    strokeOpacity: 0.5
});
map.addOverlay(polygon);

// 绘制线
var polyline = new BMapGL.Polyline([
    new BMapGL.Point(116.399, 39.910),
    new BMapGL.Point(116.405, 39.920),
    new BMapGL.Point(116.423493, 39.907445)
], {
    strokeColor: 'blue',
    strokeWeight: 2,
    strokeOpacity: 0.5
});
map.addOverlay(polyline);

// 绘制圆
var circle = new BMapGL.Circle(new BMapGL.Point(116.404, 39.915), 500, {
    strokeColor: 'blue',
    strokeWeight: 2,
    strokeOpacity: 0.5
});
map.addOverlay(circle);

// 批量绑定事件
var clickEvts = ['click', 'dblclick', 'rightclick'];
var moveEvts = ['mouseover', 'mouseout'];
var overlays = [marker, polyline, polygon, circle];

for (let i = 0; i < clickEvts.length; i++) {
    const event = clickEvts[i];
    for (let j = 0; j < overlays.length; j++) {
        const overlay = overlays[j];
        overlay.addEventListener(event, e => {
            switch (event) {
                case 'click':
                    var res = overlay.toString() +  '被单击!';
                    break;
                case 'dbclick':
                    var res = overlay.toString() + '被双击!';
                    break;
                case 'rightclick':
                    var res = overlay.toString() + '被右击!';
            }
            alert(res);
        });
    }
}
for (let i = 0; i < moveEvts.length; i++) {
    const event = moveEvts[i];
    for (let j = 1; j < overlays.length; j++) {
        const overlay = overlays[j];
        overlay.addEventListener(event, e => {
            switch (event) {
                case 'mouseover':
                    overlay.setFillColor('#6f6cd8')
                    break;
                case 'mouseout':
                    overlay.setFillColor('#fff');
                    break;
            }
        });
    }
}
</script>