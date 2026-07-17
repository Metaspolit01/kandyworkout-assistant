from typing import Optional, Dict

import httpx
from google import genai
from google.genai import types
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from config.settings import settings
from config.logger import logger


class GeminiClient:
    """Google Gemini client using the latest google-genai SDK."""

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        self.model = settings.GEMINI_MODEL
        self.temperature = settings.GEMINI_TEMPERATURE
        self.max_tokens = settings.GEMINI_MAX_TOKENS

        logger.info(f"Gemini client initialized (Model: {self.model})")

    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(
            multiplier=settings.RETRY_DELAY_SECONDS,
            min=1,
            max=10,
        ),
        retry=retry_if_exception_type(
            (
                httpx.TimeoutException,
                httpx.ConnectError,
            )
        ),
    )
    def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate a completion using Gemini."""

        prompt = f"{system_prompt}\n\n{user_prompt}"

        try:
            config = types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )

            if (
                response_format
                and response_format.get("type") == "json_object"
            ):
                config.response_mime_type = "application/json"

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )

            logger.info("Gemini response generated successfully")

            return response.text

        except Exception as e:
            logger.error(
                f"Gemini ({self.model}) failed: {e}",
                exc_info=True,
            )
            raise

    async def generate_completion_async(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[Dict[str, str]] = None,
    ) -> str:
        """Generate a completion asynchronously."""

        prompt = f"{system_prompt}\n\n{user_prompt}"

        try:
            config = types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )

            if (
                response_format
                and response_format.get("type") == "json_object"
            ):
                config.response_mime_type = "application/json"

            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config,
            )

            logger.info("Gemini async response generated successfully")

            return response.text

        except Exception as e:
            logger.error(
                f"Gemini ({self.model}) async failed: {e}",
                exc_info=True,
            )
            raise