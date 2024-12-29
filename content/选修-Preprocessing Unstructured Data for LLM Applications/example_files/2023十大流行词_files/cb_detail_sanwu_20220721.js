// JavaScript Document
$(function () {
    var pageShare = $(".pageShare"),
        pageShareTop = pageShare.offset().top,
        //metaArr = $("meta[name='pageid']").attr("content").split("."),
        releaseDate = $(".year em").html() + $.trim($(".day em").eq(0).html()) + $.trim($(".day em").eq(1).html());
    //siteIdXml = metaArr[0],
    //nodeId = metaArr[4],
    //fileUUID = metaArr[11]
    var newsHref = window.location.href; //当前文章地址
    var csdw = newsHref.split("/");
    var cbTime = newsHref.split("/")[csdw.length - 3];
    var cbUUID = newsHref.split("/")[csdw.length - 2];


    //var channelName = newsHref.split("/")[3];

    //console.log(newsHref);
    //console.log(channelName);
    var detail = {
        init: function () {
            var isMobile = (/iPad|iPhone|Android|Windows Phone|Nokia/).test(navigator.userAgent); //当前访问设备为移动端
            this.audioPlay(); //播放音频
            this.detailAudio(); //正文增加音频
            //  detailSetFont(); //设置颜色-通用js中的函数
            // detailAtlasDisplay();
            if (isMobile) {
                // detailAtlasDisplay(); //正文图片点击弹出细览图集功能-通用js中的函数
            } else {
                this.purPosition(); //当前位置
                this.fontshare(); //文字大小和分享
                this.xcxEwm(); //小程序二维码
                this.scrollSet(); //滚动设置跟随 标题和视频	
                //this.correct(); //纠错
                this.setTrim(); //去空格
                // this.setTitleFontSize();
            }
        },
        hotlist: function () {
            var htList = "";
            $(top1.list).each(function (i, item) {
                if (i > 9) {
                    return false;
                }
                htList += '<li id="' + item.id + '"><a href=http://www.newspro.cn/2021homepro/rsznb/index.htm?item=' + (i + 1) + ' target="_blank">' + item.listTitle + '</a></li>';
            })
            $(".hotList .col-cont").html(htList)
        },
        setTitleFontSize: function () {
            var titleSize = $.trim($("#fontsize").html());
            //设置字号
            if (titleSize != '') {
                $('.head-line .title').css({
                    "font-size": titleSize + "px"
                });
            }
        },
        setTitleFontColor: function () {
            var titleColor = $.trim($("#fontcolor").html());
            //设置颜色
            if (titleColor != '') {
                $('.head-line .title').css({
                    'color': titleColor
                });
                $('.mheader .title').css({
                    'color': titleColor
                });
            }
        },

        xcxEwm: function () {
            //var publishid = $("meta[name=publishid]").attr("content");
            //var articleid = publishid.split('.')[0];
            //console.log(articleid)
            //var pUrl = "https://qrapi.news.cn/code/getQRCode?type=pages/detail/detailText/detailText&articleid=" + fileUUID + "&origin=xinhuawang"
            var bigUUID = cbTime + cbUUID

            $.ajax({
                url: "https://qrapi.news.cn/code/getQRCode",
                type: "post",
                data: {
                    type: 'pages/detail/detailText/detailText',
                    articleid: bigUUID,
                    origin: 'xinhuawang'
                },
                success: function success(res) {
                    //console.log("小程序二维码地址：", res.data)
                    if (res.code == '200') {
                        //console.log(res.code, res.data)
                        //callback && callback(res.data, dom);
                        $(".pageShare .xcx-ewm img").attr("src", res.data)
                        $(".fix-ewm .fxd-xcx-ewm img").attr("src", res.data)
                    }
                }
            });
        },
        correct: function () {
            //纠错
            (function () {
                var _hexCHS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
                var _hexTBL = {
                    '0': 0,
                    '1': 1,
                    '2': 2,
                    '3': 3,
                    '4': 4,
                    '5': 5,
                    '6': 6,
                    '7': 7,
                    '8': 8,
                    '9': 9,
                    'A': 10,
                    'B': 11,
                    'C': 12,
                    'D': 13,
                    'E': 14,
                    'F': 15,
                    'G': 16,
                    'H': 17,
                    'I': 18,
                    'J': 19,
                    'K': 20,
                    'L': 21,
                    'M': 22,
                    'N': 23,
                    'O': 24,
                    'P': 25,
                    'Q': 26,
                    'R': 27,
                    'S': 28,
                    'T': 29,
                    'U': 30,
                    'V': 31,
                    'W': 32,
                    'X': 33,
                    'Y': 34,
                    'Z': 35,
                    'a': 36,
                    'b': 37,
                    'c': 38,
                    'd': 39,
                    'e': 40,
                    'f': 41,
                    'g': 42,
                    'h': 43,
                    'i': 44,
                    'j': 45,
                    'k': 46,
                    'l': 47,
                    'm': 48,
                    'n': 49,
                    'o': 50,
                    'p': 51,
                    'q': 52,
                    'r': 53,
                    's': 54,
                    't': 55,
                    'u': 56,
                    'v': 57,
                    'w': 58,
                    'x': 59,
                    'y': 60,
                    'z': 61
                };
                var key = [61, 37, 44, 31, 34, 7, 24, 6, 43, 12, 27, 3, 25, 29, 60, 33, 35, 41, 58, 2, 51, 49, 9, 5, 59, 11, 42, 32, 22, 40, 4, 57, 50, 38, 8, 56, 21, 19, 52, 53, 16, 28, 1, 26, 47, 17, 54, 46, 10, 23, 55, 13, 14, 20, 15, 36, 18];
                Hr = function () {
                    if (key.length < 57) {
                        throw new Error('the key is too short.');
                    }
                    this._sz = _hexCHS.charCodeAt(key[15]) % (key.length - 20) + 10;
                    this._ks = key.slice(-this._sz);
                    for (var _i = 0; _i < this._sz; ++_i) {
                        this._ks[_i] = _hexCHS.charCodeAt(this._ks[_i] % 62);
                    }
                    this._k16 = [], this._k41 = [];
                    this._t16 = {}, this._t41 = {};
                    for (var _i = 0; _i < 16; ++_i) {
                        this._k16[_i] = _hexCHS.charAt(key[_i]);
                        this._t16[this._k16[_i]] = _i;
                    }
                    for (var _i = 0; _i < 41; ++_i) {
                        this._k41[_i] = _hexCHS.charAt(key[_i + 16]);
                        this._t41[this._k41[_i]] = _i;
                    }
                };
                Hr.prototype.ca = function (s) {
                    var _k16 = this._k16,
                        _k41 = this._k41,
                        _ks = this._ks,
                        _sz = this._sz,
                        _cnt = 0;
                    return s.replace(/[^\s\n\r]/g, function (ch) {
                        var _n = ch.charCodeAt(0);
                        return (_n <= 0xff) ? _k16[parseInt(_n / 16)] + _k16[_n % 16] : _k41[parseInt(_n / 1681)] + _k41[parseInt(_n % 1681 / 41)] + _k41[_n % 41]
                    }).replace(/[0-9A-Za-z]/g, function (ch) {
                        return _hexCHS.charAt((_hexTBL[ch] + _ks[_cnt++ % _sz]) % 62);
                    });
                };
            })();
            /*
            $(".tiyi1").toggle(
            	function(){$('#jc_link1').attr("src",jc_link);$("#advisebox01").show();},
            	function(){$("#advisebox01").hide();}
            );
            $(".advise").toggle(
            	function(){$('.jc_link23').attr("src",jc_link);$("#advisebox02").show();},
            	function(){$("#advisebox02").hide();}
            );
            */
            $(".tiyi1").click(function () {

                $('#jc_link1').attr("src", jc_link);
                $("#advisebox01").show();
            });
            $("#jc_close1").click(function () {
                event.stopPropagation();
                $("#advisebox01").hide();
            });

            $("#jc_close1").click(function () {
                $("#advisebox01").hide();
            });
            $("#jc_close2").click(function () {
                $("#advisebox02").hide();
            });
            //获取责编id，稿件url，稿件id，稿件标题  
            var ele_pageid = $("meta[name=pageid]").attr("content");
            var ele_ids = ele_pageid.split(".");
            var bId = ele_ids[ele_ids.length - 2];
            var _code = new Hr(); //code
            var cId = _code.ca(ele_ids[ele_ids.length - 1]);
            var cTitle = $("title").html().split("_")[0];
            if (cTitle != "") {
                cTitle = encodeURI(encodeURI(cTitle));
            }
            var cUrl = window.location.href;
            var jc_link = 'http://ck.wa.news.cn/XHWCIFB/Confirm.do?bId=' + bId + "&cUrl=" + cUrl + "&cId=" + cId + "&cTitle=" + cTitle;
            /****** end *******/
        },
        setTrim: function () {
            var _day1 = $.trim($(".header .day em").eq(0).html());
            var _day2 = $.trim($(".header .day em").eq(1).html());
            $(".header .day").html(_day1 + "/" + _day2)
        },
        detailAudio: function () {
            $('img[name="audiospan"]').each(function (i) {
                console.log(i);
                var audioSrc = $(this).attr("apath");
                var audioHtml = '<audio  controls="controls" src="' + audioSrc + '"></audio>';
                $(this).after(audioHtml);
                $(this).remove();
            })
            var audios = document.getElementsByTagName("audio");

            function pauseAll() {
                var self = this;
                [].forEach.call(audios, function (i) {
                    // 将audios中其他的audio全部暂停
                    i !== self && i.pause();
                })
            }
            [].forEach.call(audios, function (i) {
                i.addEventListener("play", pauseAll.bind(i))
            });
        },
        getBookRight: function () {
            var bookHtml = "";
            var bookNum = Math.ceil(Math.random() * 5);
            $(xhBook.data.list).each(function (i, item) {
                if (i > (bookNum - 2) && i < (bookNum + 1)) {
                    bookHtml += '<li><a href="' + item.url + '" target="_blank"><div><img src="' + item.picurl + '"></div><div class="book-tit">' + item.name + '</div></li>';
                }
            })
            $(".book ul").html(bookHtml)
        },
        getBookBottom: function () {
            var bookListHtml = "";
            $(xhBook.data.list).each(function (i, item) {
                if (i > 5) {
                    return false;
                }
                bookListHtml += '<li><div class="pic"><a href="' + item.url + '" target="_blank"><img src="' + item.picurl + '" alt=""></a></div><div class="title"><a href="' + item.url + '" target="_blank">' + item.name + '</a></div></li>';
            })
            $(".bookList ul").html(bookListHtml)
        },
        purPosition: function () {
            // $(domainNameArr).each(function (i, v) {
            // 	if (newsHref.indexOf(v.name) >= 0) channelName = v.sKey;
            // });
            var curColumn = {};
            $(arrChannel).each(function (i, v) {
                if (newsHref.indexOf(v.sKey) > -1) {
                    curColumn = {
                        name: v.sValue,
                        url: v.sUrl,
                        sKey: v.sKey
                    }
                }
            });
            console.log(curColumn);
            $(".curColumn").attr({
                "href": curColumn.url,
                "target": "_blank"
            }).html(curColumn.name);
        },
        fontshare: function () {
            $("#fontSmall").click(function () {
                $(this).addClass("active").siblings().removeClass("active");
                $("#detail").css({
                    "font-size": "16px"
                })
            })
            $("#fontNormal").click(function () {
                $(this).addClass("active").siblings().removeClass("active");
                $("#detail").css({
                    "font-size": "18px"
                })
            })
            $("#fontBig").click(function () {
                $(this).addClass("active").siblings().removeClass("active");
                $("#detail").css({
                    "font-size": "20px"
                })
            })
            //分享
            var title = $(".head-line .title").html();
            var wbSrc = 'http://service.weibo.com/share/share.php?url=' + newsHref + '&title=' + title;
            //var kjSrc = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?url=' + newsHref + '&title=' + title;
            //var _src = newsHref.replace("c_", "ewm_").replace(".htm", "1n.jpg");
            //console.log(_src)
            //$(".wx-ewm img").attr("src", _src);
            // $(".fxd-wx-ewm img").attr("src", _src);
            $(".share .wb").attr("href", wbSrc).attr("target", "_blank");
            $(".fxd .fxd-wb").attr("href", wbSrc).attr("target", "_blank");
            $(".pageShare").on("mouseover", ".wx", function () {
                $(".pageShare .wx-ewm").stop(true, true).slideDown();
            })
            $(".pageShare").on("mouseleave", ".wx", function () {
                $(".pageShare .wx-ewm").stop(true, true).slideUp();
            })
            $(".pageShare").on("mouseover", ".khd", function () {
                $(".pageShare .khd-ewm").stop(true, true).slideDown();
            })
            $(".pageShare").on("mouseleave", ".khd", function () {
                $(".pageShare .khd-ewm").stop(true, true).slideUp();
            })
            $(".pageShare").on("mouseover", ".xcx", function () {
                $(".pageShare .xcx-ewm").stop(true, true).slideDown();
            })
            $(".pageShare").on("mouseleave", ".xcx", function () {
                $(".pageShare .xcx-ewm").stop(true, true).slideUp();
            })
            $(".fix-ewm").on("mouseover", ".fxd-wx", function () {
                $(".fxd-wx-ewm").stop(true, true).slideDown();
            })
            $(".fix-ewm").on("mouseleave", ".fxd-wx", function () {
                $(".fxd-wx-ewm").stop(true, true).slideUp();
            })
            $(".fix-ewm").on("mouseover", ".fxd-khd", function () {
                $(".fxd-khd-ewm").stop(true, true).slideDown();
            })
            $(".fix-ewm").on("mouseleave", ".fxd-khd", function () {
                $(".fxd-khd-ewm").stop(true, true).slideUp();
            })
            $(".fix-ewm").on("mouseover", ".fxd-xcx", function () {
                $(".fxd-xcx-ewm").stop(true, true).slideDown();
            })
            $(".fix-ewm").on("mouseleave", ".fxd-xcx", function () {
                $(".fxd-xcx-ewm").stop(true, true).slideUp();
            })
        },
        audioPlay: function () {
            //音频
            var audioSrc = 'http://vodpub1.v.news.cn/audio/' + cbTime + '/' + cbTime + cbUUID + '_title_content.mp3';
            $(".btn-audio").click(function () {
                if ($(this).hasClass("btn-audio-play")) {
                    $(this).removeClass("btn-audio-play");
                    $("#audioDom")[0].pause();
                } else {
                    console.log(audioSrc)
                    $.ajax({
                        type: "post",
                        url: 'http://contentapi.news.cn/ossUrlExist/',
                        data: {
                            url: audioSrc
                        },
                        success: function (data) {
                            console.log(data)
                            if (data) {
                                //console.log(data)
                                // $(this).addClass("isoundplay")
                                $(this).addClass("btn-audio-play");
                                $("#audioDom").attr("src", audioSrc);
                                $("#audioDom")[0].play();
                                $(".btn-audio").addClass("btn-audio-play");
                            } else {
                                alert("音频正在合成中，请稍后")
                            }

                        },
                        error: function () {
                            alert("音频正在合成中，请稍后")
                        }
                    });

                }
            })
        },
        scrollSet: function () {
            //var videoPos = $(".main-right .video").offset().top;
            //console.log(videoPos)
            $(window).scroll(function () {
                var _this = $(this);
                if (_this.scrollTop() > (pageShareTop)) {
                    $(".head-line h1").addClass("topFixed")
                } else {
                    $(".head-line h1").removeClass("topFixed")
                }

                // if (_this.scrollTop() > videoPos) {
                // 	$(".main-right .video").addClass("fixVideo");
                // } else {
                // 	$(".main-right .video").removeClass("fixVideo");
                // }
            });
        },
        // nextpage: function () {
        // 	var url = 'http://so.news.cn/inter/getNextNews?siteIdXml=' + siteIdXml + '&nodeId=' + nodeId + '&fileUUID=' + fileUUID + '&releaseDate=' + releaseDate;
        // 	$.ajax({
        // 		type: "get",
        // 		async: false,
        // 		url: url,
        // 		dataType: "jsonp",
        // 		jsonp: "callback",
        // 		success: function (json) {
        // 			console.log("下一篇返回数据：", json)
        // 			if (json.content.result !== null) {
        // 				$(".nextpage-cont a").html(json.content.result.title);
        // 				$(".nextpage-cont a").attr("href", json.content.result.originUrl[0]);
        // 			}
        // 		},
        // 		error: function (e) {
        // 			console.log(e)
        // 		}
        // 	});
        // }
    }
    detail.init();

    /* 分页调用 */
    parsePagingFun({
        // preText: 'prev',//上一页
        // nextText: 'next',//下一页
        id: 'detailContent', //正文分页id
        num: 8 //显示页码数个数
    })

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
})