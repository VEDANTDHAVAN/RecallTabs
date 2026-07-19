import pytest
from app.services.llm_service import LLMService


@pytest.mark.asyncio
async def test_complete():
    llm = LLMService()

    result = await llm.complete(
        """
        Return valid JSON only.

        {
          "topic":"",
          "summary":"",
          "keywords":[]
        }

        Text: FastAPI is a modern Python framework.
        """
    )

    print(result)

    assert result is not None