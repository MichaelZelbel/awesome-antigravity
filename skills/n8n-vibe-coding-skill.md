---
name: n8n-workflow-vibe-coding
description: Specialized guide for vibe coding n8n workflows with AI assistance. Ensures workflows import correctly, use proper node layouts, follow best practices for constants/variables, error handling, and testing. Includes n8n-specific patterns for modular design, sub-workflows, and AI agent integrations.
license: MIT
---

# N8N Workflow Vibe Coding

This skill provides specialized guidance for vibe coding n8n workflows—creating automation workflows through natural language descriptions while ensuring proper structure, importability, and maintainability.

## What is N8N Workflow Vibe Coding

N8N workflow vibe coding combines AI-assisted development with n8n's node-based automation platform. It enables rapid creation of complex workflows through conversational prompts while maintaining n8n's structural requirements and best practices.

**Core principles:**
- Generate valid, importable workflow JSON structures
- Maintain human-readable node layouts with proper positioning
- Use modular design with Config nodes for input decoupling
- ALWAYS use purpose-built nodes when available, only use HTTP Request/Code as last resort
- Follow n8n data structure patterns
- Implement proper error handling and testing

**When to use n8n vibe coding:**
- Rapid workflow prototyping and POCs
- Building AI agents and LangChain integrations
- Complex multi-step automations
- Integration between multiple services
- Data transformation pipelines
- Webhook-based automations

**When NOT to use n8n vibe coding:**
- Extremely simple single-node operations
- Workflows requiring custom node development
- Real-time streaming data processing (use dedicated tools)
- Workflows with >100 nodes (break into sub-workflows first)

## CRITICAL: Use Purpose-Built Nodes

**The Golden Rule:** ALWAYS use n8n's purpose-built nodes for services before resorting to HTTP Request or Code nodes.

### Why This Matters

Purpose-built nodes:
- Handle authentication automatically
- Provide proper error handling and retries
- Include rate limiting
- Have validated parameters
- Are maintained by n8n team
- Import cleanly without breaking

HTTP Request nodes:
- Require manual credential management
- Need custom error handling
- May have incorrect URLs or parameters
- Are harder to maintain
- Should ONLY be used when no dedicated node exists

### Common Mistakes to Avoid

**BAD - Using HTTP Request for Perplexity:**
```json
{
  "name": "Call Perplexity",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://api.perplexity.ai/chat/completions",
    "method": "POST"
  }
}
```

**GOOD - Using Perplexity Node:**
```json
{
  "name": "Call Perplexity",
  "type": "n8n-nodes-base.perplexity",
  "parameters": {
    "model": "sonar",
    "messages": {
      "message": [
        {
          "content": "={{ $json.query }}"
        }
      ]
    }
  },
  "credentials": {
    "perplexityApi": {
      "id": "perplexity_api",
      "name": "Perplexity API"
    }
  }
}
```

**BAD - Using HTTP Request to call another workflow:**
```json
{
  "name": "Trigger Processor",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "http://localhost:5678/webhook/processor",
    "method": "POST"
  }
}
```

**GOOD - Using Execute Workflow Node:**
```json
{
  "name": "Trigger Processor",
  "type": "n8n-nodes-base.executeWorkflow",
  "parameters": {
    "source": "database",
    "workflowId": {
      "__rl": true,
      "mode": "list",
      "value": "",
      "cachedResultName": "Processor Workflow"
    },
    "options": {
      "waitForCompletion": false
    }
  }
}
```

### Node Selection Decision Tree

1. **Check if dedicated node exists** for the service (Perplexity, OpenAI, PostgreSQL, etc.)
   - YES → Use the dedicated node
   - NO → Continue to step 2

2. **Check if it's a common database operation**
   - YES → Use PostgreSQL/MySQL/MongoDB node, NOT HTTP Request to REST API
   - NO → Continue to step 3

3. **Check if calling another n8n workflow**
   - YES → Use Execute Workflow node
   - NO → Continue to step 4

4. **Check if it's a standard REST API with no n8n node**
   - YES → Now you can use HTTP Request node
   - NO → Consider if this should be a custom node or different approach

## Config Node Pattern (CRITICAL)

**ALWAYS start workflows with a Config node immediately after the trigger.** This is one of the most important patterns for maintainable workflows.

### Why Config Nodes Matter

1. **Decouples input from logic** - Changes to trigger structure don't break the entire workflow
2. **Enables easy debugging** - Add Manual Trigger before Config for testing with sample data
3. **Single source of truth** - All constants and inputs defined in one place
4. **Improves maintainability** - Clear what data the workflow expects
5. **Makes testing faster** - No need to simulate webhooks or call parent workflows

### Config Node Structure

```json
{
  "name": "Config",
  "type": "n8n-nodes-base.set",
  "position": [450, 300],
  "parameters": {
    "mode": "manual",
    "duplicateItem": false,
    "assignments": {
      "assignments": [
        {
          "id": "uuid-1",
          "name": "API_TIMEOUT",
          "type": "number",
          "value": 30000
        },
        {
          "id": "uuid-2",
          "name": "BATCH_SIZE",
          "type": "number",
          "value": 20
        },
        {
          "id": "uuid-3",
          "name": "brandId",
          "type": "string",
          "value": "={{ $('Webhook Trigger').first().json.body.brandId }}"
        },
        {
          "id": "uuid-4",
          "name": "brandName",
          "type": "string",
          "value": "={{ $('Webhook Trigger').first().json.body.brandName }}"
        },
        {
          "id": "uuid-5",
          "name": "topic",
          "type": "string",
          "value": "={{ $('Webhook Trigger').first().json.body.topic }}"
        }
      ]
    }
  }
}
```

### Using Config Node Throughout Workflow

**BAD - Direct trigger reference:**
```json
{
  "jsCode": "const brandId = $('Webhook Trigger').first().json.body.brandId;"
}
```

**GOOD - Config node reference with .first():**
```json
{
  "jsCode": "const brandId = $('Config').first().json.brandId;"
}
```

**Why .first() for Config:**
- Config nodes always produce exactly one item
- `.first()` works reliably inside loops and any execution context
- `.item` can break when used inside Split in Batches or other loops

### Config Node for Different Trigger Types

**Webhook Trigger:**
```json
{
  "name": "Config",
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "name": "runId",
          "value": "={{ $('Webhook Trigger').first().json.body.runId }}"
        },
        {
          "name": "userId",
          "value": "={{ $('Webhook Trigger').first().json.body.userId }}"
        }
      ]
    }
  }
}
```

**Execute Workflow Trigger:**
```json
{
  "name": "Config",
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "name": "runId",
          "value": "={{ $('When Called By Another Workflow').first().json.runId }}"
        },
        {
          "name": "brandName",
          "value": "={{ $('When Called By Another Workflow').first().json.brandName }}"
        }
      ]
    }
  }
}
```

