from supabase import create_client, Client
from typing import Optional, Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

from config.settings import settings
from config.logger import logger


class SupabaseClient:
    """Supabase client with retry logic."""
    
    def __init__(self) -> None:
        key = settings.SUPABASE_SERVICE_KEY or settings.SUPABASE_KEY
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            key
        )
        logger.info("Supabase client initialized")
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def fetch(
        self,
        table: str,
        filters: Optional[Dict[str, Any]] = None,
        order: Optional[str] = None,
        ascending: bool = True,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Fetch data from Supabase table."""
        try:
            query = self.client.table(table).select("*")
            
            if filters:
                for key, value in filters.items():
                    if isinstance(value, (list, tuple)):
                        query = query.in_(key, value)
                    else:
                        query = query.eq(key, value)
            
            if order:
                query = query.order(order, desc=not ascending)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            logger.debug(f"Fetched {len(response.data)} records from {table}")
            return response.data
            
        except Exception as e:
            logger.error(f"Error fetching from {table}: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def insert(self, table: str, data: Dict[str, Any] | List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Insert data into Supabase table."""
        try:
            response = self.client.table(table).insert(data).execute()
            logger.debug(f"Inserted {len(response.data)} records into {table}")
            return response.data
            
        except Exception as e:
            logger.error(f"Error inserting into {table}: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def update(
        self,
        table: str,
        data: Dict[str, Any],
        filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Update data in Supabase table."""
        try:
            query = self.client.table(table).update(data)
            
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.execute()
            logger.debug(f"Updated {len(response.data)} records in {table}")
            return response.data
            
        except Exception as e:
            logger.error(f"Error updating {table}: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def delete(self, table: str, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Delete data from Supabase table."""
        try:
            query = self.client.table(table).delete()
            
            for key, value in filters.items():
                query = query.eq(key, value)
            
            response = query.execute()
            logger.debug(f"Deleted {len(response.data)} records from {table}")
            return response.data
            
        except Exception as e:
            logger.error(f"Error deleting from {table}: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def execute_raw_sql(self, sql: str) -> List[Dict[str, Any]]:
        """Execute raw SQL query."""
        try:
            response = self.client.rpc("execute_sql", {"sql": sql}).execute()
            logger.debug("Raw SQL executed successfully")
            return response.data
            
        except Exception as e:
            logger.error(f"Error executing raw SQL: {e}", exc_info=True)
            raise
