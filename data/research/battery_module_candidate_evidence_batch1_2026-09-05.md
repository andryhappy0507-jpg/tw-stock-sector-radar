# 電池模組公司證據候選池第一批（2026-09-05）

本檔承接 `semiconductor_energy_theme_audit_2026-09-05.md` 的大型候選池分批查證，只建立 `BATTERY_MODULE` 第一批研究候選，不直接寫入 `stock_theme_map.csv`。價格 PASS 不作為產業歸屬證據。

## 分類邊界

- 納入：公司直接設計、製造或組裝由電芯、保護電路、BMS、機構件等構成的電池模組或電池包；適用於 IT、BBU、UPS、儲能、工業設備或電動載具皆可。
- 排除：只製造電芯、正負極材料、添加劑、測試設備、充電器、PCS、電源供應器或儲能系統整合，但未證明有電池模組／電池包產品者。
- 公司可同時屬於 `BATTERY_CELL`、`BATTERY_MODULE`、`UPS_BBU` 或儲能相關 Theme，但每個標籤都要有對應產品層級的獨立證據。

## 第一批查證結果

| 股票 | 公司角色與主要證據 | 證據強度 | 判定 |
|---|---|---|---|
| 2308 台達電 | [官方儲能電池系統型錄](https://filecenter.deltaww.com/Products/download/21/2102/Catalogue/ESS_LFP%20Battery%20Cabinet_Leaflet_CHT_20230714.pdf)明列從電池模組、機櫃到系統均由台達自主設計生產 | high | `evidence_ready` |
| 3015 全漢 | [官方智慧微電網資料](https://www.fsp-group.com/tw/microsite/smart-energy/index.html)明列 24V／48V、50Ah／100Ah 模組化電池，並依儲能需求設計串並聯組合；公司年報亦列磷酸鋰鐵電池模組研發成果 | high | `evidence_ready` |
| 3211 順達 | [官方產品頁](https://www.dynapack.com.tw/h/Data?key=iczce&set=24)明列資訊產品、醫療、伺服器 BBU、UPS、儲能與電動載具電池模組，並具設計製造能力 | high | `evidence_ready` |
| 3323 加百裕 | [官方產品頁](https://zh-tw.celxpert.com.tw/products)明列筆電、網通、電動工具、儲能備援與電動載具電池組；[公司首頁](https://zh-tw.celxpert.com.tw/)說明依客戶需求開發製造電池模組並搭載自研 BMS | high | `evidence_ready` |
| 3625 西勝 | [官方網站](https://www.c-techone.com/tw)定位為鋰電池模組設計製造商；[官方股東會文件](https://www.c-techone.com/uploads/images/ShareholdersMeeting/%E8%A5%BF%E5%8B%9D113%E5%B9%B4%E8%82%A1%E6%9D%B1%E5%B8%B8%E6%9C%83%E8%AD%B0%E4%BA%8B%E6%89%8B%E5%86%8A.pdf)列出 BBU、UPS、ESS、3C、電動自行車及 AGV 等鋰電池模組 | high | `evidence_ready` |
| 4931 新盛力 | [官方產品頁](https://www.stl-tech.com/product_list.asp)明列使用外購電芯搭配自研 BMS，設計生產動力工具、BESS、UPS、BBU、輕型載具與無人機電池模組 | high | `evidence_ready` |
| 5309 系統電 | [官方公司資料](https://www.sysgration.com/zh-cn/about-sysgration)列出 Battery Pack 與儲能解決方案；[官方法說簡報](https://www.sysgration.com/uploads/investor-conference-information/TW/Sysgration_Investor_Conference_TC_20241204.pdf)明列 SMR、BBU 與 UPS 鋰電池包量產及業務進度 | high | `evidence_ready` |
| 6121 新普 | [官方公司資料](https://www.simplo.com.tw/article.php?cid=12&id=360&lang=tw&ot=all&tb=3)明列筆電與手機電池組裝配、研發及銷售；[官方願景與產品說明](https://www.simplo.com.tw/article_d.php?id=300&lang=tw&tb=1)定位為電池模組解決方案製造商 | high | `evidence_ready` |
| 8038 長園科 | [官方公司簡報](https://www.caec.com.tw/_i/assets/file/shareholder/ba94d5af979c71985b4b6604e36054e8.pdf)明列從材料、電池芯到電池模組與管理系統的完整研發製造鏈 | high | `evidence_ready` |
| 8171 天宇 | [官方產品頁](https://www.feii.com.tw/products)明列 AGV、BBU、UPS、動力及其他特殊用途電池模組，並提供電芯選型、結構設計與系統整合的 OEM／ODM 服務 | high | `evidence_ready` |

## 判讀重點

- 2308 台達電、3015 全漢雖也有 PCS、充電器、電源供應器或整體儲能系統，但本批證據另外明確列出自行設計／生產的電池模組，因此不是以系統整合角色代替模組證據。
- 3211 順達、3323 加百裕、3625 西勝、4931 新盛力、6121 新普是直接電池模組／電池包設計製造商。
- 5309 系統電與 8171 天宇具多種 BBU、UPS、工業或儲能電池包產品；`BATTERY_MODULE` 描述的是產品層級，不等同全部產品都屬 AI 伺服器 BBU。
- 8038 長園科已正式屬於 `BATTERY_CELL`；其公司資料亦獨立支持下游模組角色，可合理同時掛兩個產品層級標籤。

## 本批統計與建議

- 查證 10 檔現行上市／上櫃普通股。
- `evidence_ready`：10 檔，證據強度均為 high。
- 建議將 2308、3015、3211、3323、3625、4931、5309、6121、8038、8171 送人工核准。
- 不建立新 Theme；`BATTERY_MODULE` 已存在，目前正式映射為 0 筆。
- 原始候選池尚餘 9 檔：2360、2439、2459、3026、6278、6441、6509、8109、5543，留待第二批逐一排除角色混淆。

## 人工核准後的精確異動量

若使用者核准本文件建議範圍：

- 新增 10 筆 `BATTERY_MODULE` 正式映射。
- `BATTERY_MODULE` 正式映射由 0 增為 10 筆。
- 正式人工映射總數由 258 增為 268 筆。
- 不因週價格 PASS 改變上述產業證據判定。
