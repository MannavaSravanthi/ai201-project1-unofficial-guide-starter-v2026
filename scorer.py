import gate


def judge(question, expects, answer, results) -> bool:
    """
    Correct = the phrase in `expects` shows up somewhere in `answer`
    (case-insensitive). That's the definition questions.py already commits
    to: "expects is a word or short phrase you'd expect a correct answer
    to contain."

    A refusal (gate didn't let the question through) never counts as
    correct here — these are the `answered()` questions, ones you expect
    your corpus to cover, so a refusal on one of them is a miss.
    """
    if answer is None or expects is None:
        return False

    if answer == gate.REFUSAL:
        return False

    return str(expects).strip().lower() in str(answer).strip().lower()