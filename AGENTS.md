# INFORMATICS AI EDTECH - PROJECT RULES & AGENT GOVERNANCE
## Hệ Thống Ôn Luyện & Đánh Giá Năng Lực Môn Tin Học 12 (Kết Nối Tri Thức) Chuẩn Đề Thi Tốt Nghiệp THPT 2025

---

## 00. The Top 0.1% Elite Engineering Standard (Tiêu chuẩn Kỹ thuật Đỉnh cao Top 0.1%)

> **TÔN CHỈ BẮT BUỘC**: Mọi quyết định kiến trúc, giải thuật và dòng code trong dự án này **BẮT BUỘC phải đạt tư duy và chuẩn mực của Top 0.1% Kỹ sư Xuất sắc nhất trong ngành (Principal Systems Architect / EdTech Chief Engineer)**.  
> Tuyệt đối cấm tư duy "làm cho chạy được", code chắp vá phong trào, biến sản phẩm thành "bài tập lớn sinh viên thông thường" hay "ChatGPT Wrapper hời hợt".

> **ĐỊNH LUẬT VÀNG KHẢO THÍ (The AIED Assessment Axiom)**:  
> **"LLM proposes. Deterministic engine verifies. Student Model remembers. Pedagogical Policy decides."**  
> *(LLM đề xuất $\to$ Máy kiểm chứng xác định $\to$ Hồ sơ học sinh ghi nhớ $\to$ Chính sách sư phạm phán quyết)*

### 5 Trụ Cột Thực Thi của Top 0.1%:
1. **Clean Architecture & Decoupled Modularization (Kiến trúc Sạch & Phân rã Độc lập)**:
   - Cấm viết code "Spaghetti", nhồi nhét xử lý RAG, chấm bài và logic Web vào chung controller hay router.
   - Mọi module cốt lõi (RAG Bóc tách SGK, HTML DOM Evaluator, Python Code Sandbox, Adaptive Engine, Evaluation Benchmark) phải được đóng gói thành các Service độc lập, giao tiếp thông qua Data Contract (Pydantic Schema v2 / Type Hints) bất biến, plug-and-play.
2. **Defensive Design & Zero-Failure Resiliency (Thiết kế Phòng thủ & Chống sụp đổ tuyệt đối)**:
   - Luôn giả định: LLM bên thứ ba có thể timeout hoặc trả về JSON lỗi cú pháp/ảo giác; mã của học sinh nộp có thể chứa lỗi thẻ HTML vỡ giao diện hoặc vòng lặp vô tận trong bài code.
   - Bắt buộc có cơ chế HTML DOM validation độc lập, Sandbox cách ly tài nguyên, Timeout cưỡng bức, và Circuit Breaker tự động chuyển đổi giữa Local LLM (Ollama) và Cloud API (Gemini).
3. **Deterministic Mathematical Rigor over Stochastic AI (Toán học & Cơ học xác định trên hết)**:
   - LLM **CHỈ LÀ** tầng giao tiếp & sinh nội dung thô (Semantic Parser / Question Drafter).
   - Tuyệt đối không để LLM chấm điểm bài làm bằng cảm tính: Việc chấm bài **BẮT BUỘC** thực thi bằng Trình phân tích cú pháp thẻ (HTML DOM Parser) và Trình thông dịch Python thực tế qua bộ Test Cases chuẩn.
   - Thuật toán cá nhân hóa thích ứng phải được tính bằng công thức toán học xác định ($TMS$ - Topic Mastery Score), không "chém gió" bằng prompt bí ẩn.
