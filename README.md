# Example Tool Server

An example implementation of a tool server using [universal-tool-server](https://github.com/langchain-ai/universal-tool-server).

## Tools

This server implements the following example tools:

1. Exchange Rate: use an exchange rate API to find the exchange rate between two different currncies.
2. GithHub API: surface most recent 50 issues for a given github repository.
3. Hacker News: query hacker news to find the 5 most relevant matches.
4. Reddit: Query reddit for a particular topic

## Usage

### Local

#### No Authentication

If you want to spin the server up locally to test it out without authentication, you can run the following command:

```shell
DISABLE_AUTH=true uv run uvicorn app.server:app 
```

You'll need to have `uv` installed: https://docs.astral.sh/uv/

Once the server is running, if auth is disabled, you'll be able to access the API documentation at: http://localhost:8000/docs

#### With Authentication

The server implements a very basic form of authentication that supports a single user. To use it, you'll need to set an `APP_SECRET` environment variable.


1. Generate a secret using your favorite random number generator

   ```shell
   export APP_SECRET=$(openssl rand -base64 32 )
   ```

   or

   ```shell
   export APP_SECRET=$(head -c 32 /dev/urandom | base64)
   ```

   or

   ```shell
   export APP_SECRET="some_super_secure_password"
   ```

2. Run with `uv`
 
   ```shell
   APP_SECRET=$APP_SECRET uv run uvicorn app.server:app 
   ````

### Docker

1. Build with docker
 
    ```shell
    docker build -t example-tool-server .
    ```
2. Generate a secret key
3. Run the image locally
    ```shell
    docker run -e APP_SECRET=$APP_SECRET -p 8080:8080 example-tool-server
    ```

Alternatively, deploy to your favorite cloud provider.


## Client

Once the server is running you can use the universal-tool-client to interact with it. 

```shell
pip install universal-tool-client
```

### Client

```python
from universal_tool_client import get_sync_client

url = "http://localhost:8000"
headers = {
    "Authorization": "YOUR SECRET GOES HERE",
}

client = get_sync_client(url=url, headers=headers)

print(client.health())  # Health check
print(client.info())  # Server version and other information

# List tools
print(client.tools.list())  # List of tools
# Call a tool
print(client.tools.call("echo", {"msg": "hello"}))  # hello!

# Get the tools as a LangchainTools object
tools = client.tools.as_langchain_tools()
```

#### Curl

No authentication:

```shell
curl -X 'POST' \
  'http://127.0.0.1:8000/tools/call' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "$schema": "otc://1.0",
  "request": {
    "tool_id": "get_weather@1.0.0",
    "input": { "city": "san francisco"}
  }
}'
```

With authentication:

Add the `Authorization` header with the secret you generated earlier.

e.g., `-H 'Authorization: YOUR SECRET`