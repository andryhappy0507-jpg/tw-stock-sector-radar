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
9. Theme mapping 的「正確性」與 Theme 股池的「完整性」分開管理；CI 通過不得等同宣稱 coverage 完整。
10. 任何市場重要 Theme 在完成 Coverage Audit 前不得標示為 `coverage_ready` 或對外稱為完整股池。

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

角色只描述 Theme 對公司的重要程度，不等於是否納入 Theme breadth。只要關聯經證據確認，core / related / emerging 都可以納入資金擴散觀察，但應分層統計。

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

## Theme discovery and coverage workflow

市場重要 Theme 必須依序經過以下五層，不能只從既有名單找證據：

1. **Market discovery**：先定義 Theme 關鍵字、同義詞、子題與鄰接供應鏈，從全市場尋找可能候選。
2. **Candidate generation**：整合公司官網／產品頁、法說、年報、監管資料、產業鏈、主流財經媒體、研究平台等多來源候選。
3. **Evidence verification**：逐檔驗證實質產品／技術／客戶／出貨／供應鏈關係，標示 core / related / emerging 與證據強度。
4. **Coverage audit**：合併 formal + staging + new discovery，反向檢查是否仍有市場重要漏股，並記錄 suspected_missing / need_evidence 等未解項目。
5. **Human gate + formal mapping + CI**：重要 Theme 由人工確認後才可寫入正式 mapping；CI 負責資料與程式一致性，不代替投資語意審核。

標準流程為：

`Discovery → Candidate → Evidence → Coverage Audit → User Review → Formal Mapping → CI`

不得再把「已知名單 → 找證據 → CI」視為完整 Theme 建置流程。

## Coverage status

重要 Theme 在 `data/theme_coverage_rules.csv` 記錄 coverage 狀態：

- `discovery`：仍在廣泛找候選，不能宣稱股池完整。
- `auditing`：已有初步股池，正在查漏與補證據。
- `coverage_ready`：已完成一輪完整漏股檢查，且沒有 unresolved `suspected_missing` 候選。

`coverage_ready` 只代表「發現完整度達到目前標準」，不代表所有候選都已人工核准，也不代表未來不會因公司新布局而新增成分股。

每個重要 Theme 都應輸出 Coverage Summary，至少包含：

- formal approved 數量
- coverage pool 總數
- staging 數量
- awaiting user review 數量
- need evidence 數量
- suspected missing 數量
- discovery keyword 數量

## Company ↔ Theme bidirectional audit

Theme discovery 必須雙向進行：

- Theme → Company：從題材與供應鏈尋找所有可能公司。
- Company → Theme：研究公司時，同步檢查其主要業務、新事業與多個 Theme 關聯。

公司不應被單一 Theme 定義；Theme 只是公司主體資料上的多對多關聯。未來公司主頁應作為主要實體，Theme 頁面反向引用公司及其關聯角色。

## Theme reverse-pool workflow

每一個新或既有 Theme 都必須反向建立成分股池：

1. 先定義 Theme。
2. 從法說、公司資料、新聞、券商研究、Alpha Memo AI、富果等來源搜尋可能成分股。
3. 逐檔驗證並標示 core / related / emerging。
4. 執行 Coverage Audit，確認是否仍有重要漏股。
5. 通過人工規則後把 Theme 寫回每檔股票 mapping。
6. 研究過程若發現新的細 Theme，再建立候選 Theme 並重複以上流程。

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
- 市場重要 Theme 必須有 coverage audit 檔並登錄於 `data/theme_coverage_rules.csv`。
- `coverage_status=coverage_ready` 時不得仍存在 unresolved suspected_missing。
- 通過人工規則檢查後，才更新 `theme_master.csv` / `stock_theme_map.csv` / `theme_group_map.csv`。
- 每批更新後必須跑完整 CI，確認 validator、coverage summary、weekly metrics、Theme summary、Group summary 全部成功。
