var hasSwiper = false;
var cbDetailConfig = {
    detailAtlasDisplayPc: false, //设置点击图片显示图集
    detailAtlasDisplayMob: true,
    detailSetFontSizePc: true, //设置控制标题字号
    detailSetFontSizeMob: false,
    detailSetFontColorPc: true, //设置控制标题颜色
    detailSetFontColorMob: true,
}


$("script").each(function () {
    if ($(this).attr("src") && $(this).attr("src").indexOf("swiper") > -1) {
        hasSwiper = true
    }
})
if (!hasSwiper) {
    var xhHead = document.getElementsByTagName('head')[0];
    var xhScript = document.createElement('script');
    xhScript.type = 'text/javascript';
    xhScript.src = "https://imgs.news.cn/global/lib/swiper/swiper3.4.2/swiper.min.js";
    var xhCss = document.createElement('link');
    xhCss.rel = 'stylesheet';
    xhCss.href = "https://imgs.news.cn/global/lib/swiper/swiper3.4.2/swiper.min.css";
    xhHead.appendChild(xhScript);
    xhHead.appendChild(xhCss);
}

function detailAtlasDisplay() {

    var atlasStyle = "<style>.mobPicSwiper {width: 100%;height: 100%;position: fixed;top: 0;left: 0;right: 0;bottom: 0;background-color: #000;z-index: 999999;display: none;}.mobPicSwiper .swiper-slide {display: flex;justify-content: center;align-items: center;text-align: center;}.mobPicSwiper .swiper-slide img {max-width: 100%; height: auto;}.mobPicSwiper .swiper-pagination-fraction {color: #fff;}</style>"
    $('body').append(atlasStyle);

    $("#detailContent,#detail").on("click", "img", function () {
        console.log(22)
        var slide_lists = ""
        $("#detailContent img,#detail img").each(function () {
            var imgUrl = $(this).attr("src")
            if (imgUrl.indexOf("svg+xml") == -1 && imgUrl.indexOf("space.gif") == -1) {
                slide_lists += '<div class="swiper-slide"><img src="' + imgUrl + '" alt=""></div>';
            }
        })
        var swiperHtml =
            '<div class="mobPicSwiper swiper-container"><div class="swiper-wrapper">' +
            slide_lists + '</div><div class="swiper-pagination"></div></div>'
        $('body').append(swiperHtml);

        var actUrl = $(this).attr("src")
        $(".mobPicSwiper .swiper-slide").each(function () {
            var swiperImgsrc = $(this).find("img").attr("src");
            // console.log(swiperImgsrc.indexOf("svg+xml") == -1)
            if (swiperImgsrc.indexOf(actUrl) > -1) {
                var actIndex = $(this).index()
                mobPicSwiper(actIndex)
            }
        })
        $(".mobPicSwiper").on("click", function () {
            // var slide_lists = ""
            $(".mobPicSwiper").remove()
        })
    })

    function mobPicSwiper(actNb) {
        $(".mobPicSwiper").show()
        var _mobPicSwiper = new Swiper('.mobPicSwiper', {
            // autoHeight: true,
            initialSlide: actNb,
            pagination: '.mobPicSwiper .swiper-pagination',
            paginationType: 'fraction'
        });
    }
}

function detailSetFontSize() {
    if (cbDetailConfig.detailSetFont == false) {
        return false;
    }
    var titleSize = $.trim($("#fontsize").html());
    //设置字号
    if (titleSize != '') {
        $('.head-line .title').css({
            "font-size": titleSize + "px"
        });
    }
}

function detailSetFontColor() {
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
}

//执行函数位置
$(function () {
    ////正文图片点击弹出细览图集功能-通用js中的函数
    var isMobile = (/iPad|iPhone|Android|Windows Phone|Nokia/).test(navigator.userAgent); //当前访问设备为移动端
    if (isMobile) {
        if (cbDetailConfig.detailAtlasDisplayMob !== false) {
            console.log("detailAtlasDisplayMob")
            detailAtlasDisplay();
        }
        if (cbDetailConfig.detailSetFontSizeMob !== false) {
            console.log("detailSetFontSizeMob")
            detailSetFontSize();
        }
        if (cbDetailConfig.detailSetFontColorMob !== false) {
            console.log("detailSetFontColorMob")
            detailSetFontColor();
        }
    }
    if (!isMobile) {
        if (cbDetailConfig.detailAtlasDisplayPc !== false) {
            console.log("detailAtlasDisplayPc")
            detailAtlasDisplay();
        }
        if (cbDetailConfig.detailSetFontSizePc !== false) {
            console.log("detailSetFontSizePc")
            detailSetFontSize();
        }
        if (cbDetailConfig.detailSetFontColorPc !== false) {
            console.log("detailSetFontColorPc")
            detailSetFontColor();
        }
    }
})