# 電池芯與智慧電表公司證據候選池（2026-09-05）

本檔承接 `semiconductor_energy_theme_audit_2026-09-05.md` 的建議批次 B，只建立研究候選，不直接寫入 `stock_theme_map.csv`。價格 PASS 不作為產業歸屬證據。

## 分類邊界

### `BATTERY_CELL` 電池芯

- 納入：公司直接研發或製造鋰離子、鋰高分子、磷酸鐵鋰等可充式電池芯。
- 排除：只提供電池材料、電池添加劑、測試設備、電池模組、BMS、PCS 或儲能系統整合。
- 同一公司若同時製造電芯與模組，可分別進入兩個 Theme，但每個角色都要有獨立證據。

### `SMART_METER` 智慧電表

- 納入：公司直接開發、製造或供應具通訊功能的智慧電表，或具明確 AMI 電表產品與建置實績。
- 排除：只有一般智慧電網、能源管理、電力設備、連接器、觸控面板或電子代工能力，未證明智慧電表產品角色。

## `BATTERY_CELL` 查證結果

| 股票 | 官方候選理由 | 公司／主管機關證據 | 判定 | 原因 |
|---|---|---|---|---|
| 6558 興能高 | 櫃買能源元件產業鏈列為電池芯 | [興能高公司介紹](https://www.synst.com.tw/zh-tw/)明列研發、設計及生產可充式鋰離子、鋰高分子與先進混成電池，並具量產出貨紀錄 | `evidence_ready` / high | 直接電芯研發製造商，符合核心定義 |
| 8038 長園科 | 櫃買能源元件產業鏈列為電池芯 | [長園科官方網站](https://www.caec.com.tw/index_tw.php)列出儲能、不斷電、商用與工業用電池；[公司官方簡報](https://www.caec.com.tw/_i/assets/file/shareholder/ba94d5af979c71985b4b6604e36054e8.pdf)明列材料、電池芯、模組與管理系統的完整鏈 | `evidence_ready` / high | 具直接電芯研發製造與產品應用證據 |
| 6278 台表科 | 櫃買產業鏈列為電池芯及電池模組 | [櫃買公司產業鏈](https://ic.tpex.org.tw/company_chain.php?stk_code=6278)明列能源元件電池芯／模組；但[台表科公司資料](https://www.tsmt.com/cn/about-tsmt)主要定位為 SMT 電子製造服務，最新公司資料尚未找到直接電芯產品或製造說明 | `company_source_required` / medium | 主管機關分類支持，但公司角色可能是 EMS／模組製程，暫不送正式核准 |
| 2308 台達電 | 櫃買產業鏈列為電池芯 | [台達儲能系統](https://www.deltaww.com/zh-TW/products/Energy-Storage-Systems)與[官方型錄](https://filecenter.deltaww.com/Products/download/21/2102/Catalogue/ESS_LFP%20Battery%20Cabinet_Leaflet_CHT_20230714.pdf)支持電池模組、機櫃與系統整合；型錄使用 LFP 280Ah Cell，但未聲稱該電芯由台達製造 | `role_mismatch` / high | 適合 `BATTERY_MODULE`／儲能系統，不足以認定為電池芯廠 |
| 2360 致茂 | 櫃買產業鏈列為電池芯 | [致茂官方方案](https://www.chromaate.com/tw/chroma/highlights)與[電池芯測試產品](https://www.chromaate.com/tw/newsroom/news81)明列電池芯化成、信賴性與絕緣測試系統 | `role_mismatch` / high | 是電池芯測試設備供應商，不是電池芯製造商 |
| 6509 聚和 | 櫃買產業鏈列為電池芯 | [聚和官方產品頁](https://www.hopax.com/zh-tw/sitemap)明列鋰電池添加劑 | `role_mismatch` / high | 是電池材料／添加劑供應商，應留在電池材料類，不屬電池芯 |

### 電池芯建議核准範圍

- 可送人工核准：6558、8038，共 2 筆。
- 暫緩：6278，需補公司一手資料證明其直接製造電芯，而非只做 SMT、模組或代工。
- 不納入 `BATTERY_CELL`：2308、2360、6509；三者可保留在各自正確的模組／系統、測試設備或材料角色。

## `SMART_METER` 查證結果

| 股票 | 官方候選理由 | 公司／主管機關證據 | 判定 | 原因 |
|---|---|---|---|---|
| 1513 中興電 | 櫃買智慧電網產業鏈列為高／低壓 AMI | [中興電官方產品頁](https://www.chem.com.tw/tc/products_info.aspx?Class1=1&Class2=1159)明列自主開發 AMI 智慧電表並銷售台電，供民用與工業使用 | `evidence_ready` / high | 直接智慧電表產品與客戶證據完整 |
| 2371 大同 | 櫃買智慧電網產業鏈列為高／低壓 AMI | [大同智慧電表產品頁](https://www.tatung.com/products/index/489)明列單相、三相、CT 型智慧電表與 AMI 系統；[AMI 解決方案](https://www.tatung.com/solution/detail/13)列出電表、通訊與資料管理整合能力 | `evidence_ready` / high | 直接產品、系統與建置能力完整 |
| 4588 玖鼎電力 | 櫃買智慧電網產業鏈列為低壓 AMI | [玖鼎官方資料](https://www.archmeter.com/zh-tw/download-c17925/%E5%85%AC%E5%8F%B8%E9%87%8D%E5%A4%A7%E8%A8%8A%E6%81%AF.html)明列電子式電表、智慧電表晶片與電力監控產品；[櫃買公司產業鏈](https://ic.tpex.org.tw/company_chain.php?stk_code=4588)明列低壓 AMI | `evidence_ready` / high | 智慧電表核心產品與 AMI 角色明確 |
| 3622 洋華 | 櫃買智慧電網產業鏈列為高／低壓 AMI | [洋華官方產品資料](https://www.yfo.com.tw/governances_tw.php?id=25)目前明列觸控面板、電子紙、整機組裝、電纜終端匣與保護裝置，未找到智慧電表產品 | `company_source_required` / low_medium | 可能經由機電事業或代工參與，但目前不足以認定直接智慧電表角色 |
| 5457 宣德 | 櫃買智慧電網產業鏈列為高／低壓 AMI | 最新可查公司業務以連接器、線束、機構件及成機／模組組裝為主，未找到公司一手智慧電表產品或 AMI 建置證據 | `company_source_required` / low | 主管機關候選不足以證明實際智慧電表產品角色 |
| 6278 台表科 | 櫃買智慧電網產業鏈列為高／低壓 AMI | [櫃買公司產業鏈](https://ic.tpex.org.tw/company_chain.php?stk_code=6278)明列高／低壓 AMI；[台表科官方資料](https://www.tsmt.com/cn/about-tsmt)主要支持 SMT 電子製造服務，未找到智慧電表品牌、產品或標案資料 | `company_source_required` / medium | 可能是智慧電表 EMS 製造角色，仍需公司一手產品或客戶證據 |

### 智慧電表建議核准範圍

- 可送人工核准：1513、2371、4588，共 3 筆。
- 暫緩：3622、5457、6278；需補公司官方智慧電表產品、智慧電表代工或 AMI 標案證據。
- 1513 已是 `SMART_GRID` 正式成員；新增較細的 `SMART_METER` 後可保留父子雙標籤。

## 本批統計與建議

- 查證 12 筆候選，涉及 10 檔公司；6278 同時出現在兩個 Theme。
- `evidence_ready`：5 筆，分別為 `BATTERY_CELL` 2 筆、`SMART_METER` 3 筆。
- `company_source_required`：4 筆。
- `role_mismatch`：3 筆。
- 本批建議只送 5 筆人工核准：`BATTERY_CELL` 的 6558、8038；`SMART_METER` 的 1513、2371、4588。
- 不建立新 Theme；兩個 Theme 均已存在於 `theme_master.csv`，只需在核准後新增正式股票映射。

## 人工核准後的精確異動量

若使用者核准本文件建議範圍：

- 新增 5 筆 `stock_theme_map.csv` 正式映射。
- 不新增或改名 Theme。
- 不處理 2308、2360、6509、3622、5457、6278 的正式歸屬。
- 不因週價格 PASS 改變上述證據判定。
