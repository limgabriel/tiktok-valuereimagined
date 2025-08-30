# BrightShare

A transparent value-sharing platform from content consumers to creators.

## Table of Contents
	1.	Project Overview  
	2.	Problem Statement  
	3.	Features  
	4.	Technology Stack  
	5.	APIs & Libraries  
	6.	Setup & Installation  
	7.	Demo  
	8.	Screenshots  
	9.	Usage  
	10.	License  


## Project Overview

BrightShare is designed to ensure fair and transparent reward distribution for content creators.  
It evaluates content quality, detects fraudulent activity, to allocate revenue fairly from consumers to creators.


## Problem Statement

Current reward mechanisms for TikTok creators:\
	•	Are often unfair\
	•	Can be manipulated by fraudulent activity\
	•	Unintentionally incentivises unregulatory behaviour, toxicity\

BrightShare solves this by combining engagement metrics, sentiment analysis, and fraud detection to compute fair reward allocation.


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
M_quality = 0.5 * Positivity Rate + 0.5 * Toxicity Rate
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

Frontend: React.js, TailwindCSS  
Backend: FastAPI  
Database: MongoDB  
Deployment: Docker, Heroku / AWS  
Type Checking: Pydantic  


## APIs & Libraries  
	•	APIs:  
	    •	TikTok API (video & engagement data)  
	    •	OpenAI / Hugging Face API (sentiment analysis for positivity detection)  
	 	•   Perspective API (sentiment analysis for toxicity detection)
	    •	ReCaptcha / third-party bot detection  
	•	Python Libraries:  
        • fastapi - API framework  
        •	pydantic – Data validation and type enforcement  
	    •	motor – Async MongoDB client  
	    •	transformers – For sentiment analysis (Hugging Face models)  
	    •	uvicorn – ASGI server for FastAPI  
    •	JS Libraries (Frontend):  
	    •	axios (API calls)  
	    •	recharts or chart.js (charts for dashboard)  
	•	Assets:  
	    •	Sample video metadata  
	    •	Public comment datasets for testing  
	    •	Dashboard icons  


## Setup & Installation  
	1.	Clone the repository:  

git clone https://github.com/<your-team>/tiktok-valuereimagined.git

	2.	Navigate to the project folder:  

cd tiktok-valuereimagined  

	3.	Install dependencies:  

npm install  

	4.	Configure environment variables (API keys, database URI)  
	5.	Run the project:  

npm start  

	6.	Open http://localhost:3000 to view the dashboard  


## Demo  
Watch the project demo on YouTube:  
Demo Video Link  

Video Highlights:  
	•	Dashboard interface  
	•	Real-time video scoring  
	•	Fraud detection in action  
	•	Reward allocation workflow  


## Screenshots  
(Replace with actual screenshots of your project)


## Usage  
	1.	Connect TikTok account or upload video dataset  
	2.	Dashboard fetches engagement & comments  
	3.	Sentiment analysis and fraud detection run automatically  
	4.	Video Score is computed  
	5.	Rewards are displayed based on score  


## License  

This project is open-source under the MIT License.
