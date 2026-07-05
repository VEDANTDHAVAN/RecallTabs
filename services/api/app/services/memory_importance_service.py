from typing import Any

class MemoryImportanceService:
    def calculate(
        self,
        question_or_tab: Any,
        answer: str | None = None,
        sources: list[dict] | None = None,
    ) -> float:
        if answer is None and hasattr(question_or_tab, "importance_score"):
            return self.calculate_tab(question_or_tab)

        return self.calculate_message(
            str(question_or_tab),
            answer or "",
            sources or [],
        )

    # Computes an importance score (0-1) for assistant messages.
    def calculate_message(
        self, question: str, answer: str,
        sources: list[dict],
    ) -> float:
        score = 0.30
        # Longer questions are usually more meaningful
        if len(question) > 50:
            score += 0.15

        # Longer answers usually contain more knowledge
        if len(answer) > 300:
            score += 0.20

        # Reward grounded answers
        if len(sources) > 0:
            score += 0.20

        # Reward highly detailed answers
        if len(answer) > 1000:
            score += 0.15

        return min(score, 1.0)

    # Computes and stores an importance score (0-100) for saved tabs.
    def calculate_tab(self, tab) -> float:
        score = 50.0

        score += min(tab.open_count or 0, 10) * 2
        score += min(tab.chat_reference_count or 0, 10) * 3

        if tab.summary:
            score += 10

        if tab.word_count and tab.word_count > 500:
            score += 10

        if tab.last_chat_at:
            score += 10

        tab.importance_score = min(score, 100.0)

        return tab.importance_score
