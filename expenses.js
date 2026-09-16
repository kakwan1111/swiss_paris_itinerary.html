/**
 * =========================================================================
 * KWAN & ELLA HONEYMOON EXPENSES CONFIGURATION FILE
 * =========================================================================
 * 精確預算配置文件（幣種：HKD）。
 * 數據已根據 2026 年瑞士交通最新票價與 Swiss Travel Pass (STP) 效益進行審核。
 */

const honeymoonExpenses = {
    currency: "HKD",
    exchangeRateCHF: 9.0, // 考慮 2026 匯率波動預留，1 CHF ≈ 9.0 HKD
    exchangeRateEUR: 8.5, // 1 EUR ≈ 8.5 HKD
    transportComparison: {
        travelers: 2,
        exchangeRateCHF: 9.0,
        estimatedOrdinarySwissTransportFullHKD: 8100,
        halfFareCard: { passHKD: 2700, ordinaryTransportHKD: 4050, totalHKD: 6750 },
        swissTravelPass15Day: { passHKD: 8982, ordinaryTransportHKD: 0, totalHKD: 8982 },
        differenceHKD: 2232,
        note: "只比較通行證及一般火車／巴士／船；山地活動、西庸城堡及座位預約另列，避免重複計算。"
    },
    passRecommendation: {
        recommended: "Swiss Half Fare Card",
        recommendedCostForTwoHKD: 2700,
        recommendedNote: "CHF 150/人；有效一個月，瑞士一般火車、巴士、船及大部分山地鐵路以半價購票。",
        alternative: "Swiss Travel Pass 15天二等座",
        alternativeCostForTwoHKD: 9000,
        alternativeNote: "CHF 499/人；連續15日一般公共交通無限搭乘，Rigi／Stanserhorn／Stoos包含，其他山地項目最高約50%折扣。",
        reason: "本路線沒有 Rigi，且大量山地景點兩種方案均需另按規則購票；Half Fare Card 預計較省，但每段要另買票。"
    },
    
    categories: [
        {
            id: "flights",
            name: "航機交通 (Flights & Trains)",
            icon: "✈️",
            color: "#6366f1",
            items: [
                { name: "法國航空香港往返巴黎/日內瓦", amount: 28500, note: "2人特選經濟/經濟艙連稅估算" },
                { name: "Swiss Half Fare Card（推薦，2人）", amount: 2700, note: "CHF 150/人；有效一個月，瑞士一般火車、巴士、船及大部分山地鐵路以半價購票。Swiss Travel Pass 15天二等座替代方案約 HKD 8,982/2人（CHF 499/人 × 2 × HKD 9），未計入本總額。" }
            ]
        },
        {
            id: "hotels",
            name: "奢華住宿 (Accommodation)",
            icon: "🏨",
            color: "#B8975D",
            items: [
                { name: "D1-D3 巴黎：Quinzerie Hotel (3晚)", amount: 9800, note: "巴黎住宿預算；實際房價按入住日確認" },
                { name: "D4 蘇黎世：Crowne Plaza Zurich by IHG (1晚)", amount: 5500, note: "蘇黎世住宿預算；實際房價按入住日確認" },
                { name: "D5 琉森：Holiday Inn Express Luzern - Kriens by IHG (1晚)", amount: 3600, note: "Kriens 住宿預算；實際房價按入住日確認" },
                { name: "D6-D7 Wilderswil：Airbnb Chalet Allmihus - Apt. A (2晚)", amount: 7200, note: "按您提供的 Airbnb 房源；請以 2026/9/24–9/26、2位旅客重新查價" },
                { name: "D8-D9 Airbnb 房源 #45421438 (2晚)", amount: 9000, note: "用戶提供 2026/9/28–10/3 連結；房源名稱、位置及 2位旅客實際價格待確認" },
                { name: "D10 Adelboden：The Cambrian Adelboden (1晚)", amount: 7200, note: "Adelboden 山景酒店及 SPA 預算；實際房價按入住日確認" },
                { name: "D11-D13 策馬特：Resort La Ginabelle (3晚)", amount: 16500, note: "連住 3 晚；五星頂級水療度假村預算，實際房價按入住日確認" },
                { name: "D14 洛桑：Royal Savoy Hotel & Spa (1晚)", amount: 6800, note: "豪華酒店及 SPA 預算；實際房價按入住日確認" },
                { name: "D15 日內瓦：Hôtel Longemalle (日間／1晚待確認)", amount: 4600, note: "離境日可作行李寄存或短暫休息；是否留宿待確認" }
            ]
        },
        {
            id: "photography",
            name: "海外婚紗拍攝 (Wedding Photo)",
            icon: "💍",
            color: "#ec4899",
            items: [
                { name: "巴黎海外婚紗攝影團隊 (D2)", amount: 22000, note: "含攝影師、造型師、全日跟拍" },
                { name: "格林德瓦高山婚紗拍攝 (D7)", amount: 24000, note: "含艾格峰/夢幻山坡雪山外景" },
                { name: "婚紗西裝租借、運送與防皺保養", amount: 6000, note: "國際運送及專業護理" }
            ]
        },
        {
            id: "activities",
            name: "景點門票與登山纜車 (Activities)",
            icon: "⛰️",
            color: "#10b981",
            items: [
                { name: "D5 瑞士蓮巧克力之家 Lindt Home", amount: 550, note: "2人入場體驗 (STP 無折扣)" },
                { name: "D6 皮拉圖斯峰 Pilatus", amount: 2200, note: "2人往返交通及登山票估算；Swiss Half Fare Card／Swiss Travel Pass 效益按所選路線與票種確認" },
                { name: "D8 First + 勞特布龍嫩／米倫一日交通", amount: 1800, note: "2人纜車、區域鐵路及山地接駁估算；Half Fare Card／Swiss Travel Pass 折扣依實際路線確認" },
                { name: "D9 伊瑟爾特瓦爾德與哈德昆交通", amount: 1000, note: "2人布里恩茨湖區交通及觀景台接駁估算；Swiss Travel Pass 覆蓋／折扣依路線確認" },
                { name: "D10 Adelboden 村落／The Cambrian SPA", amount: 900, note: "2人 Adelboden 村落、山景及酒店休閒活動估算" },
                { name: "D11 Adelboden → 策馬特轉移及村內活動", amount: 500, note: "由 Adelboden 轉往策馬特後的村內活動預算" },
                { name: "D12 Gornergrat 登山火車", amount: 1100, note: "2人往返估算；Half Fare Card／Swiss Travel Pass 按營運公司規則享折扣" },
                { name: "D13 五湖短線＋Zermatt → Aigle", amount: 1350, note: "上午 Blauherd／Sunnegga 五湖短線纜車及交通，下午 Zermatt → Aigle 區域交通；Glacier 3000 改列 D14" },
                { name: "D14 Glacier 3000＋西庸城堡＋洛桑轉移", amount: 2600, note: "2人城堡入場、Montreux／Veytaux-Chillon 及 Lausanne 湖畔活動預算；城堡門票另購" },
                { name: "其他活動 (塞納河遊船等)", amount: 2200, note: "含部分 STP 覆蓋及付費項目" }
            ]
        },
        {
            id: "dining",
            name: "餐飲與米其林體驗 (Dining)",
            icon: "🍽️",
            color: "#f59e0b",
            items: [
                { name: "巴黎米其林/法式浪漫晚宴", amount: 5800, note: "精選高檔法式料理·含酒水" },
                { name: "瑞士特色餐飲與高山美饌", amount: 7200, note: "15天日常餐飲、起司火鍋等" }
            ]
        },
        {
            id: "shopping",
            name: "購物與雜費預備金 (Shopping & Misc)",
            icon: "🛍️",
            color: "#8b5cf6",
            items: [
                { name: "精品購物與紀念品退稅預算", amount: 18000, note: "巴黎/日內瓦名品購物預留" },
                { name: "市內交通、小費與雜費", amount: 5000, note: "含 STP 未覆蓋之市區巴士/地鐵" }
            ]
        }
    ]
};
