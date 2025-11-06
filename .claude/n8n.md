---
name: n8n
description: n8n workflow automation tool. Use for creating workflows, integrations, automations, API connections, and no-code/low-code automation tasks.
---

# N8N Skill

Comprehensive assistance with n8n workflow automation, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- **Creating or modifying n8n workflows** - Building automation workflows, connecting services
- **Working with n8n nodes** - Configuring nodes, setting up triggers, transforming data
- **Writing expressions** - Using JavaScript expressions, accessing node data, manipulating values
- **Using the Code node** - Writing custom JavaScript or Python code in workflows
- **Transforming data** - Mapping, filtering, aggregating, or restructuring workflow data
- **Setting up integrations** - Connecting APIs, authenticating services, configuring webhooks
- **Self-hosting n8n** - Installing, configuring, or troubleshooting self-hosted instances
- **Deploying to cloud platforms** - AWS, Google Cloud, Azure, Docker, Kubernetes
- **Configuring authentication** - OAuth, SAML, API keys, credentials
- **Working with date/time** - Using Luxon for date manipulation in expressions
- **Debugging workflows** - Troubleshooting execution, data flow, or error handling

## Quick Reference

### 1. Accessing Data in Expressions

```javascript
// Get current timestamp (Luxon object)
{{$now}}
// Returns: 2022-03-09T14:02:37.065+00:00

// Get today at midnight
{{$today}}

// Access data from previous node
{{ $json.customer_name }}

// Access data from specific node
{{ $node["Edit Fields"].json.customer_id }}

// Conditional message with data mapping
Hi {{ $json.customer_name }}. Your description is: {{ $json.customer_description }}
```

### 2. Data Structure Format

All data in n8n uses this array-of-objects structure:

```json
[
  {
    "json": {
      "apple": "beets",
      "carrot": {
        "dill": 1
      }
    },
    "binary": {
      "apple-picture": {
        "data": "....",
        "mimeType": "image/png",
        "fileExtension": "png",
        "fileName": "example.png"
      }
    }
  }
]
```

### 3. Convenience Functions

```javascript
// Check if value is empty, return default if so
{{ $ifEmpty($json.field, "default value") }}

// Conditional logic in expression
{{ $if($json.age > 18, "adult", "minor") }}

// Get maximum value
{{ $max(5, 10, 3, 8) }}  // Returns 10

// Get minimum value
{{ $min(5, 10, 3, 8) }}   // Returns 3
```

### 4. Email Validation (String Method)

```javascript
// Check if string is valid email
{{ "example@example.com".isEmail() }}
// Returns true

// Use in conditional
{{ $if($json.email.isEmail(), "valid", "invalid") }}
```

### 5. Boolean to Number Conversion

```javascript
// Convert boolean to 0 or 1
{{ $json.isActive.toInt() }}
// false → 0, true → 1
```

### 6. Data Transformation with Code Node

The Code node supports JavaScript and Python. From v0.166.0+, n8n automatically wraps your data:

```javascript
// Return transformed items
return items.map(item => ({
  json: {
    fullName: item.json.firstName + ' ' + item.json.lastName,
    timestamp: Date.now()
  }
}));
```

### 7. Setting Up Kafka Credentials

```json
{
  "clientId": "my-client-id",
  "brokers": "kafka-1:9092,kafka-2:9092",
  "ssl": true,
  "authentication": {
    "username": "my-username",
    "password": "my-password",
    "saslMechanism": "scram-sha-256"
  }
}
```

### 8. Docker Deployment (Quick Start)

```bash
# Deploy n8n with Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 9. Google Cloud Run Deployment

```bash
# Deploy to Cloud Run (easy mode - in-memory)
gcloud run deploy n8n \
    --image=n8nio/n8n \
    --region=us-west1 \
    --allow-unauthenticated \
    --port=5678 \
    --no-cpu-throttling \
    --memory=2Gi
