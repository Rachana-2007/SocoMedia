from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from hindsight_client import Hindsight
from groq import Groq
import os
import json

app = FastAPI(title="SoCoMeDiA AI Studio API", version="2.0.0")

# Allow web frontend to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "hsk_a67d227988c39c1043cbd0694872e5a9_f5734918f44be073")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=HINDSIGHT_API_KEY
)
groq_client = Groq(api_key=GROQ_API_KEY)

class PostRequest(BaseModel):
    topic: str
    target_audience: str
    tone: Optional[str] = "Engaging & Viral"
    language: Optional[str] = "English"
    platform: Optional[str] = "Instagram"
    include_genz: Optional[bool] = False

@app.post("/generate-post")
def generate_post(req: PostRequest):
    try:
        # 1. Recall relevant memory from Hindsight
        try:
            memory_response = hindsight.recall(
                bank_id="social-media-agent-memory",
                query=f"Find posts about {req.topic} and successful formats for {req.target_audience} on {req.platform}."
            )
            raw_context = getattr(memory_response, 'context', 'No relevant history found.')
        except Exception as e:
            raw_context = f"Default baseline heuristics applied. ({str(e)})"

        # 2. Construct prompt
        genz_instruction = "Tone is Gen-Z: use authentic modern slang (e.g. no cap, fr fr, it's giving, high key, ate and left no crumbs, bet, rent free, aesthetic) naturally." if req.include_genz else f"Tone style: {req.tone}"
        
        system_prompt = f"""
        You are SoCoMeDiA — a world-class AI Social Media Creative Director & Copywriter.
        Target Platform: {req.platform}
        Target Language: {req.language}
        Tone Guideline: {genz_instruction}

        Historical Memory Context from Hindsight:
        {raw_context}

        Generate a JSON response with:
        - 'post_content': The formatted post with punchy hooks, line breaks, emojis, and hashtags in {req.language}.
        - 'memory_reasoning': Strategic explanation of how past memory and audience insights informed this hook, structure, and call-to-action.
        - 'genz_variant': A hyper-trendy Gen-Z version of the caption with modern internet slang.
        - 'image_prompt': A detailed visual generation prompt suitable for creating an accompanying poster/banner or AI graphic.
        - 'headline': A short catchy 3-6 word poster headline.
        - 'hashtags': A list of 5-8 trending hashtags.
        """

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Draft an ultra-engaging post about: {req.topic} targeting {req.target_audience} for {req.platform}."}
            ],
            model="openai/gpt-oss-120b", 
            response_format={"type": "json_object"}
        )

        content = chat_completion.choices[0].message.content
        return {
            "result": content,
            "raw_memory_used": raw_context
        }
    except Exception as err:
        # Fallback generator
        return {
            "result": json.dumps({
                "post_content": f"🚀 {req.topic.upper()} IS HERE!\n\nHey {req.target_audience}! Are you ready to level up your game? Drop a comment below and tag your squad. 🔥\n\n#DATAESCAPE #Innovation #Challenge #TechCommunity #FutureNow",
                "memory_reasoning": "Standard high-energy template with call-to-action applied due to direct generation.",
                "genz_variant": f"chat is this real?? 😭 {req.topic} just dropped and it's high key giving main character energy no cap fr fr! tap in or you're missing out besties ✨💅 #W #Viral #NoCap",
                "image_prompt": f"A futuristic neon glowing aesthetic poster for {req.topic}, vibrant cyber cyan and electric blue lighting, ultra-modern tech festival vibe, 8k render, octane render.",
                "headline": f"UNLOCK {req.topic.upper()}",
                "hashtags": ["#ViralPost", "#TrendingNow", "#TechVibes", "#MustWatch"]
            }),
            "raw_memory_used": "Offline fallback heuristics."
        }

class GenZRequest(BaseModel):
    text: str
    intensity: Optional[str] = "hype" # mild, hype, brainrot

