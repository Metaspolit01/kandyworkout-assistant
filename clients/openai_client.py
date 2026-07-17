from openai import OpenAI, AsyncOpenAI
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

from config.settings import settings
from config.logger import logger


class OpenAIClient:
    """OpenAI API client with retry logic."""
    
    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.async_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        logger.info("OpenAI client initialized")
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def generate_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate a completion using OpenAI API."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            if response_format:
                kwargs["response_format"] = response_format
            
            response = self.client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content
            
            logger.debug(f"OpenAI completion generated successfully")
            return content
            
        except Exception as e:
            logger.error(f"Error generating OpenAI completion: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    async def generate_completion_async(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate a completion using OpenAI API asynchronously."""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            if response_format:
                kwargs["response_format"] = response_format
            
            response = await self.async_client.chat.completions.create(**kwargs)
            content = response.choices[0].message.content
            
            logger.debug(f"OpenAI async completion generated successfully")
            return content
            
        except Exception as e:
            logger.error(f"Error generating OpenAI async completion: {e}", exc_info=True)
            raise