```

### 10. OAuth Setup for Spotify (Self-Hosted)

```javascript
// Configuration steps:
// 1. Create app at https://developer.spotify.com/dashboard
// 2. Add OAuth Redirect URL from n8n
// 3. Copy Client ID and Client Secret to n8n credential
// 4. Click "Connect my account" in n8n

// Note: n8n Cloud users can skip these steps
```

## Key Concepts

### Expressions vs Code Node
- **Expressions**: Inline JavaScript in `{{ }}` brackets for simple data access and manipulation
- **Code Node**: Full JavaScript/Python environment for complex logic and loops
- Expressions auto-evaluate; Code node requires explicit `return`

### Data Items and Processing
- Nodes process **all items** in an array by default
- Each item has a `json` property for data and optional `binary` for files
- Expressions like `{{ $json.name }}` automatically process the current item

### Item Linking
- n8n tracks which input items create which output items
- Use `$node["NodeName"].json` to access data from specific nodes
- Item linking enables proper data mapping across workflow branches

### Luxon Date/Time Library
- n8n uses Luxon for date manipulation
- `$now` and `$today` are built-in Luxon objects
- Timezone defaults to `America/New_York` or set via `GENERIC_TIMEZONE` environment variable
- Use `DateTime.fromISO()` or `DateTime.fromFormat()` to parse date strings

### Data Transformation Nodes
- **Aggregate**: Group items together
- **Limit**: Restrict number of items
- **Remove Duplicates**: Filter duplicate items
- **Sort**: Order items or randomize
- **Split Out**: Expand arrays into separate items
- **Summarize**: Create pivot table-style aggregations

## Reference Files

This skill includes comprehensive documentation organized in `references/`:

- **code.md** (26 pages) - Complete guide to data structures, expressions, Luxon date/time, transformation functions, and the Code node. Includes:
  - Data structure format and item processing
  - Expression syntax and cookbook
  - Date/time manipulation with Luxon
  - Convenience methods ($ifEmpty, $if, $max, $min)
  - Data transformation functions for arrays, strings, numbers, objects
  - Mapping and item linking
  - Code examples for common tasks

- **getting_started.md** (11 pages) - Quickstart guides, tutorials, and initial setup. Covers:
  - Very quick quickstart (3-step workflow creation)
  - Server setup options (Digital Ocean, Heroku, AWS, GKE, Azure)
  - Deployment strategies and backup recommendations
  - Platform comparison (Cloud vs self-hosted vs npm vs Docker)
  - User data management and restart handling

- **hosting.md** (23 pages) - Self-hosting guides for multiple platforms. Includes:
  - Docker, Docker Compose, and Kubernetes configurations
  - AWS (EKS), Google Cloud Run, and Azure setup
  - Database configuration (Postgres, persistent volumes)
  - Environment variables and resource management
  - SSL, authentication, and security setup
  - Specific credential guides (Spotify, Kafka, etc.)

- **integrations.md** - Credential setup and authentication for various services
  - OAuth configuration examples
  - API authentication patterns
  - Service-specific setup guides

- **workflows.md** - Workflow creation patterns and best practices
  - Common workflow templates
  - Node configuration examples
  - Error handling strategies

- **other.md** - Additional documentation not categorized above

Use the Read tool to view specific reference files when you need detailed information on any topic.

## Working with This Skill

### For Beginners
Start with **getting_started.md** for:
- The very quick quickstart (load template, run workflow, add node)
- Platform selection guide (Cloud, self-host, npm, Docker)
- Basic concepts (workflows, nodes, expressions, credentials)

Then explore **code.md** for:
- Understanding data structure (the `json` and `binary` format)
- Basic expressions (accessing `$json` properties)
- Using `$now` and `$today` for dates

### For Intermediate Users
Dive into **code.md** for:
- Writing complex expressions with conditionals and functions
- Using the Code node for JavaScript/Python logic
- Data transformation techniques (mapping, filtering, aggregating)
- Luxon date/time manipulation
- Item linking across workflow branches

Explore **integrations.md** for:
- Setting up OAuth for services (Spotify, Google, etc.)
- Configuring API credentials
- Webhook setup

### For Self-Hosting and DevOps
Study **hosting.md** for:
- Platform-specific deployment (AWS EKS, GCP Cloud Run, Azure, Heroku)
- Kubernetes configuration with persistent volumes
- Postgres database setup and environment variables
- Resource limits and scaling strategies
- SSL, authentication, and security hardening

Review **getting_started.md** for:
- Server setup comparisons
- Backup and recovery strategies
- User data management

### For Advanced Use Cases
Combine knowledge from:
- **code.md**: Complex data transformations, custom functions
- **workflows.md**: Advanced workflow patterns
- **hosting.md**: Production deployment, scaling, monitoring

### Navigation Tips
1. **Know your goal** - Each reference file serves a specific purpose
2. **Use search** - Reference files include tables of contents
3. **Check examples first** - Quick reference above has common patterns
4. **Cross-reference** - Topics like authentication span multiple files
5. **Version awareness** - Note version-specific features (e.g., "From 0.166.0 on...")

## Common Patterns

### Working with API Responses
```javascript
// Extract nested data
{{ $json.response.data.items[0].name }}