**Note:** While `.item` works in Config node value extraction (since it's the immediate next node), using `.first()` consistently throughout your workflow improves readability and prevents confusion.

### Debug Pattern with Manual Trigger

```json
{
  "nodes": [
    {
      "name": "Manual Trigger for Testing",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 100]
    },
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "name": "Config",
      "type": "n8n-nodes-base.set",
      "position": [450, 200],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "name": "brandId",
              "value": "test-brand-123"
            },
            {
              "name": "topic",
              "value": "AI automation"
            }
          ]
        }
      }
    }
  ],
  "connections": {
    "Manual Trigger for Testing": {
      "main": [[{"node": "Config", "type": "main", "index": 0}]]
    },
    "Webhook Trigger": {
      "main": [[{"node": "Config", "type": "main", "index": 0}]]
    }
  }
}
```

## N8N Workflow Structure Fundamentals

### Core JSON Structure

Every n8n workflow must follow this structure for proper import:

```json
{
  "name": "Workflow Name",
  "nodes": [
    {
      "parameters": {},
      "id": "unique-node-id",
      "name": "Node Name",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300]
    }
  ],
  "connections": {
    "Node Name": {
      "main": [
        [
          {
            "node": "Target Node",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  },
  "versionId": "unique-version-id",
  "meta": {
    "templateCredsSetupCompleted": true
  }
}
```

### Node Positioning Rules

**Critical for readable workflows:**

```javascript
// Standard spacing between nodes
const HORIZONTAL_SPACING = 400;
const VERTICAL_SPACING = 200;

// Starting position
const START_X = 250;
const START_Y = 300;

// Position calculation for linear flow
position: [START_X + (nodeIndex * HORIZONTAL_SPACING), START_Y]

// Position for parallel branches
branchPosition: [START_X + (nodeIndex * HORIZONTAL_SPACING), START_Y + (branchIndex * VERTICAL_SPACING)]
```

**Layout patterns:**
- **Linear flow:** Nodes at Y=300, X incrementing by 400
- **Parallel branches:** Different Y levels (300, 500, 700)
- **Merge points:** Center Y position between branches
- **Sub-workflow groups:** Contained in visual boxes (Y offsets)

### Data Structure Requirements

N8N expects data in this format:

```javascript
// Each item must be wrapped in json key
[
  {
    "json": {
      "field1": "value1",
      "field2": "value2"
    }
  },
  {
    "json": {
      "field1": "value3",
      "field2": "value4"
    }
  }
]
```

## Database Operations

**CRITICAL:** For database operations, ALWAYS use the proper database node (PostgreSQL, MySQL, MongoDB, etc.) instead of HTTP Request to a REST API.

### Why Database Nodes Matter

**BAD - Using HTTP Request to Supabase REST API:**
```json
{
  "name": "Save to Database",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "url": "https://project.supabase.co/rest/v1/table",
    "method": "POST",
    "authentication": "genericCredentialType"
  }
}
```

**GOOD - Using PostgreSQL Node with Supabase:**
```json
{
  "name": "Save to Database",
  "type": "n8n-nodes-base.postgres",
  "typeVersion": 2.5,
  "parameters": {
    "operation": "insert",
    "schema": {
          "__rl": true,
          "value": "public",
          "mode": "list"
    },
    "table": {
      "__rl": true,
      "value": "analysis_runs",
      "mode": "list"
    },
    "columns": {
      "mappingMode": "defineBelow",
      "value": {
        "run_id": "={{ $('Config').first().json.runId }}",
        "brand_name": "={{ $('Config').first().json.brandName }}",
        "status": "pending"
      }
    }
  },
  "credentials": {
    "postgres": {
      "id": "supabase_postgres",
      "name": "Supabase PostgreSQL"
    }
  }
}
```

### Database Credential Setup

For Supabase via PostgreSQL node:
- Host: `db.xxx.supabase.co` (from Supabase database settings)
- Port: 5432
- Database: `postgres`
- User: `postgres`
- Password: Database password (not API key)

**NOT** the Supabase API URL or API keys - those are for REST API, not direct database connections.

## Calling Other Workflows
- Better error messages when parameters are missing

### Execute Workflow Node (Calling Workflow)

**Use Execute Workflow node to call other n8n workflows:**

After selecting the sub-workflow, n8n automatically shows the defined input fields. Fill them in:

```json
{
  "name": "Call Processor Workflow",
  "type": "n8n-nodes-base.executeWorkflow",
  "typeVersion": 1.2,
  "parameters": {
    "source": "database",
    "workflowId": {
      "__rl": true,
      "mode": "list",
      "value": "workflow-id",
      "cachedResultName": "Processor Workflow"
    },
    "inputData": {
      "run_id": "={{ $json.run_id }}",
      "brand_id": "={{ $json.brand_id }}",
      "brand_name": "={{ $json.brand_name }}",
      "topic": "={{ $json.topic }}",
      "ai_engine": "perplexity"
    },
    "options": {
      "waitForCompletion": false
    }
  }
}
```

### Data Flow Between Workflows

**In the sub-workflow - access via trigger using .first():**

```javascript
// Access the parameters passed from parent workflow
const data = $('When Called By Another Workflow').first().json;
const runId = data.run_id;
const brandId = data.brand_id;
const brandName = data.brand_name;
const topic = data.topic;
const aiEngine = data.ai_engine;
```

**Best Practice - Use Config Node Pattern:**

```json
{
  "name": "Config",
  "type": "n8n-nodes-base.set",
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "name": "runId",
          "value": "={{ $('When Called By Another Workflow').first().json.run_id || 'test_run' }}"
        },
        {
          "name": "brandId",
          "value": "={{ $('When Called By Another Workflow').first().json.brand_id || 'test-brand' }}"
        },
        {
          "name": "brandName",
          "value": "={{ $('When Called By Another Workflow').first().json.brand_name || 'Test Brand' }}"
        },
        {
          "name": "topic",
          "value": "={{ $('When Called By Another Workflow').first().json.topic || 'default topic' }}"
        },
        {
          "name": "aiEngine",
          "value": "={{ $('When Called By Another Workflow').first().json.ai_engine || 'perplexity' }}"
        }
      ]
    }
  }
}
```

**Why this pattern is superior:**
- Default values (`|| 'test_run'`) allow testing with Manual Trigger without errors
- Config node centralizes all input extraction in one place
- Rest of workflow references Config using `.first()`, not the trigger directly
- Clear contract between parent and child workflows

## Data Referencing Best Practices

### Referencing Previous Node Data

**ALWAYS use explicit node references:**

```javascript
// GOOD - Explicit reference with .first()
const brandName = $('Config').first().json.brandName;
const runId = $('Config').first().json.runId;

// BAD - Implicit reference (fragile)
const brandName = $json.brandName;
```

### .first() vs .item - CRITICAL DISTINCTION

**The Golden Rule: Use `.first()` for Config nodes and single-item nodes. Use `.item` only for current loop context.**

#### Why .first() is Better for Config Nodes:

1. **Explicit and unambiguous** - Always gets the first item, regardless of execution context
2. **Works inside loops** - When you're in a Split in Batches loop and reference Config, `.first()` correctly gets the single Config item
3. **Safer for single-item nodes** - Config nodes produce exactly one item, so `.first()` makes that explicit
4. **Less context-dependent** - `.item` depends on where you are in the execution flow

#### The Problem with .item:

```javascript
// Inside a Split in Batches loop
const batchItem = $('Split Batches').item.json;     // ✅ Current loop item
const brandId = $('Config').item.json.brandId;       // ❌ Wrong! Tries to match batch context
```

When you use `.item` on the Config node while inside a loop, n8n tries to get the Config item at the same index as the current loop iteration. Since Config only has one item (index 0), this breaks on iteration 2+.

#### Using .first() Correctly:

```javascript
// Inside a Split in Batches loop
const batchItem = $('Split Batches').item.json;          // ✅ Current loop item
const brandId = $('Config').first().json.brandId;        // ✅ Always gets Config's single item
const timeout = $('Config').first().json.API_TIMEOUT;    // ✅ Works in any context
```

#### When to Use Each:

| Scenario | Use | Example |
|----------|-----|---------|
| Config node (single item) | `.first()` | `$('Config').first().json.brandId` |
| Any single-item node | `.first()` | `$('Database Query').first().json.result` |
| Current loop item | `.item` | `$('Split Batches').item.json` |
| Current webhook in webhook node | `.item` | `$('Webhook Trigger').item.json.body` |
| Inside loop, referencing loop node | `.item` | `$('Process Item').item.json.status` |

### Common Data Access Patterns

**Access single item from Config or similar nodes (PREFERRED):**
```javascript
$('Config').first().json.fieldName
$('Database Query').first().json.result
$('API Call').first().json.response
```

**Access current item in loop context:**
```javascript
$('Split Batches').item.json.fieldName  // Current iteration item
```

**Access all items from node:**
```javascript
$('Node Name').all()  // Returns array of all items
```

**Check if node has data:**
```javascript
if ($('Node Name').first() !== undefined) {
  // Node has data
}
```

### Webhook Data Access

**Webhook body data:**
```javascript
// Immediate next node after webhook
$json.body.fieldName

// Later nodes - use .first() for webhook trigger
$('Webhook Trigger').first().json.body.fieldName
```

**Better - Use Config node with .first():**
```javascript
// In Config node (extracting from webhook)
{
  "name": "userId",
  "value": "={{ $('Webhook Trigger').first().json.body.userId }}"
}

// Everywhere else - reference Config
$('Config').first().json.userId
```

**Best Practice in Loops:**
```javascript
// Inside Split in Batches loop processing queries
const currentQuery = $('Split Batches').item.json.query;     // Current loop item
const brandId = $('Config').first().json.brandId;            // Config constant
const timeout = $('Config').first().json.API_TIMEOUT;        // Config constant

// Make API call with current query + config values
return {
  json: {
    query: currentQuery,
    brandId: brandId,
    timeout: timeout
  }
};
```

## Configuration Management

### Config Node Pattern (Already Covered Above)

Always start workflows with Config node containing:
1. Constants (API timeouts, batch sizes, etc.)
2. Input values extracted from trigger
3. Any computed values needed throughout workflow

### Environment Variables

For credentials and secrets, use n8n's credential system, NOT environment variables in code:

**BAD:**
```javascript
const apiKey = process.env.PERPLEXITY_API_KEY;
```

**GOOD:**
Use credential configuration in node:
```json
{
  "credentials": {
    "perplexityApi": {
      "id": "perplexity_api",
      "name": "Perplexity API"
    }
  }
}
```

## Best Practices for N8N Workflow Creation

### 1. Node Naming Conventions

Use descriptive, action-oriented names:
- **GOOD:** "Update Status Processing", "Generate Queries", "Calculate Scores"
- **BAD:** "Node1", "Process", "Do Stuff"

**NEVER use emojis in node names** - they cause encoding issues and make referencing difficult:
- **BAD:** "🔧 Configuration", "📊 Calculate"
- **GOOD:** "Configuration", "Calculate Scores"

### 2. Workflow Structure

Standard workflow pattern:
```
1. Trigger (webhook, schedule, manual, executeWorkflowTrigger)
2. Config Node (extract inputs, define constants)
3. Processing Logic
4. Database Operations
5. Response/Completion
```

### 3. Error Handling Patterns

**Implement Try-Catch patterns:**

```json
{
  "name": "Try",
  "type": "n8n-nodes-base.noOp",
  "position": [450, 200],
  "continueOnFail": false
},
{
  "name": "Error Handler",
  "type": "n8n-nodes-base.code",
  "position": [450, 400],
  "parameters": {
    "mode": "runOnceForEachItem",
    "jsCode": "const error = $input.item.error;\nconsole.error('Workflow error:', error);\nreturn {json: {error: error.message, timestamp: new Date().toISOString()}};"
  }
}
```

### 4. Retry Configuration

For external API calls, implement retry logic:

```json
{
  "parameters": {
    "retry": {
      "maxRetries": 3,
      "retryInterval": 2000,
      "retryOnStatusCodes": "429,500,502,503,504"
    }
  }
}
```

### 5. Rate Limiting

Use Wait node for rate limiting:

```json
{
  "name": "Rate Limit Delay",
  "type": "n8n-nodes-base.wait",
  "typeVersion": 1.1,
  "parameters": {
    "amount": 2000,
    "unit": "milliseconds"
  },
  "webhookId": "rate-limit-delay"
}
```

## Advanced Error Handling & Recovery Strategies

### Centralized Error Workflows

**The Professional Pattern:** Create a single "Mission Control" error workflow that handles failures from all your workflows.

#### Setting Up Centralized Error Handler

**Step 1: Create Error Handler Workflow**

```json
{
  "name": "Error Handler - Mission Control",
  "nodes": [
    {
      "name": "Error Trigger",
      "type": "n8n-nodes-base.errorTrigger",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {}
    },
    {
      "name": "Extract Error Details",
      "type": "n8n-nodes-base.set",
      "position": [450, 300],
      "parameters": {
        "mode": "manual",
        "assignments": {
          "assignments": [
            {
              "name": "workflowName",
              "value": "={{ $json.workflow.name }}"
            },
            {
              "name": "failedNode",
              "value": "={{ $json.execution.lastNodeExecuted }}"
            },
            {
              "name": "errorMessage",
              "value": "={{ $json.execution.error.message }}"
            },
            {
              "name": "executionId",
              "value": "={{ $json.execution.id }}"
            },
            {
              "name": "executionUrl",
              "value": "={{ $json.execution.url }}"
            },
            {
              "name": "timestamp",
              "value": "={{ $now.toISO() }}"
            }
          ]
        }
      }
    },
    {
      "name": "Classify Error Type",
      "type": "n8n-nodes-base.code",
      "position": [650, 300],
      "parameters": {
        "jsCode": "const errorMsg = $('Extract Error Details').item.json.errorMessage.toLowerCase();\n\n// Classify error as retryable or not\nconst retryablePatterns = [\n  'timeout',\n  'econnrefused',\n  'enotfound',\n  '503',\n  '504',\n  '429',\n  'rate limit'\n];\n\nconst isRetryable = retryablePatterns.some(pattern => \n  errorMsg.includes(pattern)\n);\n\nreturn {\n  json: {\n    ...($('Extract Error Details').item.json),\n    errorType: isRetryable ? 'retryable' : 'non-retryable',\n    isRetryable: isRetryable\n  }\n};"
      }
    },
    {
      "name": "Should Retry?",
      "type": "n8n-nodes-base.if",
      "position": [850, 300],
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $json.isRetryable }}",
              "value2": true
            }
          ]
        }
      }
    },
    {
      "name": "Log to Database",
      "type": "n8n-nodes-base.postgres",
      "position": [1050, 200],
      "parameters": {
        "operation": "insert",
        "table": {
          "__rl": true,
          "value": "workflow_errors",
          "mode": "list"
        },
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "workflow_name": "={{ $json.workflowName }}",
            "failed_node": "={{ $json.failedNode }}",
            "error_message": "={{ $json.errorMessage }}",
            "error_type": "={{ $json.errorType }}",
            "execution_id": "={{ $json.executionId }}",
            "execution_url": "={{ $json.executionUrl }}",
            "timestamp": "={{ $json.timestamp }}"
          }
        }
      }
    },
    {
      "name": "Alert Team - Slack",
      "type": "n8n-nodes-base.slack",
      "position": [1050, 400],
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "#alerts-n8n-errors",
        "text": "🚨 *Workflow Error*\n\n*Workflow:* {{ $json.workflowName }}\n*Failed Node:* {{ $json.failedNode }}\n*Error:* {{ $json.errorMessage }}\n*Type:* {{ $json.errorType }}\n*Execution:* {{ $json.executionUrl }}"
      }
    }
  ],
  "connections": {
    "Error Trigger": {
      "main": [[{"node": "Extract Error Details", "type": "main", "index": 0}]]
    },
    "Extract Error Details": {
      "main": [[{"node": "Classify Error Type", "type": "main", "index": 0}]]
    },
    "Classify Error Type": {
      "main": [[{"node": "Should Retry?", "type": "main", "index": 0}]]
    },
    "Should Retry?": {
      "main": [
        [
          {"node": "Log to Database", "type": "main", "index": 0},
          {"node": "Alert Team - Slack", "type": "main", "index": 0}
        ],
        [
          {"node": "Log to Database", "type": "main", "index": 0},
          {"node": "Alert Team - Slack", "type": "main", "index": 0}
        ]
      ]
    }
  }
}
```

**Step 2: Configure Workflows to Use Error Handler**

In each production workflow:
1. Go to Workflow Settings (gear icon)
2. Find "Error Workflow" dropdown
3. Select "Error Handler - Mission Control"

Now all errors automatically route to your centralized handler!

### Error Classification Strategy

**Retryable Errors (Transient):**
- Network timeouts (`ETIMEDOUT`, `ECONNREFUSED`)
- DNS failures (`ENOTFOUND`)
- 5xx server errors (503, 504)
- Rate limiting (429)
- Database connection issues

**Non-Retryable Errors (Permanent):**
- 4xx client errors (400, 401, 403, 404)
- 422 Unprocessable Entity (validation errors)
- Invalid credentials
- Missing required parameters
- Business logic failures

### Exponential Backoff with Jitter

**Pattern for Custom Retry Logic:**

```json
{
  "name": "Retry Logic with Exponential Backoff",
  "type": "n8n-nodes-base.code",
  "parameters": {
    "jsCode": "// Exponential backoff configuration\nconst MAX_RETRIES = 5;\nconst BASE_DELAY = 1000; // 1 second\nconst MAX_DELAY = 32000; // 32 seconds\nconst JITTER_PERCENT = 0.2; // ±20%\n\nconst retryCount = $('Config').first().json.retryCount || 0;\n\nif (retryCount >= MAX_RETRIES) {\n  throw new Error('Max retries exceeded');\n}\n\n// Calculate delay: min(BASE_DELAY * 2^retryCount, MAX_DELAY)\nlet delay = Math.min(\n  BASE_DELAY * Math.pow(2, retryCount),\n  MAX_DELAY\n);\n\n// Add jitter: delay * (1 ± JITTER_PERCENT)\nconst jitter = delay * JITTER_PERCENT * (Math.random() * 2 - 1);\ndelay = Math.round(delay + jitter);\n\nreturn {\n  json: {\n    retryCount: retryCount + 1,\n    delayMs: delay,\n    nextRetryAt: new Date(Date.now() + delay).toISOString()\n  }\n};"
  }
}
```

**Delays by retry attempt:**
- Retry 1: ~1 second (±20%)
- Retry 2: ~2 seconds (±20%)
- Retry 3: ~4 seconds (±20%)
- Retry 4: ~8 seconds (±20%)
- Retry 5: ~16 seconds (±20%)

### Failover Patterns

#### Primary-Fallback Pattern

Use when you have alternate methods to accomplish the same task:

```json
{
  "nodes": [
    {
      "name": "Try Primary API",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300],
      "parameters": {
        "url": "https://primary-api.com/endpoint",
        "options": {
          "timeout": 10000
        }
      },
      "continueOnFail": true,
      "onError": "continueErrorOutput"
    },
    {
      "name": "Check Primary Success",
      "type": "n8n-nodes-base.if",
      "position": [650, 300],
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.error }}",
              "operation": "isEmpty"
            }
          ]
        }
      }
    },
    {
      "name": "Fallback API",
      "type": "n8n-nodes-base.httpRequest",
      "position": [650, 500],
      "parameters": {
        "url": "https://fallback-api.com/endpoint",
        "options": {
          "timeout": 10000
        }
      }
    },
    {
      "name": "Merge Results",
      "type": "n8n-nodes-base.merge",
      "position": [850, 300],
      "parameters": {
        "mode": "append"
      }
    }
  ],
  "connections": {
    "Try Primary API": {
      "main": [[{"node": "Check Primary Success", "type": "main", "index": 0}]]
    },
    "Check Primary Success": {
      "main": [
        [{"node": "Merge Results", "type": "main", "index": 0}],
        [{"node": "Fallback API", "type": "main", "index": 0}]
      ]
    },
    "Fallback API": {
      "main": [[{"node": "Merge Results", "type": "main", "index": 1}]]
    }
  }
}
```

#### Circuit Breaker Pattern

Temporarily stop calling failing services:

```json
{
  "name": "Check Circuit Breaker",
  "type": "n8n-nodes-base.code",
  "parameters": {
    "jsCode": "// Circuit breaker state stored in external cache (Redis/KV store)\nconst SERVICE_NAME = 'external-api';\nconst FAILURE_THRESHOLD = 5;\nconst TIMEOUT_MS = 60000; // 1 minute\n\n// Fetch circuit breaker state from Redis/cache\nconst state = $('Get Circuit State').item.json;\n\nconst now = Date.now();\nconst isOpen = state.failureCount >= FAILURE_THRESHOLD;\nconst timeoutExpired = (now - state.lastFailureTime) > TIMEOUT_MS;\n\nif (isOpen && !timeoutExpired) {\n  return {\n    json: {\n      circuitOpen: true,\n      message: 'Circuit breaker is OPEN - using fallback',\n      failureCount: state.failureCount,\n      reopensAt: new Date(state.lastFailureTime + TIMEOUT_MS).toISOString()\n    }\n  };\n}\n\nif (isOpen && timeoutExpired) {\n  // Half-open state: try again\n  return {\n    json: {\n      circuitOpen: false,\n      circuitState: 'half-open',\n      message: 'Circuit breaker entering HALF-OPEN - attempting request'\n    }\n  };\n}\n\nreturn {\n  json: {\n    circuitOpen: false,\n    circuitState: 'closed',\n    message: 'Circuit breaker is CLOSED - normal operation'\n  }\n};"
  }
}
```

### Dead-Letter Queue (DLQ) Pattern

For items that permanently fail after all retries:

```json
{
  "name": "Send to Dead Letter Queue",
  "type": "n8n-nodes-base.postgres",
  "position": [1250, 500],
  "parameters": {
    "operation": "insert",
    "table": {
      "__rl": true,
      "value": "dead_letter_queue",
      "mode": "list"
    },
    "columns": {
      "mappingMode": "defineBelow",
      "value": {
        "original_data": "={{ JSON.stringify($json) }}",
        "error_message": "={{ $json.error }}",
        "retry_count": "={{ $json.retryCount }}",
        "workflow_name": "={{ $workflow.name }}",
        "failed_node": "={{ $node.name }}",
        "created_at": "={{ $now.toISO() }}",
        "status": "pending_manual_review"
      }
    }
  }
}
```

### Auto-Retry Engine Workflow

**Pattern for automatically retrying failed workflow executions:**

```json
{
  "name": "Auto-Retry Engine",
  "nodes": [
    {
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "minutes", "minutesInterval": 5}]
        }
      }
    },
    {
      "name": "Get Failed Executions",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:5678/api/v1/executions",
        "method": "GET",
        "qs": {
          "status": "error",
          "limit": "20"
        },
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth"
      }
    },
    {
      "name": "Filter Retryable",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "jsCode": "const executions = $input.all();\nconst retryable = [];\n\nfor (const exec of executions) {\n  const error = exec.json.stoppedAt;\n  const retryCount = exec.json.data?.retryCount || 0;\n  \n  // Only retry if under max attempts and error is retryable\n  if (retryCount < 3 && isRetryableError(error)) {\n    retryable.push(exec);\n  }\n}\n\nfunction isRetryableError(error) {\n  const retryablePatterns = ['timeout', '503', '504', 'ECONNREFUSED'];\n  return retryablePatterns.some(p => error.includes(p));\n}\n\nreturn retryable.map(e => ({json: e.json}));"
      }
    },
    {
      "name": "Retry Execution",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:5678/api/v1/executions/{{ $json.id }}/retry",
        "method": "POST"
      }
    }
  ]
}
```

## Modular Design with Sub-Workflows

### When to Use Sub-Workflows

- Reusable logic across multiple workflows
- Complex operations >10 nodes
- Different execution contexts (error isolation)
- Team collaboration (separate ownership)
- Testing individual components

### Calling Sub-Workflows (Modern Pattern)

**Use Execute Workflow node with defined input parameters:**

```json
{
  "name": "Process User Data",
  "type": "n8n-nodes-base.executeWorkflow",
  "typeVersion": 1.2,
  "parameters": {
    "source": "database",
    "workflowId": {
      "__rl": true,
      "mode": "list",
      "value": "workflow-id",
      "cachedResultName": "User Data Processor"
    },
    "inputData": {
      "user_id": "={{ $json.user_id }}",
      "data_type": "={{ $json.data_type }}",
      "options": "={{ $json.options }}"
    },
    "options": {
      "waitForCompletion": true
    }
  }
}
```

### Sub-Workflow Pattern with Defined Parameters

**CRITICAL: Always define input parameters in the Execute Workflow Trigger:**

```json
{
  "name": "User Data Processor",
  "nodes": [
    {
      "name": "When Called By Another Workflow",
      "type": "n8n-nodes-base.executeWorkflowTrigger",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "triggerMode": "manual",
        "inputDataMode": "define",
        "inputDataFields": {
          "values": [
            {
              "fieldName": "user_id",
              "fieldType": "string",
              "required": true
            },
            {
              "fieldName": "data_type",
              "fieldType": "string",
              "required": true
            },
            {
              "fieldName": "options",
              "fieldType": "object",
              "required": false
            }
          ]
        }
      }
    },
    {
      "name": "Config",
      "type": "n8n-nodes-base.set",
      "position": [450, 300],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "name": "userId",
              "value": "={{ $('When Called By Another Workflow').first().json.user_id || 'test-user' }}"
            },
            {
              "name": "dataType",
              "value": "={{ $('When Called By Another Workflow').first().json.data_type || 'default' }}"
            }
          ]
        }
      }
    },
    {
      "name": "Processing Logic",
      "type": "n8n-nodes-base.code",
      "position": [650, 300]
    }
  ]
}
```

**Benefits:**
- Parameters defined in trigger auto-populate in calling workflow
- Default values in Config enable testing with Manual Trigger
- Clear contract between workflows
- Type validation at design time

## Robust Subworkflow Error Reporting

**CRITICAL:** By default, if a subworkflow throws an error, the parent workflow just stops without detailed error information. To build production-grade workflows, subworkflows must **ALWAYS return structured responses** that communicate both success and failure to the parent.

### The Golden Rule: Always Return, Never Throw

**Subworkflows should complete successfully and return a structured response, even when the business logic fails.**

### Structured Response Contract

Every subworkflow should return this structure:

```json
{
  "success": true/false,
  "data": {
    // The actual result data (when successful)
  },
  "error": {
    "message": "Human-readable error message",
    "code": "ERROR_CODE",
    "node": "Failed Node Name",
    "timestamp": "2025-01-15T10:30:00.000Z",
    "isRetryable": true/false
  },
  "metadata": {
    "executionId": "12345",
    "duration": 1234,
    "workflowName": "Processor Workflow"
  }
}
```

### Complete Subworkflow Pattern

**Subworkflow that properly reports errors:**

```json
{
  "name": "Data Processor - Subworkflow",
  "nodes": [
    {
      "name": "When Called By Another Workflow",
      "type": "n8n-nodes-base.executeWorkflowTrigger",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "triggerMode": "manual",
        "inputDataMode": "define",
        "inputDataFields": {
          "values": [
            {
              "fieldName": "brandId",
              "fieldType": "string",
              "required": true
            },
            {
              "fieldName": "brandName",
              "fieldType": "string",
              "required": true
            }
          ]
        }
      }
    },
    {
      "name": "Config",
      "type": "n8n-nodes-base.set",
      "position": [450, 300],
      "parameters": {
        "mode": "manual",
        "assignments": {
          "assignments": [
            {
              "name": "executionStart",
              "value": "={{ $now.toISO() }}"
            },
            {
              "name": "brandId",
              "value": "={{ $('When Called By Another Workflow').first().json.brandId || 'test-brand-id' }}"
            },
            {
              "name": "brandName",
              "value": "={{ $('When Called By Another Workflow').first().json.brandName || 'Test Brand' }}"
            }
          ]
        }
      }
    },
    {
      "name": "Validate Inputs",
      "type": "n8n-nodes-base.if",
      "position": [650, 300],
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $('Config').first().json.brandId }}",
              "operation": "isNotEmpty"
            },
            {
              "value1": "={{ $('Config').first().json.brandName }}",
              "operation": "isNotEmpty"
            }
          ],
          "combineOperation": "all"
        }
      }
    },
    {
      "name": "Set Input Validation Error",
      "type": "n8n-nodes-base.set",
      "position": [650, 500],
      "parameters": {
        "mode": "manual",
        "assignments": {
          "assignments": [
            {
              "name": "success",
              "type": "boolean",
              "value": false
            },
            {
              "name": "error",
              "type": "object",
              "value": {
                "message": "Missing required parameters: brandId or brandName",
                "code": "VALIDATION_ERROR",
                "node": "Validate Inputs",
                "timestamp": "={{ $now.toISO() }}",
                "isRetryable": false
              }
            }
          ]
        }
      }
    },
    {
      "name": "Process Data",
      "type": "n8n-nodes-base.code",
      "position": [850, 300],
      "parameters": {
        "jsCode": "// Business logic here\nconst brandName = $('Config').first().json.brandName;\n\nreturn {\n  json: {\n    processedData: `Processed ${brandName}`,\n    timestamp: new Date().toISOString()\n  }\n};"
      },
      "continueOnFail": true,
      "onError": "continueErrorOutput"
    },
    {
      "name": "Check Processing Success",
      "type": "n8n-nodes-base.if",
      "position": [1050, 300],
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{ $json.error }}",
              "operation": "isEmpty"
            }
          ]
        }
      }
    },
    {
      "name": "Set Success Response",
      "type": "n8n-nodes-base.set",
      "position": [1250, 200],
      "parameters": {
        "mode": "manual",
        "assignments": {
          "assignments": [
            {
              "name": "success",
              "type": "boolean",
              "value": true
            },
            {
              "name": "data",
              "type": "object",
              "value": "={{ $('Process Data').item.json }}"
            },
            {
              "name": "metadata",
              "type": "object",
              "value": {
                "executionId": "={{ $execution.id }}",
                "duration": "={{ $now.toMillis() - $('Config').first().json.executionStart.toMillis() }}",
                "workflowName": "={{ $workflow.name }}"
              }
            }
          ]
        }
      }
    },
    {
      "name": "Set Error Response",
      "type": "n8n-nodes-base.set",
      "position": [1250, 400],
      "parameters": {
        "mode": "manual",
        "assignments": {
          "assignments": [
            {
              "name": "success",
              "type": "boolean",
              "value": false
            },
            {
              "name": "error",
              "type": "object",
              "value": {
                "message": "={{ $('Process Data').item.json.error?.message || 'Processing failed' }}",
                "code": "PROCESSING_ERROR",
                "node": "Process Data",
                "timestamp": "={{ $now.toISO() }}",
                "isRetryable": true
              }
            },
            {
              "name": "metadata",
              "type": "object",
              "value": {
                "executionId": "={{ $execution.id }}",
                "workflowName": "={{ $workflow.name }}"
              }
            }
          ]
        }
      }
    },
    {
      "name": "Merge All Paths",
      "type": "n8n-nodes-base.merge",
      "position": [1450, 300],
      "parameters": {
        "mode": "append"
      }
    },
    {
      "name": "Return Response",
      "type": "n8n-nodes-base.noOp",
      "position": [1650, 300],
      "parameters": {}
    }
  ],
  "connections": {
    "When Called By Another Workflow": {
      "main": [[{"node": "Config", "type": "main", "index": 0}]]
    },
    "Config": {
      "main": [[{"node": "Validate Inputs", "type": "main", "index": 0}]]
    },
    "Validate Inputs": {
      "main": [
        [{"node": "Process Data", "type": "main", "index": 0}],
        [{"node": "Set Input Validation Error", "type": "main", "index": 0}]
      ]
    },
    "Set Input Validation Error": {
      "main": [[{"node": "Merge All Paths", "type": "main", "index": 0}]]
    },
    "Process Data": {
      "main": [[{"node": "Check Processing Success", "type": "main", "index": 0}]]
    },
    "Check Processing Success": {
      "main": [
        [{"node": "Set Success Response", "type": "main", "index": 0}],
        [{"node": "Set Error Response", "type": "main", "index": 0}]
      ]
    },
    "Set Success Response": {
      "main": [[{"node": "Merge All Paths", "type": "main", "index": 0}]]
    },
    "Set Error Response": {
      "main": [[{"node": "Merge All Paths", "type": "main", "index": 0}]]
    },
    "Merge All Paths": {
      "main": [[{"node": "Return Response", "type": "main", "index": 0}]]
    }
  }
}
```

### Parent Workflow Error Handling

**Parent workflow that properly handles subworkflow responses:**

```json
{
  "name": "Parent Workflow",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "name": "Config",
      "type": "n8n-nodes-base.set",
      "position": [450, 300]
    },
    {
      "name": "Call Processor Subworkflow",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1.2,
      "position": [650, 300],
      "parameters": {
        "source": "database",
        "workflowId": {
          "__rl": true,
          "mode": "list",
          "value": "",
          "cachedResultName": "Data Processor - Subworkflow"
        },
        "options": {
          "waitForCompletion": true
        }
      }
    },
    {
      "name": "Check Subworkflow Success",
      "type": "n8n-nodes-base.if",
      "position": [850, 300],
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{ $json.success }}",
              "value2": true
            }
          ]
        }
      }
    },
    {
      "name": "Handle Success",
      "type": "n8n-nodes-base.code",
      "position": [1050, 200],
      "parameters": {
        "jsCode": "const response = $('Call Processor Subworkflow').item.json;\nconst data = response.data;\n\nconsole.log('Subworkflow succeeded:', data);\n\nreturn {\n  json: {\n    status: 'success',\n    result: data,\n    processedAt: new Date().toISOString()\n  }\n};"
      }
    },
    {
      "name": "Handle Subworkflow Error",
      "type": "n8n-nodes-base.code",
      "position": [1050, 400],
      "parameters": {
        "jsCode": "const response = $('Call Processor Subworkflow').item.json;\nconst error = response.error;\n\nconsole.error('Subworkflow failed:', error);\n\n// Check if error is retryable\nif (error.isRetryable) {\n  // Implement retry logic or send to retry queue\n  return {\n    json: {\n      status: 'retry_needed',\n      error: error,\n      retryAt: new Date(Date.now() + 60000).toISOString()\n    }\n  };\n}\n\n// Non-retryable error - alert and fail gracefully\nreturn {\n  json: {\n    status: 'failed',\n    error: error,\n    failedAt: new Date().toISOString()\n  }\n};"
      }
    },
    {
      "name": "Classify Error",
      "type": "n8n-nodes-base.switch",
      "position": [1250, 400],
      "parameters": {
        "dataPropertyName": "error.code",
        "rules": {
          "rules": [
            {
              "value": "VALIDATION_ERROR",
              "output": 0
            },
            {
              "value": "PROCESSING_ERROR",
              "output": 1
            }
          ]
        }
      }
    },
    {
      "name": "Alert - Validation Error",
      "type": "n8n-nodes-base.slack",
      "position": [1450, 300],
      "parameters": {
        "text": "⚠️ Validation error in workflow\n{{ $json.error.message }}"
      }
    },
    {
      "name": "Retry Processing Error",
      "type": "n8n-nodes-base.code",
      "position": [1450, 500],
      "parameters": {
        "jsCode": "// Add to retry queue or implement retry logic\nconsole.log('Adding to retry queue');\nreturn $input.all();"
      }
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [[{"node": "Config", "type": "main", "index": 0}]]
    },
    "Config": {
      "main": [[{"node": "Call Processor Subworkflow", "type": "main", "index": 0}]]
    },
    "Call Processor Subworkflow": {
      "main": [[{"node": "Check Subworkflow Success", "type": "main", "index": 0}]]
    },
    "Check Subworkflow Success": {
      "main": [
        [{"node": "Handle Success", "type": "main", "index": 0}],
        [{"node": "Handle Subworkflow Error", "type": "main", "index": 0}]
      ]
    },
    "Handle Subworkflow Error": {
      "main": [[{"node": "Classify Error", "type": "main", "index": 0}]]
    },
    "Classify Error": {
      "main": [
        [{"node": "Alert - Validation Error", "type": "main", "index": 0}],
        [{"node": "Retry Processing Error", "type": "main", "index": 0}]
      ]
    }
  }
}
```

### Subworkflow Error Communication Patterns

#### Pattern 1: Merge All Execution Paths

**Critical:** Every subworkflow should merge all possible execution paths (success, validation errors, processing errors) into a single final node:

```
Success Path ↘
              Merge Node → Format Response → Return
Error Path   ↗
```

This ensures the subworkflow ALWAYS completes and returns data to the parent.

#### Pattern 2: Input Validation First

Always validate inputs at the start and return structured errors:

```json
{
  "name": "Validate Inputs",
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $('Config').first().json.requiredParam }}",
          "operation": "isNotEmpty"
        }
      ]
    }
  }
}
```

#### Pattern 3: Continue On Fail for Critical Nodes

Set `continueOnFail: true` on nodes that might error:

```json
{
  "name": "External API Call",
  "type": "n8n-nodes-base.httpRequest",
  "continueOnFail": true,
  "onError": "continueErrorOutput"
}
```

Then check for errors:

```json
{
  "name": "Check API Success",
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "string": [
        {
          "value1": "={{ $json.error }}",
          "operation": "isEmpty"
        }
      ]
    }
  }
}
```

#### Pattern 4: Error Context Enrichment

Include helpful debugging information in error responses:

```json
{
  "name": "Enrich Error Context",
  "type": "n8n-nodes-base.set",
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "name": "error",
          "type": "object",
          "value": {
            "message": "={{ $json.error?.message }}",
            "code": "API_CALL_FAILED",
            "originalError": "={{ $json.error }}",
            "attemptedUrl": "={{ $('External API Call').first().json.url }}",
            "inputData": "={{ $('Config').first().json }}",
            "timestamp": "={{ $now.toISO() }}",
            "executionId": "={{ $execution.id }}"
          }
        }
      ]
    }
  }
}
```

### Quick Reference: Subworkflow Error Patterns

| Scenario | Pattern | Example |
|----------|---------|---------|
| Input validation fails | Return `{success: false, error: {...}}` | Missing brandId parameter |
| API call fails | Set `continueOnFail: true`, check error, return structured response | External service timeout |
| Database operation fails | Catch error, classify (retryable/not), return response | Connection refused |
| Business logic fails | Return `{success: false, error: {...}}` with clear message | Invalid data format |
| Everything succeeds | Return `{success: true, data: {...}}` | Normal operation |

### Subworkflow Testing Strategy

**Include Manual Trigger for Testing:**

```json
{
  "nodes": [
    {
      "name": "Manual Trigger - Testing",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 100]
    },
    {
      "name": "When Called By Another Workflow",
      "type": "n8n-nodes-base.executeWorkflowTrigger",
      "typeVersion": 1,
      "position": [250, 300],
      "parameters": {
        "triggerMode": "manual",
        "inputDataMode": "define",
        "inputDataFields": {
          "values": [
            {
              "fieldName": "brandId",
              "fieldType": "string",
              "required": true
            },
            {
              "fieldName": "brandName",
              "fieldType": "string",
              "required": true
            }
          ]
        }
      }
    },
    {
      "name": "Config",
      "type": "n8n-nodes-base.set",
      "position": [450, 200],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "name": "brandId",
              "value": "={{ $('When Called By Another Workflow').first().json.brandId || 'test-brand-123' }}"
            },
            {
              "name": "brandName",
              "value": "={{ $('When Called By Another Workflow').first().json.brandName || 'Test Brand' }}"
            }
          ]
        }
      }
    }
  ],
  "connections": {
    "Manual Trigger - Testing": {
      "main": [[{"node": "Config", "type": "main", "index": 0}]]
    },
    "When Called By Another Workflow": {
      "main": [[{"node": "Config", "type": "main", "index": 0}]]
    }
  }
}
```

**How this pattern works:**
- When called from parent workflow: Config extracts real parameters from trigger
- When tested with Manual Trigger: Config uses default values (e.g., `'test-brand-123'`)
- No errors during testing because defaults are provided via `||` operator
- Same Config node works for both execution paths

## Loop Patterns

### Split In Batches

For processing items sequentially:

```json
{
  "name": "Split Batches",
  "type": "n8n-nodes-base.splitInBatches",
  "typeVersion": 3,
  "parameters": {
    "batchSize": 1,
    "options": {}
  }
}
```

Connect back to itself for looping:
```json
{
  "connections": {
    "Split Batches": {
      "main": [
        [{"node": "Process Item", "type": "main", "index": 0}],
        [{"node": "After Loop", "type": "main", "index": 0}]
      ]
    },
    "Process Item": {
      "main": [[{"node": "Split Batches", "type": "main", "index": 0}]]
    }
  }
}
```

## Common Pitfalls and Solutions

### Pitfall 1: Using HTTP Request Instead of Purpose-Built Nodes

**Problem:** Workflow breaks on import, credentials don't work
**Solution:** Always check for dedicated n8n node first

### Pitfall 2: Direct Trigger References Throughout Workflow

**Problem:** Workflow breaks when trigger structure changes
**Solution:** Use Config node pattern

### Pitfall 3: Incorrect Data Referencing

**Problem:** `$json.field` doesn't work in later nodes
**Solution:** Use explicit node references: `$('Node Name').item.json.field`

### Pitfall 4: Set Node Loses Previous Data

**Problem:** Data from previous node disappears after Set node
**Solution:** Set nodes create new data by default. Reference previous nodes explicitly when needed.

### Pitfall 5: Webhook Import Failures

**Problem:** Webhook node missing required parameters
**Solution:** Always include `responseMode` and `webhookId` in webhook nodes

## N8N Best Practices - Practical Production Learnings

These are battle-tested patterns discovered during production workflow development that prevent common runtime errors and maintenance headaches.

### Generic Webhook Responses (Trigger-Agnostic Pattern)

**Problem:** Webhook response nodes break when workflow is tested with Manual Trigger instead of Webhook Trigger, causing "No path back to referenced node" errors.

**BAD - Hard-coded node references in response:**
```javascript
// In "Respond to Webhook" node
responseBody: {{ JSON.stringify({
  success: true,
  runId: $('Config').first().json.runId,
  message: 'Analysis started'
}) }}
```
*Note: This example also uses `.first()` for Config - the problem here is hard-coding node references, not the accessor method.*

This fails when:
- Testing with Manual Trigger (Config node might not be in execution path)
- Node names change during refactoring
- Multiple triggers feed into the same response node

**GOOD - Generic reference to merged data:**
```javascript
// In "Respond to Webhook" node (after Merge All Paths node)
responseBody: {{ JSON.stringify($json) }}
```

**Why this works:**
- After a Merge node, `$json` contains your complete structured response
- No hard-coded node name references that break during testing
- Works identically whether triggered by webhook, manual trigger, or schedule
- Resilient to workflow refactoring

**Pattern:**
```
Success Path → Set Success Response ↘
                                     → Merge All Paths → Respond to Webhook
Error Paths  → Set Error Responses  ↗

Respond to Webhook: responseBody = {{ JSON.stringify($json) }}
```

### Use Native Error Outputs Instead of IF Nodes

**Problem:** Adding IF nodes after every database/API operation to check for `$json.error` is verbose and cluttered.

**BAD - Manual error checking with IF nodes:**
```json
{
  "nodes": [
    {
      "name": "Database Insert",
      "type": "n8n-nodes-base.postgres",
      "continueOnFail": true
    },
    {
      "name": "Check If Insert Failed",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "string": [{
            "value1": "={{ $json.error }}",
            "operation": "isEmpty"
          }]
        }
      }
    }
  ]
}
```

**GOOD - Use native error output:**
```json
{
  "name": "Database Insert",
  "type": "n8n-nodes-base.postgres",
  "parameters": {
    "operation": "insert"
  },
  "onError": "continueErrorOutput"
}
```

**Configuration:**
- Set node parameter: **On Error** → `Continue (using error output)`
- This creates **two outputs** on the node:
  - **Top output (main)**: Successful executions
  - **Bottom output (error)**: Failed executions

**Benefits:**
- Cleaner workflow structure
- More n8n-native approach
- Explicit visual branching (success/error paths)
- No need for IF nodes to check `$json.error`

**Pattern:**
```
                     ┌→ Success Path (top output) → Next Step
Database/API Node ──┤
                     └→ Error Path (bottom output) → Set Error Response
```

**Supported nodes:**
- PostgreSQL, MySQL, MongoDB (database operations)
- HTTP Request
- Perplexity, OpenAI (AI services)
- Most external API nodes

### Correct Object Field Syntax in Set Nodes (v3.4+)

**Problem:** In Set node v3.4+, when setting a field type as "Object", pasting JSON strings causes validation errors: `'error' expects a object but we got '{"key": "value"}'`

**BAD - JSON string in Object field:**
```json
{
  "name": "Set Error Response",
  "type": "n8n-nodes-base.set",
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "name": "error",
          "type": "object",
          "value": {
            "message": "Failed to process",
            "timestamp": "={{ $now.toISO() }}"
          }
        }
      ]
    }
  }
}
```

This syntax causes: `'error' expects a object but we got '...'` error.

**GOOD - Proper object expression syntax:**
```json
{
  "name": "Set Error Response",
  "type": "n8n-nodes-base.set",
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "name": "error",
          "type": "object",
          "value": "={{ { message: 'Failed to process', timestamp: $now.toISO() } }}"
        }
      ]
    }
  }
}
```

**In the n8n UI (for Object-type fields):**

```javascript
// Wrapper: {{ { ... } }}
// NO leading "=" (the field handles expressions automatically)

{{
  {
    "message": "Failed to process",
    "code": "ERROR_CODE",
    "timestamp": $now.toISO(),
    "isRetryable": true,
    "details": $json.error
  }
}}
```

**Critical Rules:**
1. **Wrapper**: `{{ { ... } }}` - Double curly braces around single-brace object
2. **No leading `=`**: The Object field in n8n UI doesn't need `=` prefix
3. **String literals**: Use quotes → `"ERROR_CODE"`
4. **Expressions**: NO quotes, NO `={{` → just `$now.toISO()` or `$json.error`
5. **Dynamic strings**: Use template literals → `` `Failed on ${$json.nodeName}` ``

**Examples:**

```javascript
// Simple object
{{
  {
    "executionId": $execution.id,
    "workflowName": $workflow.name,
    "timestamp": $now.toISO()
  }
}}

// Object with nested data
{{
  {
    "runId": $('Config').first().json.runId,
    "status": "completed",
    "results": $json.data,
    "completedAt": $now.toISO()
  }
}}

// Object with dynamic message using template literal
{{
  {
    "message": `Failed to process brand: ${$('Config').first().json.brandName}`,
    "code": "PROCESSING_ERROR",
    "timestamp": $now.toISO()
  }
}}

// Complex nested object
{{
  {
    "success": false,
    "error": {
      "message": $json.error?.message || "Unknown error",
      "code": "DATABASE_ERROR",
      "isRetryable": true
    },
    "metadata": {
      "executionId": $execution.id,
      "duration": Math.round(($now.toMillis() - new Date($('Config').first().json.executionStart).getTime()) / 1000)
    }
  }
}}
```

**What NOT to do:**
```javascript
// ❌ Wrong - Extra ={{ inside object
{{
  {
    "timestamp": "={{ $now.toISO() }}"  // Don't do this!
  }
}}

// ❌ Wrong - Missing wrapper braces
{
  "timestamp": $now.toISO()
}

// ❌ Wrong - Leading = in UI field
={{
  {
    "timestamp": $now.toISO()
  }
}}
```

### Avoid Hard-Coded Node References in Final Response Nodes

**Problem:** Final response nodes that reference specific upstream nodes break when:
- Workflow structure changes
- Nodes are renamed
- Testing with different triggers

**BAD - Direct node references:**
```javascript
// In final Respond to Webhook node
{
  "runId": $('Validate and Prepare').first().json.runId,
  "status": $('Config').first().json.status
}
```
*Note: Even with `.first()`, hard-coding node references is fragile - use merged data instead.*

**GOOD - Reference merged data:**
```javascript
// After Merge All Paths node
$json  // Contains all structured response data
```

**Pattern:**
```
Set Success Response (creates: {success: true, data: {...}})    ↘
                                                                 → Merge All Paths ($json now has complete response)
Set Error Response (creates: {success: false, error: {...}})    ↗                              ↓
                                                                                     Respond: {{ JSON.stringify($json) }}
```

**Why this matters:**
- **Resilient to refactoring**: Node names can change
- **Works with all triggers**: Manual, webhook, schedule
- **Single source of truth**: Merged data is the canonical response
- **Maintainable**: One place to look for response structure

### Use Real Database IDs in Test Data

**Problem:** Test workflows fail with foreign key constraint errors when using fake UUIDs.

**BAD - Fake test IDs:**
```javascript
// In Config node
{
  "name": "brandId",
  "value": "00000000-0000-4000-8000-000000000001"  // Doesn't exist in database!
}
```

**Error:**
```
insert or update on table "analysis_runs" violates foreign key constraint "fk_analysis_runs_brand"
```

**GOOD - Real database IDs:**
```javascript
// Option 1: Query your database first
// In Supabase/PostgreSQL SQL editor:
SELECT id, name FROM brands LIMIT 1;

// Use real ID in Config node
{
  "name": "brandId",
  "value": "abc123-real-uuid-from-database"
}

// Option 2: For Manual Trigger testing, fetch a real brand first
```

**Best Practice Pattern:**
```json
{
  "nodes": [
    {
      "name": "Manual Trigger for Testing",
      "type": "n8n-nodes-base.manualTrigger"
    },
    {
      "name": "Get Test Brand",
      "type": "n8n-nodes-base.postgres",
      "parameters": {
        "operation": "select",
        "table": "brands",
        "limit": 1
      }
    },
    {
      "name": "Config",
      "type": "n8n-nodes-base.set",
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "name": "brandId",
              "value": "={{ $('Get Test Brand').item.json.id }}"
            }
          ]
        }
      }
    }
  ]
}
```

### Bonus: Testing Webhook Workflows with Manual Trigger

**Problem:** Webhook-only workflows require external requests to test, slowing development.

**Solution:** Dual-trigger pattern with Config node bridge:

```json
{
  "nodes": [
    {
      "name": "Manual Trigger for Testing",
      "type": "n8n-nodes-base.manualTrigger",
      "position": [250, 100]
    },
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "name": "Config",
      "type": "n8n-nodes-base.set",
      "position": [450, 200],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "name": "brandId",
              "value": "={{ $json.body ? $json.body.brandId : 'test-brand-123' }}"
            }
          ]
        }
      }
    }
  ],
  "connections": {
    "Manual Trigger for Testing": {
      "main": [[{"node": "Config", "type": "main", "index": 0}]]
    },
    "Webhook Trigger": {
      "main": [[{"node": "Config", "type": "main", "index": 0}]]
    }
  }
}
```

**Pattern:**
- Both triggers connect to same Config node
- Config node uses ternary: `$json.body ? $json.body.brandId : 'test-value'`
- Manual trigger provides test data directly
- Webhook trigger extracts from `$json.body`

## Workflow Import Checklist

Before finalizing any n8n workflow JSON:

### Structure Validation

- [ ] Valid JSON syntax
- [ ] All nodes have unique IDs
- [ ] Node types use correct typeVersion
- [ ] Connections object properly structured
- [ ] Position arrays have [x, y] coordinates

### Best Practices

- [ ] Config node immediately after trigger
- [ ] Purpose-built nodes used (not HTTP Request)
- [ ] Execute Workflow node used for calling other workflows
- [ ] Database operations use database nodes (not HTTP)
- [ ] Error handling on external calls
- [ ] Consistent node naming (no emojis)
- [ ] Proper node spacing (400px horizontal)
- [ ] Explicit node references in code

### Testing Preparation

- [ ] Manual trigger included for debugging
- [ ] Test data can be configured in Config node
- [ ] All credentials use proper node credential system

### Production-Ready Error Handling & Resilience

- [ ] Centralized error workflow configured (Error Trigger)
- [ ] Error classification implemented (retryable vs non-retryable)
- [ ] Retry logic with exponential backoff on API calls
- [ ] Rate limiting configured where needed
- [ ] Timeout settings on all external calls
- [ ] Dead-letter queue for permanently failed items
- [ ] Monitoring and alerting (Slack/Email) configured
- [ ] Circuit breaker pattern for critical external services

### Subworkflow Communication

- [ ] Subworkflows return structured responses (success/error format)
- [ ] All execution paths merge to single return node
- [ ] Input validation at start of subworkflow
- [ ] `continueOnFail: true` on nodes that may error
- [ ] Parent workflow checks `success` flag from subworkflow
- [ ] Error handling includes `isRetryable` flag
- [ ] Manual trigger included for independent testing

## Quick Reference: Node Selection

| Task | Use This Node | NOT This |
|------|---------------|----------|
| Call Perplexity | `n8n-nodes-base.perplexity` | HTTP Request |
| Call OpenAI | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | HTTP Request |
| Database operations | `n8n-nodes-base.postgres` | HTTP Request to REST API |
| Call another workflow | `n8n-nodes-base.executeWorkflow` | HTTP Request to webhook |
| Configuration | Config Set node after trigger | Scattered throughout |
| Constants | Config Set node | Environment variables |

## Complete Example: GEORISE Pattern

```json
{
  "name": "GEORISE Analysis Starter",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "parameters": {
        "path": "analysis-start",
        "responseMode": "responseNode"
      }
    },
    {
      "name": "Config",
      "type": "n8n-nodes-base.set",
      "position": [450, 300],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "name": "brandId",
              "value": "={{ $('Webhook Trigger').item.json.body.brandId }}"
            },
            {
              "name": "brandName",
              "value": "={{ $('Webhook Trigger').item.json.body.brandName }}"
            },
            {
              "name": "topic",
              "value": "={{ $('Webhook Trigger').item.json.body.topic }}"
            }
          ]
        }
      }
    },
    {
      "name": "Create Run Record",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2.5,
      "position": [650, 300],
      "parameters": {
        "operation": "insert",
        "table": {
          "__rl": true,
          "value": "analysis_runs",
          "mode": "list"
        },
        "columns": {
          "mappingMode": "defineBelow",
          "value": {
            "brand_id": "={{ $('Config').first().json.brandId }}",
            "brand_name": "={{ $('Config').first().json.brandName }}",
            "status": "pending"
          }
        }
      },
      "credentials": {
        "postgres": {
          "id": "supabase_postgres"
        }
      }
    },
    {
      "name": "Trigger Processor",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1.2,
      "position": [850, 300],
      "parameters": {
        "source": "database",
        "workflowId": {
          "__rl": true,
          "mode": "list",
          "cachedResultName": "Analysis Processor"
        },
        "options": {
          "waitForCompletion": false
        }
      }
    }
  ]
}
```

## Resources and Core Principles Summary

### Core Node Selection Principles

1. **ALWAYS use purpose-built nodes** - Check for dedicated nodes before HTTP Request
2. **Execute Workflow for sub-workflows** - Never use HTTP Request to call workflows
3. **PostgreSQL node for databases** - Never use HTTP Request for database operations
4. **Config node pattern** - Decouple inputs immediately after trigger
5. **Explicit node references** - Always use `$('Node Name').item.json.field`
6. **No emojis in names** - ASCII only for proper referencing
7. **Credentials in nodes** - Use n8n credential system, not environment variables

### Error Handling & Resilience Principles

8. **Centralized error workflows** - One Error Trigger workflow for all workflows
9. **Error classification** - Distinguish retryable (timeouts, 5xx) from non-retryable (4xx, validation)
10. **Exponential backoff** - 3-5 retries with delays: 1s, 2s, 4s, 8s, 16s (±20% jitter)
11. **Failover patterns** - Primary-Fallback for redundancy, Circuit Breaker for failing services
12. **Dead-letter queue** - Capture permanently failed items for manual review
13. **Monitoring and alerting** - Slack/Email notifications on failures

### Subworkflow Communication Principles

14. **Always return, never throw** - Subworkflows return structured responses, even on errors
15. **Structured response contract** - `{success: boolean, data: any, error: {...}, metadata: {...}}`
16. **Merge all execution paths** - Success and error paths converge to single return node
17. **Input validation first** - Check parameters at start, return structured errors
18. **Continue on fail** - Set `continueOnFail: true` on nodes that may error
19. **Parent checks success flag** - Parent workflow always checks `response.success`
20. **Include isRetryable** - Error responses indicate if retry is appropriate

### Testing & Deployment Principles

21. **Manual trigger for debugging** - Include for easy testing without webhooks
22. **Validate imports** - Test in clean instance before production
23. **Monitor and iterate** - Start simple, add complexity incrementally
24. **Version control** - Track workflow changes in Git
