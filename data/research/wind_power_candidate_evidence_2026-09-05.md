# 風電三角色公司證據候選池（2026-09-05）

本檔承接 `semiconductor_energy_theme_audit_2026-09-05.md` 的風電補齊批次，只查證尚未正式映射的候選，不直接寫入 `stock_theme_map.csv`。價格 PASS 不作為產業歸屬證據。

## 分類邊界

### `WIND_EQUIPMENT` 風電設備

- 納入：公司直接製造或明確供應風機、葉片材料、塔架／水下基礎、風電變流器、風機用變壓器或其他風電專用設備與材料。
- 排除：只有一般重電、鋼材、機電或再生能源產品，未能證明實際用於風電者。

### `WIND_SERVICE` 風場工程維運

- 納入：公司或其受控制事業直接執行風場規劃、EPC、海事施工、輸變電工程、風機安裝或風場長期運維。
- 排除：只供應設備或泛稱能源工程，未能證明風電專案服務者。

### `WIND_OPERATION` 風場開發營運

- 納入：公司或其受控制事業持有風場開發權、投資／持有風力發電案場，或實際經營風力發電。
- 排除：只做工程、設備、綠電交易，或風電僅停留在未具體化的可能業務者。

控股公司可以因受控制子公司的實際業務取得集團曝險標籤，但須明列「透過子公司」角色，不能把母公司描述成直接承攬或直接持有案場。

## `WIND_EQUIPMENT` 查證結果

