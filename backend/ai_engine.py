import openai
import json
import os
from typing import Dict, List

class AIEngine:
    def __init__(self):
        # Configure OpenRouter client
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY", "sk-or-v1-your-key-here"),
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = os.getenv("OPENROUTER_MODEL", "microsoft/phi-3-medium-128k-instruct:free")
        self.system_prompt = """You are a Viral Social Media Strategist. You analyse social media posts to maximise reach.

**Input:** The text content of a user's post.
**Task:** Analyse the core topics, tone, and industry.
**Output:** Return ONLY a JSON object with three arrays of hashtags:
1. 'safe': High-volume, broad tags (e.g., #Marketing, #Tech). Use these for baseline visibility.
2. 'rising': Trending, mid-volume tags relevant *right now* or to specific modern sub-cultures (e.g., #GenAI, #GrowthHacking).
3. 'niche': Specific, low-competition tags that target high-intent users (e.g., #SaaSMarketingTips).

**Rules:**
* Do not include the # symbol in the string, just the word.
* Ensure tags are CamelCase (e.g., 'DigitalMarketing', not 'digitalmarketing').
* Do not return any conversational text, only the JSON."""
    
    async def analyze_post(self, text_content: str) -> Dict[str, List[str]]:
        """Analyze post content and generate hashtags."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text_content}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                hashtags = json.loads(content)
                
                # Validate structure
                if not all(key in hashtags for key in ['safe', 'rising', 'niche']):
                    raise ValueError("Invalid hashtag structure")
                
                # Ensure all values are lists
                for key in hashtags:
                    if not isinstance(hashtags[key], list):
                        hashtags[key] = [hashtags[key]]
                
                return hashtags
                
            except json.JSONDecodeError:
                # Fallback: try to extract JSON from response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    hashtags = json.loads(json_match.group())
                    return hashtags
                else:
                    raise ValueError("Could not parse AI response")
            
        except Exception as e:
            print(f"Error analyzing post: {e}")
            # Check for rate limit error
            if "rate-limit" in str(e).lower() or "429" in str(e):
                print("Rate limit exceeded. Using fallback hashtags.")
            # Return default hashtags on error
            return {
                "safe": ["SocialMedia", "Marketing"],
                "rising": ["DigitalTrends"],
                "niche": ["ContentStrategy"]
            }
