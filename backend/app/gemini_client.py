"""Gemini API 클라이언트를 감싸는 간단한 래퍼입니다."""

# 타입 힌트를 위해 Optional을 가져옵니다.
from typing import Optional

# Google Generative AI 라이브러리를 가져옵니다.
import google.generativeai as genai
# 생성 관련 설정을 위한 타입을 가져옵니다.
from google.generativeai.types import GenerationConfig

# 프로젝트 설정 값을 가져옵니다.
from .config import Settings

# Gemini 모델에게 역할을 부여하고 지시사항을 정의하는 시스템 프롬프트입니다.
SUMMARY_SYSTEM_PROMPT = (
    "You are a helpful assistant that summarizes user provided text. "
    "Return the summary in exactly three lines. Each line should be concise "
    "and capture a key aspect of the input. 한국어로 답하라."
    # "당신은 사용자가 제공한 텍스트를 요약하는 유용한 어시스턴트입니다. "
    # "요약은 반드시 세 줄로 반환해야 합니다. 각 줄은 간결해야 하며 "
    # "입력 내용의 핵심적인 측면을 담아야 합니다. 한국어로 답하세요."
)


class GeminiClient:
    """Gemini 모델과 통신하는 클라이언트입니다."""

    def __init__(self, settings: Settings) -> None:
        """
        GeminiClient를 초기화합니다.

        Args:
            settings: API 키와 모델 이름 등 설정을 담고 있는 객체입니다.
        """
        settings.validate()  # 설정 값의 유효성을 검사합니다.
        # Google Generative AI 라이브러리에 API 키를 설정합니다.
        genai.configure(api_key=settings.gemini_api_key)
        # 설정에 지정된 모델 이름으로 GenerativeModel 인스턴스를 생성합니다.
        self._model = genai.GenerativeModel(model_name=settings.gemini_model)

    def summarize(self, text: str) -> str:
        """제공된 텍스트를 세 줄로 요약합니다."""
        """
        Args:
            text: 요약할 텍스트입니다.

        Returns:
            모델이 생성한 요약 텍스트입니다.

        Raises:
            RuntimeError: Gemini API 응답에 텍스트 출력이 없는 경우 발생합니다.
        """
        # Gemini 모델에 콘텐츠 생성을 요청합니다.
        response = self._model.generate_content(
            # 시스템 프롬프트와 사용자 텍스트를 함께 전달합니다.
            contents=[SUMMARY_SYSTEM_PROMPT, f"Source text:\n{text.strip()}"],
            # 생성 결과에 대한 설정을 지정합니다.
            generation_config=GenerationConfig(
                max_output_tokens=300,  # 최대 출력 토큰 수를 300으로 제한합니다.
                temperature=0.4,      # 생성 결과의 다양성을 조절합니다. (낮을수록 결정적)
            ),
        )
        # 응답 객체에서 'text' 속성을 가져옵니다. 없으면 None을 반환합니다.
        summary = getattr(response, "text", None)
        if not summary:
            # 요약 내용이 없으면 오류를 발생시킵니다.
            raise RuntimeError("Gemini response did not contain text output.")
        # 앞뒤 공백을 제거한 요약 텍스트를 반환합니다.
        return summary.strip()