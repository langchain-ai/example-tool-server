# Example Tool Server

An example implementation of a tool server using `open-tool-server`.

https://github.com/langchain-ai/open-tool-server

## Tools

This server implements the following example tools:

1. Exchange Rate: use an exchange rate API to find the exchange rate between two different currncies.
2. GithHub API: surface most recent 50 issues for a given github repository.
3. Hacker News: query hacker news to find the 5 most relevant matches.
4. Reddit: Query reddit for a particular topic
5. Wikipedia: Get information about current events.

## Usage

1. Build with docker

```shell
docker build -t example-tool-server .
```

2. Generate a secret using your favorite random number generator


```shell
export APP_SECRET=$(openssl rand -base64 32 )
```

```shell
export APP_SECRET=$(head -c 32 /dev/urandom | base64)
```

```shell
export APP_SECRET=$( let your cat walk across your keyboard)
```


3. Run the image locally

```shell
docker run -e APP_SECRET=$APP_SECRET -p 8080:8080 example-tool-server
```


or deploy to your favorite cloud provider
