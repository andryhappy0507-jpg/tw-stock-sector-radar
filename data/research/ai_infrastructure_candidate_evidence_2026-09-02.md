# AI 基礎建設細分 Theme 公司證據候選池（2026-09-02，2026-09-03 複核）

本檔只建立研究候選，不直接寫入 `theme_master.csv` 或 `stock_theme_map.csv`。候選公司仍須完成證據補強與人工核准，價格 PASS 不作為產業歸屬證據。

## 第一批候選

| 候選 Theme | 股票 | 建議角色 | 主要證據 | 證據強度 | 目前狀態 |
|---|---|---|---|---|---|
| `AI_COLD_PLATE_CDU` | 2308 台達電 | 冷板、CDU與完整液冷系統核心 | [Delta COMPUTEX 2026](https://www.deltaww.com/en-US/landing/Computex-2026) 明列 Vera Rubin 冷板、3MW CDU、2.4MW HVDC CDU等AI資料中心產品 | high | evidence_ready |
| `AI_COLD_PLATE_CDU` | 3324 雙鴻 | Cold Plate、CDU、Manifold核心 | [Auras官方液冷資料](https://www.auras.com.tw/CMSFS/InformationCenters/English/ecfc7b18-d55e-4ca3-a673-b449f83d051c.pdf) 明列Cold Plate、L2L/L2A/Sidecar/In-row CDU及AI/HPC應用 | high | evidence_ready |
| `AI_COLD_PLATE_CDU` | 3017 奇鋐 | 整體散熱候選 | [奇鋐官方網站](https://www.avc.co/zh-tw/ProductTechnology/%E7%B3%BB%E7%B5%B1%E7%B5%84%E8%A3%9D%E8%88%87%E6%95%B4%E6%A9%9F%E6%95%A3%E7%86%B1%E6%96%B9%E6%A1%88) 支持整體散熱方案，但目前頁面未明列AI冷板或CDU | low_medium | ai_specific_primary_source_required |
| `HIGH_SPEED_CONNECTOR` | 3665 貿聯-KY | AEC／ACC高速銅纜核心 | [BizLink官方資料中心方案](https://telecom-networking.bizlinktech.com/applications/bizlink-data-center-solutions/) 明列800G以上ACC/AEC與最高1.6T DAC | high | existing_mapping_evidence_upgrade_ready |
| `HIGH_SPEED_CONNECTOR` | 3533 嘉澤 | MCIO高速線纜與AI互連核心 | [嘉澤MCIO產品頁](https://www.lotes.cc/zh-tw/product.php?act=view&id=805) 明列PCIe Gen4／5與伺服器、資料中心、儲存應用；[公司官方新聞](https://www.lotes.cc/zh-tw/news.php?act=view&id=34) 明列NVIDIA MGX合作與AI Factory高速互連 | high | existing_mapping_evidence_upgrade_ready |
| `HIGH_SPEED_CONNECTOR` | 3526 凡甲 | AI伺服器高速連接線候選 | [凡甲2025年報](https://www.alltopconnector.com/data/information/files/1779087124881442433.pdf) 明列升級伺服器高速連接線，並將高速運算、AI資料中心列為高頻、高功率、高可靠度產品需求動能 | high | existing_mapping_evidence_upgrade_ready |
| `AI_SERVER_CHASSIS` | 8210 勤誠 | AI伺服器機殼核心 | [Chenbro MGX產品頁](https://www.chenbro.com/en-US/product/MGX) 明列MGX 2U AI Server Chassis；同頁整櫃方案證明其跨足rack，但本筆只核對機殼角色 | high | evidence_ready |
| `AI_RACK_SYSTEM` | 2317 鴻海 | AI機櫃級系統整合核心 | [鴻海官方新聞](https://www.foxconn.com/zh-tw/press-center/press-releases/latest-news/2053) 明列AI伺服器垂直整合、機櫃級系統整合與AI資料中心方案 | high | evidence_ready |
| `AI_RACK_SYSTEM` | 2382 廣達 | 整櫃與Rackmount系統核心 | [QCT官方產品資料](https://www.qct.io/product/index/Server/rackmount-server/GPGPU-Xeon-Phi?page=1) 明列多款AI／HPC Rackmount伺服器 | high | evidence_ready |
| `AI_RACK_SYSTEM` | 6669 緯穎 | Rack-scale AI平台核心 | [Wiwynn COMPUTEX 2026](https://www.wiwynn.com/events/computex) 明列Vera Rubin NVL72與AMD Helios rack-scale AI方案 | high | evidence_ready |
| `AI_STORAGE_SYSTEM` | 6669 緯穎 | AI儲存系統核心 | [Wiwynn COMPUTEX 2026](https://www.wiwynn.com/events/computex) 明列支援GPU-direct storage的儲存伺服器原型，用於AI推論與檢索工作負載 | high | evidence_ready |
| `AI_STORAGE_SYSTEM` | 2356 英業達 | AI伺服器內建GPU Direct Storage功能 | [Inventec官方產品資料](https://ebg.inventec.com/en/tool-download/product_files/file/201?note=) 明列NVMe與GPU同交換板並支援NVIDIA GPUDirect Storage，但證據指向AI運算平台內建功能，未證實獨立AI儲存系統 | medium_high | ai_storage_product_required |
| `AI_STORAGE_SYSTEM` | 2382 廣達 | AI／HPC伺服器內建高速儲存功能 | [QCT官方產品資料](https://www.qct.io/product/index/Server/rackmount-server/GPGPU-Xeon-Phi?page=1) 明列AI／HPC系統的全NVMe GPU Direct Storage，但未證實獨立AI儲存系統 | medium_high | ai_storage_product_required |

## 第一批統計

- 4 個新增候選 Theme；原 `AI_SERVER_RACK_CHASSIS` 已拆成 `AI_SERVER_CHASSIS` 與 `AI_RACK_SYSTEM`。
- 高速線纜不另建 `AI_HIGH_SPEED_CABLE`：其3檔候選與既有 `HIGH_SPEED_CONNECTOR` 股票池完全相同，且既有定義已包含AEC／高速線纜，因此改為補強原Theme證據。
- 13 筆候選對應、11 檔上市／上櫃公司。
- 7 筆新增映射 `evidence_ready`，另有3筆既有映射可升級為公司第一手證據。
- 1 筆（3017）需要公司第一手AI冷板／CDU證據。
- 2 筆（2356、2382）需要獨立AI儲存產品證據。

## 分類邊界複核結論（2026-09-03）

1. `AI_SERVER_CHASSIS` 只描述單機機殼／機箱；`AI_RACK_SYSTEM` 描述包含運算節點、網路與系統整合的整櫃平台。公司可以因不同產品同時成為兩者候選，但必須各自有證據。
2. 原擬 `AI_HIGH_SPEED_CABLE` 與既有 `HIGH_SPEED_CONNECTOR` 都是3526、3533、3665，股票池100%重疊；不新增Theme，改以公司一手來源取代既有媒體證據。
3. `AI_RACK_SYSTEM` 不含只提供Busbar、PDB、電源轉換或備援電力的公司；這些仍歸 `AI_POWER_RACK`、`AI_RACK_POWER_DISTRIBUTION` 等電力Theme。
4. `AI_STORAGE_SYSTEM` 必須是獨立儲存伺服器／平台，且公司明確連結AI、GPU Direct Storage或AI推論／檢索工作負載。AI伺服器內建NVMe或支援GPU Direct Storage，不足以單獨通過。
5. 依此規則，6669維持 `evidence_ready`；2356與2382改為待補獨立儲存產品證據。此Theme目前只有1筆可核准候選，尚不足以形成具廣度的週報Theme。

## 可送人工核准的分批方式

| 批次 | Theme | 本輪可核准候選 | 處理建議 |
|---|---|---|---|
| A | `AI_COLD_PLATE_CDU` | 2308、3324 | 可送人工核准；3017暫不納入 |
| B | `HIGH_SPEED_CONNECTOR` | 3665、3533、3526 | 不新增映射；核准以公司一手來源升級3筆既有證據 |
| C | `AI_RACK_SYSTEM` | 2317、2382、6669 | 三家公司角色一致，可送人工核准 |
| D | `AI_SERVER_CHASSIS` | 8210 | 證據足夠，但目前只有1檔，先保留研究候選較穩妥 |
| E | `AI_STORAGE_SYSTEM` | 6669 | 證據足夠，但目前只有1檔；2356、2382補證前不送核准 |

## 人工審核前必做

1. 為3017補公司官網、年報或公司法說中明列AI冷板／CDU的原始資料。
2. 為2356、2382補公司明列的獨立AI儲存伺服器／平台資料；補到前不列入 `AI_STORAGE_SYSTEM` 核准批次。
3. A、B、C已完成現有Theme重複檢查，可提交人工核准；其中B只升級證據，不新增Theme或股票映射。
4. D、E因候選廣度不足，先保留研究狀態；價格PASS不改變此限制。
