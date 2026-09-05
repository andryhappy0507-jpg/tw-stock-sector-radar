# 半導體材料公司證據候選池（2026-09-05）

本檔承接半導體與能源 Theme 覆蓋盤點，只建立 `SEMICONDUCTOR_MATERIALS` 研究候選，不直接寫入 `stock_theme_map.csv`。價格 PASS 不作為產業歸屬證據。

## 分類邊界

- 納入：直接製造或明確供應晶圓製造、IC 載板、半導體封裝使用的光阻、濕製程化學品、特殊氣體、靶材、研磨液、焊接材料、介電材、離型材、矽晶圓、石英或其他關鍵製程材料。
- 可納入供應商：專業代理／整合商若公司資料明確列出半導體材料品項與供應業務，可標示「材料供應／整合」，不冒充材料製造商。
- 排除：只有一般化學品、電子組裝膠、設備、太陽能、熱管理材料，或尚在評估、送樣而未證明已有半導體材料業務者。

## 查證結果

| 股票 | 公司角色與主要證據 | 證據強度 | 判定 |
|---|---|---|---|
| 1711 永光 | [官方電子化學事業](https://ecbu.ecic.com/)明列半導體及封裝黃光製程用 G-line、I-line、厚膜光阻、顯影液、研磨液與濕製程化學品 | high | `evidence_ready` |
| 1717 長興 | [官方產品頁](https://www.eternal-group.com/ProductPage?AttributeID=ATT2023060700079&CategoryID=PC2023060200003)明列 IC 載板與 IC 封裝精密蝕刻、電鍍使用的乾膜光阻；公司資料亦列半導體製程電子化學材料研發製造 | high | `evidence_ready` |
| 1727 中華化 | [官方電子級硫酸頁](https://www.chciworld.com.tw/product/ppt_ppb_electronic_grade_sulfuric_acid/)明列矽晶片清洗、光刻及蝕刻用途；[電子化學品頁](https://www.chciworld.com.tw/product-category/product/electron/)另列 TMAH、NMP、IPA、PGMEA、金屬蝕刻液等 | high | `evidence_ready` |
| 1742 台蠟 | [官方網站](https://www.wax.com.tw/)目前主業為蠟品、太陽能與水產；公司資料只支持石蠟相變材料用於電子元件溫控，未證明晶圓或封裝製程材料 | high | `role_mismatch` |
| 1785 光洋科 | [官方公司資料](https://www.solartech.com.tw/investors/)明列薄膜濺鍍靶材、貴稀金屬精煉與電子半導體應用；[官方簡報](https://www.solartech.com.tw/download/0/124/)明列半導體薄膜沉積靶材 | high | `evidence_ready` |
| 2493 揚博 | [臺灣證券交易所公司資料](https://wwwc.twse.com.tw/pdf/ch/2493_ch.pdf)明列半導體製程／檢測設備、材料及製程化學品業務 | medium | `evidence_ready` |
| 3010 華立 | [官方半導體材料頁](https://www.wahlee.com/ZH/Products/List/?Top=mlnraXWF1yBMoOm5L83Rww%3D%3D&id=mlnraXWF1yBMoOm5L83Rww%3D%3D)明列光阻、顯影液、去光阻液、特殊氣體、CMP 研磨液、石英、矽環、陶瓷與矽晶圓 | high | `evidence_ready`，角色為材料供應／整合 |
| 3305 昇貿 | [官方半導體封裝產品頁](https://www.shenmao.com/zh-tw/product-c46410/%E5%8D%8A%E5%B0%8E%E9%AB%94%E5%B0%81%E8%A3%9D.html)明列 BGA 錫球與 Bumping 錫膏 | high | `evidence_ready` |
| 3663 鑫科 | [官方產品頁](https://www.e-ttmc.com.tw/chinese/series1.html)明列被動元件、光學元件與半導體鍍膜用高純度濺鍍靶材 | high | `evidence_ready` |
| 4720 德淵 | [官方網站](https://www.texyear.com/zh-tw)目前支持電子組裝、AI 伺服器 PCBA 三防漆與熱熔膠等應用，尚未證明晶圓或半導體封裝製程材料 | high | `role_mismatch` |
| 4722 國精化 | [官方年報頁](https://www.qualipoly.com/zh-tw/a3-2820/%E5%85%AC%E5%8F%B8%E5%B9%B4%E5%A0%B1.html)所列最新年報揭露高階半導體製程特用化學品，涵蓋 EUV 光阻相關材料 | high | `evidence_ready` |
| 4749 新應材 | [官方網站](https://www.aemc.com.tw/)明列 IC 製造清洗化學品、先進封裝材料與 CMOS 影像感測材料；[官方沿革](https://www.aemc.com.tw/about/history/)記錄先進製程顯影、清洗與洗邊材料量產 | high | `evidence_ready` |
| 4755 三福化 | [官方公司與產業資料](https://www.sfchem.com.tw/zh-hant/page/csr-aboutus)明列供應 IC 半導體所需濕式化學品，包含顯影、剝離、蝕刻、清洗液及研磨液代工 | high | `evidence_ready` |
| 4764 雙鍵 | [公司年報](https://www.dbc.com.tw/upload/11723514512.pdf)只表示評估半導體 PI 代工機會，尚未證明已量產、出貨或形成現行半導體材料業務 | medium | `business_evidence_required` |
| 4768 晶呈科技 | [官方公司資料](https://www.ingenteccorp.com.tw/)明列自有特殊氣體合成、純化、混配與分析技術；公司年報確認蝕刻與雷射特殊氣體供應半導體客戶 | high | `evidence_ready` |
| 4772 台特化 | [官方公司簡介](https://www.tscs.com.tw/about)明列矽乙烷、矽丙烷、無水氟化氫等半導體特氣／化學材料，用於 CVD、蝕刻與清潔 | high | `evidence_ready` |
| 5234 達興材料 | [官方半導體材料頁](https://www.daxinmat.com/?c=251&lang=zh-TW&sn=762)明列晶圓級／面板級先進封裝離型層、感光介電材、高純度濕製程與奈米微影化學品 | high | `evidence_ready` |
| 5434 崇越 | [官方半導體展資料](https://www.topco-global.com/archives/129588)明列先進製程材料、CoWoS／HBM 先進封裝材料供應；[公司營運資料](https://www.topco-global.com/zh-CN/archives/129449)列出矽晶圓、光阻、研磨液與晶圓載具 | high | `evidence_ready`，角色為材料供應／整合 |

## 結果統計

- 查證 18 檔官方產業鏈候選。
- `evidence_ready`：15 檔，其中 2493 為主管機關直接公司資料、證據強度 medium，其餘 14 檔為公司一手資料、證據強度 high。
- `role_mismatch`：1742、4720，共 2 檔。
- `business_evidence_required`：4764，共 1 檔。

## 建議送核准範圍

### A：直接材料製造／產品角色

- 1711 永光
- 1717 長興
- 1727 中華化
- 1785 光洋科
- 2493 揚博
- 3305 昇貿
- 3663 鑫科
- 4722 國精化
- 4749 新應材
- 4755 三福化
- 4768 晶呈科技
- 4772 台特化
- 5234 達興材料

### B：材料供應／整合角色

- 3010 華立
- 5434 崇越

### 本批不納入

- 1742 台蠟：現有證據未連結半導體製程或封裝材料。
- 4720 德淵：目前證據屬電子組裝／PCBA 膠材，不等同半導體製程材料。
- 4764 雙鍵：只有評估半導體 PI 代工機會，需補量產、出貨或現行產品證據。

## 人工核准後的精確異動量

若使用者核准 A、B：

- 新增 15 筆 `SEMICONDUCTOR_MATERIALS` 正式映射。
- 不新增或改名 Theme。
- 1742、4720、4764 維持非正式候選狀態。
- `SEMICONDUCTOR_MATERIALS` 正式映射由 0 增為 15 筆。
