# AI 基礎建設第二批正式核准包（2026-09-05）

本檔只建立人工核准清單，尚未修改正式Theme或股票映射。所有候選均為TWSE／TPEx普通公司股票，價格PASS不作為產業歸屬證據。

## D：新增 `AI_SERVER_CHASSIS`

- 名稱：AI伺服器機殼
- 父Theme：`AI_SERVER`
- Theme Group：`AI_INFRA`（core）
- 納入：明確為AI／GPU伺服器設計或量產的機殼、機箱與其機構設計。
- 排除：一般PC機殼、一般金屬加工，以及整櫃系統整合。

| 股票 | 證據結論 | 公司一手來源 |
|---|---|---|
| 8210 勤誠 | MGX 2U AI Server Chassis | [Chenbro MGX](https://www.chenbro.com/en-US/product/MGX) |
| 3032 偉訓 | 與AI伺服器廠合作開發風冷／水冷機殼，已量產並進入核准供應鏈 | [偉訓官方法說簡報](https://www.hec-group.com.tw/fileadmin/downloads/inventory/EarningsCall/1131211_3032_eng.pdf) |
| 6117 迎廣 | 6.5U GPU Rackmount Chassis專為AI、LLM、深度學習與HPC設計 | [迎廣IW-RG658 PRO](https://ipc.in-win.com/rackmount-chassis-iw-rg658-pro) |

## E：新增 `AI_STORAGE_SYSTEM`

- 名稱：AI儲存系統
- 父Theme：`DATA_CENTER`
- Theme Group：`AI_INFRA`（core）
- 納入：獨立儲存伺服器／平台，且公司明確連結AI訓練、推論、RAG、GPU Direct Storage或AI資料管線。
- 排除：一般SSD、一般儲存伺服器，以及僅為AI伺服器內建NVMe功能者。

| 股票 | 證據結論 | 公司一手來源 |
|---|---|---|
| 6669 緯穎 | GPU啟動、96顆NVMe的Storage-Next架構，服務GNN、LLM推論與RAG | [Wiwynn GTC 2026](https://www.wiwynn.com/news/wiwynn-showcases-nvidia-vera-rubin-nvl72-ai-factory-infrastructure-at-nvidia-gtc-2026) |
| 3693 營邦 | F2026 DPU-ready AI Storage平台，具MLPerf Storage驗證並支援AI訓練與LLM checkpointing | [AIC F2026](https://www.aicipc.com/resources-detail/182/) |
| 2495 普安 | EonStor GS 5000U為AI基礎架構、訓練與推論設計的企業級NVMe儲存 | [Infortrend COMPUTEX 2026](https://www.infortrend.com/tw/event/2026/computex2026) |

## 邊界與重複檢查

- `AI_SERVER_CHASSIS`描述單機機構；不與已核准的`AI_RACK_SYSTEM`整櫃系統混用。
- `AI_STORAGE_SYSTEM`描述獨立資料平台；不因2356、2382的AI伺服器支援NVMe／GPU Direct Storage就納入。
- 六家公司目前均未在正式資料中擁有本批對應Theme，因此不會產生重複股票＋Theme映射。

## 核准後異動量

- 新增2個正式Theme。
- 新增6筆正式股票映射。
- 新增2筆`AI_INFRA` Theme Group關係。
- 不處理3017、2356、2382的待補證項目。

只有使用者明確核准D、E後，才可修改正式資料。
