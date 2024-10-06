"use strict";

/* 微信分享 */
function wxConfig(config) {
  console.log(config);
  var url = 'http://api.home.news.cn/wx/jsapi.do';
  $.ajax({
    url: url,
    type: 'get',
    // 设置的是请求参数
    data: {
      // mpId: 356,
      mpId: 390,
      url: window.location.href
    },
    dataType: 'jsonp',
    success: function success(res) {
      console.log(res);

      if (res.code === 200) {
        window.wx.config({
          debug: false,
          // 开启调试模式,调用的所有api的返回值会在客户端// alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
          appId: res.content.appId,
          // 必填，公众号的唯一标识
          timestamp: res.content.timestamp,
          // 必填，生成签名的时间戳
          nonceStr: res.content.nonceStr,
          // 必填，生成签名的随机串
          signature: res.content.signature,
          // 必填，签名，见附录1
          jsApiList: ['updateAppMessageShareData', 'updateTimelineShareData', 'chooseImage', 'getLocalImgData'] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2

        }); // config.callback && config.callback(config.data)

        wxReady(config);
      }
    }
  });
}

function wxReady(config) {
  window.wx.ready(function () {
    // window.global.canUse = true
    // alert('can')
    // alert(config.imgUrl)
    // 自定义“分享给朋友”及“分享到QQ”按钮的分享内容
    window.wx.updateAppMessageShareData({
      title: config.title,
      desc: config.desc,
      link: config.link,
      imgUrl: config.imgUrl
    }); // 自定义“分享到朋友圈”及“分享到QQ空间”按钮的分享内容

    window.wx.updateTimelineShareData({
      title: config.title,
      link: config.link,
      imgUrl: config.imgUrl
    });
  });
}
//# sourceMappingURL=maps/share.js.map
