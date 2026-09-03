# AI 基礎建設細分 Theme 公司證據候選池（2026-09-02）

本檔只建立研究候選，不直接寫入 `theme_master.csv` 或 `stock_theme_map.csv`。候選公司仍須完成證據補強與人工核准，價格 PASS 不作為產業歸屬證據。

## 第一批候選

| 候選 Theme | 股票 | 建議角色 | 主要證據 | 證據強度 | 目前狀態 |
|---|---|---|---|---|---|
| `AI_COLD_PLATE_CDU` | 2308 台達電 | 冷板、CDU與完整液冷系統核心 | [Delta COMPUTEX 2026](https://www.deltaww.com/en-US/landing/Computex-2026) 明列 Vera Rubin 冷板、3MW CDU、2.4MW HVDC CDU等AI資料中心產品 | high | evidence_ready |
| `AI_COLD_PLATE_CDU` | 3324 雙鴻 | Cold Plate、CDU、Manifold核心 | [Auras官方液冷資料](https://www.auras.com.tw/CMSFS/InformationCenters/English/ecfc7b18-d55e-4ca3-a673-b449f83d051c.pdf) 明列Cold Plate、L2L/L2A/Sidecar/In-row CDU及AI/HPC應用 | high | evidence_ready |
| `AI_COLD_PLATE_CDU` | 3017 奇鋐 | 整體散熱候選 | [奇鋐官方網站](https://www.avc.co/zh-tw/ProductTechnology/%E7%B3%BB%E7%B5%B1%E7%B5%84%E8%A3%9D%E8%88%87%E6%95%B4%E6%A9%9F%E6%95%A3%E7%86%B1%E6%96%B9%E6%A1%88) 支持整體散熱方案，但目前頁面未明列AI冷板或CDU | low_medium | ai_specific_primary_source_required |
| `AI_HIGH_SPEED_CABLE` | 3665 貿聯-KY | AEC／ACC高速銅纜核心 | [BizLink官方資料中心方案](https://telecom-networking.bizlinktech.com/applications/bizlink-data-center-solutions/) 明列800G以上ACC/AEC與最高1.6T DAC | high | evidence_ready |
| `AI_HIGH_SPEED_CABLE` | 3533 嘉澤 | 高速線纜互連候選 | 現有證據支持GPU Socket與高速線纜研發，但主要來源仍為財經媒體 | medium | company_primary_source_required |
| `AI_HIGH_SPEED_CABLE` | 3526 凡甲 | AI伺服器高速連接線候選 | 現有證據支持高頻高速AI伺服器連接器與連接線需求，但主要來源仍為法說轉述／財經媒體 | medium | company_primary_source_required |
| `AI_SERVER_RACK_CHASSIS` | 8210 勤誠 | AI伺服器機殼／機櫃核心 | [Chenbro MGX產品頁](https://www.chenbro.com/en-US/product/MGX) 明列MGX 2U AI Server Chassis及GB200 NVL36／NVL72 rack solution | high | evidence_ready |
| `AI_SERVER_RACK_CHASSIS` | 2317 鴻海 | AI機櫃級系統整合核心 | [鴻海官方新聞](https://www.foxconn.com/zh-tw/press-center/press-releases/latest-news/2053) 明列AI伺服器垂直整合、機櫃級系統整合與AI資料中心方案 | high | evidence_ready |
| `AI_SERVER_RACK_CHASSIS` | 2382 廣達 | 整櫃與Rackmount系統核心 | [QCT官方產品資料](https://www.qct.io/product/index/Server/rackmount-server/GPGPU-Xeon-Phi?page=1) 明列多款AI/HPC Rackmount伺服器與GPU Direct Storage架構 | high | evidence_ready |
| `AI_SERVER_RACK_CHASSIS` | 6669 緯穎 | Rack-scale AI平台核心 | [Wiwynn COMPUTEX 2026](https://www.wiwynn.com/events/computex) 明列Vera Rubin NVL72與AMD Helios rack-scale AI方案 | high | evidence_ready |
| `AI_STORAGE_SYSTEM` | 6669 緯穎 | AI儲存系統核心 | [Wiwynn COMPUTEX 2026](https://www.wiwynn.com/events/computex) 明列支援GPU-direct storage的儲存伺服器原型，用於AI推論與檢索工作負載 | high | evidence_ready |
| `AI_STORAGE_SYSTEM` | 2356 英業達 | GPU Direct Storage平台核心 | [Inventec官方產品資料](https://ebg.inventec.com/en/tool-download/product_files/file/201?note=) 明列NVMe與GPU同交換板並支援NVIDIA GPUDirect Storage的AI訓練／推論平台 | high | evidence_ready |
| `AI_STORAGE_SYSTEM` | 2382 廣達 | AI/HPC高速儲存候選 | [QCT官方產品資料](https://www.qct.io/product/index/Server/rackmount-server/GPGPU-Xeon-Phi?page=1) 明列AI/HPC系統的全NVMe GPU Direct Storage，但仍需確認是否應歸類為獨立儲存系統而非AI伺服器功能 | medium_high | taxonomy_boundary_review |

## 第一批統計

- 4 個候選 Theme。
- 13 筆候選對應、11 檔上市／上櫃公司。
- 9 筆 `evidence_ready`。
- 3 筆需要公司第一手AI專用證據。
- 1 筆需要確認「AI儲存系統」與「AI伺服器內建儲存」的分類邊界。

## 人工審核前必做

1. 為 3017、3533、3526 補公司官網、年報或公司法說原始資料。
2. 確認 `AI_SERVER_RACK_CHASSIS` 是否同時接受機殼製造與整櫃系統整合；若不接受，應拆成兩個 Theme。
3. `AI_STORAGE_SYSTEM` 只收具AI資料管線、GPU Direct Storage或AI檢索用途的儲存系統，不收一般SSD或一般儲存伺服器。
4. 完成第二來源與重複 Theme 檢查後，再提交人工核准。
