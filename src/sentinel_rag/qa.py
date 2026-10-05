from dataclasses import dataclass

from .domain import Citation, GroundedAnswer
from .llm import LanguageModel
from .retrieval import SemanticRetriever


@dataclass
class GroundedQA:
    retriever: SemanticRetriever
    model: LanguageModel
    minimum_score: float = 0.2

    def ask(self, repository: str, question: str, limit: int = 5) -> GroundedAnswer:
        evidence = [
            chunk
            for chunk in self.retriever.retrieve(repository, question, limit)
            if chunk.score >= self.minimum_score
        ]
        if not evidence:
            return GroundedAnswer(
                answer="Insufficient repository evidence to answer this question.",
                citations=[],
                confidence=0.0,
                status="insufficient-evidence",
            )

        answer = self.model.answer(question, evidence)
        citations = [
            Citation(path=item.path, start_line=item.start_line, end_line=item.end_line)
            for item in evidence
        ]
        confidence = min(1.0, max(item.score for item in evidence))
        return GroundedAnswer(
            answer=answer,
            citations=citations,
            confidence=confidence,
            status="grounded",
        )
