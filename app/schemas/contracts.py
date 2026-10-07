"""
Hợp đồng dữ liệu bất biến giữa 3 module (AGENTS.md §8.1).
Cập nhật hỗ trợ:
- Môn Tin học 12 (bộ Kết Nối Tri Thức Với Cuộc Sống) bám sát Cấu trúc Đề thi Tốt nghiệp THPT 2025.
- Hỗ trợ 3 định dạng câu hỏi:
  1. 'mcq': Trắc nghiệm 4 lựa chọn (Phần I đề thi tốt nghiệp - 24 câu).
  2. 'true_false': Trắc nghiệm Đúng/Sai 4 ý a, b, c, d (Phần II đề thi tốt nghiệp - 4 câu).
  3. 'code': Thực hành lập trình/viết mã (HTML/CSS cho lớp 12, Python cho lớp 10/11).
- Ràng buộc sư phạm linh hoạt: Bài lý thuyết (AI, Mạng) không ép buộc code; bài thực hành (HTML/CSS) có kiểm tra cấu trúc.
"""
from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

BloomLevel = Literal["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"]
QuestionType = Literal["mcq", "true_false", "code"]
TopicType = Literal["theory", "html_css", "python"]
ExecutionStatus = Literal["PASSED", "FAILED", "TIMEOUT", "SYNTAX_ERROR", "SECURITY_VIOLATION"]

MCQ_LETTERS = ("A", "B", "C", "D")
TF_LABELS = ("a", "b", "c", "d")
MIN_TEST_CASES = 5  # Đối với bài code Python (2 normal, 2 boundary, 1 hidden)

# Bảng mã ngộ nhận chuẩn hóa cho 18 bài SGK Tin học 12 KNTT (Predefined Misconception Taxonomy)
MisconceptionCode = Literal[
    "ERR_AI_WEAK_VS_STRONG",        # Bài 1, 2: Nhầm lẫn AI hẹp (Narrow AI) và AI tổng quát (AGI)
    "ERR_AI_ETHICS_BIAS",           # Bài 2: Nhầm lẫn về khía cạnh đạo đức, thiên kiến AI
    "ERR_NET_L2_L3_DEVICE",         # Bài 3: Nhầm lẫn Switch (L2) và Router (L3)
    "ERR_NET_IP_MAC_COLLISION",     # Bài 3, 4: Nhầm lẫn IP logic và MAC vật lý
    "ERR_NET_TCP_UDP_CONFUSION",    # Bài 4: Nhầm tính tin cậy của TCP và tốc độ UDP
    "ERR_NET_RESOURCE_PERMISSION",  # Bài 5: Cấu hình sai quyền Read vs Full Control trong chia sẻ thư mục
    "ERR_ETHICS_COPYRIGHT_FAIRUSE", # Bài 6: Vi phạm bản quyền, hiểu sai quyền trích dẫn số
    "ERR_HTML_TAG_NESTING",         # Bài 7: Đóng/mở sai thứ tự cặp thẻ lồng nhau
    "ERR_HTML_HEADING_VS_P",        # Bài 8: Nhầm thẻ heading (h1-h6) và thẻ paragraph (p)
    "ERR_HTML_TABLE_INCOMPLETE",    # Bài 9: Thiếu thẻ tr hoặc lồng thẻ td/th ngoài table
    "ERR_HTML_HREF_SYNTAX",         # Bài 10: Nhầm thuộc tính href và src, hoặc sai đường dẫn tương đối
    "ERR_HTML_MEDIA_ATTR",          # Bài 11: Thiếu controls/src trong video/audio/iframe
    "ERR_HTML_FORM_METHOD_ACTION",  # Bài 12: Nhầm method (GET/POST) và action của form
    "ERR_CSS_SYNTAX_PROPERTY",      # Bài 13: Cú pháp property: value; sai dấu hai chấm hoặc chấm phẩy
    "ERR_CSS_FONT_FORMATTING",      # Bài 14: Nhầm font-size, font-family, font-weight
    "ERR_CSS_COLOR_SYNTAX",         # Bài 15: Cú pháp mã màu hex, rgb(), tên màu
    "ERR_CSS_BOX_MODEL",            # Bài 16: Nhầm margin (lề ngoài) và padding (đệm trong)
    "ERR_CSS_SPECIFICITY_CONFLICT", # Bài 17: Không hiểu độ ưu tiên Inline > ID > Class > Tag
    "ERR_CSS_INTEGRATION_EXTERNAL", # Bài 18: Nhầm cách nhúng inline, internal <style>, external <link>
    "OTHER_MISCONCEPTION",          # Dự phòng mở rộng
]


