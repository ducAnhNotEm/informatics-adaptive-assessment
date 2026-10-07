"""
Kiểm thử hợp đồng dữ liệu chuẩn Tin học 12 (Cánh Diều)
Bao gồm:
- Toàn bộ mock files nạp thành công 100%.
- Kiểm tra tính hợp lệ của câu hỏi MCQ (Phần I thi THPT).
- Kiểm tra tính hợp lệ của câu Đúng/Sai 4 ý (Phần II thi THPT).
- Kiểm tra bài thực hành HTML (expected_elements) và Python (test_cases).
"""
import copy
import json
from pathlib import Path
import pytest
from pydantic import ValidationError

from app.schemas.contracts import (
    CodeSubmissionContract,
    CurriculumChapter,
    ExecutionResultContract,
    QuestionContract,
    StudentKnowledgeStateContract,
    TestResultDetail,
    TopicMasteryContract,
    TrueFalseSubItem,
)

MOCK = Path(__file__).resolve().parents[1] / "data" / "mock"


def load(name):
    return json.loads((MOCK / name).read_text(encoding="utf-8"))


QUESTIONS = load("mock_questions.json")
MCQ = next(q for q in QUESTIONS if q["question_type"] == "mcq")
TF = next(q for q in QUESTIONS if q["question_type"] == "true_false")
CODE_HTML = next(q for q in QUESTIONS if q["question_type"] == "code")


def test_all_mock_files_match_contracts():
    for q in QUESTIONS:
        QuestionContract.model_validate(q)
    for e in load("mock_execution.json"):
        ExecutionResultContract.model_validate(e["result"])
    for c in load("mock_curriculum.json"):
        CurriculumChapter.model_validate(c)
    for m in load("mock_mastery.json"):
        TopicMasteryContract.model_validate(m)
    StudentKnowledgeStateContract.model_validate(load("mock_student_state.json"))


def test_mock_covers_all_question_types():
    types = {q["question_type"] for q in QUESTIONS}
    assert "mcq" in types
    assert "true_false" in types
    assert "code" in types


# ---------- Kiểm thử tính nghiêm ngặt của MCQ (Phần I) ----------
def _mut(base, **changes):
    d = copy.deepcopy(base)
    d.update(changes)
    return d


@pytest.mark.parametrize("bad", [
    _mut(MCQ, options=["A", "B", "C"]),                       # Thiếu 1 phương án
    _mut(MCQ, options=["A", "A", "B", "C"]),                  # Trùng lặp
    _mut(MCQ, options=["A. A", "B. B", "C. C", "D. D"]),      # Kèm tiền tố chữ cái
    _mut(MCQ, correct_answer="Z"),                            # Đáp án ngoài dải
    _mut(MCQ, tf_items=[]),                                   # MCQ nhưng lại có tf_items
])
def test_invalid_mcq_rejected(bad):
    with pytest.raises(ValidationError):
        QuestionContract.model_validate(bad)


# ---------- Kiểm thử tính nghiêm ngặt của Đúng/Sai 4 ý (Phần II) ----------
@pytest.mark.parametrize("bad", [
    _mut(TF, tf_items=TF["tf_items"][:3]),                   # Chỉ có 3 mệnh đề (phải đủ 4)
    _mut(TF, options=["A", "B", "C", "D"]),                  # Đúng/Sai lại có options MCQ
    _mut(TF, correct_answer="A"),                            # Đúng/Sai lại có đáp án A
    _mut(TF, tf_items=[{**item, "label": "x"} for item in TF["tf_items"]]),  # Nhãn sai thứ tự
    _mut(TF, tf_items=[{**item, "is_correct": True} for item in TF["tf_items"]]),   # Cả 4 ý đều Đúng (0 phân hóa)
    _mut(TF, tf_items=[{**item, "is_correct": False} for item in TF["tf_items"]]),  # Cả 4 ý đều Sai (0 phân hóa)
])
def test_invalid_true_false_rejected(bad):
    with pytest.raises(ValidationError):
        QuestionContract.model_validate(bad)


@pytest.mark.parametrize("true_count", [1, 2, 3])
def test_valid_true_false_distributions(true_count):
    """Đảm bảo các tỷ lệ phân bố 1 Đúng/3 Sai, 2 Đúng/2 Sai, 3 Đúng/1 Sai đều hợp lệ."""
    items = copy.deepcopy(TF["tf_items"])
    for i, it in enumerate(items):
        it["is_correct"] = (i < true_count)
    good = _mut(TF, tf_items=items)
    QuestionContract.model_validate(good)


# ---------- Kiểm thử Misconception Taxonomy & Metadata ----------
def test_mcq_misconception_on_correct_answer_rejected():
    """Đáp án đúng không được gán mã ngộ nhận lỗi."""
    bad = _mut(MCQ, misconception_map={"A": "ERR_AI_WEAK_VS_STRONG"})  # 'A' là correct_answer
    with pytest.raises(ValidationError):
        QuestionContract.model_validate(bad)


def test_mcq_misconception_invalid_option_key_rejected():
    """Key phải thuộc A, B, C, D."""
    bad = _mut(MCQ, misconception_map={"Z": "ERR_AI_WEAK_VS_STRONG"})
    with pytest.raises(ValidationError):
        QuestionContract.model_validate(bad)


# ---------- Kiểm thử bài thực hành Code HTML/Python ----------
def test_valid_html_code_question():
    QuestionContract.model_validate(CODE_HTML)


def test_html_missing_expected_elements_rejected():
    bad = _mut(CODE_HTML, expected_elements=None, test_cases=None)
    with pytest.raises(ValidationError):
        QuestionContract.model_validate(bad)


def test_code_question_missing_language_rejected():
    bad = _mut(CODE_HTML, language=None)
    with pytest.raises(ValidationError):
        QuestionContract.model_validate(bad)


# ---------- Kiểm thử Localized Fatality & Explainable Student State ----------
def test_execution_result_with_localized_fatality():
    """Kiểm tra cấu trúc phân rã Localized Fatality và Rubric Breakdown."""
    res = ExecutionResultContract(
        status="FAILED",
        passed_tests=1,
        total_tests=4,
        runtime_ms=15.0,
        error_message="Thiếu thẻ bọc gốc <table> nhưng dữ liệu hàng/cột hợp lệ.",
        socratic_hint="Bảng HTML bắt buộc phải có thẻ bọc nào ngoài cùng?",
        fatal_violations=["Missing required root <table>"],
        recoverable_warnings=[],
        task_completion_cap=0.70,
        rubric_breakdown={
            "structure": 0.0,
            "content": 20.0,
            "attributes": 20.0,
            "grid_consistency": 15.0,
            "total_score": 55.0,
        },
    )
    assert res.rubric_breakdown.total_score == 55.0
    assert "Missing required root <table>" in res.fatal_violations


def test_explainable_student_knowledge_state():
    """Kiểm tra mô hình Student Knowledge State với Evidence và Intervention Stage."""
    state = StudentKnowledgeStateContract.model_validate(load("mock_student_state.json"))
    node_b03 = state.knowledge_nodes["tin12_kntt_b03"]
    assert node_b03.intervention_stage == "MISCONCEPTION_INTERVENTION"
    assert node_b03.evidence.attempts == 8
    assert node_b03.evidence.correct == 3
    assert node_b03.misconceptions[0].count == 4
    assert node_b03.misconceptions[0].status == "intervention_required"

