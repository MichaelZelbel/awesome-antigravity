import pytest
import discord
import os
import sys
from unittest.mock import MagicMock, patch, AsyncMock

# Add the parent directory to sys.path to import bridge
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock client.run to prevent the bot from starting during import
with patch('discord.Client.run'):
    import bridge

@pytest.fixture
def mock_client():
    # Patch the client object in the bridge module
    with patch('bridge.client') as mock:
        mock.user = MagicMock()
        yield mock

@pytest.fixture
def mock_message():
    message = AsyncMock(spec=discord.Message)
    message.author.bot = False
    message.content = "Hello ZeroG"
    message.channel = AsyncMock(spec=discord.TextChannel) # Use AsyncMock for channel
    message.channel.id = 123456789
    message.channel.name = "general"
    message.guild.id = 987654321
    message.author.name = "TestUser"
    message.author.id = 111222
    message.reference = None
    return message

@pytest.mark.asyncio
async def test_on_ready(capsys):
    """Test the on_ready event."""
    # Mock environment variable
    with patch.dict(os.environ, {"N8N_WEBHOOK_URL": "http://test-url"}):
        bridge.N8N_WEBHOOK_URL = "http://test-url" # Update global var
        await bridge.on_ready()
        captured = capsys.readouterr()
        assert "Logged in as" in captured.out

@pytest.mark.asyncio
async def test_on_message_ignore_bot(mock_message):
    """Test that messages from bots are ignored."""
    mock_message.author.bot = True
    
    with patch('requests.post') as mock_post:
        await bridge.on_message(mock_message)
        mock_post.assert_not_called()

@pytest.mark.asyncio
async def test_on_message_trigger_mention(mock_client, mock_message):
    """Test that the bot responds when mentioned."""
    # Setup
    # We need to ensure the heuristic returns True
    # The bridge code calls client.user.mentioned_in(message)
    # Our mock_client is the 'bridge.client' object.
    # So bridge.client.user.mentioned_in.return_value = True
    
    mock_client.user.mentioned_in.return_value = True
    bridge.N8N_WEBHOOK_URL = "http://test-url"
    
    # Mock N8N response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Hello from N8N"
    
    with patch('requests.post', return_value=mock_response) as mock_post:
        await bridge.on_message(mock_message)
        
        # Verify N8N was called
        mock_post.assert_called_once()
        
        # Verify reply was sent
        mock_message.channel.send.assert_called_with("Hello from N8N")
