import openai
import google.generativeai as genai
import anthropic
import pyttsx3  # For voice synthesis
import re  # For citation formatting

# CelestiCode: Modular AI Writing Bot
class CelestiCode:
    def __init__(self, openai_api_key, gemini_api_key, claude_api_key):
        self.openai_api_key = openai_api_key
        self.gemini_api_key = gemini_api_key
        self.claude_api_key = claude_api_key
        
        openai.api_key = self.openai_api_key
        genai.configure(api_key=self.gemini_api_key)
        self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)
        
        self.voice_engine = pyttsx3.init()
        self.voice_engine.setProperty('rate', 150)
        self.voice_engine.setProperty('volume', 1.0)
    
    def generate_paper(self, prompt, model="openai", length=1000, style="academic"):
        if model == "openai":
            return self._openai_generate(prompt, length, style)
        elif model == "gemini":
            return self._gemini_generate(prompt, length, style)
        elif model == "claude":
            return self._claude_generate(prompt, length, style)
        else:
            return "Invalid model selection. Choose from: openai, gemini, claude."

    def _openai_generate(self, prompt, length, style):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": f"You are CelestiCode, a highly sophisticated AI writing bot specializing in {style} writing."},
                      {"role": "user", "content": prompt}],
            max_tokens=length
        )
        return response["choices"][0]["message"]["content"].strip()

    def _gemini_generate(self, prompt, length, style):
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Write in a {style} style. {prompt}")
        return response.text

    def _claude_generate(self, prompt, length, style):
        response = self.claude_client.completions.create(
            model="claude-3-opus-2024-02-29",
            max_tokens=length,
            messages=[{"role": "user", "content": f"Write in a {style} style. {prompt}"}]
        )
        return response.completion.strip()
    
    def format_paper(self, content):
        return f"\033[94m{content}\033[0m"  # Adds blue coloring for a holographic feel
    
    def speak(self, text):
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()
    
    def add_citations(self, content):
        citations = re.findall(r'\[(.*?)\]', content)
        if citations:
            content += "\n\nReferences:\n"
            for index, citation in enumerate(citations, start=1):
                content += f"[{index}] {citation}\n"
        return content
    
    def guide_prompt(self, topic):
        return f"To write an effective paper on {topic}, consider including background, analysis, and a conclusion."

# Example Usage
if __name__ == "__main__":
    openai_key = "your-openai-key"
    gemini_key = "your-gemini-key"
    claude_key = "your-claude-key"
    
    celesti = CelestiCode(openai_key, gemini_key, claude_key)
    prompt = "Write a college-level essay on the impact of AI in education."
    paper = celesti.generate_paper(prompt, model="openai")
    paper = celesti.add_citations(paper)
    print(celesti.format_paper(paper))
    celesti.speak("Here is your generated paper.")