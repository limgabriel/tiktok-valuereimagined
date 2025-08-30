
# BrightShare — Fair, Transparent, and Inclusive Rewards for TikTok Creators

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi"/>
  <img src="https://img.shields.io/badge/React-19-61dafb?logo=react"/>
  <img src="https://img.shields.io/badge/TypeScript-Frontend-blue?logo=typescript"/>
  <img src="https://img.shields.io/badge/Node.js-18+-green?logo=node.js"/>
  <img src="https://img.shields.io/badge/Vite-Bundler-646cff?logo=vite"/>
  <img src="https://img.shields.io/badge/Playwright-Scraping-orange?logo=microsoft"/>
  <img src="https://img.shields.io/badge/HuggingFace-Sentiment-yellow?logo=huggingface"/>
  <img src="https://img.shields.io/badge/Google-Perspective-4285F4?logo=google"/>
  <img src="https://img.shields.io/badge/Reality_Defender-AIGC_Detection-red"/>
</p>



## Table of Contents  
1. [Overview](#overview)  
2. [Problem Statement](#problem-statement)  
3. [Features](#features)  
4. [Reward System](#reward-system)  
5. [Tech Stack](#tech-stack)  
6. [Live Deployment](#live-deployment)
7. [Setup & Local Installation](#setup--installation)  
8. [Usage](#usage)  
9.  [Demo](#demo)  
10. [Screenshots](#screenshots)  
11. [License](#license)  


## Overview  

BrightShare is a reward distribution system that **fairly allocates revenue to TikTok creators** based on:  
- Engagement metrics  
- Sentiment in comment sections  
- Detection of AI-generated content  
- Inclusivity factors  

By combining these into a **normalized reward score**, BrightShare:  
- Ensures fair and transparent payouts  
- Discourages low-quality or fraudulent content  
- Promotes inclusivity and ecosystem health

Creators also gain access to a **dashboard** showing reward calculations, engagement breakdowns, and sentiment analysis for full transparency.  



## Problem Statement  

While TikTok monetization exists, current mechanisms suffer from:  
- **Inconsistent/opaque rewards** → many creators underpaid  
- **System gaming & fraud** → inflated metrics, AIGC spam  
- **Toxic/low-quality content incentives** → hurts community trust  

BrightShare addresses these by **rewarding quality, authenticity, and inclusivity**.  



## Features  

- **Base Value Analysis** → Compute core revenue from TikTok (ads, gifts, EVI)  
- **Sentiment Analysis** → Assess positivity & toxicity in comments  
- **Comment Section Regulation** → Incentivize creators to maintain healthy, safe comment spaces  
- **AIGC Detection** → Penalize suspected AI-generated content  
- **Inclusivity Analysis** → Uplift small/underrepresented creators  
- **Reward Allocation** → Transparent score-based payouts  
- **Creator Dashboard** → Track engagement, scores, and payouts  


## Reward System  

The final reward for a TikTok creator is calculated as:

$$
\text{Reward} = R_{base} \times M_{quality} \times M_{integrity} \times I_{index}
$$  

Each component is described below.

---

### 1. Base Revenue ($R_{base}$)  

$$
R_{base} = \text{Ad Revenue} + \text{Gift Revenue} + \text{EVI}
$$  

where Engagement Value Index (EVI) is:

$$
EVI = 0.1 \cdot \frac{Likes}{Views} 
+ 0.4 \cdot \frac{Shares}{Views} 
+ 0.3 \cdot \frac{Comments}{Views} 
+ 0.2 \cdot \frac{Reposts}{Views}
$$  

- **Purpose:** Capture the core monetization of a video, including ads, gifts, and engagement quality.  
- **Adjustable weights:** Can be tuned to reflect platform priorities.

---

### 2. Community Quality Multiplier ($M_{quality}$)  

$$
M_{quality} = 0.5 \cdot (\text{Positivity Rate}) + 0.5 \cdot (1 - \text{Toxicity Rate})
$$  

- **Positivity** via Hugging Face RoBERTa Twitter model  
- **Toxicity** via Google Perspective API  

#### 🛡️ Comment Section Regulation  

BrightShare enforces creator accountability for their audience:  

1. **Weighted Influence on Rewards**  
   - Positive, low-toxicity comment sections **boost $M_{quality}$**, increasing payouts.  
   - Toxic comment sections **reduce $M_{quality}$**, even with high engagement.  

2. **Creator Responsibility**  
   - Encourages creators to **moderate and foster respectful discussions**.  

3. **Dynamic Penalties & Bonuses**  
   - Extremely toxic comment sections → significant reward reduction.  
   - Exceptionally positive comment sections → bonus multiplier.  

This ties **community health directly to income**, incentivizing better moderation.

---

### 3. Integrity Multiplier ($M_{integrity}$)  

$$
M_{integrity} = 1 - 0.25 \cdot \min(1, P(\text{AIGC}))
$$  

- **Detection Model:** Reality Defender API  
- **Purpose:** Penalize suspected AI-generated content (up to 25%).  

#### 🤖 AIGC Regulation  

1. **Authenticity Check**  
   - Videos are scanned for AI generation probability (\(P(\text{AIGC})\)).  

2. **Reward Penalty Mechanism**  
   - Proportional penalty based on probability:  
     - \(P(\text{AIGC}) = 0.5 \Rightarrow M_{integrity} = 0.875\)  
     - \(P(\text{AIGC}) = 1 \Rightarrow M_{integrity} = 0.75\) (max penalty)  

3. **Balancing Creativity & Fairness**  
   - Minor AI assistance tolerated; full AI-generated content is penalized.  

4. **Transparency**  
   - Dashboard shows **AIGC risk and resulting multiplier**.  

Ensures **human creators are fairly rewarded** while discouraging content farms.

---

### 4. Inclusivity Index ($I_{index}$)  

$$
I_{index} = 1 \times (1 + 0.1 \cdot \text{Small Creator}) \times (1 + 0.1 \cdot \text{Underrepresented Community})
$$  

- **Small Creator:** Follower count < `_SMALL_CREATOR_THRESHOLD` → +10%  
- **Underrepresented Community:** Creator from `_TARGET_COUNTRIES` → +10%  

#### 🌍 Promoting Inclusivity  

1. **Boosting Small Creators**  
   - Small creators receive a **10% reward boost**, leveling the playing field.  

2. **Supporting Underrepresented Communities**  
   - Creators from target countries also receive a **10% bonus**.  

3. **Multiplicative Bonuses**  
   - If a creator qualifies for both:  
     $$
     I_{index} = 1 \times 1.1 \times 1.1 = 1.21 \quad (\text{+21\% boost})
     $$  

4. **Dashboard Transparency**  
   - Creators can see exactly how **size and location affect rewards**.  

Encourages a **diverse, globally representative creator ecosystem**.

 

##  Tech Stack  

**Frontend**  
- React 19 + TypeScript (Vite)  
- ESLint  
- CSS  

**Backend**  
- FastAPI (Python 3.10+)  
- Pydantic  
- TikTokApi + Apify (scraping metadata & comments)  
- Hugging Face API (sentiment)  
- Google Perspective API (toxicity)  
- Reality Defender (deepfake/AIGC detection)  

**Tooling**  
- Node.js 18+ / npm  
- dotenv (env management)  
- Playwright (web scraping)  


## Project Directory Skeleton  

```bash
tiktok-valuereimagined/
│── backend/
│   ├── app/
│   │   ├── analysis.py
│   │   ├── main.py
│   │   ├── nlp_sentiment.py
│   │   ├── requirements.txt
│   │   ├── schemas.py
│   ├── download_model.py
│   └── railway.json
│
│── frontend-react/
│   ├── public/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
│── .env
│── .gitignore
│── README.md
````
## Live Deployment

The BrightShare frontend is now **hosted on Railway** and accessible to anyone without local setup.  

🌐 **Access the live app here:** [BrightShare on Railway](https://front-end-production-af24.up.railway.app/)

- Fully functional **dashboard** and reward computation  
- Supports **real-time engagement, sentiment, AIGC analysis**, and inclusivity scoring  
- Ideal for quick demos or testing without local installation  

> ⚠️ Backend API calls still rely on your configured environment variables if using a local or custom backend.  

## Setup & Installation (Local Installation)

### Prerequisites

* Python 3.10.6
* Node.js >= 18 (with npm)

### 1. Clone repository

```bash
git clone https://github.com/limgabriel/tiktok-valuereimagined
cd tiktok-valuereimagined
```

### 2. Backend setup

```bash
# Create and activate virtual environment
# macOS/Linux
python3.10.6 -m venv .venv
source .venv/bin/activate

# Windows
py -3.10.6 -m venv .venv
.venv\Scripts\activate      

# Install dependencies
pip install -r backend/app/requirements.txt

# Install Playwright for TikTok scraping
playwright install
```

Optionally, if you are running it on VSCode, you could follow the following shortcuts:
  1. Ctr + Shift + P
  2. Type Python: Create Environment
  3. Select Venv
  4. Choose Python 3.10.6
  5. Select to install via `requirements.txt`

### 3. Frontend setup

```bash
cd frontend-react
npm install
```

### 4. Run services

**Backend**

```bash
uvicorn backend.app.main:app --reload
```

**Frontend**

```bash
cd frontend-react
npm run dev
```

Open local browser → [http://localhost:5173/](http://localhost:5173/)

## Usage

You can use BrightShare in two ways:

1. **Live Deployment (Recommended for demos):**
   - Open [BrightShare on Railway](https://front-end-production-af24.up.railway.app/)
   - Paste a TikTok video link
   - Dashboard fetches engagement + comments
   - Sentiment & AIGC detection auto-run
   - Reward score is computed & displayed

2. **Local Installation (for development or testing):**
   - Follow the steps in **Setup & Installation**

## Demo

📺 [Live Demo](https://youtu.be/6_Y6nS7LfGc)

Highlights:

* Real-time scoring
* Reward allocation formulas explained
* Transparent breakdown per TikTok video


## Screenshots
![Landing Page](https://github.com/user-attachments/assets/b5aa3049-13da-425e-b483-d61c6f4e1be0)
*Figure 1: BrightShare Landing Page*

![Example of a Real TikTok Link](https://github.com/user-attachments/assets/89c42677-d2d3-4e58-9f8e-67f2a58da66e)
*Figure 2: Example of a Real TikTok Video URL Input*

![BrightShare's Analysis Page](https://github.com/user-attachments/assets/68b13bca-9e85-407e-93e8-d56778033be8)
*Figure 3: BrightShare Analysis & Reward Score Dashboard*

## License

This project is open-source under the **MIT License**.
