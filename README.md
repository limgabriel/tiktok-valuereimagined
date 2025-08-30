# BrightShare

A transparent and fair reward system for content creators.

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Problem Statement](#problem-statement)  
3. [Features](#features)  
4. [Technology Stack](#technology-stack)  
5. [APIs & Libraries](#apis--libraries)  
6. [Setup & Installation](#setup--installation)  
7. [Demo](#demo)  
8. [Screenshots](#screenshots)  
9. [Usage](#usage)  
10. [License](#license)  


## Project Overview  

BrightShare is a transparent reward system designed to fairly distribute revenue to content creators on TikTok. It evaluates content using engagement metrics, sentiment analysis, and AI-generated content detection, then calculates a normalized reward score that reflects quality, authenticity, and inclusivity. By providing creators with clear insights and a dashboard, BrightShare ensures fair compensation, discourages fraud, and promotes high-quality, community-friendly content.  


## Problem Statement  

TikTok allows creators worldwide to earn revenue through short videos and live streams. While higher-quality content generally earns higher rewards, the current reward mechanisms face several challenges:  
•	Unfair or inconsistent compensation, leaving some creators under-rewarded.
•	Vulnerability to manipulation, including fraudulent activity and system gaming.
•	Incentivization of low-quality or toxic content, reducing ecosystem health.  

These issues result in misaligned incentives, lower creator engagement, and reduced trust in the platform. There is therefore a need for a transparent, automated, and fair value-sharing system that accurately reflects content quality and creator contribution while ensuring compliance and ecosystem integrity.  


## Features
	•	Base Value Analysis: Computes base revenue from TikTok sources.
	•	Sentiment Analysis: Evaluates comment sections for positive and toxic sentiment.
	•	AIGC Analysis: Identifies AI generated content automatically.
	•	Underrepresentation Analysis: Classifies content creator based on popularity and communities.
	•	Reward Allocation: Distribute revenue proportionally based on normalized scores
	•	Creator Dashboard: Transparency on scores and engagement stats


## Reward System Calculations

Reward = R_base * M_quality * M_integrity * I_index

### 1. Base Revenue (R_base)

Calculating the current revenue of a video.  
Includes:

1. Advertising Revenue from Tiktok
2. Gifted Revenue from consumers
3. Engagement Value Index (EVI)

```
R_base = Ad Revenue from TikTok + Gifted (Stickers) + Engagement Value Index (EVI)

EVI = 0.1 * (Likes / Views)
    + 0.4 * (Shares / Views)
    + 0.3 * (Comments / Views)
    + 0.2 * (Reposts / Views)
```

(Adjust weights as desired)

### 2. Quality Multiplier (M_quality)  

```
M_quality = 0.5 * Positivity Rate + 0.5 * (1 - Toxicity Rate)
```  
•	Both rates use Wilson’s lower bound for confidence adjustment, preventing inflation from small sample sizes.
(Example: 8/10 vs 80/100 positivity rate.)
(Adjust weights as desired)

### 3. Integrity Multiplier (M_integrity)  
```
M_integrity = 1 - 0.25 * min(1, Probability of AIGC)
```  
•	Penalizes suspected AI-generated content (up to 25%).
(Adjust weights as desired)

### 4. Inclusivity Index (I_index)
```  
I_index = (1 + 0.1 * Indicator(Small Creator) + 0.1 * Indicator(Underrepresented Community))
```  
•	Small Creator: Followers < threshold.
•	Underrepresented Community: Creator from TikTok’s expansion communities.
(Adjust weights as desired)


## Technology Stack

**Frontend**
- React 19, TypeScript, Vite
- ESLint for linting
- CSS for styling

**Backend**
- FastAPI (Python)
- Pydantic for validation
- TikTokApi for TikTok metadata
- Apify for TikTok comment section
- Reality Defender for deepfake detection
- Huggingface model and Google Perspective API for sentiment analysis

**Tooling**
- Node.js, npm
- Python 3.10+
- ChatGPT 5
- dotenv for env management


## APIs & Libraries

### APIs
- TikTokApi
- Reality Defender API
- Google Perspective API
- Apify API
- Hugging Face API

### Frontend Libraries
- React 19, React DOM
- Vite
- TypeScript
- ESLint & plugins

### Backend Libraries
- FastAPI
- Pydantic
- TikTokApi
- Reality Defender SDK
- Playwright
- Requests
- dotenv


## Setup & Installation  

### Prerequisites  
- Python 3.10.6
- Node.js (>= 18)
- npm

### 1. Clone the repository
```
git clone https://github.com/limgabriel/tiktok-valuereimagined
```

### 2.	Navigate to the project folder:  
```
cd tiktok-valuereimagined  
```

### 3.	Install dependencies:  
**Backend**  
Create Environment by selecting requirements.txt when prompted to install dependencies.  

```
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```  

Navigate to root and then install playwright, this enables scraping of TikTok comments.   

```
playwright install
``` 

**Frontend**  
```
cd frontend-react
npm install
```  

### 4.	Running the App:  
**Frontend**  
Navigate to frontend-react folder  
```
npm run dev
```  
Open the app in your browser by clicking on the link displayed.  

**Backend**  
Navigate to project root  
```
uvicorn backend.app.main:app --reload
```  


## Demo  
Watch the project demo on YouTube:  
Demo Video Link:   **insert here**

Video Highlights:  
	•	Real-time video scoring  
	•	Reward allocation formulas  
	•	Transparency in reward calculation  


## Screenshots  
(Replace with actual screenshots of your project)


## Usage  
	1.	Upload TikTok link
	2.	Dashboard fetches engagement & comments  
	3.	Sentiment analysis and AIGC run automatically  
	4.	Reward Score is computed  


## License  

This project is open-source under the MIT License.