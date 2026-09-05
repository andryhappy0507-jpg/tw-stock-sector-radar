# AI 基礎建設正式核准包（2026-09-05）

本檔是人工核准前的精確變更清單，不代表已核准，也不直接修改 `theme_master.csv`、`stock_theme_map.csv` 或 `theme_group_map.csv`。價格 PASS 不作為產業歸屬依據。

## 建議核准範圍

### A：新增 `AI_COLD_PLATE_CDU`

- 名稱：AI冷板／CDU
- 父Theme：`LIQUID_COOLING`
- Theme Group：`AI_INFRA`（core）
- 定義：具體供應AI資料中心冷板、CDU、Manifold或其關鍵液冷模組。
- 排除：只有一般散熱、風扇、熱管或未揭露產品位置的液冷概念。

| 股票 | 正式角色 | 證據 | 建議 |
|---|---|---|---|
| 2308 台達電 | AI資料中心冷板、CDU與完整液冷系統 | [Delta COMPUTEX 2026](https://www.deltaww.com/en-US/landing/Computex-2026) | 新增正式映射 |
| 3324 雙鴻 | Cold Plate、CDU與Manifold | [Auras官方液冷資料](https://www.auras.com.tw/CMSFS/InformationCenters/English/ecfc7b18-d55e-4ca3-a673-b449f83d051c.pdf) | 新增正式映射 |

3017奇鋐不在本批：公司官網目前只證實整體散熱方案，尚未明列AI冷板或CDU。

### B：沿用 `HIGH_SPEED_CONNECTOR` 並升級證據

不新增 `AI_HIGH_SPEED_CABLE`。擬議股票池與現有 `HIGH_SPEED_CONNECTOR` 均為3526、3533、3665，重疊率100%，且現有Theme定義已包含PCIe高速線纜、AEC與高速資料互連。

| 股票 | 原證據 | 新公司一手證據 | 建議 |
|---|---|---|---|
| 3665 貿聯-KY | 財經媒體、medium | [BizLink官方資料中心方案](https://telecom-networking.bizlinktech.com/applications/bizlink-data-center-solutions/) 明列800G以上ACC／AEC與最高1.6T DAC | 保留映射，證據升為high |
| 3533 嘉澤 | 財經媒體、medium | [嘉澤MCIO產品頁](https://www.lotes.cc/zh-tw/product.php?act=view&id=805)與[MGX合作新聞](https://www.lotes.cc/zh-tw/news.php?act=view&id=34) | 保留映射，證據升為high |
| 3526 凡甲 | 財經媒體、medium | [凡甲2025年報](https://www.alltopconnector.com/data/information/files/1779087124881442433.pdf)明列升級伺服器高速連接線與AI資料中心需求 | 保留映射，證據升為high |

### C：新增 `AI_RACK_SYSTEM`

- 名稱：AI整櫃系統
- 父Theme：`AI_SERVER`
- Theme Group：`AI_INFRA`（core）
- 定義：具AI運算節點、網路與整櫃系統整合能力的rack-scale平台。
- 排除：單一機殼、一般伺服器，以及只供應Busbar、PDB、電源轉換或備援電力者。

| 股票 | 正式角色 | 證據 | 建議 |
|---|---|---|---|
| 2317 鴻海 | AI機櫃級系統整合與AI資料中心方案 | [鴻海官方新聞](https://www.foxconn.com/zh-tw/press-center/press-releases/latest-news/2053) | 新增正式映射 |
| 2382 廣達 | AI／HPC Rackmount與整櫃運算系統 | [QCT官方產品資料](https://www.qct.io/product/index/Server/rackmount-server/GPGPU-Xeon-Phi?page=1) | 新增正式映射 |
| 6669 緯穎 | Vera Rubin NVL72與AMD Helios rack-scale AI平台 | [Wiwynn COMPUTEX 2026](https://www.wiwynn.com/events/computex) | 新增正式映射 |

## 本批明確不處理

| 候選Theme | 股票 | 原因 |
|---|---|---|
| `AI_SERVER_CHASSIS` | 8210 勤誠 | 證據足夠，但目前只有1檔，先保留研究候選 |
| `AI_STORAGE_SYSTEM` | 6669 緯穎 | 獨立AI儲存證據足夠，但目前只有1檔，先保留研究候選 |
| `AI_STORAGE_SYSTEM` | 2356 英業達、2382 廣達 | 現有證據只有AI伺服器內建NVMe／GPU Direct Storage功能，未證實獨立AI儲存平台 |

## 核准後的精確異動量

- 新增2個正式Theme：`AI_COLD_PLATE_CDU`、`AI_RACK_SYSTEM`。
- 新增5筆正式股票映射：2308、3324；2317、2382、6669。
- 更新3筆既有映射證據：3526、3533、3665的 `HIGH_SPEED_CONNECTOR`。
- 新增2筆 `AI_INFRA` Theme Group關係。
- 不新增 `AI_HIGH_SPEED_CABLE`，不處理3017、8210、2356的正式歸屬。

## 核准閘門

只有使用者明確核准A、B、C後，才可製作正式化程式與修改正式資料；若只核准部分批次，必須只執行被點名的批次。
