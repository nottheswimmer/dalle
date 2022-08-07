"""
This module contains strings about the outside world which were not parameterized
because during development it was assumed that they wouldn't change.
"""

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
OPENAI_LABS_GENERATION_URL = "https://labs.openai.com/api/labs/generations"
OPENAI_LABS_GENERATION_URL_TEMPLATE = f"{OPENAI_LABS_GENERATION_URL}/%s"
OPENAI_LABS_GENERATION_DOWNLOAD_URL_TEMPLATE = f"{OPENAI_LABS_GENERATION_URL_TEMPLATE}/download"
OPENAI_LABS_BILLING_URL = f"{OPENAI_LABS_API_URL}/billing"
OPENAI_LABS_BILLING_CREDIT_SUMMARY_URL = f"{OPENAI_LABS_BILLING_URL}/credit_summary"
OPENAI_LABS_GENERATION_SHARE_URL_TEMPLATE = f"{OPENAI_LABS_GENERATION_URL}/%s/share"
OPENAI_LABS_GENERATION_FLAG_URL_TEMPLATE = f"{OPENAI_LABS_GENERATION_URL}/%s/flags"
OPENAI_LABS_COLLECTION_URL = f"{OPENAI_LABS_API_URL}/collections"
OPENAI_LABS_COLLECTION_GENERATION_URL_TEMPLATE = f"{OPENAI_LABS_COLLECTION_URL}/%s/generations"
OPENAI_LABS_SHARE_URL_TEMPLATE = "https://labs.openai.com/s/%s"
