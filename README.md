# 🤖 AI 스케줄 어시스턴트

OpenAI API와 Google Calendar를 연동한 지능형 스케줄 관리 시스템입니다. AI가 사용자의 일정을 분석하고 최적의 시간을 추천해줍니다.

## ✨ 주요 기능

- 📅 **Google Calendar 연동**: 실제 캘린더 데이터 또는 가상 데이터 사용
- 🧠 **AI 기반 분석**: OpenAI GPT를 활용한 지능형 스케줄 분석
- ⏰ **최적 시간 추천**: 요청 유형별 맞춤형 시간 추천
- 📊 **시각화**: 사용 가능한 시간대를 차트로 표시
- 🎯 **스마트 분석**: 시간대, 요일, 패턴을 고려한 점수 기반 추천

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd ai-schedule-assistant
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
cp .env.example .env
```

`.env` 파일을 편집하여 다음 정보를 입력하세요:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json
CALENDAR_ID=your_email@gmail.com
```

### 5. Google Calendar API 설정 (선택사항)

실제 Google Calendar를 사용하려면:

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트 생성
2. Calendar API 활성화
3. OAuth 2.0 클라이언트 ID 생성
4. `credentials.json` 파일 다운로드하여 프로젝트 루트에 저장

### 6. 애플리케이션 실행
```bash
streamlit run app.py
```

## 🎮 사용 방법

### 데모 모드 (권장)
1. 애플리케이션 실행 후 "데모 모드" 체크박스 선택
2. 가상의 캘린더 데이터로 시스템 테스트

### 실제 API 사용
1. OpenAI API 키 입력
2. Google Calendar API 설정 (선택사항)
3. 스케줄 요청 입력 및 분석

## 📝 사용 예시

### 입력 예시
```
병원 예약 2시간 소요
고객 미팅 1시간
헬스장 운동 1.5시간
치과 예약 1시간
```

### AI 분석 결과
- 요청 유형 분류 (의료, 업무, 운동 등)
- 최적 시간대 추천 (상위 3개)
- 시간대별 적합도 점수
- 일반적인 조언 및 주의사항

## 🏗️ 프로젝트 구조

```
ai-schedule-assistant/
├── app.py                 # Streamlit 메인 애플리케이션
├── ai_agent.py           # OpenAI API 연동 AI 에이전트
├── calendar_manager.py   # Google Calendar 연동 관리자
├── config.py             # 설정 파일
├── requirements.txt      # Python 의존성
├── .env.example         # 환경 변수 예시
└── README.md            # 프로젝트 문서
```

## 🔧 주요 컴포넌트

### CalendarManager
- Google Calendar API 연동
- 가상 캘린더 데이터 생성
- 사용 가능한 시간대 계산

### ScheduleAIAgent
- OpenAI GPT API 연동
- 스케줄 요청 분석
- 지능형 시간 추천

### Streamlit UI
- 사용자 친화적 웹 인터페이스
- 실시간 차트 및 시각화
- 반응형 디자인

## 🎯 AI 분석 기능

### 요청 유형 분류
- **의료**: 병원, 의사, 검진, 치과
- **업무**: 미팅, 회의, 프레젠테이션
- **운동**: 헬스, 요가, 피트니스
- **사회**: 식사, 점심, 저녁, 카페
- **쇼핑**: 쇼핑, 구매, 마트

### 시간대별 점수 계산
- 요청 유형별 최적 시간대
- 요일별 가중치
- 시간 길이 고려
- 개인 패턴 분석

## 📊 시각화 기능

- 사용 가능한 시간대 막대 차트
- 시간대별 적합도 점수 차트
- 일정 요약 테이블
- 실시간 메트릭 표시

## ⚠️ 주의사항

1. **API 키 보안**: OpenAI API 키를 안전하게 관리하세요
2. **Google Calendar 권한**: 필요한 최소 권한만 요청합니다
3. **데모 모드**: API 키 없이도 가상 데이터로 테스트 가능
4. **시간대**: 기본적으로 한국 시간대(Asia/Seoul) 사용

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해주세요.

---

**Made with ❤️ by AI Assistant**
