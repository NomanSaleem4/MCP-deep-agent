# mcp-deepagent

## Docker

Build the image:

```bash
docker build -t mcp-deepagent .
```

Run the container (loads config from `.env`, maps port 8000):

```bash
docker run -d --name mcp-deepagent --env-file .env -p 8000:8000 mcp-deepagent
```

Stop the container:

```bash
docker stop mcp-deepagent
```

Remove the container:

```bash
docker rm mcp-deepagent
```

Remove the image:

```bash
docker rmi mcp-deepagent
```
