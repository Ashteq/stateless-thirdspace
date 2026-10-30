Markdown
# ThirdSpace

**A Discord for real-life connection. An algorithmic wellbeing coach powered by Qloo.**

## The Problem: The Isolation Crisis
Big tech recommendation algorithms have optimized for endless scrolling, creating a paradox where society is more digitally connected, yet physically more isolated than ever before. We are trapped in algorithmic echo chambers that prioritize platform engagement over genuine human connection. 

## The Solution: Discord for Real Life
Just as Discord helps users find hyper-specific digital "servers" based on niche interests, Third Space helps users find their physical servers. We use cultural data to guide users to real-world hangout spots—cafes, lounges, or arcades—in their exact neighborhood where their type of people already congregate. We are transforming digital vibes into physical community gathering points.

## The Dual-Persona Architecture
To prove commercial viability, Third Space operates on a dual-persona LangChain architecture:

### 1. B2C: The Digital Off-Ramp
Instead of a sterile search bar, our B2C chat interface acts as an empathetic algorithmic wellbeing coach. The AI is explicitly programmed using the philosophical framework of a "Prudent Cooperator" (inspired by Löb's Theorem). It validates the user's media tastes and anticipates their mood, but it actively refuses to be an enabler of screen addiction. It gently and firmly nudges the user to log off and step outside into a physical Third Space where serendipity and offline connection thrive.

### 2. B2B: The Third-Space Architect
On the enterprise side, Third Space acts as a formal real estate consultant analyzing demographic viability for commercial developers and urban planners. With shifting urban populations and remote work, developers need to know exactly what kind of physical space a specific neighborhood's culture actually wants before they build it. The B2B persona ingests target demographic data, queries taste clusters, and cross-references them with local geography to identify lucrative "cultural gaps" in a neighborhood.

## Qloo Integration (The Taste & Locality Engine)
This application is built entirely upon Qloo's Cultural Graph API, acting as the intelligent bridge between digital culture and physical community.

- **Stateless Inference:** We map the culture, not the individual. The application operates entirely on stateless inference so zero Personally Identifiable Information (PII) is ever retained, ensuring complete user privacy.
- **Search & Translation:** We utilize Qloo's `/search` endpoint to accurately identify specific media entities mentioned by the user. 
- **Locality Mapping:** We then pass those entity IDs to the `/v2/insights` endpoint, explicitly filtering by `urn:entity:place` to translate digital media affinities into highly correlated physical locations.
- **Live Telemetry:** The UI features a persistent Developer Console that displays the live Qloo JSON payload, providing total transparency into the AI's data-backed reasoning.

## Local Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/stateless-thirdspace.git](https://github.com/your-username/stateless-thirdspace.git)
   cd stateless-thirdspace
Create and activate a virtual environment:

Bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory and add your API keys:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
QLOO_API_KEY=your_qloo_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
Run the application:

Bash
streamlit run app.py
