'use strict';

function parsePagingFun(data) {
    /**
     * id : content 父元素id
     * preText、nextText： 上一页下一页显示内容
     * num： 当前显示多少分页按钮。
     * **/

    // console.log("fenyehanshu:")
    var domId = data.id || 'content'; // content 包裹内容容器id
    var preText = data.preText || '上一页';
    var nextText = data.nextText || '下一页';
    var isShowPicButton = data.showPicButton || false;

    var q = window.location.search.substr(1).split('&');
    // 根据 URL 获取当前读取的是第几页
    var params = {};
    for (var i = 0; i < q.length; i++) {
        var val = q[i];
        var e = val.split('=');
        params[e[0]] = e[1];
    }
    var pageNum = parseInt(params['page'] || 1); // 当前页

    var contentElem = document.getElementById(domId);

    // 样式
    var aStyle = {
        'display': 'inline-block',
        'padding': '0 10px',
        'height': '26px',
        'fontSize': '12px',
        'color': '#818181',
        'textAlign': 'center',
        'lineHeight': '26px',
        'backgroundColor': '#F1F3F5',
        'textDecoration': 'none',
        'margin': '0 3px',
        'cursor': 'pointer'
    };

    var spanStyle = {
        'display': 'inline-block',
        'width': '26px',
        'height': '26px',
        'fontSize': '12px',
        'fontWeight': '600',
        'color': '#FFF',
        'textAlign': 'center',
        'lineHeight': '26px',
        'backgroundColor': '#348CEC',
        'margin': '0 3px'
    };

    var num = data.num || 10; // 固定分页 每次显示


    var html = contentElem.innerHTML;
    // 兼容导入数据
    var imgReg = /<img.*?id="xinhuabreak".*?\/?>/gi;

    var pages = html.split(imgReg);
    if (pages.length == 1) {
        pages = html.split('<b style="display: none;">pagebreak</b>');
    }
    var pagesLen = pages.length;
    // console.log("pages",pages)
    // console.log("pagesLen",pagesLen)

    var curIndex = 0; // 分组 当前显示分页组

    if (pagesLen > 1) {
        if (pageNum < 1) {
            pageNum = 1;
        }
        if (pageNum > pagesLen) {
            pageNum = pagesLen;
        }

        // 当前页码数量 10页 为一页
        var arr = [];
        for (var index = 1; index <= pagesLen; index++) {
            arr.push(index);
        }
        var result = []; // 对分页进行拆分接收
        for (var i = 0; i < pagesLen; i += num) {
            result.push(arr.slice(i, i + num)); // 每10项分成一组        
        }

        var renderArr = [];
        for (var inde = 0; inde <= result.length - 1; inde++) {

            if (result[inde].indexOf(pageNum) != -1) {
                renderArr = result[inde];
                curIndex = inde;
                // throw new Error('结束循环')
            }
        }

        contentElem.innerHTML = pages[pageNum - 1];
        //翻页控件
        var pager = document.createElement('center');
        pager.className = 'xinhuaPager';
        var left = document.createElement('a');
        left.className = 'xinhuaLeftBtn';
        left.innerText = '|<<';
        pager.appendChild(left);
        var right = document.createElement('a');
        right.className = 'xinhuaRightBtn';
        right.innerText = '>>|';

        pager.addEventListener('click', function (evt) {
            evt = evt || window.event; //兼容ie

            var cName = evt.target.className; // 读取点击dom的 class
            var dom = document.getElementById('xinhuaPagerBox');

            // 切换分页
            if (cName == 'xinhuaLeftBtn') {
                curIndex -= 1;
                renderFun(result[curIndex], pageNum, dom);
            }
            if (cName == 'xinhuaRightBtn') {
                curIndex += 1;
                renderFun(result[curIndex], pageNum, dom);
            }
        }, false);

        for (var key in aStyle) {
            left.style[key] = aStyle[key];
            right.style[key] = aStyle[key];
        }
        if (pageNum > 1) {
            // 上一页
            var prev = document.createElement('a');
            for (var key in aStyle) {
                prev.style[key] = aStyle[key];
            }
            prev.href = window.location.pathname + '?page=' + (pageNum - 1);
            prev.innerText = preText;
            pager.appendChild(prev);
        }

        // 用来盛放 页码
        var pagerBox = document.createElement('span');
        pagerBox.setAttribute('id', 'xinhuaPagerBox');
        pager.appendChild(pagerBox);

        if (pageNum < pagesLen) {
            // 下一页
            var next = document.createElement('a');
            for (var key in aStyle) {
                next.style[key] = aStyle[key];
            }
            next.href = window.location.pathname + '?page=' + (pageNum + 1);
            next.innerText = nextText;
            pager.appendChild(next);
        }

        // console.log(111)
        pager.appendChild(right);
        renderFun(renderArr, pageNum, pagerBox);
        // console.log(222)

        contentElem.appendChild(pager);

        // 内容区域添加监听
        contentElem.addEventListener("click", function (evt) {
            evt = evt || window.event; //兼容ie
            var clickNode = evt.target;
            var parentNode = clickNode.parentNode;
            if (clickNode.nodeName === "IMG") {
                pageNum += 1;
                if (pageNum > pagesLen) {
                    pageNum = pagesLen;
                    return;
                }
                if (parentNode.nodeName === "A") {
                    // c_1310560642_2.htm
                    // 备份 a 标签地址
                    var copyHref = parentNode.href;
                    // 阻止 a 标签的默认跳转行为
                    parentNode.href = "javascript:;";
                    // 获取 地址的最后一位 匹配是否符合 cms分页规则
                    var hrefArr = copyHref.split('/');
                    var lastStr = hrefArr[hrefArr.length - 1];
                    // cms 分页规则  {c_1310560642_2.htm}
                    var reg = new RegExp("^c_1[1|2|3][0-9]+_[0-9]{0,3}.htm$");
                    // 符合规则直接跳转下一页
                    if (reg.test(lastStr)) {
                        window.location.href = window.location.pathname + '?page=' + pageNum;
                    } else {
                        // 不符合规则则继续跳转
                        parentNode.href = copyHref;
                    }
                } else {
                    window.location.href = window.location.pathname + '?page=' + pageNum;
                }
            }
        }, false);

        // 设置翻页按钮链接
        if (isShowPicButton) {
            setPicLink(pagesLen);
        }
    }

    // 渲染分页
    function renderFun(arr, pageNum, dom) {
        // console.log(333)
        dom.innerHTML = ""; // 置空当前dom 所有元素 下面重新渲染
        for (var _index = 0; _index < arr.length; _index++) {
            var ele = arr[_index];
            // 判断当前 是否是选中
            if (pageNum == ele) {
                var a = document.createElement('span');
                for (var key in spanStyle) {
                    a.style[key] = spanStyle[key];
                }
                a.innerText = ele;
                dom.appendChild(a);
            } else {
                var a = document.createElement('a');
                for (var key in aStyle) {
                    a.style[key] = aStyle[key];
                }
                a.href = window.location.pathname + '?page=' + ele;
                a.innerText = ele;
                dom.appendChild(a);
            }
        }

        setTimeout(function (params) {
            var totalNum = Math.ceil(pagesLen / num);
            var rightbtn = document.getElementsByClassName('xinhuaRightBtn')[0];
            var leftbtn = document.getElementsByClassName('xinhuaLeftBtn')[0];

            if (rightbtn && leftbtn) {
                // 判断如果是最后一页和第一页隐藏按钮 |<< ， >>|
                if (curIndex == totalNum - 1 || curIndex == 0) {
                    // rightbtn.style.display = 'none'
                    // console.log('1')
                    // 判断只有一页时
                    if (curIndex == 0) {
                        leftbtn.style.display = 'none';
                    } else {
                        leftbtn.style.display = 'inline-block';
                    }
                    if (curIndex == totalNum - 1) {
                        rightbtn.style.display = 'none';
                    } else {
                        rightbtn.style.display = 'inline-block';
                    }
                }
                // else if (curIndex == 0) {
                //     leftbtn.style.display = 'none'
                //     console.log('2')
                //     if (curIndex == totalNum - 1) {
                //         rightbtn.style.display = 'none'
                //     } else {
                //         rightbtn.style.display = 'inline-block'
                //     }
                // } 
                else {
                    leftbtn.style.display = 'inline-block';
                    rightbtn.style.display = 'inline-block';

                }
            }
        }, 0);


    }
}

