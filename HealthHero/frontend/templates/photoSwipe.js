function loadXML(url) {
    if (window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    }
    else { // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (xmlhttp != null) {
        xmlhttp.onreadystatechange = stateChange;
        xmlhttp.open("GET",url,false);
        xmlhttp.send();
    }
    else {
        alert("Your browser does not support XMLHTTP");
    }
}

function stateChange() {
    if (xmlhttp.readyState === 4) {// loaded
        if (xmlhttp.status === 200) {// OK
            var response_obj = JSON.parse(xmlhttp.responseText);
            photoSwipe.infoArr = response_obj.answer;
        }
        else {
            alert("Load XML data failed.");
        }
    }
}

var photoSwipe={
    /*info array*/
    infoArr:[],
    /*element position*/
    site:{
        _x_start:0,
        _y_start:0,
        _x_move:0,
        _y_move:0,
        _x_end:0,
        _y_end:0,
        top_val:0,
        left_val:0
    },
    /*current index*/
    index:0,
    /*animation enable*/
    run:true,
    /*is load completed*/
    load:false,
    /*initialization*/
    init:function () {
        document.querySelector("#photo_box>div>div").innerHTML=this.imgHtml();
    },
    /*flag for answer*/
    false_number:0,
    /*HTML for card*/
    imgHtml:function () {
        if (this.index >= this.infoArr.length) {
            let percent = (1-this.false_number/this.infoArr.length) * 100;
            var str='<div id="ind-'+this.index+'">'
            +'<div class="div1">Your score is...</div>'
            +'<div style="padding-top: 80px;font-size: 70px; color: gray">'+ parseInt(percent) +'</div>'
            +'<div style="padding-top: 120px"><a href="index.html">Go back to Home Page</a></div>'
            +'</div>';
        }
        else {
            var str='<div id="ind-'+this.index+'">'
            +'<div class="div1">Question No.'+(this.index+1)+'</div>'
            +'<div style="padding-top: 60px;color: #d01d33;font-weight: bold;">' + this.infoArr[this.index].Question + '</div>'
            +'<div style="padding-top: 80px;font-weight: bold;">Hint:' + this.infoArr[this.index].Response + '</div>'
            +'<div style="padding-top: 80px">Swipe to answer</div>'
            +'<div style="padding-top: 20px">Left -> False  Right -> True</div>'
            +'</div>';
        }
        return str;
    },
    /*animation for move card*/
    animateMove:function (el,val) {
        if(!this.run){
            return;
        }
        this.run=false;

        el.css({"transform":"translate3d("+doc_width*val+"px,"+photoSwipe.top_val*2.2+"px,0px)","transition-duration":"0.3s"});
        var moveTime=setTimeout(function () {
            el.remove();
            var ind_el=$("#ind-"+(photoSwipe.index));
            photoSwipe.activeEl(ind_el);
            photoSwipe.index++;
            $("#photo_box>div>div").append(photoSwipe.imgHtml());
            photoSwipe.run=true;
        },300);
    },
    /*animation for reset*/
    animateReset:function (el) {
        el.css({"transform":"translate3d(0px,0px,0px)","transition-duration":"0.3s"});
        var resetTime=setTimeout(function () {
            el.css("transition-duration","0s");
        },1000);
    },
    activeEl:function (el) {
        el.css("z-index","2");
    },
    clearLocation:function () {
        this.left_val=0;
    }

};

loadXML('http://127.0.0.1:5000/getquestions');
photoSwipe.init();

var doc_width=$(document).width(),doc_height=$(document).height();

photoSwipe.activeEl($("#ind-0"));
photoSwipe.index++;
$("#photo_box>div>div").append(photoSwipe.imgHtml());

$("#photo_box").on("touchstart",function(e) {
    if(!photoSwipe.load || !photoSwipe.run){
        return;
    }

    var ev = e || window.event;
    photoSwipe._x_start=ev.touches[0].pageX;
    photoSwipe._y_start=ev.touches[0].pageY;
    var act_el=$("#ind-"+(photoSwipe.index-1).toString(10));
});
$("#photo_box").on("touchmove",function(e) {
    if(!photoSwipe.load || !photoSwipe.run){
        return;
    }
    var ev = e || window.event;
    photoSwipe._x_move=ev.touches[0].pageX;
    photoSwipe._y_move=ev.touches[0].pageY;

    var act_el=$("#ind-"+(photoSwipe.index-1).toString(10));
    photoSwipe.top_val=parseFloat(photoSwipe._y_move)-parseFloat(photoSwipe._y_start);
    photoSwipe.left_val=parseFloat(photoSwipe._x_move)-parseFloat(photoSwipe._x_start);

    act_el.css({"transform":"translate3d("+photoSwipe.left_val+"px,"+photoSwipe.top_val+"px,0px)","transition-duration":"0s"});
});
$("#photo_box").on("touchend",function(e) {
    if(!photoSwipe.load || !photoSwipe.run){
        return;
    }
    var ev = e || window.event;
    photoSwipe._x_end=ev.changedTouches[0].pageX;
    photoSwipe._y_end=ev.changedTouches[0].pageY;
    var act_el=$("#ind-"+(photoSwipe.index-1).toString(10));
    
    if(photoSwipe.left_val>0 && photoSwipe.left_val>doc_width/2-doc_width/4.5){
        if (photoSwipe.index < photoSwipe.infoArr.length && photoSwipe.infoArr[photoSwipe.index].Answer == "False") {
            photoSwipe.false_number++;
        }
        photoSwipe.animateMove(act_el,1);
    }else if(photoSwipe.left_val<0 && photoSwipe.left_val<-doc_width/2+doc_width/4.5){
        if (photoSwipe.index < photoSwipe.infoArr.length && photoSwipe.infoArr[photoSwipe.index].Answer == "True") {
            photoSwipe.false_number++;
        }
        photoSwipe.animateMove(act_el,-1);
    }else {
        photoSwipe.animateReset(act_el);
    }
});

$(function () {
    photoSwipe.load=true;
});