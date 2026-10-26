"""
API Providers Module

Handles communication with different AI providers (OpenRouter, Cerebras, Gemini)
with automatic fallback mechanism.
"""

import os
import json
import requests
from typing import List, Dict, Optional
from abc import ABC, abstractmethod


class APIProvider(ABC):
    """Abstract base class for API providers"""
    
    @abstractmethod
    def call_api(self, messages: List[Dict], temperature: float = 0.3) -> Optional[str]:
        """Call the API and return the response content"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the API provider is available"""
        pass


class OpenRouterProvider(APIProvider):
    """OpenRouter API provider"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "qwen/qwen3-coder:free"
        
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def call_api(self, messages: List[Dict], temperature: float = 0.3) -> Optional[str]:
        if not self.is_available():
            return None
            
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 2000
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://resume-tailor-app.com",
            "X-Title": "Resume Tailor"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            return None


class CerebrasProvider(APIProvider):
    """Cerebras API provider"""
    
    def __init__(self):
        self.api_key = os.getenv('CEREBRAS_API_KEY')
        self.model = "qwen-3-coder-480b"
        
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def call_api(self, messages: List[Dict], temperature: float = 0.3) -> Optional[str]:
        if not self.is_available():
            return None
            
        try:
            from cerebras.cloud.sdk import Cerebras
            
            client = Cerebras(api_key=self.api_key)
            
            # Convert messages to the format expected by Cerebras
            cerebras_messages = []
            for msg in messages:
                if msg['role'] == 'user':
                    cerebras_messages.append({
                        "role": "user",
                        "content": msg['content']
                    })
                elif msg['role'] == 'assistant':
                    cerebras_messages.append({
                        "role": "assistant", 
                        "content": msg['content']
                    })
            
            response = client.chat.completions.create(
                messages=cerebras_messages,
                model=self.model,
                stream=False,
                max_completion_tokens=2000,
                temperature=temperature,
                top_p=0.8
            )
            
            return response.choices[0].message.content
            
        except ImportError:
            print("Cerebras SDK not installed. Install with: pip install cerebras-cloud-sdk")
            return None
        except Exception as e:
            print(f"Error calling Cerebras API: {e}")
            return None


class GeminiProvider(APIProvider):
    """Gemini API provider"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.model = "gemini-2.0-flash-exp"
        
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def call_api(self, messages: List[Dict], temperature: float = 0.3) -> Optional[str]:
        if not self.is_available():
            return None
            
        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            if msg['role'] == 'user':
                gemini_messages.append({
                    "role": "user",
                    "parts": [{"text": msg['content']}]
                })
            elif msg['role'] == 'assistant':
                gemini_messages.append({
                    "role": "model",
                    "parts": [{"text": msg['content']}]
                })
        
        data = {
            "contents": gemini_messages,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 2000
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(
                f"{self.base_url}/{self.model}:generateContent?key={self.api_key}",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return None


class APIManager:
    """Manages multiple API providers with fallback logic"""
    
    def __init__(self):
        self.providers = [
            OpenRouterProvider(),
            CerebrasProvider(),
            GeminiProvider()
        ]
    
    def call_with_fallback(self, messages: List[Dict], temperature: float = 0.3) -> Optional[str]:
        """Call API with fallback to different providers"""
        
        for provider in self.providers:
            if provider.is_available():
                try:
                    result = provider.call_api(messages, temperature)
                    if result:
                        return result
                except Exception as e:
                    print(f"{provider.__class__.__name__} failed: {e}")
                    continue
        
        # All APIs failed
        print("All API providers failed. You may have exceeded daily request limits.")
        return None
    
    def has_any_provider(self) -> bool:
        """Check if any API provider is available"""
        return any(provider.is_available() for provider in self.providers) 