# UNNC Campus AIGC Generator
### UNNC 30H AI Hackathon Submission

## Project Title
UNNC Campus AIGC Generator – AI-Powered Campus Content Generator for UNNC Community

## Introduction
UNNC Campus AIGC Generator is a lightweight, user-friendly web application developed for the UNNC 30H AI Hackathon. It leverages generative AI to transform simple user-input keywords into high-quality, contextually relevant content tailored specifically for the University of Nottingham Ningbo China (UNNC) community.

Designed to address the content creation needs of UNNC students, clubs, faculty, and staff, the tool generates diverse content—including social media posts, event descriptions, study tips, promotional copy, and campus stories—in real time. Powered by the Minimax M2.7 API, it ensures fast, reliable, and campus-centric outputs that align with UNNC’s academic and social environment.

## Features
- **Keyword-Based AI Generation**: Convert simple keywords (e.g., "library", "campus life", "graduation") into polished, inspiring content.
- **Modern Responsive UI**: Clean, visually appealing interface optimized for both desktop and mobile devices.
- **Real-Time Feedback**: Loading animations and clear status updates during content generation.
- **User-Friendly Tools**: One-click copy of generated content and regenerate function for iterative refinement.
- **Robust Error Handling**: Clear, actionable messages for empty inputs, network issues, and API errors.
- **UNNC-Specific Optimization**: Prompts tailored to UNNC’s campus culture, ensuring relevant and relatable content.

## How to Run
### Prerequisites
- Python 3.8 or higher
- Valid Minimax API Key and Group ID (obtained from [Minimax Platform](https://www.minimaxi.com/))

### 1. Install Dependencies
Clone the repository and install required packages:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the project root directory and add your Minimax credentials:
```env
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_GROUP_ID=your_minimax_group_id_here
```

### 3. Start the Flask Server
```bash
python app.py
```

### 4. Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## API Configuration
- **AI Model**: Minimax M2.7 (compatible with Minimax Trial/Free Plan)
- **Backend Endpoint**: `/api/generate` (POST request)
- **Request Format**: JSON with `keyword` parameter (e.g., `{"keyword": "study, library"}`)
- **Response Format**: JSON with `content` (generated text) or `error` (error message)
- **Required Headers**: Authorization (Minimax API Key), Content-Type (application/json)

## Tech Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (no external frameworks)
- **Backend**: Flask (Python) – lightweight, easy-to-deploy web framework
- **AI Engine**: Minimax M2.7 API – core text generation model
- **Development Tools**: TRAE.ai IDE (rapid prototyping)
- **Deployment**: Local Flask Server (for hackathon demonstration)

## Author
UNNC AI Hackathon Team--kim    
Submitted for UNNC 30H AI Hackathon  
Powered by Minimax M2.7 API