class _Strict(BaseModel):
    """Cấm trường lạ: LLM tự chế key sẽ bị từ chối ngay lập tức."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=False)


# ---------------------------------------------------------------------------
# 1. Câu hỏi & Mệnh đề Đúng/Sai (RAG/LLM Engine -> Web)
# ---------------------------------------------------------------------------
class TrueFalseSubItem(_Strict):
    """Một mệnh đề trong câu hỏi Đúng/Sai (Phần II đề thi tốt nghiệp THPT)."""
    label: Literal["a", "b", "c", "d"]
    statement: str = Field(min_length=1)
    is_correct: bool
    cognitive_level: Optional[BloomLevel] = None
    misconception_code: Optional[MisconceptionCode] = None
    explanation: str = Field(min_length=1)


class TestCaseSchema(_Strict):
    """Test case cho bài tập lập trình (Python hoặc HTML structure check)."""
    __test__ = False

    input_data: str
    expected_output: str
    is_hidden: bool = False


class QuestionContract(_Strict):
    id: str = Field(min_length=1)
    chapter_id: str = Field(min_length=1)
    bloom_level: BloomLevel
    question_type: QuestionType
    question_text: str = Field(min_length=1)
    code_snippet: Optional[str] = None
    case_study_context: Optional[str] = None  # Đoạn văn bản ngữ cảnh chung (neo giữ các mệnh đề Đúng/Sai hoặc câu hỏi)
    misconception_map: Optional[dict[str, MisconceptionCode]] = None  # Ánh xạ phương án sai -> mã ngộ nhận

    # Dành cho 'mcq' (Trắc nghiệm 4 lựa chọn)
    options: Optional[List[str]] = None       # Đúng 4 phương án, KHÔNG kèm tiền tố "A."
    correct_answer: Optional[str] = None      # "A" | "B" | "C" | "D"

    # Dành cho 'true_false' (Trắc nghiệm Đúng/Sai 4 ý theo chuẩn Bộ GD&ĐT 2025)
    tf_items: Optional[List[TrueFalseSubItem]] = None

    # Dành cho 'code' (Thực hành HTML/CSS hoặc Python)
    language: Optional[Literal["html", "css", "python"]] = None
    test_cases: Optional[List[TestCaseSchema]] = None
    expected_elements: Optional[List[str]] = None  # Danh sách thẻ/thuộc tính bắt buộc (với HTML)

    explanation: str = Field(min_length=1)

    @model_validator(mode="after")
    def _enforce_pedagogy(self) -> "QuestionContract":
        if self.misconception_map is not None:
            if self.question_type != "mcq":
                raise ValueError("misconception_map chỉ áp dụng cho câu hỏi mcq.")
            for opt_key in self.misconception_map.keys():
                if opt_key not in MCQ_LETTERS:
                    raise ValueError(f"Key trong misconception_map phải là một trong {MCQ_LETTERS}.")
                if opt_key == self.correct_answer:
                    raise ValueError("Đáp án đúng (correct_answer) không được gán mã ngộ nhận lỗi.")

        if self.question_type == "mcq":
            if not self.options or len(self.options) != 4:
                raise ValueError("Câu mcq phải có đúng 4 phương án.")
            if len({o.strip() for o in self.options}) != 4:
                raise ValueError("4 phương án trắc nghiệm không được trùng lặp.")
            if any(o.strip()[:2] in {f"{l}." for l in MCQ_LETTERS} for o in self.options):
                raise ValueError("Phương án không được kèm tiền tố 'A.' — UI tự đánh chữ cái.")
            if self.correct_answer not in MCQ_LETTERS:
                raise ValueError("correct_answer của mcq phải là một trong A, B, C, D.")
            if self.tf_items is not None:
                raise ValueError("Câu mcq không được chứa tf_items.")
            if self.test_cases is not None:
                raise ValueError("Câu mcq không được chứa test_cases.")

        elif self.question_type == "true_false":
            if not self.tf_items or len(self.tf_items) != 4:
                raise ValueError("Câu đúng/sai chuẩn Bộ GD&ĐT phải có đúng 4 mệnh đề a, b, c, d.")
            labels = [item.label for item in self.tf_items]
            if labels != list(TF_LABELS):
                raise ValueError(f"Các mệnh đề phải được gắn nhãn đúng thứ tự {TF_LABELS}.")
            if self.options is not None or self.correct_answer is not None:
                raise ValueError("Câu đúng/sai không dùng options và correct_answer.")
            if self.test_cases is not None:
                raise ValueError("Câu đúng/sai không chứa test_cases.")

            # Invariant khảo thí THPT 2025: Tuyệt đối cấm trường hợp thoái hóa 0 đúng hoặc 4 đúng
            true_count = sum(1 for item in self.tf_items if item.is_correct)
            if true_count in (0, 4):
                raise ValueError("Câu đúng/sai không được toàn đúng (4) hoặc toàn sai (0) để đảm bảo độ phân hóa chuẩn Bộ GD&ĐT.")

        elif self.question_type == "code":
            if self.options is not None or self.correct_answer is not None or self.tf_items is not None:
                raise ValueError("Bài thực hành code không có options, correct_answer hoặc tf_items.")
            if not self.language:
                raise ValueError("Bài code bắt buộc chỉ định trường language ('html', 'css', 'python').")

            # Nếu là bài Python -> bắt buộc test cases
            if self.language == "python":
                tcs = self.test_cases or []
                if len(tcs) < MIN_TEST_CASES:
                    raise ValueError(f"Bài Python cần tối thiểu {MIN_TEST_CASES} test cases.")
                if not any(t.is_hidden for t in tcs):
                    raise ValueError("Bài Python cần ít nhất 1 hidden test chống hardcode.")
                if all(t.is_hidden for t in tcs):
                    raise ValueError("Cần ít nhất 1 test công khai làm ví dụ cho học sinh.")
            # Nếu là bài HTML -> có thể dùng expected_elements hoặc test_cases
            elif self.language in ("html", "css"):
                if not self.expected_elements and not self.test_cases:
                    raise ValueError("Bài tập HTML/CSS cần có expected_elements hoặc test_cases để chấm.")

        return self


# ---------------------------------------------------------------------------
# 2. Nộp bài & Kết quả chấm (Web <-> Sandbox/HTML Evaluator)
# ---------------------------------------------------------------------------
class CodeSubmissionContract(_Strict):
    user_id: str = Field(min_length=1)
    question_id: str = Field(min_length=1)
    student_code: str = Field(max_length=20_000)
    language: Literal["html", "css", "python"] = "html"


class TestResultDetail(_Strict):
    __test__ = False

    index: int = Field(ge=0)
    is_hidden: bool
    passed: bool
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    actual_output: Optional[str] = None

    @model_validator(mode="after")
    def _no_hidden_leak(self) -> "TestResultDetail":
        if self.is_hidden and any(
            v is not None for v in (self.input_data, self.expected_output, self.actual_output)
        ):
            raise ValueError("Hidden test không được lộ input/expected/actual ra client.")
        return self


# Bản đồ barem tính điểm thi chính thức Phần II Đúng/Sai Bộ GD&ĐT 2025 (Official Exam Scoring)
OFFICIAL_EXAM_SCORE_MAP = {
    0: 0.0,
    1: 0.1,
    2: 0.25,
    3: 0.5,
    4: 1.0,
}


class RubricBreakdown(_Strict):
    """Bảng điểm phân rã cấu trúc HTML theo nguyên lý Localized Fatality."""
    structure: float = Field(default=0.0, ge=0.0, le=30.0)
    content: float = Field(default=0.0, ge=0.0, le=20.0)
    attributes: float = Field(default=0.0, ge=0.0, le=20.0)
    grid_consistency: float = Field(default=0.0, ge=0.0, le=30.0)
    total_score: float = Field(default=0.0, ge=0.0, le=100.0)


class ExecutionResultContract(_Strict):
    status: ExecutionStatus
    passed_tests: int = Field(ge=0)
    total_tests: int = Field(ge=0)
    runtime_ms: float = Field(ge=0)
    error_message: Optional[str] = None
    socratic_hint: Optional[str] = None
    test_results: List[TestResultDetail] = Field(default_factory=list)

    # Tầng đánh giá phân rã theo Rubric Invariants (Localized Fatality)
    rubric_breakdown: Optional[RubricBreakdown] = None
    fatal_violations: List[str] = Field(default_factory=list)
    recoverable_warnings: List[str] = Field(default_factory=list)
    task_completion_cap: Optional[float] = None

    @model_validator(mode="after")
    def _consistent_counts(self) -> "ExecutionResultContract":
        if self.passed_tests > self.total_tests:
            raise ValueError("passed_tests không thể lớn hơn total_tests.")
        all_passed = self.total_tests > 0 and self.passed_tests == self.total_tests
        if (self.status == "PASSED") != all_passed:
            raise ValueError("status PASSED <=> qua toàn bộ test (và total_tests > 0).")
        if self.status in {"SYNTAX_ERROR", "SECURITY_VIOLATION"} and self.passed_tests:
            raise ValueError("Code bị chặn trước khi chạy thì passed_tests phải = 0.")
        if self.status != "PASSED" and not self.error_message:
            raise ValueError("Kết quả không PASSED bắt buộc có error_message.")
        if self.test_results:
            if len(self.test_results) > self.total_tests:
                raise ValueError("Số test_results vượt total_tests.")
            if sum(r.passed for r in self.test_results) > self.passed_tests:
                raise ValueError("test_results báo pass nhiều hơn passed_tests.")
        return self


# ---------------------------------------------------------------------------
# 3. Cây tri thức SGK (RAG Engine - Bộ Kết Nối Tri Thức)
# ---------------------------------------------------------------------------
class CurriculumSection(_Strict):
    section_id: str = Field(min_length=1)
    heading: str = Field(min_length=1)
    concepts: List[str] = Field(min_length=1)
    syntax_samples: List[str] = Field(default_factory=list)
    raw_text: str = Field(min_length=1)
    page_start: Optional[int] = Field(default=None, ge=1)


class CurriculumChapter(_Strict):
    chapter_id: str = Field(min_length=1)
    subject: Literal["Tin học"] = "Tin học"
    grade: Literal[10, 11, 12]
    book_series: Literal["Cánh Diều", "Kết Nối Tri Thức"] = "Kết Nối Tri Thức"
    theme: str = Field(min_length=1)               # VD: "Chủ đề: Máy tính và xã hội tri thức"
    chapter: str = Field(min_length=1)             # VD: "Bài 1: Làm quen với Trí tuệ nhân tạo"
    topic_type: TopicType = "theory"               # "theory" | "html_css" | "python"
    sections: List[CurriculumSection] = Field(min_length=1)


# ---------------------------------------------------------------------------
# 4. Yêu cầu sinh đề & Năng lực học sinh
# ---------------------------------------------------------------------------
class GenerationRequestContract(_Strict):
    chapter_id: str = Field(min_length=1)
    section_id: str = Field(min_length=1)
    bloom_level: BloomLevel
    question_type: QuestionType = "mcq"
    count: int = Field(default=1, ge=1, le=20)


class TopicMasteryContract(_Strict):
    user_id: str = Field(min_length=1)
    chapter_id: str = Field(min_length=1)
    tms: float = Field(ge=0.0, le=1.0)
    attempts: int = Field(default=0, ge=0)


InterventionStage = Literal[
    "NORMAL",
    "CORRECTIVE_FEEDBACK",        # Lỗi lần 1: Phản hồi gợi ý sửa sai nhanh
    "CONTRASTIVE_EXAMPLE",       # Lỗi lần 2: So sánh ví dụ tương phản
    "MISCONCEPTION_INTERVENTION", # Lỗi >= 3: Debugging/Counter-example -> Self-explanation -> Re-test
]


class CognitiveCoverage(_Strict):
    remember: bool = False
    understand: bool = False
    apply: bool = False
    analyze: bool = False


class AssessmentEvidence(_Strict):
    attempts: int = Field(default=0, ge=0)
    correct: int = Field(default=0, ge=0)
    recent_correct_streak: int = Field(default=0, ge=0)


class MisconceptionRecord(_Strict):
    code: MisconceptionCode
    count: int = Field(default=1, ge=1)
    last_seen: str
    status: Literal["active", "cleared", "intervention_required"] = "active"


class NodeMasteryDetail(_Strict):
    """Trạng thái làm chủ một nút kiến thức bài học trong SGK (Knowledge Node)."""
    chapter_id: str = Field(min_length=1)
    chapter_title: str = Field(min_length=1)
    tms: float = Field(ge=0.0, le=1.0)
    attempts: int = Field(default=0, ge=0)
    correct_count: int = Field(default=0, ge=0)
    evidence: Optional[AssessmentEvidence] = None
    cognitive_coverage: Optional[CognitiveCoverage] = None
    active_misconceptions: List[MisconceptionCode] = Field(default_factory=list)
    misconceptions: List[MisconceptionRecord] = Field(default_factory=list)
    intervention_stage: InterventionStage = "NORMAL"
    prerequisite_met: bool = True


class StudentKnowledgeStateContract(_Strict):
    """Mô hình trạng thái kiến thức học sinh (Longitudinal Student Knowledge State)."""
    user_id: str = Field(min_length=1)
    user_name: str = Field(min_length=1)
    knowledge_nodes: dict[str, NodeMasteryDetail]
    misconception_frequencies: dict[str, int] = Field(default_factory=dict)
    recommended_chapter_id: Optional[str] = None
    prerequisite_warning: Optional[str] = None
