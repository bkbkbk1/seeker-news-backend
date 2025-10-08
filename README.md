# Seeker News Backend

Solana Seeker 프로젝트 소식을 자동으로 수집하고 분석하는 백엔드

## 모니터링 계정
- @solanamobile
- @aeyakovenko
- @solana_devs

## 설정 방법
1. GitHub Secrets에 API 키 등록
   - `TWITTER_BEARER_TOKEN`: X API Bearer Token
   - `OPENAI_API_KEY`: OpenAI API Key

2. GitHub Actions가 1시간마다 자동 실행

## 결과 확인
- `data/projects.json` 파일에 분석 결과 저장