| 股票 | 公司角色與主要證據 | 證據強度 | 判定 |
|---|---|---|---|
| 1503 士電 | [公司官方消息](https://www.seec.com.tw/Content/NewsLetter/contents.aspx?MSID=1163476642103520334&MmmID=655355404322064661&SSize=10&SiteID=10)可證明 CIP、Vestas 曾參訪重電廠並肯定合作，但未指出士電實際供應的風電專用產品、規格或訂單 | medium | `product_evidence_required` |
| 1514 亞力 | [公司下載／產品資料](https://www.allis.com.tw/zh-tw/download.html)支持變壓器、配電盤、開關設備與 SCADA 等一般重電能力，尚未找到風電專用產品或風場供貨實績 | low_medium | `company_source_required` |
| 1519 華城 | [公司官方資料](https://www.fortune.com.tw/tw/about_news_detail.aspx?Id=25)明列離岸風場陸上變電站工程，並製造風機塔內變壓器及電力模組 | high | `evidence_ready` |
| 2013 中鋼構 | [公司官方永續資料](https://csr.cssc.com.tw/chr_05_03_quality/)記錄離岸風電水下基礎資格、彰芳西島 10 座交貨，以及中能風場水下基礎塔架製造 | high | `evidence_ready` |
| 2031 新光鋼 | [公司官方資料](https://www.hkssteel.com.tw/fin_abu.html)明列風電水下基礎樁管研發生產中心，[公司簡報](https://www.hkssteel.com.tw/download/fin/note/2026Apr15.pdf)亦列離岸風電基礎建設 | high | `evidence_ready` |
| 2308 台達電 | [公司風電產品頁](https://landing.deltaww.com/zh-TW/products/Wind-Power-Converter/ALL/)明列自行開發生產 MW 級雙饋式與全功率風力發電變流器 | high | `evidence_ready` |
| 3708 上緯投控 | [公司官方網站](https://www.swancor.com/)與[股東信](https://www.swancor.com/tw/ir/letter)明列風機葉片樹脂、國際風機商供應資格與接單進度 | high | `evidence_ready` |

### 設備建議核准範圍

- 可送人工核准：1519、2013、2031、2308、3708，共 5 筆。
- 暫緩：1503、1514；兩者具重電或合作關聯，但目前不足以確認具體風電產品角色。
- 既有正式成員 1504 不重複異動。

## `WIND_SERVICE` 查證結果

| 股票 | 公司角色與主要證據 | 證據強度 | 判定 |
|---|---|---|---|
| 1513 中興電 | [櫃買產業鏈公司頁](https://ic.tpex.org.tw/company_chain.php?stk_code=1513)列為風場規劃與營造；另一份[櫃買公開申請文件](https://www.tpex.org.tw/storage/emerging_register/2023/10/1696301559_12152_CH_7702.pdf)描述其承作風力發電變電所及系統開發，但尚缺中興電公司一手風電專案或合約資料 | medium | `company_source_required` |
| 3712 永崴投控 | [公司官方公告](https://www.fit-holding.com/%E5%AF%8C%E5%B4%B4%E8%83%BD%E6%BA%90%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%BE%97%E6%A8%99%E5%8F%B0%E9%9B%BB%E3%80%8C%E9%9B%A2%E5%B2%B8%E9%A2%A8%E9%9B%BB%E4%BA%8C%E6%9C%9F%E8%A8%88/)明列旗下富崴能源得標 300MW 離岸風場建置案；[公司沿革](https://www.fit-holding.com/history/)確認集團持有森崴能源控制性股權 | high | `evidence_ready`，透過受控制子公司 |
| 6806 森崴能源 | [公司官方資料](https://www.shinfox.com.tw/offshore_wind_power.html)明列富崴能源承攬台電離岸風電二期 EPC 與五年運維；[公司介紹](https://www.shinfox.com.tw/aboutus.html)亦列離岸／陸域風電建置維運及海事工程 | high | `evidence_ready` |
| 7786 東方風能 | [公司官方資料](https://www.dfo.com.tw/?route=article%2Fcompany)明列離岸風場探勘、建置及長期運維完整週期服務；[實績頁](https://www.dfo.com.tw/news/Track-record/)另列 12 年及 15 年運維合約 | high | `evidence_ready` |
| 8926 台汽電 | [公司官方再生能源頁](https://esg.cogen.com.tw/tw/environment-renewable)明列風力 EPC、離岸風電陸域輸變電工程及 116 座風機運維實績；[2025 個體財報](https://www.cogen.com.tw/files/9B3AD642557F3FDDb58d601d9Ca1246aD16d5bDf.pdf)亦揭露大型離岸風電工程收入 | high | `evidence_ready` |

### 工程維運建議核准範圍

- 可送人工核准：3712、6806、7786、8926，共 4 筆。
- 暫緩：1513；主管機關分類與公開申請文件支持其角色，但仍需公司一手風電實績才能達到本批正式化門檻。
- 既有正式成員 2208 不重複異動。

## `WIND_OPERATION` 查證結果

| 股票 | 公司角色與主要證據 | 證據強度 | 判定 |
|---|---|---|---|
| 1102 亞泥 | [公司官方新聞](https://www.acc.com.tw/news-center/latest-news/670-111)明列持續增加風電投資，並與 RWE 推動竹風風力發電計畫 | high | `evidence_ready`，角色為投資／開發中案場 |
| 3712 永崴投控 | [公司官方投資資料](https://www.fit-holding.com/invest/)將森崴能源列為再生能源開發事業；[公司沿革](https://www.fit-holding.com/history/)確認集團持有森崴能源控制性股權，集團並透過子公司投入風電開發與工程 | high | `evidence_ready`，透過受控制子公司 |
| 6806 森崴能源 | [公司官方資料](https://www.shinfox.com.tw/aboutus.html)明列陸域與離岸風電業務；[公司治理資料](https://www.shinfox.com.tw/report_governance_committee.html)記錄風電開發權與投資事項 | high | `evidence_ready` |
| 6873 泓德能源 | [公司介紹](https://www.hdrenewables.com/about/)與[解決方案](https://www.hdrenewables.com/solutions/)目前可證明電站開發、光電、儲能、售電及智慧電網能力；最新官方案場與發電資料未顯示實際風場開發、持有或營運 | high | `role_mismatch` |
| 8926 台汽電 | [公司官方再生能源頁](https://esg.cogen.com.tw/tw/environment-renewable)明列風電投資開發 98MW、2024 年風力發電量 1.1 億度，並列苗栗風場與星寶陸域風場 | high | `evidence_ready` |

### 開發營運建議核准範圍

- 可送人工核准：1102、3712、6806、8926，共 4 筆。
- 不納入：6873；目前實際業務證據集中在光電、儲能與智慧電網，不能由泛綠能描述推定風電營運。
- 既有正式成員 6869 不重複異動。

## 本批統計與建議

- 查證 17 筆尚未正式化候選，涉及 13 檔公司；3712、6806、8926各跨兩個風電角色。
- `evidence_ready`：13 筆，分別為 `WIND_EQUIPMENT` 5 筆、`WIND_SERVICE` 4 筆、`WIND_OPERATION` 4 筆。
- `company_source_required`／`product_evidence_required`：3 筆（1503、1514、1513）。
- `role_mismatch`：1 筆（6873）。
- 建議送人工核准的 13 筆映射，共涵蓋 10 檔公司。
- 不建立新 Theme；三個風電子 Theme 均已存在。跨 Theme 只代表公司具多個產業角色，不代表重複計算為不同公司。

## 人工核准後的精確異動量

若使用者核准本文件建議範圍：

- `WIND_EQUIPMENT` 新增 5 筆，由 1 筆增為 6 筆。
- `WIND_SERVICE` 新增 4 筆，由 1 筆增為 5 筆。
- `WIND_OPERATION` 新增 4 筆，由 1 筆增為 5 筆。
- 合計新增 13 筆 `stock_theme_map.csv` 正式映射，涵蓋 10 檔公司。
- 1503、1514、1513、6873 維持非正式候選狀態。
