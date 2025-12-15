import os
import pytest
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
N8N_MCP_URL = os.getenv("N8N_MCP_URL")
N8N_MCP_TOKEN = os.getenv("N8N_MCP_TOKEN")

@pytest.mark.skipif(not N8N_MCP_URL or not N8N_MCP_TOKEN, reason="N8N MCP credentials not found")
def test_n8n_connection():
    """Verify connection to the n8n MCP server."""
    headers = {"Authorization": f"Bearer {N8N_MCP_TOKEN}"}
    try:
        # Simple health check or list tools to verify auth
        response = requests.get(f"{N8N_MCP_URL}/tools", headers=headers, timeout=10)
        assert response.status_code == 200, f"Failed to connect to MCP: {response.text}"
    except Exception as e:
        pytest.fail(f"Connection failed: {e}")

@pytest.mark.skipif(not N8N_MCP_URL or not N8N_MCP_TOKEN, reason="N8N MCP credentials not found")
def test_workflow_trigger():
    """
    Example E2E test: Trigger a specific workflow via MCP.
    
    NOTE: This is a template. You should replace 'YOUR_WORKFLOW_ID' 
    with a real ID from your n8n instance to make this test meaningful.
    """
    # TODO: Replace with a real workflow ID from your Gravilo project
    workflow_id = "test-workflow-id" 
    
    # If we don't have a real ID yet, we skip this part but keep the structure
    if workflow_id == "test-workflow-id":
        pytest.skip("Workflow ID not configured in test_n8n_e2e.py")

    headers = {"Authorization": f"Bearer {N8N_MCP_TOKEN}"}
    payload = {
        "name": "n8n_run_workflow",
        "arguments": {
            "workflowId": workflow_id,
            "data": {"test": "true"}
        }
    }
    
    response = requests.post(f"{N8N_MCP_URL}/tools/call", headers=headers, json=payload, timeout=30)
    assert response.status_code == 200
    result = response.json()
    assert "content" in result
