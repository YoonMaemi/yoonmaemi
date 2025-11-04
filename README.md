# 세 줄 요약 데모 애플리케이션

사용자로부터 입력받은 문장을 Google Gemini 2.0 Flash 모델을 사용해 **세 줄로 요약**해 주는 풀스택 데모 MVP입니다.  
FastAPI 기반의 백엔드와 React(Vite) 기반의 프런트엔드로 구성되어 있으며, 모든 데이터는 인메모리로 관리됩니다.

## 프로젝트 개요
- **백엔드**: Python, FastAPI, Google Gemini API 호출
- **프런트엔드**: React + TypeScript (Vite)
- **저장소**: 인메모리 단일 채팅 히스토리 (앱 종료 시 초기화)

## 사전 준비물
1. [Python 3.10 이상](https://www.python.org/downloads/)  
2. [Node.js 18 이상](https://nodejs.org/en/download/) (npm 포함)  
3. Google Gemini API 키  
   - [Google AI Studio](https://aistudio.google.com/app/apikey)에서 발급  
   - 무료 모델: `gemini-2.0-flash`

## 빠른 시작

### 1. 백엔드 실행
1. 프로젝트 루트(현재 디렉터리)에서 `.env.example`을 복사해 `.env` 파일을 만들고 `GEMINI_API_KEY` 값을 입력하세요.  
   - Windows (PowerShell): `Copy-Item .env.example .env`  
   - macOS/Linux: `cp .env.example .env`
2. 다음 명령으로 FastAPI 서버를 실행합니다.

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. 프런트엔드 실행
별도의 터미널에서 다음 명령을 실행하세요.

```bash
cd frontend
npm install
npm run dev
```

Vite 개발 서버가 `http://localhost:5173`에서 실행되며, 브라우저가 자동으로 열립니다.  
첫 메시지를 입력하면 FastAPI 서버가 Gemini API를 호출해 세 줄 요약을 반환합니다.

## 폴더 구조
```
demopy/
├── backend/                # FastAPI 애플리케이션
│   ├── app/
│   │   ├── chat_state.py   # 인메모리 채팅 히스토리 관리
│   │   ├── config.py       # 환경 변수 로딩 및 검증
│   │   ├── gemini_client.py# Gemini API 래퍼
│   │   ├── main.py         # FastAPI 엔트리포인트
│   │   └── models.py       # Pydantic 데이터 모델
│   └── requirements.txt
├── frontend/               # React + Vite SPA
│   ├── src/
│   │   ├── api.ts          # 백엔드 호출 유틸리티
│   │   ├── App.tsx         # 메인 화면
│   │   ├── App.css, index.css
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig*.json
│   └── vite.config.ts
├── .env.example            # 환경 변수 템플릿
└── README.md               # 현재 문서
```

## 환경 변수 & 설정
- `.env` 파일은 프로젝트 루트에 위치하며, 서버 시작 시 자동으로 로드됩니다.
- `GEMINI_API_KEY`: Google Gemini 호출에 필요한 API 키 (**필수**)
- `GEMINI_MODEL` (선택): 기본값은 `gemini-2.0-flash`
- 프런트엔드에서 다른 백엔드 주소를 사용하려면 `frontend/.env` 파일을 만들고 `VITE_API_BASE_URL`을 설정하세요.

```bash
# frontend/.env
VITE_API_BASE_URL=http://localhost:8000
```

## API 엔드포인트
| 메서드 | 경로           | 설명                         |
| ------ | -------------- | ---------------------------- |
| GET    | `/healthz`     | 애플리케이션 상태 확인       |
| GET    | `/api/history` | 현재 인메모리 채팅 히스토리 |
| POST   | `/api/chat`    | 요약 요청 (본문: `{message}`)|

`POST /api/chat` 호출 흐름:
1. 사용자의 입력 문장을 히스토리에 추가
2. Gemini 2.0 Flash 모델에게 세 줄 요약 요청
3. 응답을 히스토리에 저장하고 클라이언트로 반환

## 개발/디버깅 팁
- 백엔드 서버 실행 전에 `.env`의 `GEMINI_API_KEY`가 설정되어 있는지 확인하세요. 설정되지 않으면 서버 시작 시 오류가 발생합니다.
- 프런트엔드 개발 서버는 기본적으로 백엔드 `http://localhost:8000`을 사용합니다. 포트를 바꾸면 `VITE_API_BASE_URL`도 함께 변경해야 합니다.
- 인메모리 저장 방식이므로 서버 또는 프런트엔드를 재시작하면 히스토리가 초기화됩니다.

## 다음 단계 아이디어
1. 에러 로그 파일 저장 및 사용자 피드백 향상
2. 멀티 채팅룸 지원 및 영구 저장소 연동
3. 인증/인가 및 요금제별 모델 선택 옵션 추가

행복한 코딩 되세요! 🙌

