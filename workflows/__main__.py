from datetime import datetime
import sys

from clients.openai_client import OpenAIClient
from clients.supabase_client import SupabaseClient
from clients.notion_client import NotionClientWrapper
from workflows.morning_workflow import MorningWorkflow
from workflows.night_workflow import NightWorkflow
from config.logger import logger


def main():
    """Main entry point for workflow execution."""
    if len(sys.argv) < 2:
        logger.error("Usage: python -m workflows <morning|night>")
        sys.exit(1)
    
    workflow_type = sys.argv[1].lower()
    
    # Initialize clients
    openai_client = OpenAIClient()
    supabase_client = SupabaseClient()
    notion_client = NotionClientWrapper()
    
    if workflow_type == "morning":
        workflow = MorningWorkflow(openai_client, supabase_client, notion_client)
        result = workflow.execute()
    elif workflow_type == "night":
        workflow = NightWorkflow(openai_client, supabase_client, notion_client)
        result = workflow.execute()
    else:
        logger.error(f"Unknown workflow type: {workflow_type}")
        sys.exit(1)
    
    if result.get("success"):
        logger.info(f"Workflow completed successfully: {result}")
        sys.exit(0)
    else:
        logger.error(f"Workflow failed: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