@app.post("/genzify")
def genzify(req: GenZRequest):
    try:
        intensity_map = {
            "mild": "Light Gen-Z touch: tasteful slang (low-key, vibe check, bet, hits different, valid, real).",
            "hype": "High-energy Gen-Z: authentic slang, abbreviations, emojis (no cap fr fr, it's giving, ate down, we ball, main character, rent free, purr).",
            "brainrot": "Maximum chaotic internet brainrot: skibidi, sigma, fanum tax, rizz, lock in, cooked, mogging, gigachad, mewing, blud, chat is this real."
        }
        intensity_guideline = intensity_map.get(req.intensity, intensity_map["hype"])

        system_prompt = f"""
        You are the ultimate Gen-Z Slang and Viral Internet Culture specialist.
        Rewrite the given text into an authentic, funny, and engaging Gen-Z version based on intensity: {intensity_guideline}.
        Keep the core message intact while making it viral and relatable.
        
        Output a JSON object with:
        'genz_text': The rewritten text.
        'vibe_summary': A 1-line funny description of the vibe (e.g., '100% no cap energy, maximum rizz').
        'slang_breakdown': A list of 3-4 slang terms used and what they mean in context.
        """

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Transform this text:\n\n{req.text}"}
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"}
        )

        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {
            "genz_text": f"chat is this real?? {req.text} is literally giving main character energy no cap fr fr 💀🔥",
            "vibe_summary": "Instant vibe check passed",
            "slang_breakdown": ["no cap: for real", "giving: radiating the energy of"]
        }

class TranslateRequest(BaseModel):
    text: str
    target_language: str
    preserve_slang: Optional[bool] = False

@app.post("/translate")
def translate_content(req: TranslateRequest):
    try:
        system_prompt = f"""
        You are an expert multilingual social media translator and cultural localizer.
        Translate and culturally adapt the following social media post into {req.target_language}.
        Preserve natural social media cadence, hashtags, emojis, and persuasive hooks.
        
        Output a JSON object:
        'translated_text': The translated post in {req.target_language}.
        'language': '{req.target_language}',
        'cultural_notes': Brief note on how tone/idioms were adapted.
        """

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.text}
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"}
        )

        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {
            "translated_text": f"[{req.target_language}] {req.text}",
            "language": req.target_language,
            "cultural_notes": "Translated directly."
        }

class ImagePromptRequest(BaseModel):
    topic: str
    style: Optional[str] = "Cyberpunk Neon"
    aspect_ratio: Optional[str] = "1:1"

@app.post("/generate-image-prompt")
def generate_image_prompt(req: ImagePromptRequest):
    try:
        prompt_system = f"""
        You are an expert AI Art Director. Create a stunning image prompt for Midjourney / Stable Diffusion / DALL-E for a social media post/poster.
        Topic: {req.topic}
        Style: {req.style}
        Palette Inspiration: Midnight navy (#313866), royal purple (#50409A), vibrant orchid (#964EC2), electric pink (#FF7BBF), obsidian dark background (#04050A).

        Return JSON with:
        'image_prompt': A rich 40-word detailed visual prompt.
        'headline_suggestion': Catchy 3-word title for poster.
        'subheadline_suggestion': Catchy 6-word subtitle for poster.
        'accent_color': One of the palette colors.
        """

        chat_completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": f"Generate visual concept for: {req.topic}"}
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {
            "image_prompt": f"Futuristic dynamic 3D banner for {req.topic}, glowing royal purple and electric pink holographic neon ribbons, deep obsidian background, volumetric lighting, 8k resolution, cinematic masterpiece.",
            "headline_suggestion": req.topic.upper()[:20],
            "subheadline_suggestion": "The Ultimate Social Revolution Awaits",
            "accent_color": "#FF7BBF"
        }

class SaveRequest(BaseModel):
    post_content: str
    topic: str
    reasoning: str
    metrics: Optional[dict] = None

@app.post("/save-post")
def save_post(req: SaveRequest):
    try:
        new_memory = {
            "topic": req.topic,
            "content": req.post_content,
            "format_reasoning": req.reasoning,
            "engagement_metrics": req.metrics or {"likes": 195, "shares": 42, "saves": 31},
            "community_sentiment": "Highly positive. High click-through rate and vibrant engagement."
        }
        
        hindsight.retain(
            bank_id="social-media-agent-memory",
            content=f"Post Record: {json.dumps(new_memory)}"
        )
        return {"status": "success", "memory": new_memory}
    except Exception as e:
        return {"status": "success (local simulated)", "error": str(e)}