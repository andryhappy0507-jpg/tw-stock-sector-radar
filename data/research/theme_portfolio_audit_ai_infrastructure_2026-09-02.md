# Theme 產業架構盤點與 AI 基礎建設細分候選（2026-09-03）

- 資料來源：GitHub Actions #175（ec77259）
- 市場資料基準日：2026-09-03
- Active Theme：119；Active Theme Group：25
- 核准映射：661 筆、534 檔股票；人工證據 216 筆、官方自動分類 445 筆

## 結論

機器人已完成細分 Theme、證據矩陣、人工核准與週訊號，是目前最完整的人工題材樣板。其他產業已具備骨架，但成熟度不一致：半導體、生技、能源與航運主要依官方大分類；AI、PCB、被動元件與連接器則是小型人工證據池，仍需擴充與澄清邊界。

共有 49 個 active Theme 尚無正式映射，其中 15 個是結構父節點、34 個是真正尚未覆蓋的葉節點。父節點為零不一定是錯誤，但葉節點為零代表 taxonomy 已建立、證據池尚未完成。

## Theme Group 覆蓋盤點

| Theme Group | Theme數 | 正式股票數 | 人工池 | 官方自動 | 成熟度 |
|---|---:|---:|---:|---:|---|
| 半導體供應鏈族群（SEMICONDUCTOR_SUPPLY） | 9 | 206 | 17 | 206 | 混合 |
| 生技醫療族群（BIOTECH_CLUSTER） | 1 | 159 | 0 | 159 | 官方廣覆蓋 |
| 能源基建族群（ENERGY_INFRA） | 19 | 60 | 15 | 46 | 混合 |
| 航運族群（SHIPPING_CLUSTER） | 3 | 34 | 1 | 34 | 混合 |
| 機器人族群（ROBOTICS_CHAIN） | 14 | 28 | 28 | 0 | 人工證據池 |
| 電子核心零組件族群（ELECTRONICS_CORE） | 9 | 15 | 15 | 0 | 人工證據池 |
| AI基礎建設族群（AI_INFRA） | 14 | 14 | 14 | 0 | 人工證據池 |
| 數位基礎建設族群（DIGITAL_INFRA） | 21 | 12 | 12 | 0 | 人工證據池 |
| 顯示面板族群（DISPLAY_CLUSTER） | 4 | 12 | 12 | 0 | 人工證據池 |
| PCB供應鏈族群（PCB_CHAIN） | 9 | 12 | 12 | 0 | 人工證據池 |
| 被動元件族群（PASSIVE_CLUSTER） | 5 | 10 | 10 | 0 | 人工證據池 |
| 先進封裝族群（ADV_PACKAGING_CHAIN） | 4 | 7 | 7 | 0 | 人工證據池 |
| 連接器族群（CONNECTOR_CLUSTER） | 6 | 6 | 6 | 0 | 人工證據池 |
| 軍工航太族群（DEFENSE_AERO） | 4 | 4 | 4 | 0 | 人工證據池 |
| 智慧移動族群（SMART_MOBILITY） | 8 | 4 | 4 | 0 | 人工證據池 |
| 消費服務族群（CONSUMER_SERVICES） | 5 | 3 | 3 | 0 | 人工證據池 |
| 散熱族群（COOLING_CLUSTER） | 2 | 3 | 3 | 0 | 人工證據池 |
| 金融族群（FINANCE_CLUSTER） | 1 | 3 | 3 | 0 | 人工證據池 |
| 記憶體族群（MEMORY_CHAIN） | 3 | 3 | 3 | 0 | 人工證據池 |
| 智慧電網族群（SMART_GRID_CLUSTER） | 3 | 3 | 3 | 0 | 人工證據池 |
| 軟體雲端資安族群（SOFTWARE_CLOUD） | 6 | 3 | 3 | 0 | 人工證據池 |
| 傳統產業族群（TRADITIONAL_INDUSTRY） | 9 | 3 | 3 | 0 | 人工證據池 |
| 風力發電族群（WIND_POWER_CLUSTER） | 4 | 3 | 3 | 0 | 人工證據池 |
| 邊緣AI族群（AI_EDGE） | 2 | 2 | 2 | 0 | 人工證據池 |
| 高速光通訊族群（OPTICAL_INTERCONNECT） | 3 | 1 | 1 | 0 | 人工證據池 |

## AI 基礎建設現況

| Theme | 父Theme | 股票數 | 人工核准 | 平均週報酬 | 上漲比 |
|---|---|---:|---:|---:|---:|
| AI（AI） | — | 0 | 0 | — | — |
| AI伺服器（AI_SERVER） | AI | 2 | 2 | 0.4% | 100.0% |
| 資料中心（DATA_CENTER） | AI | 1 | 1 | -0.6% | 0.0% |
| 散熱（COOLING） | AI_SERVER | 2 | 2 | -0.9% | 0.0% |
| 液冷（LIQUID_COOLING） | COOLING | 2 | 2 | 13.4% | 50.0% |
| 電源（POWER） | AI_SERVER | 0 | 0 | — | — |
| 電源供應器（POWER_SUPPLY） | POWER | 3 | 3 | -1.8% | 0.0% |
| UPS/BBU備援電力（UPS_BBU） | POWER | 4 | 4 | -6.5% | 0.0% |
| HVDC/800V AI電源（HVDC_AI_POWER） | POWER | 3 | 3 | -1.8% | 0.0% |
| AI伺服器BBU（AI_SERVER_BBU） | UPS_BBU | 4 | 4 | -6.5% | 0.0% |
| AI電源機櫃/Power Rack（AI_POWER_RACK） | POWER | 4 | 4 | 0.3% | 33.3% |
| AI機櫃配電/Busbar/PDB（AI_RACK_POWER_DISTRIBUTION） | AI_POWER_RACK | 2 | 2 | -0.6% | 0.0% |
| AI伺服器連接器（AI_SERVER_CONNECTOR） | CONNECTOR | 3 | 3 | 1.5% | 66.7% |
| 高功率大電流連接器（HIGH_POWER_CONNECTOR） | CONNECTOR | 2 | 2 | 0.8% | 50.0% |