4. **Deep Real-World Domain Modeling (Mô hình hóa sâu sắc bản chất sư phạm môn Tin học 12)**:
   - Bám sát thực tế chuẩn chương trình GDPT 2018 môn Tin học 12 (bộ Kết nối tri thức với cuộc sống - KNTT) và Cấu trúc Đề thi Tốt nghiệp THPT Quốc gia từ năm 2025 (Phần I: 24 câu trắc nghiệm 4 lựa chọn; Phần II: 4 câu Đúng/Sai 4 ý a, b, c, d).
   - Mô hình hóa chuẩn xác 4 cấp độ thang nhận thức Bloom (Nhận biết $\to$ Thông hiểu $\to$ Vận dụng $\to$ Vận dụng cao), triệt tiêu hoàn toàn hiện tượng câu hỏi "Nhận biết trá hình".
5. **Simplicity as the Ultimate Sophistication (Đỉnh cao của sự tinh tế là sự giản đơn)**:
   - Không thêm thư viện thừa thãi. YAGNI (You Aren't Gonna Need It). Tận dụng tối đa thư viện chuẩn Python (stdlib: `html.parser`, `urllib`, `sqlite3`, `subprocess`, `ast`).

---

## 0. Triết Lý Coding — Lazy Senior Dev (Ponytail Principle)

> **"The best code is the code never written."**  
> Lấy cảm hứng từ [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) — chuẩn hóa cho dự án EdTech.

Trước khi viết **bất kỳ** dòng code nào, dừng lại ở bậc thang đầu tiên còn thỏa mãn:

```
1. Tính năng này có thực sự cần thiết không?   → Không: Loại bỏ ngay. (YAGNI)
2. Đã có trong codebase chưa?                 → Tái sử dụng — kiểm tra app/services/ trước.
3. Thư viện chuẩn Python (stdlib) có sẵn?     → Dùng luôn (html.parser, subprocess, ast, json, re, sqlite3).
4. Package đã cài đặt có làm được không?       → Dùng package đó (FastAPI, Pydantic, python-docx, PyMuPDF). Cấm cài bừa.
5. Viết gọn trong vài dòng code sạch được ko? → Viết ngắn gọn, rõ ràng.
6. Chỉ khi không còn cách nào khác:           → Viết code mới tối thiểu đủ chạy an toàn.
```

### 🔒 Quy tắc An toàn Bất biến (Safety Overrides — Luôn thắng bậc thang trên):
- **Bảo mật Sandbox & DOM Parser** $\to$ **TUYỆT ĐỐI KHÔNG CẮT GIẢM** (Timeout + AST Check + Memory Cap).
- **Validation dữ liệu Pydantic (`extra='forbid'`)** $\to$ **BẮT BUỘC** cho mọi JSON từ LLM và request từ Client.
- **Tính toán điểm số & Test Case** $\to$ **LUÔN DÙNG Engine xác định**, cấm để LLM tự chấm nhẩm.
- **Khóa API Key** $\to$ **CHỈ LƯU BACKEND** (`.env`), tuyệt đối không lộ lên Frontend/Git.

---

## 1. Quy Trình Làm Việc Bắt Buộc Của AI Agent (Mandatory Agent Workflow)

Mọi thao tác chỉnh sửa hoặc tạo code mới phải tuân thủ nghiêm ngặt 8 bước:

```
NHIỆM VỤ ĐƯỢC GIAO
      │
      ▼
1. ĐỌC KỸ AGENTS.md & PROJECT_CONTEXT.md
      │
      ▼
2. KIỂM TRA HIỆN TRẠNG CODEBASE (Inspect app/schemas/contracts.py, services, data/mock)
      │
      ▼
3. TRÁNH TRÙNG LẶP & ĐẢM BẢO TƯƠNG THÍCH (Check API Contracts & Pydantic Schemas)
      │
      ▼
4. PHÂN TÍCH ẢNH HƯỞNG & LẬP KẾ HOẠCH TỪNG BƯỚC
      │
      ▼
5. THỰC THI CODE (Bảo tồn các chức năng đang chạy ổn định)
      │
      ▼
6. CHẠY TEST THỰC TẾ TRÊN BỘ DỮ LIỆU CHUẨN (pytest test_contracts.py & ground_truth.json)
      │  ┌────────────────────────────────────────────────────────┐
      ├──┤ Nếu test fail: Áp dụng Root-Cause Debugging (Mục 1.1)  │
      │  └────────────────────────────────────────────────────────┘
      ▼
7. CƠ CHẾ PHẢN BIỆN CHÉO (Challenger Review Checkpoint - Mục 1.2)
      │
      ▼
8. CẬP NHẬT TRẠNG THÁI (IMPLEMENTATION_STATUS.md) & BÁO CÁO KẾT QUẢ
```

### 1.1. Systematic Root-Cause Debugging Protocol (Truy vết Lỗi Gốc rễ):
- ❌ **CẤM CHỮA CHÁY BỀ MẶT**: Cấm bọc `try-except pass` hoặc hardcode điều kiện để làm xanh test một cách giả tạo khi test bị fail.
- ✅ **4 Bước Bắt buộc**:
  1. **Quan sát & Cô lập**: Đọc kỹ traceback, chỉ rõ dòng code và điều kiện biên (edge case) làm phát sinh lỗi.
  2. **Tái hiện Tối thiểu (Minimal Reproduction)**: Viết 1 test case nhỏ cô lập đúng payload gây crash.
  3. **Tìm Nguyên nhân Gốc rễ**: Lỗi ở logic toán học, ở cấu trúc prompt LLM hay ở giới hạn môi trường?
  4. **Can thiệp Đúng điểm & Kiểm thử Hồi quy**: Sửa tại gốc, chạy lại toàn bộ test suite (`pytest -q`) để bảo đảm zero-regression.

### 1.2. Challenger Review Protocol (Cơ chế Phản biện Chéo):
Trước khi xác nhận hoàn thành một module, Agent phải tự chất vấn bằng 3 câu hỏi của hội đồng khó tính:
1. *Nếu học sinh nộp mã HTML vỡ thẻ hoặc mã Python chứa vòng lặp vô tận thì hệ thống có sập không?*
2. *Nếu LLM trả về JSON bị thiếu mệnh đề hoặc sinh câu hỏi ngoài phạm vi SGK KNTT thì hệ thống xử lý thế nào?*
3. *Công thức cá nhân hóa $TMS$ có code chạy thật trong DB hay chỉ là biến giả lập?*

---

## 2. BỘ LUẬT CHỐNG ẢO GIÁC & "NÓI BỪA" (ANTI-HALLUCINATION & MODEL ASSURANCE)

> **TÔN CHỈ TỐI CAO (Học từ Model Assurance Manifesto):**  
> **"LLM được thiết kế với vai trò là SEMANTIC PARSER & CONTENT DRAFTER, tuyệt đối KHÔNG PHẢI là một Decision Maker hay Chân lý Độc lập."**

Hệ thống bắt buộc tuân thủ **5 Định Luật Bất Biến Chống Ảo Giác**:

### 📜 Định luật 1: Semantic Parser, NOT Decision Maker (Phân lập Quyền lực)
* LLM chỉ có nhiệm vụ: Đọc văn bản bài học SGK, sinh bản nháp câu hỏi (MCQ / Đúng-Sai) và biên soạn lời gợi ý sư phạm gợi mở (Socratic Hint).
* LLM **TUYỆT ĐỐI CẤM** tự quyết định điểm số của học sinh. 
* Mọi điểm số phải do **Deterministic Engine** (HTML DOM Parser, Test Runner, TMS Math Engine) phán quyết dựa trên sự thật khách quan.

### 📜 Định luật 2: Zero-Curriculum Hallucination (Khóa Chặt Cây Tri Thức SGK)
* Mọi câu hỏi sinh ra **CHỈ ĐƯỢC PHÉP TRUY XUẤT** kiến thức nằm trong phạm vi đoạn văn bản của đúng bài học được chỉ định trong SGK Tin học 12 Kết nối tri thức.
* Nghiêm cấm đem kiến thức ngoài chương trình phổ thông vào đề thi (ví dụ: không đưa JavaScript nâng cao, PHP, React vào các bài HTML/CSS; không đưa công nghệ ngoài luồng vào bài AI).
* **Provenance bắt buộc**: Mọi câu hỏi phải lưu vết số trang SGK KNTT gốc (`page_start`, `source`).

### 📜 Định luật 3: Zero-Unchecked-Code (Cấm Tuyệt Đối Code Ma / Code Lỗi)
* Mọi đoạn mã HTML/CSS hoặc Python xuất hiện trong đề bài hoặc phương án trả lời do AI sinh ra **BẮT BUỘC PHẢI CHẠY QUA BỘ KIỂM DUYỆT (CodeValidator)**.
* Nếu đoạn mã bị lỗi cú pháp (`SyntaxError`), thẻ HTML không hợp lệ hoặc không thể render $\to$ Loại bỏ ngay lập tức và regenerate. Cấm hiển thị câu hỏi có code lỗi cho học sinh.

### 📜 Định luật 4: Plausible Diagnostic Distractors (Phương Án Nhiễu Có Cơ Sở)
* Đối với câu hỏi trắc nghiệm 4 lựa chọn (MCQ): 3 phương án sai (nhiễu) **KHÔNG ĐƯỢC PHÉP LÀ TỪ NGỮ BỊA ĐẶT NGẪU NHIÊN**, mà phải phản ánh đúng các ngộ nhận tư duy phổ biến của học sinh (ví dụ: nhầm thẻ `<th>` với `<td>`, nhầm thuộc tính `target="_blank"`, nhầm Switch với Router).
* Trường `explanation` bắt buộc giải thích rõ lý do từng phương án sai.

### 📜 Định luật 5: Pydantic Strict Validation (`extra="forbid"`)
* Mọi phản hồi từ LLM phải được validate qua Pydantic Schema ở chế độ nghiêm ngặt. Nếu LLM tự chế thêm trường lạ (như `"test_list"`, `"custom_field"`) hoặc thiếu các trường bắt buộc, API từ chối ngay lập tức ở tầng gateway.

---

## 3. Chuẩn Mực Bóc Tách SGK Tin Học 12 KNTT (Curriculum Ground Truth)

Dựa trên **Mục lục chính thức của SGK Tin học 12 — Kết nối tri thức với cuộc sống**, hệ thống khóa chặt phạm vi 4 Chủ đề kiến thức chung (Trang 5 đến 105):

```
CHỦ ĐỀ 1: MÁY TÍNH VÀ XÃ HỘI TRI THỨC (Trang 5 - 13)
  ├── Bài 1: Làm quen với Trí tuệ nhân tạo (Trang 5)        [topic_type: theory]
  └── Bài 2: Trí tuệ nhân tạo trong KH & ĐS (Trang 9)      [topic_type: theory]

CHỦ ĐỀ 2: MẠNG MÁY TÍNH VÀ INTERNET (Trang 14 - 33)
  ├── Bài 3: Một số thiết bị mạng thông dụng (Trang 14)     [topic_type: theory]
  ├── Bài 4: Giao thức mạng (Trang 21)                     [topic_type: theory]
  └── Bài 5: Thực hành chia sẻ tài nguyên (Trang 26)       [topic_type: theory]

CHỦ ĐỀ 3: ĐẠO ĐỨC, PHÁP LUẬT VÀ VĂN HOÁ TRONG MÔI TRƯỜNG SỐ (Trang 34 - 38)
  └── Bài 6: Giao tiếp và ứng xử trong không gian mạng     [topic_type: theory]

CHỦ ĐỀ 4: GIẢI QUYẾT VẤN ĐỀ VỚI SỰ TRỢ GIÚP CỦA MÁY TÍNH (Trang 39 - 105)
  ├── [PHẦN HTML]
  │   ├── Bài 7: HTML và cấu trúc trang web (Trang 39)     [topic_type: html_css]
  │   ├── Bài 8: Định dạng văn bản (Trang 46)              [topic_type: html_css]
  │   ├── Bài 9: Tạo danh sách, bảng (Trang 52)            [topic_type: html_css]
  │   ├── Bài 10: Tạo liên kết (Trang 57)                  [topic_type: html_css]
  │   ├── Bài 11: Tệp đa phương tiện & iframe (Trang 62)   [topic_type: html_css]
  │   └── Bài 12: Tạo biểu mẫu (Trang 67)                  [topic_type: html_css]
  └── [PHẦN CSS]
      ├── Bài 13: Khái niệm, vai trò của CSS (Trang 71)    [topic_type: html_css]
      ├── Bài 14: Định dạng văn bản bằng CSS (Trang 76)    [topic_type: html_css]
      ├── Bài 15: Tạo màu cho chữ và nền (Trang 83)        [topic_type: html_css]
      ├── Bài 16: Định dạng khung (Trang 89)               [topic_type: html_css]
      ├── Bài 17: Các mức ưu tiên của bộ chọn (Trang 96)   [topic_type: html_css]
      └── Bài 18: Thực hành tổng hợp (Trang 102)           [topic_type: html_css]
```

### Schema Lưu Trữ Cây Tri Thức (`CurriculumChapter`):
```json
{
  "chapter_id": "tin12_kntt_b07",
  "subject": "Tin học",
  "grade": 12,
  "book_series": "Kết Nối Tri Thức",
  "theme": "Chủ đề 4: Giải quyết vấn đề với sự trợ giúp của máy tính",
  "chapter": "Bài 7: HTML và cấu trúc trang web",
  "topic_type": "html_css",
  "sections": [
    {
      "section_id": "b07.1",
      "heading": "1. Cấu trúc cơ bản của tài liệu HTML",
      "concepts": ["HTML", "thẻ đóng mở", "phần tử", "thuộc tính", "doctype"],
      "syntax_samples": ["<!DOCTYPE html>", "<html>", "<head>", "<body>"],
      "raw_text": "Tài liệu HTML được cấu tạo bởi các phần tử...",
      "page_start": 39
    }
  ]
}
```

---

## 4. Đặc Tả Thang Tư Duy Bloom & Định Dạng Khảo Thí THPT 2025

Bám sát Cấu trúc Đề thi Tốt nghiệp THPT môn Tin học từ năm 2025:

| Cấp độ Bloom | Định dạng câu hỏi | Bản chất kỹ thuật kiểm tra | Chuẩn mực chất lượng |
| :--- | :--- | :--- | :--- |
| **1. Nhận biết (Remember)** | Trắc nghiệm 4 lựa chọn (`mcq`) | Khái niệm AI, thiết bị mạng, từ khóa, tên thẻ HTML/CSS (`<p>`, `<a>`, `<table>`). | Bám sát định nghĩa trong SGK KNTT, không hỏi mẹo. |
| **2. Thông hiểu (Understand)** | Trắc nghiệm 4 lựa chọn (`mcq`) hoặc Đúng/Sai (`true_false`) | Đọc đoạn mã HTML/CSS, dự đoán hiển thị; hoặc phân tích tình huống mạng LAN/IP. | Đoạn mã phải chuẩn cú pháp W3C; Đúng/Sai có đúng 4 mệnh đề $a, b, c, d$. |
| **3. Vận dụng (Apply)** | Đúng/Sai 4 ý (`true_false`) hoặc MCQ Điền khuyết | Điền thẻ còn thiếu vào biểu mẫu form/bảng; phân tích mô hình mạng trường học/gia đình. | Ngữ cảnh thực tế gắn với cuộc sống theo tinh thần KNTT. |
| **4. Vận dụng cao (Create/Analyze)** | Thực hành viết mã (`code`) | Viết mã HTML/CSS tạo trang web (bảng, danh sách, form) hoặc bài toán tối ưu. | Chấm tự động qua **HTML DOM Parser** kiểm tra đầy đủ các thẻ yêu cầu. |

---

## 5. Chuẩn Mực Chấm Bài Thực Hành (Deterministic Evaluators)

### 5.1. Module Chấm Thực Hành HTML/CSS (`html_evaluator.py`)
- Sử dụng `html.parser` (thư viện chuẩn Python, không cần cài thêm package).
- Phân tích cú pháp tài liệu HTML học sinh nộp:
  1. Kiểm tra tính hợp lệ cú pháp (Cặp thẻ mở/đóng, không có thẻ lỗi).
  2. Đối chiếu danh sách thẻ bắt buộc (`expected_elements`, ví dụ: `["table", "tr", "th", "td"]`).
  3. Kiểm tra các thuộc tính chỉ định (ví dụ: `target="_blank"`, `type="text"`).
- Hoàn toàn an toàn (No-execution): Không chạy tiến trình con, không lo mã độc hại.

### 5.2. Module Sandbox Python (`sandbox_runner.py` - Dự phòng mở rộng lớp 10, 11)
- Lớp 1: Static AST Analysis chặn danh sách đen (`os`, `sys`, `subprocess`, `eval`, `exec`).
- Lớp 2: Subprocess Execution với Timeout 2.0 giây, Memory Cap 128MB.
- Lớp 3: Test Suite Runner kiểm tra 5 test cases (2 normal, 2 boundary, 1 hidden).

---

## 6. Thuật Toán Cá Nhân Hóa Xác Định (Deterministic Adaptive Engine)

> **NGUYÊN TẮC**: Mọi quyết định tăng/giảm độ khó và gợi ý bài tập đều bắt buộc chạy bằng thuật toán toán học lưu vết trong Database.

### 6.1. Chỉ Số Làm Chủ Chủ Đề (Topic Mastery Score - $TMS$)
Với mỗi học sinh $u$ và chủ đề/bài học $k$, hệ thống duy trì điểm $TMS_{u,k} \in [0.0, 1.0]$.  
Sau mỗi lượt làm bài hoặc kiểm tra:

$$TMS_{u,k}^{(t)} = \alpha \cdot TMS_{u,k}^{(t-1)} + (1 - \alpha) \cdot S^{(t)}$$

* Trong đó: $\alpha = 0.7$ (Trọng số lịch sử), $1 - \alpha = 0.3$ (Trọng số phiên hiện tại), $S^{(t)} \in [0.0, 1.0]$ là tỷ lệ điểm đạt được.

### 6.2. Ma Trận Phân Bổ Câu Hỏi Thích Ứng

| Ngưỡng $TMS_{u,k}$ | Phân loại năng lực | Ma trận sinh câu hỏi phiên tiếp theo | Hành động sư phạm của hệ thống |
| :---: | :---: | :---: | :--- |
| **$TMS < 0.50$** | **Cần Củng Cố** | 70% Nhận biết, 30% Thông hiểu, 0% Vận dụng | Tập trung ôn lại khái niệm cốt lõi, trích dẫn số trang SGK KNTT cần đọc lại. |
| **$0.50 \le TMS \le 0.80$** | **Đạt Chuẩn** | 30% Nhận biết, 40% Thông hiểu, 30% Vận dụng | Rèn luyện câu hỏi Đúng/Sai 4 ý và đọc hiểu cú pháp mã nguồn. |
| **$TMS > 0.80$** | **Khá / Giỏi** | 10% Thông hiểu, 30% Vận dụng, 60% Thực hành Code | Thách thức bằng bài thực hành thiết kế trang web HTML/CSS hoàn chỉnh. |

---

## 7. Quy Chuẩn Kiểm Định Khoa Học (Ground Truth 30-Question Benchmark)

Hệ thống tích hợp file đối chứng `data/ground_truth_30.json` gồm 30 câu hỏi chuẩn hóa do giáo viên Tin học 12 biên soạn bám sát SGK Kết nối tri thức:
- 10 câu Nhận biết (Trắc nghiệm 4 lựa chọn).
- 10 câu Thông hiểu (Đoán output HTML hoặc Đúng/Sai mạng máy tính).
- 6 câu Vận dụng (Tình huống thực tế Đúng/Sai hoặc điền khuyết).
- 4 bài Vận dụng cao (Thực hành viết mã HTML kèm danh sách thẻ bắt buộc).

### Bộ Chỉ Số Đánh Giá Độc Lập (Evaluation Metrics):
1. **Code Syntax Validity Rate**: $\text{CSVR} = 100\%$ (Mọi đoạn mã AI sinh ra phải hợp lệ cú pháp).
2. **Bloom Level Alignment Accuracy**: $\ge 80\%$ (Giáo viên xác nhận đúng cấp độ).
3. **Curriculum Grounding Accuracy**: $100\%$ (Mọi câu hỏi đều trích dẫn chính xác số trang SGK KNTT).

---

## 8. Hợp Đồng Dữ Liệu Pydantic Chuẩn Hóa (`app/schemas/contracts.py`)

Hợp đồng dữ liệu bất biến giữa 3 kỹ sư được mã hóa chặt chẽ trong [`app/schemas/contracts.py`](file:///d:/AI_hoc_tap/app/schemas/contracts.py):
- `QuestionContract`: Hỗ trợ 3 loại `question_type` (`mcq`, `true_false`, `code`).
- `TrueFalseSubItem`: Chuẩn hóa 4 mệnh đề $a, b, c, d$ cho câu hỏi Đúng/Sai.
- `CodeSubmissionContract`: Hỗ trợ nộp mã `html`, `css` hoặc `python`.
- `ExecutionResultContract`: Chuẩn hóa kết quả chấm (5 trạng thái bất biến).

---

## 9. Kiến Trúc AI Tự Chủ & Cơ Chế Phòng Thủ Kép (Local-First & Circuit Breaker)

- **Lõi Chính Khi Triển Khai Thực Địa (Offline Support)**:
  - Máy chủ cục bộ **Ollama** (`http://localhost:11434`) chạy mô hình **`qwen2.5-coder:7b`** hoặc **`llama3.2:3b`**.
  - Đảm bảo hệ thống có thể chạy trong phòng máy trường THPT không có kết nối internet ổn định.
- **Lõi Fallback Điện Toán Đám Mây (Circuit Breaker cho Buổi Demo)**:
  - Tự động chuyển mạch sang **Google Gemini 1.5/2.0 Flash API** khi kết nối Ollama bị từ chối hoặc thời gian sinh câu hỏi $> 5.0\text{ giây}$.
  - Bảo đảm buổi bảo vệ đồ án **LUÔN LUÔN MƯỢT MÀ**, phản hồi chỉ trong 1–2 giây, không bao giờ bị đứng máy trước mắt hội đồng.

---

## 10. Tiêu Chuẩn Giao Diện Phòng Thi Thực Địa (Field-Grade EdTech UI/UX)

1. **Khung Soạn Thảo Chuẩn Monaco Editor**:
   - Tích hợp Monaco Editor (nhân VS Code) hỗ trợ highlight HTML, CSS, Python.
2. **Bố Cục 3 Phân Vùng (Split-Pane Desktop UI)**:
   - **Vùng Trái (40%)**: Đề bài, yêu cầu thẻ/test case, trích dẫn số trang SGK KNTT liên quan.
   - **Vùng Phải Trên (45%)**: Trình soạn thảo mã của học sinh.
   - **Vùng Phải Dưới (15%)**: Terminal kết quả chấm thẻ/test cases (Xanh: Pass, Đỏ: Fail kèm lời khuyên Socratic).
3. **Dashboard Giáo Viên Trực Quan**:
   - Biểu đồ phân bổ năng lực học sinh theo 4 mức Bloom trong từng bài học SGK KNTT.
   - Nút 1-chạm: *"Xuất Đề Thi Ra File Word (.docx)"* chuẩn mẫu trình bày đề thi tốt nghiệp của Bộ GD&ĐT.
