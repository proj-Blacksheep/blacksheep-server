Table users {
  id integer [primary key]
  username varchar [not null, unique]
  api_key varchar [not null, unique]
  role varchar
  created_at timestamp [default: `now()`]
}

Table models {
  id integer [primary key]
  name varchar [not null]
  description text
  created_at timestamp [default: `now()`]
}

Table user_model_access {
  id integer [primary key]
  user_id integer [not null]
  model_id integer [not null]
  access_level varchar [not null]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
}

Ref: user_model_access.user_id > users.id
Ref: user_model_access.model_id > models.id
