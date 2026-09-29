import json
import os
from hindsight_client import Hindsight

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key="hsk_a67d227988c39c1043cbd0694872e5a9_f5734918f44be073"
)

agent_bank_id = "social-media-agent-memory"

with open('social_media_history.json', 'r') as file:
    data = json.load(file)

# Extract the array whether it is a direct list or wrapped in a dictionary
historical_posts = data if isinstance(data, list) else next(iter(data.values()))

print(f"Loaded {len(historical_posts)} posts. Beginning memory ingestion...")

for post in historical_posts:
    post_content = f"Post Record: {json.dumps(post)}"
    
    client.retain(
        bank_id=agent_bank_id,
        content=post_content
    )
    print(f"Retained memory for post: {post.get('post_id')}")

# Close the client to prevent aiohttp unclosed session warnings
client.close()
print("Memory seeding complete. The agent is ready to learn.")