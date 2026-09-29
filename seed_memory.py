import json
import os
from hindsight_client import Hindsight

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key="hsk_a67d227988c39c1043cbd0694872e5a9_f5734918f44be073"
)

agent_bank_id = "social-media-agent-memory"

# Explicit A/B Test Failure & Success Records
ab_test_records = [
    {
        "post_id": "ab_test_failure_01",
        "topic": "Vector Databases Deep Dive",
        "format": "long-form deep-dive essay",
        "engagement_metrics": {"likes": 42, "shares": 6},
        "community_sentiment": "low engagement / dropped retention",
        "ab_test_result": "FAILURE: Long-form deep-dive on vector databases last month received 40% less engagement than short-form technical teasers."
    },
    {
        "post_id": "ab_test_success_01",
        "topic": "Vector Databases & AI Memory Teaser",
        "format": "concise bulleted list",
        "engagement_metrics": {"likes": 410, "shares": 118},
        "community_sentiment": "highly positive",
        "ab_test_result": "SUCCESS: Concise bulleted lists published on Tuesday mornings consistently outperform long-form deep dives by +40% engagement."
    },
    {
        "post_id": "community_comment_01",
        "topic": "DATA//ESCAPE Cipher Challenge",
        "user_comment": "Are there any hint drops for the cipher challenge?",
        "user_handle": "@alex_coder",
        "upvotes": 48,
        "community_sentiment": "High community anticipation for hint drops and clues."
    }
]

with open('social_media_history.json', 'r') as file:
    data = json.load(file)

historical_posts = data if isinstance(data, list) else next(iter(data.values()))

print(f"Loaded {len(historical_posts)} posts + {len(ab_test_records)} A/B test records. Ingesting into Hindsight...")

# Ingest A/B test failure records first
for ab_record in ab_test_records:
    client.retain(
        bank_id=agent_bank_id,
        content=f"A/B Test Memory Benchmark: {json.dumps(ab_record)}"
    )
    print(f"Retained A/B benchmark: {ab_record.get('post_id')}")

for post in historical_posts:
    post_content = f"Post Record: {json.dumps(post)}"
    client.retain(
        bank_id=agent_bank_id,
        content=post_content
    )
    print(f"Retained memory for post: {post.get('post_id')}")

client.close()
print("Memory seeding complete. A/B test benchmarks and community comments memorized.")