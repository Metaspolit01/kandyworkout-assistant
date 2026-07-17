from notion_client import Client as NotionClient
from typing import Optional, Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import httpx

from config.settings import settings
from config.logger import logger


class NotionClientWrapper:
    """Notion API client with retry logic."""
    
    def __init__(self) -> None:
        self.client = NotionClient(auth=settings.NOTION_TOKEN)
        self.database_id = settings.NOTION_DATABASE_ID
        logger.info("Notion client initialized")
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def create_page(
        self,
        title: str,
        properties: Optional[Dict[str, Any]] = None,
        content: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Create a new page in Notion."""
        try:
            page_properties = properties or {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                }
            }
            
            page_data = {
                "parent": {"database_id": self.database_id},
                "properties": page_properties
            }
            
            if content:
                page_data["children"] = content
            
            response = self.client.pages.create(**page_data)
            logger.info(f"Created Notion page: {title}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating Notion page: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def query_database(
        self,
        filters: Optional[Dict[str, Any]] = None,
        sorts: Optional[List[Dict[str, Any]]] = None
    ) -> List[Dict[str, Any]]:
        """Query the Notion database."""
        try:
            query_params = {"database_id": self.database_id}
            
            if filters:
                query_params["filter"] = filters
            
            if sorts:
                query_params["sorts"] = sorts
            
            response = self.client.databases.query(**query_params)
            results = response.get("results", [])
            logger.debug(f"Queried Notion database, found {len(results)} pages")
            return results
            
        except Exception as e:
            logger.error(f"Error querying Notion database: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def get_page(self, page_id: str) -> Dict[str, Any]:
        """Get a specific page by ID."""
        try:
            response = self.client.pages.retrieve(page_id=page_id)
            logger.debug(f"Retrieved Notion page: {page_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error getting Notion page: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def update_page(
        self,
        page_id: str,
        properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a page's properties."""
        try:
            response = self.client.pages.update(page_id=page_id, properties=properties)
            logger.debug(f"Updated Notion page: {page_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating Notion page: {e}", exc_info=True)
            raise
    
    @retry(
        stop=stop_after_attempt(settings.MAX_RETRIES),
        wait=wait_exponential(multiplier=settings.RETRY_DELAY_SECONDS, min=1, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError))
    )
    def append_block_children(
        self,
        block_id: str,
        children: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Append blocks to a page."""
        try:
            response = self.client.blocks.children.append(
                block_id=block_id,
                children=children
            )
            logger.debug(f"Appended {len(children)} blocks to {block_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error appending blocks to Notion page: {e}", exc_info=True)
            raise
    
    def create_workout_page(
        self,
        title: str,
        workout_data: Dict[str, Any],
        date: str
    ) -> Dict[str, Any]:
        """Create a formatted workout page in Notion."""
        try:
            properties = {
                "title": {
                    "title": [{"text": {"content": title}}]
                },
                "Date": {
                    "date": {"start": date}
                },
                "Status": {
                    "select": {"name": "Not Started"}
                }
            }
            
            # Build content blocks
            children = [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "💪 Greeting"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": workout_data.get("greeting", "")}}]
                    }
                }
            ]
            
            # Add warm-up section
            if "warmup" in workout_data:
                children.extend(self._create_exercise_blocks("🔥 Warm-up", workout_data["warmup"]))
            
            # Add main workout section
            if "main_workout" in workout_data:
                children.extend(self._create_exercise_blocks("🏋️ Main Workout", workout_data["main_workout"]))
            
            # Add cooldown section
            if "cooldown" in workout_data:
                children.extend(self._create_exercise_blocks("🧘 Cooldown", workout_data["cooldown"]))
            
            # Add daily habits
            if "daily_habits" in workout_data and workout_data["daily_habits"]:
                children.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "📋 Daily Habits"}}]
                    }
                })
                for habit in workout_data["daily_habits"]:
                    children.append({
                        "object": "block",
                        "type": "to_do",
                        "to_do": {
                            "rich_text": [{"type": "text", "text": {"content": habit}}],
                            "checked": False
                        }
                    })
            
            # Add feedback section
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📝 Workout Feedback"}}]
                }
            })
            children.append({
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": "Fill this out after your workout!"}}],
                    "icon": {"emoji": "💡"}
                }
            })
            
            return self.create_page(title, properties, children)
            
        except Exception as e:
            logger.error(f"Error creating workout page: {e}", exc_info=True)
            raise
    
    def _create_exercise_blocks(self, title: str, section: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create Notion blocks for an exercise section."""
        blocks = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": title}}]
                }
            }
        ]
        
        for exercise in section.get("exercises", []):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": exercise.get("name", "")}}]
                }
            })
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Sets: {exercise.get('sets', '')}"}}]
                }
            })
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Reps: {exercise.get('reps', '')}"}}]
                }
            })
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Rest: {exercise.get('rest_seconds', '')}s"}}]
                }
            })
            
            if exercise.get("technique_tips"):
                blocks.append({
                    "object": "block",
                    "type": "toggle",
                    "toggle": {
                        "rich_text": [{"type": "text", "text": {"content": "Technique Tips"}}],
                        "children": [
                            {
                                "object": "block",
                                "type": "bulleted_list_item",
                                "bulleted_list_item": {
                                    "rich_text": [{"type": "text", "text": {"content": tip}}]
                                }
                            }
                            for tip in exercise["technique_tips"]
                        ]
                    }
                })
            
            # Add checkbox for completion
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": "Completed"}}],
                    "checked": False
                }
            })
        
        return blocks
