/**
 * =========================================================================
 * KWAN & ELLA HONEYMOON EXPENSES CONFIGURATION FILE
 * =========================================================================
 * 精確預算配置文件（幣種：HKD）。
 * 您可以隨時在此檔案中修改各項費用，儲存後重新整理網頁即可自動更新！
 */

const honeymoonExpenses = {
    currency: "HKD",
    exchangeRateCHF: 8.8, // 1 CHF 約等於 8.8 HKD
    exchangeRateEUR: 8.5, // 1 EUR 約等於 8.5 HKD
    
    categories: [
        {
            id: "flights",
            name: "航機交通 (Flights & Trains)",
            icon: "✈️",
            color: "#6366f1",
            items: [
                { name: "法國航空香港往返巴黎/日內瓦 (長途+歐陸航段)", amount: 28500, note: "2人特選經濟/經濟艙連稅估算" },
                { name: "瑞士交通通行證 Swiss Travel Pass (15天二等座)", amount: 10800, note: "2人同行·含全境無限次火車、巴士、船及登山優惠" }
            ]
        },
        {
            id: "hotels",
            name: "奢華住宿 (Accommodation)",
            icon: "🏨",
            color: "#B8975D",
            items: [
                { name: "D1-D3 巴黎：Villa Alessandra Hotel (3晚)", amount: 9800, note: "凱旋門附近優選精品房含早" },
                { name: "D4 蘇黎世：Storchen Zürich (1晚)", amount: 5500, note: "利馬特河畔豪華景觀房" },
                { name: "D5 琉森瑞吉山：Rigi Kaltbad (1晚)", amount: 6200, note: "含山頂無邊際溫泉及早晚餐" },
                { name: "D6-D7 格林德瓦：Hotel Spinne (2晚)", amount: 11000, note: "艾格峰景觀設計房含早" },
                { name: "D8 藍湖：Blausee Alpine Lodge (1晚)", amount: 4800, note: "水晶藍湖畔特色湖景房" },
                { name: "D9 因特拉肯：Private Pool Room (1晚)", amount: 3500, note: "私人泳池特色浪漫民宿" },
                { name: "D10-D12 策馬特：Resort La Ginabelle (3晚)", amount: 16500, note: "五星頂級水療度假村·馬特洪峰景" },
                { name: "D13 洛桑：Château d'Ouchy (1晚)", amount: 5800, note: "萊芒湖畔歷史城堡飯店" },
                { name: "D14-D15 日內瓦：Hôtel Longemalle (2晚)", amount: 9200, note: "市中心五星級精品房" }
            ]
        },
        {
            id: "photography",
            name: "海外婚紗拍攝 (Wedding Photo)",
            icon: "💍",
            color: "#ec4899",
            items: [
                { name: "巴黎海外婚紗攝影團隊 (D2)", amount: 22000, note: "含專業攝影師、造型師、全日跟拍" },
                { name: "格林德瓦高山婚紗拍攝 (D7)", amount: 24000, note: "含艾格峰/夢幻山坡雪山外景跟拍" },
                { name: "婚紗西裝租借、運送與防皺保養", amount: 6000, note: "國際婚紗運送及防皺護理" }
            ]
        },
        {
            id: "activities",
            name: "景點門票與登山纜車 (Activities)",
            icon: "⛰️",
            color: "#10b981",
            items: [
                { name: "少女峰登頂套票 (Jungfraujoch)", amount: 5200, note: "2人同行·含冰宮與觀景台 (Pass 5折優惠)" },
                { name: "Gornergrat & 冰川天堂纜車票", amount: 5800, note: "3,883m 冰川天堂及觀景台 (Pass 5折優惠)" },
                { name: "塞納河遊船晚餐 & 哈德昆觀景台", amount: 3200, note: "浪漫餐飲與觀光纜車往返" }
            ]
        },
        {
            id: "dining",
            name: "餐飲與米其林體驗 (Dining)",
            icon: "🍽️",
            color: "#f59e0b",
            items: [
                { name: "巴黎米其林/法式浪漫晚宴", amount: 5800, note: "精選高檔法式料理·含酒水" },
                { name: "瑞士起司火鍋、烤起司與高山美饌", amount: 7200, note: "15天日常餐飲·Fondue、Raclette、高山餐廳" }
            ]
        },
        {
            id: "shopping",
            name: "購物與雜費預備金 (Shopping & Misc)",
            icon: "🛍️",
            color: "#8b5cf6",
            items: [
                { name: "精品購物與紀念品退稅預算", amount: 18000, note: "巴黎香榭麗舍/日內瓦Rue du Rhône精品購物" },
                { name: "市內交通、纜車、小費及零散支出", amount: 5000, note: "地鐵、計程車、行李運送及雜費" }
            ]
        }
    ]
};
