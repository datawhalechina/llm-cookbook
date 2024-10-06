
var footLibStyle =   '<style>'+
                        '.lib-foot{margin-top:40px;padding:20px 0;font-size:14px;line-height:26px;text-align:center;color:#fff;background:#024ac2}@media screen and (max-width: 768px) {.lib-foot {margin-top: 10px;font-size:12px}}'+
                      '</style>'
var footLibDom =   '<div class="lib-foot">'+
                      '<p>Copyright © 2000 - ' + new Date().getFullYear() + ' XINHUANET.com　All Rights Reserved.</p>'+
                      '<p>制作单位：新华网股份有限公司　　版权所有：新华网股份有限公司</p>'+
                    '</div>'


$('body').append(footLibStyle + footLibDom)
