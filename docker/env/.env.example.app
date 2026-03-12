APP_NAME="mini-RAG"
APP_VERSION="0.1"

FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=512000 # 512KB

POSTGRES_USERNAME="postgres"
POSTGRES_PASSWORD="postgres_password"
POSTGRES_HOST="pgvector"
POSTGRES_PORT=5432
POSTGRES_MAIN_DATABASE="minirag"

# ========================= LLM Config =========================
GENERATION_BACKEND = "OPENAI"
EMBEDDING_BACKEND = "JINA"

OPENAI_API_KEY="ollama"
COHERE_API_KEY="******"
JINA_API_KEY="******"
OPENAI_API_URL="http://172.18.0.1:11434/v1/"

GENERATION_MODEL_ID_LITERAL = ["qwen2.5:1.5b-instruct-q4_K_M", "ministral-3:8b-cloud", "gemma2:9b-instruct-q5_0", "gpt-4o-mini"]
GENERATION_MODEL_ID = "ministral-3:8b-cloud"
EMBEDDING_MODEL_ID="jina-embeddings-v3"
EMBEDDING_MODEL_SIZE=1024

INPUT_DAFAULT_MAX_CHARACTERS=1024
GENERATION_DAFAULT_MAX_TOKENS=200
GENERATION_DAFAULT_TEMPERATURE=0.1

# ========================= Vector DB Config =========================
VECTOR_DB_BACKEND_LITERAL = ["QDRANT", "PGVECTOR"]
VECTOR_DB_BACKEND = "PGVECTOR"
VECTOR_DB_PATH = "qdrant_db"
VECTOR_DB_DISTANCE_METHOD = "cosine"
VECTOR_DB_PGVEC_INDEX_THRESHOLD = 100


# ========================= Template Configs =========================
PRIMARY_LANG = "en"
DEFAULT_LANG = "en"
