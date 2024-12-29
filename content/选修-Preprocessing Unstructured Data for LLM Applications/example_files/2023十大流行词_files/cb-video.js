// JavaScript Document
/*var new_element = document.createElement("script");
new_element.setAttribute("type", "text/javascript");
new_element.setAttribute("src", "https://player.v.news.cn/player/sdk/h5/v2.0.6/DHYPlayer-2.0.6.min.js");
var new_element2 = document.createElement("script");
new_element2.setAttribute("type", "text/javascript");
new_element2.setAttribute("src", "http://pv.sohu.com/cityjson?ie=utf-8");
document.body.appendChild(new_element);
document.body.appendChild(new_element2);
*/
$(function () {

    var allVideoList = [];
    var detailVideo = $("#detail .pageVideo");
    //console.log(detailVideo)
    //detailVideo.attr("src", "")

    var isMobile = (/iPad|iPhone|Android|Windows Phone|Nokia/).test(navigator.userAgent); //当前访问设备为移动端
    var isLow750 = document.querySelector("body").clientWidth <= 750; //判断是否屏幕尺寸小于750，针对pc，小于750展示手机版页面
    var ieNum = IEVersion();

    //视频内容渲染中的判断
    //var _tempDetail = $("#detail").html();
    //     $("#detail").html(_tempDetail.replace("视频正在解压，请稍等！", ""));

    //console.log("视频个数：", $("#detail .pageVideo").length)
    if ($("#detail .pageVideo").length > 0) {
        detailVideo.each(function () {
            var _videoSrc = $(this).attr("video_src");
            if (_videoSrc.indexOf("bucket") > 0) {
                return false;
            }
        });
        if (ieNum == -1 || ieNum > 11 || ieNum == "edge") {
            //console.log("ieNum:", ieNum);
            // dynamicLoadJs("http://static.danghongyun.com/player/xh/h5/v2.0.13/DHYPlayer-2.0.13.min.js", laodjs3);
            dynamicLoadJs("https://player.v.news.cn/player/sdk/h5/DHYPlayer-latest.min.js", laodjs3);
        } else {
            //需创建简单的视频播放器
            simpleVideo();
        }
    }

    function simpleVideo() {

        detailVideo.each(function (i, item) {
            //console.log("i:",i)
            var videoWidth = $(this).attr("width");
            var videoTrueWidth = $(this).attr("video_width");
            var videoTrueHeight = $(this).attr("video_height");
            var videoNeedHeight = videoWidth * videoTrueHeight / videoTrueWidth;
            var videoPoster = $(this).attr("poster");

            $(this).parent().after('<div class="simpleVideo" style="text-align:center"><video width="' + videoWidth + '" height="' + videoNeedHeight + '" poster="' + videoPoster + '" src="' + $(this).attr("video_src") + '" controls="controls"></div>');
            $(this).remove();
        })
    }


    function dynamicLoadJs(url, callback) {
        var head = document.getElementsByTagName('head')[0];
        var script = document.createElement('script');
        detailVideo.each(function (i, item) {
            var _detalJson = {
                "vid": $(this).attr("vid"),
                "src": $(this).attr("video_src"),
                "uuid": $(this).attr("uuid"),
                "width": $(this).attr("width").replace("px", ""),
                "height": $(this).attr("height"),
                "trueWidth": $(this).attr("video_width"),
                "trueHeight": $(this).attr("video_height"),
                "poster": $(this).attr("poster"),
                "id": "DH-PLAYERID" + i
            }
            allVideoList.push(_detalJson);
            $(this).parent().after('<div id="DH-PLAYERID' + i + '"></div>');
        })

        //console.log("allVideoList", allVideoList)

        script.type = 'text/javascript';
        script.src = url;
        if (typeof (callback) == 'function') {
            script.onload = script.onreadystatechange = function () {
                if (!this.readyState || this.readyState === "loaded" || this.readyState === "complete") {
                    callback();
                    script.onload = script.onreadystatechange = null;
                }
            };
        }
        head.appendChild(script);
    }

    function IEVersion() {
        var userAgent = navigator.userAgent; //取得浏览器的userAgent字符串  
        var isIE = userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1; //判断是否IE<11浏览器  
        var isEdge = userAgent.indexOf("Edge") > -1 && !isIE; //判断是否IE的Edge浏览器  
        var isIE11 = userAgent.indexOf('Trident') > -1 && userAgent.indexOf("rv:11.0") > -1;
        if (isIE) {
            var reIE = new RegExp("MSIE (\\d+\\.\\d+);");
            reIE.test(userAgent);
            var fIEVersion = parseFloat(RegExp["$1"]);
            if (fIEVersion == 7) {
                return 7;
            } else if (fIEVersion == 8) {
                return 8;
            } else if (fIEVersion == 9) {
                return 9;
            } else if (fIEVersion == 10) {
                return 10;
            } else {
                return 6; //IE版本<=7
            }
        } else if (isEdge) {
            return 'edge'; //edge
        } else if (isIE11) {
            return 11; //IE11  
        } else {
            return -1; //不是ie浏览器
        }
    }

    function laodjs3() {
        $(function () {
            //var videoWidth = detailVideo.attr("width");
            // var playerCallback = ;


            //console.log("allVideoList", allVideoList)
            allVideoList.forEach(function (item, i, array) {
                //视频增加src属性，判断vid和src都没有情况才用iframe直接播放
                if (allVideoList[i].vid == undefined && allVideoList[i].src == undefined) {
                    var tempSrc = $("#detail .pageVideo").eq(i).attr("src");
                    $("#detail .pageVideo").eq(i).show().attr("src", tempSrc);
                    return false;
                } else {

                    // var player_poster = $("#detail .pageVideo").eq(i).attr("poster");

                    // 2021-12-14修改视频适配旧cms通过vid，uid方式输出封面图
                    var player_vars = {
                        "vid": item.vid,
                        "src": item.src,
                        "analyseUrl": "http://vodstat.v.news.cn/vms/api/pub/player/recordContent",
                        "uid": item.uuid,
                        //"autoplay": true,
                        "rServer": "http://player.v.news.cn",
                        "analyse": false,
                        "logo": "",
                        "playAndPauseLayoutEnable": false,
                        "watermark": "",
                        //"muted":true,
                        //"poster": player_poster,
                        //"width": item.width + "px",
                        //"height": item.height + "px",
                        "eventCallback": function (playerId, status) {
                            console.log(playerId,status); 
                            var getVideoNum = playerId.substr(playerId.length - 1, 1);
                            //console.log("getVideoNum",getVideoNum);
                            var videoWidth = allVideoList[getVideoNum].width;
                            var videoTrueWidth = allVideoList[getVideoNum].trueWidth;
                            var videoTrueHeight = allVideoList[getVideoNum].trueHeight;
                            //var thisPlay = $('#' + playerId).find("video");
                            //视频动态控制高度
                            if (status === 'playerInitComplate') {
                                $(".player-container").css({
                                    "margin": "0 auto 10px"
                                });
                                //手机端动态增加样式					
                                if (isMobile || isLow750) {
                                    var videoNeedHeight = $("#detail").width() * videoTrueHeight / videoTrueWidth;
                                    $("#DH-PLAYERID" + getVideoNum + " .player-container").css({
                                        "width": "100%",
                                        "height": videoNeedHeight
                                    });
                                } else {
                                    var videoNeedHeight = videoWidth * videoTrueHeight / videoTrueWidth;
                                    // console.log("videoNeedHeight11111", videoNeedHeight)
                                    $("#DH-PLAYERID" + getVideoNum + " .player-container").css({
                                        "width": videoWidth,
                                        "height": videoNeedHeight
                                    });
                                }
                            }
                            if (status == "playing") {
                                stopOtherVideo(getVideoNum);                                
                                $("#DH-PLAYERID" + getVideoNum + " .control-slider-container").show();
                                $("#DH-PLAYERID" + getVideoNum + " .PlayToggle").show().siblings().show();   
                                $("#DH-PLAYERID" + getVideoNum + " .PlayToggle img").css({
                                    width:"20px",
                                    height:"20px",
                                    "margin-top":"0"
                                });
                            }
                            // if (status == "ended") {
                            // 	stopOtherVideo(getVideoNum);
                            // }
                            if (status == "ended" || status == "complete") {
                                //xilanAutoPlay();
                            }
                            if(status=="canplay"){
                                $("#DH-PLAYERID" + getVideoNum + " .control-slider-container").hide();
                                $("#DH-PLAYERID" + getVideoNum + " .PlayToggle").show().siblings().hide();                                
                                $("#DH-PLAYERID" + getVideoNum + " .PlayToggle img").attr("src","data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC4AAAAuCAYAAABXuSs3AAAEO0lEQVRogc2aX4jVRRTHP2vbrsKWZbu2WZsV1AbrUoKyEkXQH6KHHt1MhCiJDIJIFEF8qIcgwQdfRN/yz/pSoNuTQRAYsgtB1lKKBUKkSVLEbiuoW+6Rs5xZzk73yu/3m7nd+4Vhhju/Oec75ze/M2fO3DYRoQFoA+4CbgB/N0JBewYZK4AXgGeBAeAx4G7Xr+T/As4B3wFngRPArylKq1q8A9gIvAE8YxYugwngyRTiZS2uz78F7AQeqNGvVvwJuARccUvmHuAJoNeeuxSN08n3A0eBq4WYqMULliER+V4WYkZERkVko4jcV0DOUhF5XEQ63G9PicisSR0pyqfIQ7qcthrJgCkR+VBElpeYeL2yyckdz0W8XUQ+iax8RETuzUA4lMUiclhEvjHrJxNX0sciKw9nJJxUbrU8RhzpiyKyqlVI34r4Nkf6goisbCXSWmr58SHga/PVuus9DfxQ0m02HIsiBeqnDxhpzGe3HGlqEH/b7Wi6GXzaBE4eS4CDwBjQt6DHrZsO+wiDB+ltgbW8yn1rp/3G5S2+Cbjf2vuA3ytYSLf3nhymNpwBRqy9Ghie73GzO2kzuy4iPRUttF9E/hSRVzJa/UER+ce4nYrdYZ+LF44nKDlqMlTWXhHpzER+1Mnt80vlZReafpbhFaus94Bxi89TcdzJfQnnVdaFlQN8mUFRgK7Lb4HXE+V84dprccQHrP4F+CNRSYwuc2lHgDsqyrgM/GbtQRzxfqvPZaW8EOq11PprKo4/Y/UcVyV+G7DUfoxPJrnxKHAK2FJB7mWrl+laXxS9visNJq7oBN6tMG7Kte+Mt/z/Az8u2EiK41/35JzFp90PXQ0mfsC8wtkKY/3KmG63vMe0dazISNJjEtgMHEuQEbhpqH0jLJXzVvfXGZSCMUtNpJDGbWRzXAPxCasfzhgkzQIfWYYrKWtlnB6x9hzXQHzMat1Sn09UgrnVF4Fd0UdVFc+5kGTcEz9h273i1QQFp4FRO4x8lYFwwAarxbjWDWu7W+AQEUqPcRLj+J+DxCGr9by5NaO1UvG+OwMfmpflZtbpjm6TLXJ06zUuIbdT8+h2HfjY2hq77GkBa+9xcZRym5nviWbYHmVkm5lyG3Y8JozbfH+tAUMuM6uvabAJpAfdElEu6+Jn6g3c3sQU3ErTGbC91nP1Bjcr6TngHIQYh7YyxLEv+PMozby+gaTXm46A0ejmojBxLbdb0t3jYOYNqttkehw23XXHFRGsr2pHdJWiH84HiRPoNhmTTu6M6aq5PMoSD2XI3JLHNbu12FDwekWfec2STtciWROmoxCfsvecevB4B9jh8owemt74Gbjozq9ddrWo8fRDNcZo2mE3sL9UJFnxNWt48KYFPbNSHrM2dnPVNF2Ou/w+i5fDlXi/26YDpuziVnMjJy3kvZCitFF/QtAYKJBX0noaygfgJsI00YX19pVQAAAAAElFTkSuQmCC").css({
                                    width:"50px",
                                    height:"50px",
                                    "max-height":"50px",
                                    "margin-top":"-25px"
                                });
                                $("#DH-PLAYERID" + getVideoNum + " .control-bar").css({
                                    "background":"none"
                                });                              
                            }
                        }
                    };

                    if (i !== 0) {
                        player_vars.autoplay = false;
                    }
                    // if (player_poster) {
                    // 	player_vars.poster = player_poster;
                    // }
                    if (item.poster) {
                        player_vars.poster = item.poster;
                    }

                    detailVideo[i].remove();
                    // console.log("player_vars", player_vars)
                    creatVideo(player_vars, i);
                }

            })

            function stopOtherVideo(i) {
                var index = parseInt(i);
                allVideoList.forEach(function (item, i, array) {
                    if (index !== i) {
                        //console.log(allVideoList)
                        allVideoList[i].dhplayer.pause();
                    }
                })
            }

            function getVideoHeight(width, trueWidth, trueHeight, i) {
                if (isMobile) {
                    var videoNeedHeight = $("#detail").width() * trueHeight / trueWidth;

                    $("#DH-PLAYERID" + i + " .player-container").css({
                        "width": "100%",
                        "height": videoNeedHeight
                    });
                } else {
                    var videoNeedHeight = width * trueHeight / trueWidth;
                    $("#DH-PLAYERID" + i + " .player-container").css({
                        "height": videoNeedHeight
                    });
                }
                //return videoNeedHeight;
            }

            function creatVideo(player_vars, i) {
                var inits_vars = {
                    autoHideControlBar: true,
                    autoHideTime: 1,
                    env: "xhw",
                };
                Object.keys(player_vars).forEach(function (key) {
                    if (key === 'uid') {
                        inits_vars.UUID = player_vars[key];
                        return;
                    }
                    inits_vars[key] = player_vars[key];
                });


                allVideoList[i].dhplayer = new DHYPlayer('DH-PLAYERID' + i, inits_vars);
            }

            // allVideoList.each(function(i,item){				
            // })	

            //细缆自动播放下一篇
            function xilanAutoPlay() {
                //console.log("下一篇开始")
                var metaMessage = $("meta[name='pageid']").attr("content").split(".");
                var siteID = metaMessage[0];
                var pageID = metaMessage[11];
                var nodeId = metaMessage[4];
                var pageUrl = 'http://qv.wa.news.cn/queryVideo/get?articleid=' + pageID + '&nodeid=' + nodeId;
                //console.log(pageUrl);
                $.ajax({
                    url: pageUrl,
                    success: function (data) {
                        if (data == 0) {
                            window.location.reload();
                        } else {
                            window.location.href = data;
                        }
                    }
                });
            }
        })
    }
})