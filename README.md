# Kandy AI - AI Calisthenics Coach

An intelligent calisthenics workout coach that generates personalized daily workouts, tracks progress in Notion, and uses AI to optimize training through progressive overload.

## Features

- **Daily Workout Generation**: AI-powered personalized workouts based on your profile and history
- **Weekly Split**: Structured training schedule (Push, Pull, Legs, Core, Full Body, Skill Work, Active Recovery)
- **Notion Integration**: Automatic workout page creation with interactive checklists
- **Progressive Overload**: Smart progression based on RPE, recovery, pain, and performance
- **Long-term Tracking**: Supabase database for workout history, feedback, and achievements
- **Achievement System**: Unlock badges for consistency and milestones
- **Automated Workflows**: GitHub Actions for morning (generation) and night (analysis) routines

## Tech Stack

- **Python 3.12+**
- **Google Gemini** for workout generation and analysis
- **Supabase** for PostgreSQL database
- **Notion API** for workout page creation
- **Pydantic** for data validation
- **GitHub Actions** for automation

## Project Structure

```
kandy-ai/
├── clients/              # API clients (Gemini, Supabase, Notion)
├── config/               # Configuration and logging
├── database/             # SQL migrations and seed data
├── models/               # Pydantic models
├── prompts/              # AI prompt templates
├── repositories/         # Data access layer
├── services/             # Business logic layer
├── workflows/            # Workflow orchestrators
├── utils/                # Utility functions
├── tests/                # Unit and integration tests
└── .github/workflows/    # GitHub Actions workflows
```

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- Supabase project
- Notion integration
- OpenAI API key

### 1. Clone the Repository

```bash
git clone <repository-url>
cd kandy-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000

# Supabase
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Notion
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id

# User Profile
USER_NAME=Karthik
USER_AGE=20
USER_HEIGHT_CM=163
USER_WEIGHT_KG=58
USER_LEVEL=beginner
USER_GOAL=Become an advanced calisthenics athlete

# Application
LOG_LEVEL=INFO
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY_SECONDS=1.0
```

### 4. Set Up Supabase Database

Run the SQL migrations in order:

1. **Initial Schema**
   ```bash
   # Execute database/001_initial_schema.sql in your Supabase SQL editor
   ```

2. **Seed Data**
   ```bash
   # Execute database/002_seed_data.sql in your Supabase SQL editor
   ```

### 5. Set Up Notion Database

Create a Notion database with the following properties:

- **Title**: Text
- **Date**: Date
- **Status**: Select (Not Started, In Progress, Completed)

### 6. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

- `GEMINI_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `NOTION_TOKEN`
- `NOTION_DATABASE_ID`

## Usage

### Manual Execution

Run workflows manually for testing:

```bash
# Morning workflow (generate workout)
python -m workflows morning

# Night workflow (analyze workout)
python -m workflows night
```

### Automated Execution

The workflows run automatically via GitHub Actions:

- **Morning Workflow**: 4:30 AM IST (11:00 PM UTC previous day)
- **Night Workflow**: 10:00 PM IST (4:30 PM UTC)

You can also trigger workflows manually from the GitHub Actions tab.

## Weekly Split

- **Monday**: Push (chest, shoulders, triceps)
- **Tuesday**: Pull (back, biceps, forearms)
- **Wednesday**: Legs (quads, hamstrings, glutes, calves)
- **Thursday**: Core (abs, obliques, lower back)
- **Friday**: Full Body (compound movements)
- **Saturday**: Skill Work (handstand, planche, front lever)
- **Sunday**: Active Recovery (mobility, flexibility, light cardio)

## Progressive Overload Logic

The system decides whether to **progress**, **maintain**, or **deload** based on:

- **Completion percentage**: Workouts completed vs. prescribed
- **RPE (Rate of Perceived Exertion)**: 1-10 scale
- **Pain level**: 0-5 scale (triggers deload if ≥3)
- **Recovery quality**: poor/fair/good/excellent
- **Sleep hours**: Affects recovery assessment
- **Recent performance trend**: Last 3 workouts

**Never increases difficulty if pain or poor recovery is reported.**

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=. --cov-report=html
```

## Architecture

The project follows SOLID principles with clear separation of concerns:

- **Clients**: Handle external API communication with retry logic
- **Repositories**: Data access layer for Supabase operations
- **Services**: Business logic (workout planning, generation, analysis, progression)
- **Workflows**: Orchestrate the end-to-end processes
- **Models**: Pydantic models for type safety and validation

## Key Components

### WorkoutPlanner
Determines the workout day based on the day of the week.

### WorkoutGenerator
Uses OpenAI GPT to generate personalized workout plans.

### WorkoutAnalyzer
Analyzes completed workouts and provides insights.

### CoachMemoryService
Manages long-term memory for progression tracking.

### ProgressionEngine
Calculates progressive overload decisions.

### MorningWorkflow
Orchestrates the daily workout generation process.

### NightWorkflow
Orchestrates the workout analysis and progress update process.

## Logging

Logs are stored in the `logs/` directory with rotation:
- Maximum file size: 10MB
- Backup count: 5 files
- Log level: Configurable via `LOG_LEVEL`

## Troubleshooting

### Workflow Fails
- Check GitHub Actions logs for error details
- Verify all secrets are correctly configured
- Ensure Supabase and Notion are accessible

### Workout Not Generated
- Verify OpenAI API key is valid
- Check Supabase connection
- Review logs in `logs/kandy_ai.log`

### Notion Page Not Created
- Verify Notion token and database ID
- Check Notion database permissions
- Ensure database has required properties

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on the GitHub repository.