// Handle missing data safely
{{ $ifEmpty($json.response?.data, []) }}
```

### Date Manipulation
```javascript
// Get date 7 days ago
{{ $today.minus({ days: 7 }) }}

// Format date
{{ $now.toFormat("yyyy-MM-dd") }}

// Parse date string
{{ DateTime.fromISO('2019-06-23') }}
{{ DateTime.fromFormat("23-06-2019", "dd-MM-yyyy") }}
```

### Conditional Logic
```javascript
// Simple if/else
{{ $if($json.status === "active", "Process", "Skip") }}

// With empty check
{{ $if($ifEmpty($json.email, "").isEmail(), $json.email, "invalid@example.com") }}
```

### Loop Through Items in Code Node
```javascript
// Process all items
for (const item of items) {
  item.json.processed = true;
  item.json.timestamp = Date.now();
}
return items;
```

## Resources

### Official Documentation
- n8n Documentation: https://docs.n8n.io
- Community Forum: https://community.n8n.io
- Workflow Templates: https://n8n.io/workflows

### Self-Hosting Resources
- Docker Image: `n8nio/n8n`
- Latest version: 1.118.1 (production)
- Next version: 1.119.0 (beta)
- GitHub: https://github.com/n8n-io/n8n
- License: Sustainable Use License (fair-code model)

### Quick Setup Paths
1. **n8n Cloud**: Free trial, no setup - https://n8n.io/cloud/
2. **npm**: `npm install n8n -g && n8n start`
3. **Docker**: `docker run -it --rm -p 5678:5678 n8nio/n8n`
4. **Self-hosted Production**: See hosting.md for platform guides

## Notes

- **Python in expressions**: Python is only available in the Code node, NOT in `{{ }}` expressions
- **Data wrapping**: From v0.166.0+, Code node automatically wraps items in `json` key if missing
- **Version awareness**: Always check if features require specific n8n versions
- **Rate limiting**: Most documentation sites need rate limiting during scraping
- **Security**: Never commit credentials; use environment variables or Secret Manager
- **Timezone**: Default is `America/New_York`; override with `GENERIC_TIMEZONE`

## Troubleshooting

### Expression Not Working
- Check syntax: `{{ $json.field }}` not `{ $json.field }`
- Verify node name: `$node["Exact Node Name"].json`
- Use expressions editor to see available data

### Code Node Errors
- Ensure `return` statement exists
- Return array of objects with `json` property
- Check for syntax errors in JavaScript/Python

### Self-Hosting Issues
- Verify Docker/Kubernetes resources (memory, CPU)
- Check database connection strings
- Ensure environment variables are set
- Review logs for authentication errors

### Data Not Mapping
- Check item linking with input/output data
- Verify previous node executed successfully
- Use expressions editor to browse available data
- Try `$node["NodeName"].json` instead of `$json`
