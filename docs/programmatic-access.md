# Programmatic Access to the Standards Explorer

The Bridge2AI Standards Explorer data is hosted on [Sage Synapse](https://www.synapse.org/) and is accessible through the Synapse REST API. All data tables are public, so **no API key or authentication is required** for read access.

## Overview

The Standards Explorer consists of several public Synapse tables:

- **DataStandardOrTool** (`syn63096833`): Main table containing all standards, tools, and resources
- **DST_denormalized** (`syn65676531`): Flattened view of DataStandardOrTool and referenced data for easier querying
- **DataTopics** (`syn63096835`): Topics/domains that standards concern (e.g., EHR, Genomics, Image)
- **DataSubstrate** (`syn63096834`): Data formats and structures (e.g., JSON, CSV, BIDS)
- **Organization** (`syn63096836`): Organizations related to standards (e.g., HL7, W3C, CDISC)

All tables belong to the Bridge2AI Standards Explorer project (`syn63096806`).

## REST API Access

The Synapse REST API endpoint is: `https://repo-prod.prod.sagebase.org`

### Basic Query Structure

To query a Synapse table, you need to:

1. Start an async query job
2. Poll for results using the returned token
3. Retrieve the final results

### Example: Query Standards Table (cURL)

```bash
# Step 1: Start the async query
curl -X POST https://repo-prod.prod.sagebase.org/repo/v1/entity/syn63096833/table/query/async/start \
  -H "Content-Type: application/json" \
  -d '{
    "concreteType": "org.sagebionetworks.repo.model.table.QueryBundleRequest",
    "entityId": "syn63096833",
    "query": {
      "sql": "SELECT * FROM syn63096833 LIMIT 10"
    },
    "partMask": 29
  }'

# This returns a token like: {"token": "12345"}

# Step 2: Poll for results (repeat until status is not 202)
curl https://repo-prod.prod.sagebase.org/repo/v1/entity/syn63096833/table/query/async/get/12345

# Step 3: Parse the results from the JSON response
```

### Example: Search by Name (cURL)

```bash
# Search for standards with "FHIR" in the name
curl -X POST https://repo-prod.prod.sagebase.org/repo/v1/entity/syn63096833/table/query/async/start \
  -H "Content-Type: application/json" \
  -d '{
    "concreteType": "org.sagebionetworks.repo.model.table.QueryBundleRequest",
    "entityId": "syn63096833",
    "query": {
      "sql": "SELECT id, name, description FROM syn63096833 WHERE name LIKE '\''%FHIR%'\'' LIMIT 5"
    },
    "partMask": 29
  }'
```

### Example: Query Denormalized Table

The denormalized table includes expanded columns for easier querying:

```bash
curl -X POST https://repo-prod.prod.sagebase.org/repo/v1/entity/syn65676531/table/query/async/start \
  -H "Content-Type: application/json" \
  -d '{
    "concreteType": "org.sagebionetworks.repo.model.table.QueryBundleRequest",
    "entityId": "syn65676531",
    "query": {
      "sql": "SELECT * FROM syn65676531 WHERE concerns_data_topic_names LIKE '\''%Genomics%'\''"
    },
    "partMask": 29
  }'
```

## Python Access

### Simplest Example (requests library)

Here's the most minimal example to search the Standards Explorer:

```python
import requests
import time

def search_standards(search_term):
    """Simple function to search standards by name."""
    # Start query
    response = requests.post(
        "https://repo-prod.prod.sagebase.org/repo/v1/entity/syn63096833/table/query/async/start",
        json={
            "concreteType": "org.sagebionetworks.repo.model.table.QueryBundleRequest",
            "entityId": "syn63096833",
            "query": {"sql": f"SELECT id, name, description FROM syn63096833 WHERE name LIKE '%{search_term}%' LIMIT 10"},
            "partMask": 29
        },
        headers={"Content-Type": "application/json"}
    )
    token = response.json()["token"]
    
    # Wait for results
    while True:
        result = requests.get(
            f"https://repo-prod.prod.sagebase.org/repo/v1/entity/syn63096833/table/query/async/get/{token}",
            headers={"Content-Type": "application/json"}
        )
        if result.status_code != 202:  # 202 = still processing
            return result.json()["queryResult"]["queryResults"]["rows"]
        time.sleep(1)

# Use it
for row in search_standards("FHIR"):
    values = row["values"]
    print(f"{values[0]}: {values[1]}")

# Output:
# B2AI_STANDARD:109: FHIR
# B2AI_STANDARD:845: CDC Introduction to FHIR
# B2AI_STANDARD:846: FHIR Drills
```

**Note:** The Synapse API requires an async query pattern (start query → poll for results), but the above function wraps this complexity for you.

### Using httpx (Async)

This example shows how to query the API without the Synapse Python client:

```python
import httpx
import asyncio
import json

SYNAPSE_BASE_URL = "https://repo-prod.prod.sagebase.org"
TABLE_ID = "syn63096833"

async def poll_async_job(client, table_id, async_token, max_wait=30):
    """Poll an async job until it completes or times out."""
    url = f"{SYNAPSE_BASE_URL}/repo/v1/entity/{table_id}/table/query/async/get/{async_token}"
    headers = {"Content-Type": "application/json"}
    
    start_time = asyncio.get_event_loop().time()
    while True:
        elapsed = asyncio.get_event_loop().time() - start_time
        if elapsed > max_wait:
            raise TimeoutError(f"Query timed out after {max_wait} seconds")
        
        response = await client.get(url, headers=headers)
        
        # 202 means still processing
        if response.status_code == 202:
            await asyncio.sleep(1)
            continue
        
        response.raise_for_status()
        return response.json()

async def query_standards(sql_query):
    """Query the Standards Explorer table."""
    query_request = {
        "concreteType": "org.sagebionetworks.repo.model.table.QueryBundleRequest",
        "entityId": TABLE_ID,
        "query": {"sql": sql_query},
        "partMask": 0x1 | 0x4 | 0x10  # queryResults + selectColumns + columnModels
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Start the async query
        start_response = await client.post(
            f"{SYNAPSE_BASE_URL}/repo/v1/entity/{TABLE_ID}/table/query/async/start",
            json=query_request,
            headers={"Content-Type": "application/json"}
        )
        start_response.raise_for_status()
        
        # Get the async token
        async_token = start_response.json().get("token")
        
        # Poll for results
        result_bundle = await poll_async_job(client, TABLE_ID, async_token)
        
        # Extract rows
        rows = result_bundle.get("queryResult", {}).get("queryResults", {}).get("rows", [])
        columns = result_bundle.get("selectColumns", [])
        
        return {
            "columns": [col.get("name") for col in columns],
            "rows": rows,
            "row_count": len(rows)
        }

# Example usage
async def main():
    # Get all standards (limited to 10)
    result = await query_standards("SELECT * FROM syn63096833 LIMIT 10")
    print(f"Found {result['row_count']} standards")
    
    # Search for FHIR-related standards
    result = await query_standards(
        "SELECT id, name, description FROM syn63096833 WHERE name LIKE '%FHIR%'"
    )
    for row in result['rows']:
        values = row.get('values', [])
        print(f"ID: {values[0]}, Name: {values[1]}")

# Run the async function
asyncio.run(main())

# Expected output:
# Found 10 standards
# ID: B2AI_STANDARD:109, Name: FHIR
# ID: B2AI_STANDARD:845, Name: CDC Introduction to FHIR
# ID: B2AI_STANDARD:846, Name: FHIR Drills
```

### Using requests (Synchronous)

```python
import requests
import time

SYNAPSE_BASE_URL = "https://repo-prod.prod.sagebase.org"
TABLE_ID = "syn63096833"

def query_standards(sql_query, max_wait=30):
    """Query the Standards Explorer table synchronously."""
    query_request = {
        "concreteType": "org.sagebionetworks.repo.model.table.QueryBundleRequest",
        "entityId": TABLE_ID,
        "query": {"sql": sql_query},
        "partMask": 29  # Request all parts
    }
    
    # Start the async query
    response = requests.post(
        f"{SYNAPSE_BASE_URL}/repo/v1/entity/{TABLE_ID}/table/query/async/start",
        json=query_request,
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    async_token = response.json().get("token")
    
    # Poll for results
    start_time = time.time()
    while True:
        if time.time() - start_time > max_wait:
            raise TimeoutError(f"Query timed out after {max_wait} seconds")
        
        result = requests.get(
            f"{SYNAPSE_BASE_URL}/repo/v1/entity/{TABLE_ID}/table/query/async/get/{async_token}",
            headers={"Content-Type": "application/json"}
        )
        
        if result.status_code == 202:  # Still processing
            time.sleep(1)
            continue
        
        result.raise_for_status()
        return result.json()

# Example usage
result = query_standards("SELECT id, name, description FROM syn63096833 WHERE name LIKE '%FHIR%' LIMIT 5")
rows = result.get("queryResult", {}).get("queryResults", {}).get("rows", [])

for row in rows:
    values = row.get("values", [])
    print(f"ID: {values[0]}, Name: {values[1]}")

# Output:
# ID: B2AI_STANDARD:109, Name: FHIR
# ID: B2AI_STANDARD:845, Name: CDC Introduction to FHIR
# ID: B2AI_STANDARD:846, Name: FHIR Drills
```

### Using the Synapse Python Client

The official Synapse Python client provides a simpler interface:

```python
import synapseclient

# Login (anonymous access for public data)
syn = synapseclient.Synapse()
syn.login()

# Query the table
query = "SELECT * FROM syn63096833 WHERE name LIKE '%FHIR%' LIMIT 10"
results = syn.tableQuery(query)

# Convert to pandas DataFrame
df = results.asDataFrame()
print(df.head())

# Access specific columns
print(df[['id', 'name', 'description']])

# Example output:
#                    id                           name  \
# 0  B2AI_STANDARD:109                           FHIR   
# 1  B2AI_STANDARD:845  CDC Introduction to FHIR   
# 2  B2AI_STANDARD:846                    FHIR Drills   
#
#                                         description  
# 0       Fast Healthcare Interoperability Resources  
# 1          CDC Introduction to FHIR - Training...  
# 2                                        FHIR Drills
```

**Installation:**
```bash
pip install synapseclient
```

### Using the Synapse CLI

Query tables directly from the command line:

```bash
# Install synapseclient
pip install synapseclient

# Query and save to CSV
synapse query "SELECT * FROM syn63096833 LIMIT 10" > tmp.csv

# Clean the result (remove header rows)
tail -n +3 tmp.csv > standards.csv
rm tmp.csv
```

## Common Query Examples

### List Available Topics

First, see what topics are available:

```python
import requests
import time

def query_topics():
    result = query_standards("SELECT id, name FROM syn63096835 LIMIT 10")
    rows = result.get("queryResult", {}).get("queryResults", {}).get("rows", [])
    for row in rows:
        values = row.get("values", [])
        print(f"{values[0]}: {values[1]}")

# Output:
# B2AI_TOPIC:1: Biology
# B2AI_TOPIC:2: Cell
# B2AI_TOPIC:3: Cheminformatics
# B2AI_TOPIC:4: Clinical Observations
# B2AI_TOPIC:5: Data
# B2AI_TOPIC:6: Demographics
# B2AI_TOPIC:7: Disease
# B2AI_TOPIC:8: Drug
# B2AI_TOPIC:9: EHR
# B2AI_TOPIC:10: EKG
```

### Search by Topic

```sql
-- Find all standards related to genomics (topic ID: B2AI_TOPIC:5)
SELECT id, name, description 
FROM syn63096833 
WHERE concerns_data_topic LIKE '%B2AI_TOPIC:5%'
LIMIT 5
```

```python
# Example output:
# B2AI_STANDARD:114: Genomics Operations
# B2AI_STANDARD:127: FuGE-ML
# B2AI_STANDARD:128: FuGEFlow
# B2AI_STANDARD:141: GCDML
```

### Search by Organization

```sql
-- Find standards from HL7 (org ID: B2AI_ORG:48)
SELECT id, name, description, url
FROM syn63096833 
WHERE responsible_organization LIKE '%B2AI_ORG:48%' 
   OR has_relevant_organization LIKE '%B2AI_ORG:48%'
```

### Search by Data Substrate

```sql
-- Find standards that work with JSON (substrate ID: B2AI_SUBSTRATE:58)
SELECT id, name, description 
FROM syn63096833 
WHERE has_relevant_data_substrate LIKE '%B2AI_SUBSTRATE:58%'
```

### Filter by Category

```sql
-- Find all biomedical standards
SELECT id, name, description 
FROM syn63096833 
WHERE category = 'B2AI_STANDARD:BiomedicalStandard'
```

### Full-text Search

```sql
-- Search across multiple text fields
SELECT id, name 
FROM syn63096833 
WHERE description LIKE '%genomic%'
LIMIT 5
```

```python
# Example output:
# B2AI_STANDARD:44: SDTM
# B2AI_STANDARD:114: Genomics Operations
# B2AI_STANDARD:127: FuGE-ML
# B2AI_STANDARD:128: FuGEFlow
# B2AI_STANDARD:141: GCDML
```

### Filter by Properties

```sql
-- Find open standards
SELECT id, name, is_open 
FROM syn63096833 
WHERE is_open = 'true'
LIMIT 5
```

```python
# Example output:
# B2AI_STANDARD:1: .ACE format (Open: true)
# B2AI_STANDARD:2: DMS (Open: true)
# B2AI_STANDARD:3: ABCD (Open: true)
# B2AI_STANDARD:4: AGP (Open: true)
# B2AI_STANDARD:5: AnIML (Open: true)
```

## Query the Denormalized Table

For easier querying with human-readable values, use the denormalized table:

```sql
-- Search by topic name instead of ID
SELECT id, name, concerns_data_topic_names
FROM syn65676531 
WHERE concerns_data_topic_names LIKE '%Genomics%'
```

```python
import synapseclient

syn = synapseclient.Synapse()
syn.login()

# Query denormalized table with readable column names
query = """
SELECT id, name, category_label, concerns_data_topic_names, 
       responsible_organization_names
FROM syn65676531 
WHERE concerns_data_topic_names LIKE '%EHR%'
"""

df = syn.tableQuery(query).asDataFrame()
print(df)
```

## Rate Limits and Best Practices

- **No authentication required** for public tables (read-only access)
- The API uses **async queries** - always poll for results rather than expecting immediate responses
- **Set reasonable timeouts** (30-60 seconds for most queries)
- Use **LIMIT** clauses to avoid retrieving too much data at once
- The **partMask** parameter controls which parts of the query result are returned:
  - `0x1` (1): Query results
  - `0x4` (4): Select columns
  - `0x10` (16): Column models
  - `0x1D` (29): All parts (commonly used)

## Additional Resources

- [Synapse REST API Documentation](https://rest-docs.synapse.org/rest/index.html)
- [Synapse Python Client Documentation](https://python-docs.synapse.org/)
- [Standards Explorer MCP Implementation](https://github.com/bridge2ai/standards-explorer-mcp)
- [Standards Explorer Project on Synapse](https://www.synapse.org/#!Synapse:syn63096806)

## Support

For questions or issues:
- Open an issue on the [b2ai-standards-registry GitHub repository](https://github.com/bridge2ai/b2ai-standards-registry/issues)
- Contact the Bridge2AI Standards team

