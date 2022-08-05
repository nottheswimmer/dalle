AUTH0_AUTHORIZE_URL_TEMPLATE = "https://%s/authorize"
AUTH0_TOKEN_URL_TEMPLATE = "https://%s/oauth/token"

OPENAI_AUTH0_CLIENT_ID = "DMg91f5PCHQtc7u018WKiL0zopKdiHle"
OPENAI_AUTH0_DOMAIN = "auth0.openai.com"
OPENAI_AUTH0_AUDIENCE = "https://api.openai.com/v1"
OPENAI_AUTH0_SCOPE = "openid profile email offline_access"

OPENAI_LABS_REDIRECT_URI = "https://labs.openai.com/auth/callback"
OPENAI_LABS_API_URL = "https://labs.openai.com/api/labs"
OPENAI_LABS_LOGIN_URL = f"{OPENAI_LABS_API_URL}/auth/login"
OPENAI_LABS_TASKS_URL = f"{OPENAI_LABS_API_URL}/tasks"
OPENAI_LABS_TASK_URL_TEMPLATE = f"{OPENAI_LABS_TASKS_URL}/%s"
OPENAI_LABS_GENERATION_DOWNLOAD_URL_TEMPLATE = f"{OPENAI_LABS_API_URL}/generations/%s/download"