### 需要澄清的重疊

- `POWER_SUPPLY` 與 `HVDC_AI_POWER`：相同股票池，交集 3／聯集 3 檔。
- `UPS_BBU` 與 `AI_SERVER_BBU`：相同股票池，交集 4／聯集 4 檔。

### 價格資料警示

- 已隔離疑似公司行動或價格不連續股票：4747、6669；正式 Theme 平均報酬與上漲比不納入這些觀測值。

## AI 基礎建設細分候選架構

| 產業層 | Theme／候選Theme | 名稱 | 建議 | 納入範圍 | 排除範圍 |
|---|---|---|---|---|---|
| 運算系統 | `AI_SERVER` | AI伺服器 | 保留 | AI伺服器、加速運算伺服器與整機／系統級ODM | 僅供應單一零組件者 |
| 資料中心平台 | `DATA_CENTER` | 資料中心 | 澄清邊界 | 資料中心基礎設施平台、整體電力或機房級解決方案 | 單一伺服器或一般雲端軟體 |
| 熱管理 | `COOLING` | 散熱 | 保留為父Theme | AI伺服器風冷、液冷與熱管理總類 | 非資料中心用途的一般消費電子散熱 |
| 熱管理 | `LIQUID_COOLING` | 液冷 | 保留 | 冷板、CDU、歧管、泵浦與液冷系統 | 只有一般風扇或熱管產品 |
| 熱管理 | `AI_COLD_PLATE_CDU` | AI冷板／CDU | 新增候選 | 具體供應AI資料中心冷板、CDU或液冷關鍵模組 | 只有液冷概念但未揭露產品位置 |
| 電源轉換 | `POWER_SUPPLY / HVDC_AI_POWER` | 電源供應／HVDC 800V | 澄清父子邊界 | POWER_SUPPLY涵蓋一般伺服器電源；HVDC只收AI資料中心高壓直流架構 | 兩個Theme使用完全相同證據而無AI專用佐證 |
| 備援電力 | `UPS_BBU / AI_SERVER_BBU` | UPS／AI伺服器BBU | 澄清父子邊界 | UPS_BBU為一般備援電力；AI_SERVER_BBU須有AI伺服器機櫃應用證據 | 僅有一般電池模組或消費電子電池 |
| 機櫃供配電 | `AI_POWER_RACK / AI_RACK_POWER_DISTRIBUTION` | Power Rack／Busbar／PDB | 保留並澄清 | Power Rack為系統級機櫃；配電Theme限Busbar、PDB等機櫃內配電 | 一般機構件或無配電功能的機櫃 |
| 高速互連 | `AI_SERVER_CONNECTOR / HIGH_POWER_CONNECTOR` | AI伺服器連接器／大電流連接器 | 澄清功能邊界 | 分開高速訊號互連與高功率大電流連接，不以同一證據重複核准 | 一般消費性連接器 |
| 高速互連 | `AI_HIGH_SPEED_CABLE` | AI高速線纜／AEC | 新增候選 | AI叢集高速銅纜、AEC或機櫃間高速線纜 | 一般電源線或低速消費性線材 |
| 光網路 | `CPO / OPTICAL_COMMUNICATION` | CPO／光通訊 | 跨族群沿用 | 沿用既有高速光通訊族群，作為AI基礎建設related關係 | 複製建立內容相同的新Theme |
| 機構系統 | `AI_SERVER_CHASSIS` | AI伺服器機殼 | 新增候選 | AI伺服器專用機殼、機箱與其機構設計 | 整櫃運算平台、Power Rack電源系統或一般金屬加工 |
| 機構系統 | `AI_RACK_SYSTEM` | AI整櫃系統 | 新增候選 | 具AI運算節點、網路與整櫃整合能力的rack-scale平台 | 單一機殼、一般伺服器或只提供機櫃供配電者 |
| 儲存系統 | `AI_STORAGE_SYSTEM` | AI儲存系統 | 新增候選 | 獨立儲存伺服器或平台，並明確連結AI、GPU Direct Storage或AI檢索工作負載 | 一般消費性SSD、一般儲存伺服器或僅為AI伺服器內建NVMe功能者 |

## 建議執行順序

1. 先修正或隔離除權／分割等公司行動造成的週報酬異常。
2. 對現有 AI 基礎建設 Theme 做邊界去重，不先新增股票。
3. 為 `AI_COLD_PLATE_CDU`、`AI_HIGH_SPEED_CABLE`、`AI_SERVER_CHASSIS`、`AI_RACK_SYSTEM`、`AI_STORAGE_SYSTEM` 建立證據候選池。
4. CPO／光通訊沿用既有 Theme，新增 AI_INFRA 的 related 關係，避免重複 taxonomy。
5. 完成公司證據矩陣後再交由使用者人工核准；價格 PASS 不作為概念股資格證據。
