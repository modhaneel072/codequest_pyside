"""Quiz and assessment grading system."""

import logging
from typing import Dict, Tuple, Any, List

logger = logging.getLogger(__name__)


def grade_quiz(quiz: Dict[str, Any], answers: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
    """
    Grade a quiz based on multiple choice and free response questions.
    
    Policy: 2 MCQ + 1 FRQ, total 100 points.
      - Each MCQ = 40 pts (80 total)
      - FRQ = 20 pts
      
    FRQ grading:
      - Keyword rubric with partial credit
      - Must contain valid fix line if expected_fix_contains is specified
    
    Args:
        quiz: Quiz definition with 'mcq' and 'frq' sections
        answers: User answers with 'mcq' (list) and 'frq' (string)
        
    Returns:
        Tuple of (total_points, detail_dict)
    """
    if not isinstance(quiz, dict) or not isinstance(answers, dict):
        logger.error(f"Invalid quiz or answers type: quiz={type(quiz)}, answers={type(answers)}")
        return 0, {"mcq": [], "frq": {"points": 0, "matched": [], "fix_ok": False}, "error": "Invalid input"}
    
    points = 0
    detail: Dict[str, Any] = {"mcq": [], "frq": {"points": 0, "matched": [], "fix_ok": False}}

    # Grade multiple choice questions
    mcq_items = quiz.get("mcq", [])
    chosen = answers.get("mcq", [])

    for i, q in enumerate(mcq_items):
        try:
            corr = int(q.get("correct_index", 0))
            pick = chosen[i] if i < len(chosen) else None
            ok = (pick == corr)
            earned = 40 if ok else 0
            points += earned
            detail["mcq"].append({
                "ok": ok,
                "earned": earned,
                "picked": pick,
                "correct": corr
            })
            logger.debug(f"MCQ {i}: {'passed' if ok else 'failed'}")
        except (ValueError, TypeError) as e:
            logger.warning(f"Error grading MCQ {i}: {e}")
            detail["mcq"].append({"ok": False, "earned": 0, "error": str(e)})

    # Grade free response question
    frq = quiz.get("frq", {})
    txt = (answers.get("frq", "") or "").lower().strip()

    # Keyword partial credit
    keywords = [k.lower() for k in frq.get("keywords", [])]
    matched = [k for k in keywords if k in txt]
    detail["frq"]["matched"] = matched

    base = 0
    if keywords:
        ratio = len(matched) / max(1, len(keywords))
        base = int(round(20 * ratio))
        logger.debug(f"FRQ: {len(matched)}/{len(keywords)} keywords matched, base score={base}")
    else:
        base = 20 if len(txt) >= 20 else 0
        logger.debug(f"FRQ: no keywords defined, base score={base}")

    # Check for required fix strings
    expected_fix = [s.lower() for s in frq.get("expected_fix_contains", [])]
    fix_ok = True
    if expected_fix:
        fix_ok = any(s in txt for s in expected_fix)
        logger.debug(f"FRQ: fix_ok={fix_ok}")

    detail["frq"]["fix_ok"] = fix_ok

    # Apply fix requirement
    if expected_fix and not fix_ok:
        earned = 0
        logger.info("FRQ: Required fix not found, score=0")
    else:
        earned = base

    detail["frq"]["points"] = earned
    points += earned

    logger.info(f"Quiz graded: total_points={points}")
    return points, detail


def passed(score: int, passing_score: int = 90) -> bool:
    """
    Check if a score is passing.
    
    Args:
        score: Score to check
        passing_score: Minimum score to pass (default: 90)
        
    Returns:
        True if score >= passing_score, False otherwise
    """
    try:
        result = int(score) >= passing_score
        logger.debug(f"Score {score} passed: {result}")
        return result
    except (ValueError, TypeError):
        logger.error(f"Invalid score type: {type(score)}")
        return False