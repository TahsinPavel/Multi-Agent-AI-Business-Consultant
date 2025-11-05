# Multi-Agent AI Business Consultant

A multi-agent AI system designed to provide comprehensive business consulting services using specialized AI agents for market analysis, financial planning, and strategic guidance.

## Features

- **Market Analysis Agent**: Provides insights on target markets, competition, and opportunities
- **Financial Analysis Agent**: Offers financial projections, cost analysis, and funding guidance
- **Strategy Agent**: Delivers strategic plans and implementation roadmaps
- **Comprehensive Consultation**: Get insights from all agents in one request

## Architecture

The system consists of:
- Backend API built with FastAPI
- Specialized AI agents for different business domains
- Frontend interface built with Streamlit
- OpenAI GPT models for analysis and recommendations

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Multi-Agent AI Business Consultant"
   ```

2. **Set up the Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   - Edit `backend/.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the backend server**
   ```bash
   cd backend
   python main.py
   ```

6. **Run the frontend interface**
   ```bash
   cd frontend
   streamlit run app.py
   ```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /consult/market` - Market analysis
- `POST /consult/financial` - Financial analysis
- `POST /consult/strategy` - Strategic guidance
- `POST /consult/comprehensive` - Comprehensive consultation

## Usage

1. Start the backend server
2. Start the frontend application
3. Enter your business idea or question in the frontend
4. Select the type of consultation you need
5. Enter your OpenAI API key
6. Click "Get Business Insights" to receive AI-powered business advice

## Customization

You can customize the prompt templates for each agent by editing the files in `backend/prompts/`:
- `market_analysis_prompt.txt`
- `financial_analysis_prompt.txt`
- `strategy_prompt.txt`


## License

This project is licensed under the MIT License.