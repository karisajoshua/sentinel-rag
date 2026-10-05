# Deployment

SentinelRAG requires two production dependencies:

1. PostgreSQL with the pgvector extension.
2. An OpenAI API credential supplied through the deployment platform's secret store.

Required environment variables:

- `SENTINEL_DATABASE_URL`
- `SENTINEL_OPENAI_API_KEY`
- `SENTINEL_OPENAI_CHAT_MODEL` (optional)

Never commit production credentials to the repository.

The included Dockerfile runs the API. `docker-compose.yml` is intended for local development and initializes a pgvector-enabled PostgreSQL database using `db/schema.sql`.

Before public deployment, add authentication and rate limiting to indexing and question endpoints. The current API is a portfolio development interface and should not be exposed anonymously with a funded LLM credential.
