# Theme Approval Policy

## Purpose

Theme 是本專案的主要交易分類軸；官方產業分類保留作為市場大類與 fallback metadata，不作為細題材的主要判斷依據。

## Core principles

1. 一檔股票可以屬於多個 Theme，但每一個 Stock→Theme mapping 都必須有可查核證據。
2. 不因市場傳聞、單一社群貼文或一次性「概念股」標籤直接 approved。
3. Candidate 與 Formal mapping 分離。研究中的關聯只能進 pending/candidate；只有通過本政策才可進 active + approved/auto_approved。
4. 若既有 Theme 已足以表達關聯，優先使用既有 Theme，避免為同義詞重複造 Theme。
5. 新 Theme 必須能回答「這個題材是否有多檔股票可形成同步資金行為？」；若只是單一公司產品名，原則上不建立獨立 Theme。
6. 細 Theme 不以證交所／櫃買中心大類分類作為主要來源。法說逐字稿、法說簡報、公司產品資料、主流財經新聞、券商研究、Alpha Memo AI、富果等研究平台皆可用於細 Theme 發現與驗證。
7. 法說會不是必要條件。若法說未明確提及，但多個獨立且可信的新聞／研究來源長期反覆確認，並具體指出產品、技術、客戶、出貨、認證或供應鏈關係，仍可人工 approved。
8. 反之，法說若僅提到評估、關注、可能合作或未來布局，且缺乏其他實質證據，不因出現在法說中就自動視為正式 Theme。

## Evidence hierarchy

### HIGH
- COMPANY_OFFICIAL：公司官網、產品頁、新聞稿
- ANNUAL_REPORT：年報
- INVESTOR_CONFERENCE：法說會／投資人簡報／法說逐字稿
- MOPS / OFFICIAL_REGULATOR：公開資訊觀測站、主管機關、交易所／櫃買中心正式資料

### MEDIUM_HIGH
- BROKER_ANALYST：券商／法人研究
- FINANCIAL_MEDIA：主流財經媒體，且內容有具體業務／產品／客戶／出貨依據
- RESEARCH_PLATFORM：Alpha Memo AI、富果等具產業研究內容的平台
- INDUSTRY_EXPERT：可信產業研究或專家資料

### LOW / NOT SUFFICIENT FOR FORMAL APPROVAL
- 單一媒體僅列「概念股」而無具體業務證據
- 社群、論壇、聊天室、未具名傳聞
- 僅因股價同漲而反推公司業務屬於某 Theme

## Relationship role

每筆正式 mapping 應增加或在研究檔標示角色：

- `core`：公司明確核心產品／服務／技術，或已形成可辨識事業線。
- `related`：有明確產品、供應鏈、應用或客戶關係，但不是核心營收主體。
- `emerging`：公司已公開投入、驗證、量產初期或新事業轉型，關聯成立但仍在早期。

## Approval rules

### auto_approved
僅限高可信且規則可機器化的官方分類／監管資料，並且 Theme 定義與來源分類是一對一或高度直接對應。

### approved
可由人工審核通過：
- 至少一個 HIGH 證據，且內容直接支持 Theme；或
- 至少兩個互相獨立的 MEDIUM_HIGH 證據，且描述具體產品／業務／技術／出貨／客戶鏈結；或
- 一個 MEDIUM_HIGH 主來源加上法說／公司資料中的擦邊但一致訊號，整體足以支持實質產業關聯。

### pending
下列情況維持 pending：
- 只有市場題材稱號，缺乏公司層級或實質產業證據。
- 公司只是表示「關注／評估／合作可能」，尚無具體產品或商業化內容。
- Theme 定義過寬或與現有 Theme 高度重疊，尚未完成去重。
- 多篇文章其實只是轉載同一來源，不能當成多個獨立證據。

## Reverse checks before approval

每筆 Stock→Theme 升格前必須回答：

1. 這家公司是否真的有產品、業務、技術、客戶或供應鏈關聯，而不是只有股市標籤？
2. 證據是否仍具時效性，而不是多年以前的一次性事件？
3. 拿掉股票名稱後，僅看證據內容是否仍足以判定屬於該 Theme？
4. 是否已有更精準的既有 Theme 可以使用，避免重複造 Theme？
5. 若屬 parent/child Theme，同時 mapping 是否會造成重複計算或語意膨脹？
6. 多個新聞／研究來源是否真正獨立，而不是彼此轉載同一則材料？

任一題無法合理回答，就不得直接 approved。

## New Theme creation gate

新增 Theme 前至少滿足：

- 有清楚、可長期理解的市場題材定義。
- 至少存在 2 檔以上可被證據支持的候選股票，或有明確理由預期形成供應鏈／同題材群聚。
- 與現有 Theme 不只是同義詞。
- 能對資金同步分析產生額外資訊，而不是只增加標籤數量。
- 先進 research/candidate staging，再進 theme_master。

## Theme reverse-pool workflow

每一個新或既有 Theme 都必須反向建立成分股池：

1. 先定義 Theme。
2. 從法說、公司資料、新聞、券商研究、Alpha Memo AI、富果等來源搜尋可能成分股。
3. 逐檔驗證並標示 core / related / emerging。
4. 通過規則後把 Theme 寫回每檔股票 mapping。
5. 研究過程若發現新的細 Theme，再建立候選 Theme 並重複以上流程。

## Priority audit order

1. 市場重要 Theme 的反向成分股池。
2. 市場重要個股多 Theme 缺口。
3. 已有 Theme 下的重要漏股。
4. 從重要個股與新聞／研究反推缺失的新 Theme。
5. zero-approved Theme 補強。
6. 長尾個股與低交易重要性 Theme。

## Operational safeguard

任何批次正式升格前：

- 先在 `data/research/` 產生 audit/staging 檔。
- 記錄 source_type、publisher、published_date、source_url、evidence_summary、confidence、role、decision。
- 通過人工規則檢查後，才更新 `theme_master.csv` / `stock_theme_map.csv` / `theme_group_map.csv`。
- 每批更新後必須跑完整 CI，確認 validator、weekly metrics、Theme summary、Group summary 全部成功。
