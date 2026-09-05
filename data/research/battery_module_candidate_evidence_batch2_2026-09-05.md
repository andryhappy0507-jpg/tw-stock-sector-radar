# 電池模組公司證據候選池第二批（2026-09-05）

本檔完成 `BATTERY_MODULE` 官方候選池剩餘 9 檔的逐一查證，只建立研究候選，不直接寫入 `stock_theme_map.csv`。價格 PASS 不作為產業歸屬證據。

## 延用分類邊界

- 納入：公司直接設計、製造或組裝由電芯、保護電路、BMS、機構件等構成的電池模組／電池包，或以自有產品形式提供可辨識的電池組與電池堆疊。
- 排除：只提供電池測試設備、充電器、DC/DC 電源模組、材料、添加劑、BMS／控制板 SMT 或整體儲能系統整合，但未證明具有電池模組／電池包產品者。
- 官方產業鏈名單只作候選來源，不能取代公司產品與實績證據。

## 第二批查證結果

| 股票 | 公司角色與主要證據 | 證據強度 | 判定 |
|---|---|---|---|
| 2360 致茂 | [官方電池測試資料](https://www.chromaate.com/tw/newsroom/news1086)明列 BBU 與電池模組充放電測試解決方案；[公司認證資料](https://www.chromaate.com/tw/chroma/certification)定位為量測設備製造商，未顯示自行製造電池模組 | high | `role_mismatch` |
| 2439 美律 | [官方電池產品頁](https://www.merry.com.tw/page/product_merry/index.aspx?kind=59)明列輕型電動交通、醫療、工業、IoT 電池組與儲能產品；[公司資料](https://www.merry.com.tw/page/about/index.aspx?kind=30)亦說明與電芯廠合作並掌握電池封裝解決方案 | high | `evidence_ready` |
| 2459 敦吉 | [官方網站](https://www.audix.com/)目前支持電子零組件製造、通路與產品驗證三項事業；[公司年報](https://www.audix.com/upfiles/ADUpload/bc_ir_report2659710887.pdf)所列製造重點為繼電器、變壓器、線圈、模具及模組組裝，未找到可辨識的電池模組／電池包產品 | medium | `company_source_required` |
| 3026 禾伸堂 | [官方投資人與事業資料](https://www.holystone.com.tw/page_details.php?lang=ch&mlevel1=4)列出被動、主動、週邊、消費與電源元件事業群；公司財報主要支持積層陶瓷電容器、IC、模組及電子零組件業務，未證明電池模組產品 | high | `role_mismatch` |
| 6278 台表科 | [官方 2025 年報](https://www.tsmt.com/uploads/8d14da52-8f25-4d9f-bb1f-a08769256aad-%E5%8F%B0%E8%A1%A8114%E5%B9%B4%E5%BA%A6%E5%B9%B4%E5%A0%B1.pdf)明列 BMS、ECU 與換電站管理系統模組的 SMT／組裝服務；但未明列將電芯、BMS 與外殼組成電池包的製造角色 | high | `company_source_required` |
| 6441 廣錠 | [官方能源產品頁](https://www.ibasesolution.com/products-energy/)提供 Battery Stack 與整體儲能產品；[電池堆疊產品頁](https://www.ibasesolution.com/battery-stack/)明列一套 230K 電池堆疊含 11 個可獨立更換的電池包及 Battery Monitoring Unit | high | `evidence_ready`，角色為儲能電池包／堆疊產品 |
| 6509 聚和 | [官方網站](https://www.hopax.com/zh-tw)定位為生物緩衝劑、功能添加劑、水性高分子單體與生物體分子等化學材料供應商；既有公司資料只支持鋰電池添加劑，不支持電池模組製造 | high | `role_mismatch` |
| 8109 博大 | [官方網站](https://pduke.com/tc/)與[產品文件](https://www.pduke.com/tc/document-download2_20.htm)明列工業、醫療、軌道與軍工用 AC/DC、DC/DC 電源模組及濾波器，未找到電池模組／電池包產品 | high | `role_mismatch` |
| 5543 桓鼎-KY | [官方網站](https://www.buima.com.tw/)明列鋰電池模組研發、生產、製造及銷售，產品涵蓋穿戴裝置、工具、醫療、輕型載具及儲能；[官方事業頁](https://www.buima.com.tw/zh-tw/application-65)另列完整電池模組解決方案 | high | `evidence_ready` |

## 判讀重點

- 2360 致茂的產品是「測試電池模組的設備」，不是電池模組本身。
- 6278 台表科有 BMS／換電站控制模組的 SMT 與組裝能力，但現有公司資料仍不足以證明組裝完整電池包，故不以 EMS 能力推定產品角色。
- 6441 廣錠的核心證據是公司直接銷售由 11 個電池包構成、具監控單元的電池堆疊產品，而不是只因承作儲能案場就納入。
- 6509 聚和屬材料／添加劑；8109 博大屬電源轉換模組，兩者產品名稱雖都可能出現「模組」，但不等同電池模組。

## 本批統計與建議

- 查證第二批 9 檔現行上市／上櫃普通股。
- `evidence_ready`：3 檔（2439、6441、5543）。
- `company_source_required`：2 檔（2459、6278）。
- `role_mismatch`：4 檔（2360、3026、6509、8109）。
- 建議只將 2439 美律、6441 廣錠、5543 桓鼎-KY 送人工核准。
- 第一批已正式核准 10 檔；若本批 3 檔通過，原始 19 檔官方候選池即完成全數查證，正式覆蓋為 13 檔。

## 人工核准後的精確異動量

若使用者核准本文件建議範圍：

- 新增 3 筆 `BATTERY_MODULE` 正式映射。
- `BATTERY_MODULE` 正式映射由 10 增為 13 筆。
- 正式人工映射總數由 268 增為 271 筆。
- 2360、2459、3026、6278、6509、8109 維持非正式候選或排除狀態。