function setPicLink(picLinkLenght) {
    if (!$(".xinhuaPager").length) {
        return false;
    }
    // console.log("picLinkLenght", picLinkLenght)
    var pageSrc = window.location.href;
    var pageSrcArr = pageSrc.split("?page=");
    var pageNum = 1;
    var leftLink = "";
    var rightLink = "";
    if (pageSrc.indexOf("page=") !== -1) { // 判断非第一页时，当前的页数
        pageNum = parseInt(pageSrc.substring(pageSrc.indexOf("page=") + 5, pageSrc.length));
    }
    // console.log("pageNum", pageNum)
    if (pageNum == 1) {
        // console.log("第一页")
        leftLink = pageSrcArr[0] + "?page=" + picLinkLenght;
        rightLink = pageSrcArr[0] + "?page=" + (pageNum + 1);
    } else if (pageNum == picLinkLenght) {
        // console.log("最后一页")
        leftLink = pageSrcArr[0] + "?page=" + (pageNum - 1);
        rightLink = pageSrcArr[0];
    } else {
        // console.log("中间页面")
        leftLink = pageSrcArr[0] + "?page=" + (pageNum - 1);
        rightLink = pageSrcArr[0] + "?page=" + (pageNum + 1);
    }
    // console.log("leftLink", leftLink)
    // console.log("rightLink", rightLink)
    $("#detail img").each(function (i) {
        if ($(this).attr("id") == "wxsharepic") {
            return false;
        }
        $(this).wrap("<div class='dask'></div>").parent().append("<a href='#' class='picleft'></a><a href='#' class='picright'></a>").parent().addClass("bigPic");
        this.style.cursor = "pointer";
        $(this).siblings(".picleft").attr("href", leftLink).siblings(".picright").attr("href", rightLink);
        // $(".dask").hover(function () {
        //     $(".dask .picleft,.dask .picright").show();
        // }, function () {
        //     $(".dask .picleft,.dask .picright").hide();
        // })
    });
}