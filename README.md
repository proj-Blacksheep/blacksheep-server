# blacksheep-server
black sheep project api server repo

# API Plan

## For basic user
- They can only get their own api key, reload it
    - /users/get_api_key
    - /users/update_api_key
    - /users/update_password

- They can only get their own usage
    - /users/get_usage

- They can only look up models
    - /models/get_models

- They can call models
    - /api


## For admin user
- They can create, delete users
    - /users/create
    - /users/delete

- They can create, delete models
    - /models/create
    - /models/delete

- They can get all users, models
    - /users/get_all
    - /models/get_all

- They can get all usage
    - /usage/get_all

- (TODO) They can set usage limit for users
    - /users/set_usage_limit

---

# Model Notes

#### Azure OpenAI

Needs
- deployment_name
- end_point
- api_key


#### OpenAI

Needs
- api_key


#### GCP Gemini (Vertex AI)

Needs
- GCP Service Account

#### Gemini - Google AI Studio

Needs
- api_key

#### Anthropic

Needs
- api_key
