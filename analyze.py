"""Analyze tweets and generate project summaries using OpenAI"""
import os
import json
from datetime import datetime
from openai import OpenAI

def analyze_tweets(tweets):
    """Analyze tweets and generate summaries"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set")
        return []

    client = OpenAI(api_key=api_key)
    projects = []

    for tweet in tweets:
        try:
            # Generate summary for each tweet
            prompt = f"""다음 트윗을 분석해서 Seeker/Solana Mobile 관련 프로젝트나 소식을 한국어로 소개해주세요.

트윗 내용: {tweet['text']}
작성자: @{tweet['username']}

다음 형식으로 답변해주세요:
제목: [프로젝트/소식 제목]
설명: [2-3문장으로 핵심 내용 요약]
카테고리: [DeFi/NFT/게임/인프라/기타 중 하나]

만약 Seeker/Solana Mobile과 직접 관련이 없다면 "관련없음"이라고만 답변하세요."""

            response = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "system", "content": "당신은 Solana 생태계 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            summary = response.choices[0].message.content.strip()

            if "관련없음" not in summary:
                # Parse the response
                lines = summary.split('\n')
                title = ""
                description = ""
                category = "기타"

                for line in lines:
                    if line.startswith("제목:"):
                        title = line.replace("제목:", "").strip()
                    elif line.startswith("설명:"):
                        description = line.replace("설명:", "").strip()
                    elif line.startswith("카테고리:"):
                        category = line.replace("카테고리:", "").strip()

                if title and description:
                    projects.append({
                        "id": tweet["tweet_id"],
                        "title": title,
                        "description": description,
                        "category": category,
                        "source_tweet": tweet["url"],
                        "source_username": tweet["username"],
                        "created_at": tweet["created_at"],
                        "engagement": {
                            "likes": tweet["likes"],
                            "retweets": tweet["retweets"]
                        },
                        "analyzed_at": datetime.now().isoformat()
                    })

        except Exception as e:
            print(f"Error analyzing tweet {tweet['tweet_id']}: {e}")

    return projects

if __name__ == "__main__":
    # Load raw tweets
    with open("data/raw_tweets.json", "r", encoding="utf-8") as f:
        tweets = json.load(f)

    print(f"Analyzing {len(tweets)} tweets...")
    projects = analyze_tweets(tweets)

    print(f"Generated {len(projects)} project summaries")

    # Save to JSON
    with open("data/projects.json", "w", encoding="utf-8") as f:
        json.dump({
            "updated_at": datetime.now().isoformat(),
            "total_projects": len(projects),
            "projects": projects
        }, f, indent=2, ensure_ascii=False)

    print("Saved to data/projects.json")

