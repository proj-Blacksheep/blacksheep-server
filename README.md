# Blacksheep Server
AI 모델 API 서버

## API 문서

### 인증 API
| 엔드포인트 | 메소드 | 설명 | 요청 데이터 |
|------------|--------|------|------------|
| `/login` | POST | 사용자 로그인 및 토큰 발급 | username, password |

### 사용자 관리 API (`/users`)

#### 일반 사용자 엔드포인트
| 엔드포인트 | 메소드 | 설명 |
|------------|--------|------|
| `/users/me` | GET | 현재 사용자 정보 조회 |
| `/users/usage/{username}` | GET | 자신의 API 사용량 조회 |
| `/users/password` | POST | 비밀번호 변경 |

#### 관리자 엔드포인트
| 엔드포인트 | 메소드 | 설명 |
|------------|--------|------|
| `/users/create` | POST | 새로운 사용자 생성 |
| `/users/all` | GET | 모든 사용자 정보 조회 |
| `/users/{username}` | DELETE | 사용자 삭제 |
| `/users/limit/{username}` | POST | 사용자 사용량 제한 설정 |

### 모델 API
| 엔드포인트 | 메소드 | 설명 | 권한 |
|------------|--------|------|------|
| `/models/create` | POST | 새로운 모델 생성 | 관리자 |
| `/models/all` | GET | 사용 가능한 모델 목록 조회 | 모든 사용자 |
| `/models/{model_name}` | DELETE | 모델 삭제 | 관리자 |


### 모델 호출
| 엔드포인트 | 메소드 | 설명 | 요청 데이터 |
|------------|--------|------|------------|
| `/api/call` | POST | AI 모델 호출 | model_name, prompt, max_tokens (선택), temperature (선택) |


## 지원하는 AI 모델

### Azure OpenAI
- 필요한 설정:
  - deployment_name
  - end_point
  - api_key
<!--
### OpenAI
- 필요한 설정:
  - api_key

### GCP Gemini (Vertex AI)
- 필요한 설정:
  - GCP Service Account

### Gemini - Google AI Studio
- 필요한 설정:
  - api_key

### Anthropic
- 필요한 설정:
  - api_key -->
