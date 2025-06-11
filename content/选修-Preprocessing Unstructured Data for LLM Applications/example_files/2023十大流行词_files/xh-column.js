// var domainNameArr = [{
//         "name": "http://cx.",
//         "sKey": "cx"
//     },
//     {
//         "name": "http://education.",
//         "sKey": "edu"
//     },
//     {
//         "name": "http://uav.",
//         "sKey": "uav"
//     },
//     {
//         "name": "http://m.news.cn",
//         "sKey": "sjb"
//     },
//     {
//         "name": "http://us.",
//         "sKey": "us"
//     },
//     {
//         "name": "http://www.news.cn/20",
//         "sKey": "newscenter"
//     },
//     {
//         "name": "http://travel.",
//         "sKey": "travel"
//     }
// ];
var arrChannel = [{
        sKey: "politicspro",
        sValue: "时政",
        sUrl: "http://www.news.cn/politicspro/",
        sIdx: 1
    }, {
        sKey: "worldpro",
        sValue: "国际",
        sUrl: "http://www.news.cn/worldpro/",
        sIdx: 2
    }, {
        sKey: "fortunepro",
        sValue: "财经",
        sUrl: "http://www.news.cn/fortunepro/",
        sIdx: 3
    }, {
        sKey: "videopro",
        sValue: "视频",
        sUrl: "http://www.news.cn/videopro/",
        sIdx: 4
    }, {
        sKey: "multimediapro",
        sValue: "富媒体",
        sUrl: "http://www.news.cn/multimediapro/",
        sIdx: 5
    }, {
        sKey: "techpro",
        sValue: "科技",
        sUrl: "http://www.news.cn/techpro/",
        sIdx: 6
    }, {
        sKey: "culturepro",
        sValue: "文化",
        sUrl: "http://www.news.cn/culturepro/",
        sIdx: 7
    }, {
        sKey: "healthpro",
        sValue: "健康",
        sUrl: "http://www.news.cn/healthpro/",
        sIdx: 8
    }, {
        sKey: "milpro",
        sValue: "军事",
        sUrl: "http://www.news.cn/milpro/",
        sIdx: 9
    }, {
        sKey: "sikepro",
        sValue: "思客智库",
        sUrl: "http://www.news.cn/sikepro/",
        sIdx: 10
    }, {
        sKey: "governmentpro",
        sValue: "政务",
        sUrl: "http://www.news.cn/governmentpro/",
        sIdx: 11
    }, {
        sKey: "businesspro",
        sValue: "商务",
        sUrl: "http://www.news.cn/businesspro/",
        sIdx: 12
    }, {
        sKey: ".cn/20",
        sValue: "新闻",
        sUrl: "http://www.news.cn/"
    }, {
        sKey: ".com/20",
        sValue: "新闻",
        sUrl: "http://www.news.cn/"
    }, {
        sKey: "politics",
        sValue: "时政",
        sUrl: "http://www.news.cn/politics/"
    }, {
        sKey: "politics/xhll",
        sValue: "理论",
        sUrl: "http://www.news.cn/politics/xhll/"
    }, {
        sKey: "comments",
        sValue: "网评",
        sUrl: "http://www.news.cn/comments/"
    }, {
        sKey: "legal",
        sValue: "法治",
        sUrl: "http://www.news.cn/legal/"
    }, {
        sKey: "politics/rs",
        sValue: "人事",
        sUrl: "http://www.news.cn/politics/xhrs/"
    }, {
        sKey: "legal/ffu",
        sValue: "廉政",
        sUrl: "http://www.news.cn/legal/ffu.htm?page=xhlz"
    }, {
        sKey: "local",
        sValue: "地方",
        sUrl: "http://www.news.cn/local/"
    }, {
        sKey: "gangao",
        sValue: "港澳",
        sUrl: "http://www.news.cn/gangao/"
    }, {
        sKey: "tw",
        sValue: "台湾",
        sUrl: "http://www.news.cn/tw/"
    }, {
        sKey: "edu",
        sValue: "教育",
        sUrl: "http://education.news.cn/"
    }, {
        sKey: "sports",
        sValue: "体育",
        sUrl: "http://sports.news.cn/"
    }, {
        sKey: "live",
        sValue: "直播",
        sUrl: "http://www.news.cn/live/"
    }, {
        sKey: "talking",
        sValue: "新华访谈",
        sUrl: "http://www.news.cn/talking/"
    }, {
        sKey: "datanews",
        sValue: "数据新闻",
        sUrl: "http://www.news.cn/datanews/index.htm"
    }, {
        sKey: "photo",
        sValue: "图片",
        sUrl: "http://www.news.cn/photo/index.htm"
    }, {
        sKey: "video/xinhuaradio",
        sValue: "广播",
        sUrl: "http://www.news.cn/video/xinhuaradio/"
    }, {
        sKey: "uav",
        sValue: "无人机",
        sUrl: "http://uav.news.cn/"
    }, {
        sKey: "silkroad",
        sValue: "一带一路",
        sUrl: "http://www.news.cn/silkroad/"
    }, {
        sKey: "info",
        sValue: "信息化",
        sUrl: "http://www.news.cn/info/"
    }, {
        sKey: "politics/zywj",
        sValue: "中央文件",
        sUrl: "http://www.news.cn/politics/zywj/index.htm"
    }, {
        sKey: "money",
        sValue: "金融",
        sUrl: "http://www.news.cn/money/"
    }, {
        sKey: "finance",
        sValue: "上市公司",
        sUrl: "http://www.news.cn/finance/"
    }, {
        sKey: "auto",
        sValue: "汽车",
        sUrl: "http://www.news.cn/auto/"
    }, {
        sKey: "food",
        sValue: "食品",
        sUrl: "http://www.news.cn/food/"
    }, {
        sKey: "house",
        sValue: "人居生活",
        sUrl: "http://www.news.cn/house/"
    }, {
        sKey: "travel",
        sValue: "旅游",
        sUrl: "http://www.news.cn/travel/"
    }, {
        sKey: "energy",
        sValue: "能源",
        sUrl: "http://www.news.cn/energy/"
    }, {
        sKey: "enterprise",
        sValue: "公司",
        sUrl: "http://www.news.cn/enterprise/"
    }, {
        sKey: "expo",
        sValue: "会展",
        sUrl: "http://www.news.cn/expo/"
    }, {
        sKey: "caipiao",
        sValue: "彩票",
        sUrl: "http://www.news.cn/caipiao/"
    }, {
        sKey: "ent/",
        sValue: "娱乐",
        sUrl: "http://www.news.cn/ent/"
    }, {
        sKey: "fashion",
        sValue: "时尚",
        sUrl: "http://www.news.cn/fashion/"
    }, {
        sKey: "book",
        sValue: "悦读",
        sUrl: "http://www.news.cn/book/"
    }, {
        sKey: "gongyi",
        sValue: "公益",
        sUrl: "http://www.news.cn/gongyi/"
    }, {
        sKey: "shuhua",
        sValue: "书画",
        sUrl: "http://www.news.cn/shuhua/"
    }, {
        sKey: "foto",
        sValue: "摄影",
        sUrl: "http://www.news.cn/foto/"
    }, {
        sKey: "asia/chinese",
        sValue: "亚太网",
        sUrl: "http://www.news.cn/asia/chinese/"
    }, {
        sKey: "sg",
        sValue: "新加坡频道",
        sUrl: "http://sg.news.cn/"
    }, {
        sKey: "info/xbsyzg",
        sValue: "溯源中国",
        sUrl: "http://www.news.cn/info/xbsyzg/"
    }, {
        sKey: "finance/tjjd",
        sValue: "投教基地",
        sUrl: "http://www.news.cn/finance/tjjd/"
    },
    {
        sKey: "newscenter",
        sValue: "新闻中心",
        sUrl: "http://www.news.cn/newscenter/index.htm"
    },
    {
        sKey: "hr",
        sValue: "人才",
        sUrl: "http://www.news.cn/hr/index.htm"
    },
    {
        sKey: "ziliao",
        sValue: "资料",
        sUrl: "http://www.news.cn/ziliao/index.htm"
    },
    {
        sKey: "legal",
        sValue: "法治",
        sUrl: "http://www.news.cn/legal/"
    },
    {
        sKey: "local",
        sValue: "地方",
        sUrl: "http://www.news.cn/local/"
    },
    {
        sKey: "book",
        sValue: "悦读",
        sUrl: "http://www.news.cn/book/"
    },
    {
        sKey: "world",
        sValue: "国际",
        sUrl: "http://www.news.cn/world/"
    },
    {
        sKey: "overseas",
        sValue: "海外华人",
        sUrl: "http://www.news.cn/overseas/"
    },
    {
        sKey: "gangao",
        sValue: "港澳",
        sUrl: "http://www.news.cn/gangao/"
    },
    {
        sKey: "tw",
        sValue: "台湾",
        sUrl: "http://www.news.cn/tw/"
    },
    {
        sKey: "mil",
        sValue: "军事",
        sUrl: "http://news.cn/milpro/"
    },
    {
        sKey: "culture",
        sValue: "文化",
        sUrl: "http://www.news.cn/culture/"
    },
    {
        sKey: "fortune",
        sValue: "财经",
        sUrl: "http://www.news.cn/fortune/"
    },
    {
        sKey: "money",
        sValue: "金融",
        sUrl: "http://www.news.cn/money/"
    },
    {
        sKey: "caipiao",
        sValue: "彩票",
        sUrl: "http://www.news.cn/caipiao/"
    },
    {
        sKey: "jiaju",
        sValue: "家居",
        sUrl: "http://www.news.cn/jiaju/"
    },
    {
        sKey: "gongyi",
        sValue: "公益",
        sUrl: "http://www.news.cn/gongyi/"
    },
    {
        sKey: "futures",
        sValue: "期货",
        sUrl: "http://www.news.cn/futures/index.htm"
    },
    {
        sKey: "finance",
        sValue: "上市公司",
        sUrl: "http://www.news.cn/finance/"
    },
    {
        sKey: "auto",
        sValue: "汽车",
        sUrl: "http://www.news.cn/auto/"
    },
    {
        sKey: "edu",
        sValue: "教育",
        sUrl: "http://education.news.cn/"
    },
    {
        sKey: "abroad",
        sValue: "出国",
        sUrl: "http://www.news.cn/abroad/index.htm"
    },
    {
        sKey: "food",
        sValue: "食品",
        sUrl: "http://www.news.cn/food/"
    },
    {
        sKey: "tea",
        sValue: "茶叶",
        sUrl: "http://www.news.cn/tea/index.htm"
    },
    {
        sKey: "air",
        sValue: "航空",
        sUrl: "http://www.news.cn/air/index.htm"
    },
    {
        sKey: "tech",
        sValue: "科技",
        sUrl: "http://www.news.cn/tech/"
    },
    {
        sKey: "jiadian",
        sValue: "家电",
        sUrl: "http://www.news.cn/jiadian/index.htm"
    },
    {
        sKey: "health",
        sValue: "健康",
        sUrl: "http://www.news.cn/health/"
    },
    {
        sKey: "environment",
        sValue: "环保",
        sUrl: "http://www.news.cn/environment/index.htm"
    },
    {
        sKey: "coal",
        sValue: "煤炭",
        sUrl: "http://www.news.cn/coal/index.htm"
    },
    {
        sKey: "power",
        sValue: "电力",
        sUrl: "http://www.news.cn/power/"
    },
    {
        sKey: "energy",
        sValue: "能源",
        sUrl: "http://www.news.cn/energy/"
    },
    {
        sKey: "shuhua",
        sValue: "书画",
        sUrl: "http://www.news.cn/shuhua/"
    },
    {
        sKey: "collection",
        sValue: "收藏",
        sUrl: "http://www.news.cn/collection/index.htm"
    },
    {
        sKey: "travel",
        sValue: "旅游",
        sUrl: "http://www.news.cn/travel/"
    },
    {
        sKey: "fashion",
        sValue: "时尚",
        sUrl: "http://www.news.cn/fashion/"
    },
    {
        sKey: "city",
        sValue: "城市",
        sUrl: "http://city.news.cn/"
    },
    {
        sKey: "sports",
        sValue: "体育",
        sUrl: "http://sports.news.cn/"
    },
    {
        sKey: "insurance",
        sValue: "保险",
        sUrl: "http://www.news.cn/insurance/"
    },
    {
        sKey: "expo",
        sValue: "会展",
        sUrl: "http://www.news.cn/expo/"
    },
    {
        sKey: "xiangtu",
        sValue: "新闻中心",
        sUrl: "http://www.news.cn/xiangtu/"
    },
    {
        sKey: "info",
        sValue: "信息化",
        sUrl: "http://www.news.cn/info/"
    },
    {
        sKey: "zhcs",
        sValue: "智慧城市",
        sUrl: "http://www.news.cn/zhcs/index.htm"
    },
    {
        sKey: "yuqing",
        sValue: "舆情",
        sUrl: "http://www.news.cn/yuqing/"
    },
    {
        sKey: "newmedia",
        sValue: "传媒",
        sUrl: "http://www.news.cn/newmedia/"
    },
    {
        sKey: "video",
        sValue: "视频",
        sUrl: "http://www.news.cn/video/"
    },
    {
        sKey: "foto",
        sValue: "摄影",
        sUrl: "http://www.news.cn/foto/"
    },
    {
        sKey: "house",
        sValue: "人居生活",
        sUrl: "http://www.news.cn/house/"
    },
    {
        sKey: "forum",
        sValue: "论坛",
        sUrl: "http://forum.home.news.cn/list/50-0-0-1.html"
    },
    {
        sKey: "silkroad",
        sValue: "一带一路",
        sUrl: "http://www.news.cn/silkroad/"
    },
    {
        sKey: "yzyd/politics",
        sValue: "时政",
        sUrl: "http://www.news.cn/politics/"
    },
    {
        sKey: "yzyd/comments",
        sValue: "网评",
        sUrl: "http://www.news.cn/comments/"
    },
    {
        sKey: "yzyd/newscenter",
        sValue: "新闻中心",
        sUrl: "http://www.news.cn/newscenter/index.htm"
    },
    {
        sKey: "yzyd/legal",
        sValue: "法治",
        sUrl: "http://www.news.cn/legal/"
    },
    {
        sKey: "yzyd/local",
        sValue: "地方",
        sUrl: "http://www.news.cn/local/"
    },
    {
        sKey: "yzyd/book",
        sValue: "悦读",
        sUrl: "http://www.news.cn/book/"
    },
    {
        sKey: "yzyd/world",
        sValue: "国际",
        sUrl: "http://www.news.cn/world/"
    },
    {
        sKey: "yzyd/overseas",
        sValue: "海外华人",
        sUrl: "http://www.news.cn/overseas/"
    },
    {
        sKey: "yzyd/gangao",
        sValue: "港澳",
        sUrl: "http://www.news.cn/gangao/"
    },
    {
        sKey: "yzyd/tw",
        sValue: "台湾",
        sUrl: "http://www.news.cn/tw/"
    },
    {
        sKey: "yzyd/mil",
        sValue: "军事",
        sUrl: "http://news.cn/milpro/"
    },
    {
        sKey: "yzyd/fortune",
        sValue: "财经",
        sUrl: "http://www.news.cn/fortune/"
    },
    {
        sKey: "yzyd/jiaju",
        sValue: "家居",
        sUrl: "http://www.news.cn/jiaju/"
    },
    {
        sKey: "yzyd/finance",
        sValue: "金融",
        sUrl: "http://www.news.cn/money/"
    },
    {
        sKey: "yzyd/auto",
        sValue: "汽车",
        sUrl: "http://www.news.cn/auto/"
    },
    {
        sKey: "yzyd/edu",
        sValue: "教育",
        sUrl: "http://education.news.cn"
    },
    {
        sKey: "yzyd/food",
        sValue: "食品",
        sUrl: "http://www.news.cn/food/"
    },
    {
        sKey: "yzyd/tech",
        sValue: "科技",
        sUrl: "http://www.news.cn/tech/"
    },
    {
        sKey: "yzyd/jiadian",
        sValue: "家电",
        sUrl: "http://www.news.cn/jiadian/index.htm"
    },
    {
        sKey: "yzyd/health",
        sValue: "健康",
        sUrl: "http://www.news.cn/health/"
    },
    {
        sKey: "yzyd/energy",
        sValue: "能源",
        sUrl: "http://www.news.cn/energy/"
    },
    {
        sKey: "yzyd/travel",
        sValue: "旅游",
        sUrl: "http://www.news.cn/travel/"
    },
    {
        sKey: "yzyd/fashion",
        sValue: "时尚",
        sUrl: "http://www.news.cn/fashion/"
    },
    {
        sKey: "yzyd/ent",
        sValue: "娱乐",
        sUrl: "http://www.news.cn/ent/"
    },
    {
        sKey: "yzyd/foto",
        sValue: "摄影",
        sUrl: "http://www.news.cn/foto/"
    },
    {
        sKey: "yzyd/house",
        sValue: "人居生活",
        sUrl: "http://www.news.cn/house/"
    },
    {
        sKey: "japan",
        sValue: "日本频道",
        sUrl: "http://japan.news.cn/"
    },
    {
        sKey: "koreas",
        sValue: "韩国频道",
        sUrl: "http://korea.news.cn/"
    },
    {
        sKey: "drone",
        sValue: "无人机",
        sUrl: "http://www.news.cn/drone/"
    },
    {
        sKey: "vr/",
        sValue: "VR/AR",
        sUrl: "http://www.news.cn/vr/"
    },
    {
        sKey: "photo",
        sValue: "图片",
        sUrl: "http://www.news.cn/photo/"
    },
    {
        sKey: "cx.news.cn",
        sValue: "双创",
        sUrl: "http://cx.news.cn/"
    },
    {
        sKey: "zgly",
        sValue: "中国旅游新闻",
        sUrl: "http://zgly.news.cn/"
    },
    {
        sKey: "talking",
        sValue: "新华访谈",
        sUrl: "http://www.news.cn/talking/"
    },
    {
        sKey: "us.news.cn",
        sValue: "美国频道",
        sUrl: "http://us.news.cn/index.htm"
    },
    {
        sKey: "science",
        sValue: "科普",
        sUrl: "http://www.news.cn/science/"
    },
    {
        sKey: "itown",
        sValue: "互联网小镇",
        sUrl: "http://www.news.cn/itown/index.htm"
    },
    {
        sKey: "yingjijiuyuan",
        sValue: "应急救援",
        sUrl: "http://www.news.cn/yingjijiuyuan/index.htm"
    },
    {
        sKey: "enterprise",
        sValue: "公司",
        sUrl: "http://www.news.cn/enterprise/"
    },
    {
        sKey: "ci/",
        sValue: "文化产业",
        sUrl: "http://www.news.cn/ci/"
    },
    {
        sKey: "app/",
        sValue: "政企服务",
        sUrl: "http://www.news.cn/"
    }, {
        sKey: "government/",
        sValue: "政务",
        sUrl: "http://www.news.cn/government/"
    },
];