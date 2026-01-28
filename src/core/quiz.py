# -*- coding: utf-8 -*-
def grade_quiz(spec: dict, answers: list[int]):
    qs = spec.get("questions", [])
    if len(answers) != len(qs):
        return False, 0, "Answer count mismatch."
    correct = 0
    for i, q in enumerate(qs):
        if answers[i] == q.get("answer_index"):
            correct += 1
    score = int(round(100 * correct / max(1, len(qs))))
    pass_score = spec.get("pass_score", 80)
    passed = score >= pass_score
    return passed, score, f"{correct}/{len(qs)} correct ({score}%)."
