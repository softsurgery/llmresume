# ResumeAI - AI-Powered CV Generator

An intelligent CV/Resume generator powered by Qwen3 LLM and RenderCV. Simply paste your career details and get a professionally formatted CV in multiple formats (PDF, HTML, Markdown, Typst) in seconds.

## Features

✨ **AI-Powered CV Generation** - Uses Qwen3 LLM to intelligently process and structure career information

📄 **Multiple Export Formats** - Generate CVs in PDF, HTML, Markdown, Typst, and YAML

🎨 **Professional Design** - Beautiful, ATS-friendly CV templates via RenderCV

⚡ **Lightning Fast** - Generate complete CVs in under a minute

🔒 **Privacy First** - All processing done locally via Ollama

🌙 **Dark Mode** - Modern UI with built-in dark/light mode support

## Technology Stack

### Backend

- **Django 6.0** - REST API framework
- **Django REST Framework** - API scaffolding
- **Ollama** - Local LLM inference (Qwen3)
- **RenderCV** - CV rendering engine
- **Python** - Backend language

### Frontend

- **React 19** - UI framework
- **TypeScript** - Type-safe development
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - High-quality React components
- **Lucide Icons** - Beautiful icon library
- **React Router** - Client-side routing

## Project Structure

```
llmresume/
├── api/                          # Django backend
│   ├── api/                      # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── resumes/                  # Resume app
│   │   ├── viewsets/
│   │   │   └── resume_view.py   # CV generation logic
│   │   ├── views.py              # File download endpoint
│   │   ├── urls.py
│   │   └── models.py
│   ├── integrations/
│   │   └── ollama/
│   │       ├── core.py           # Ollama integration
│   │       └── templates/        # LLM prompt templates
│   ├── utils/                    # Utility modules
│   │   ├── transformers/
│   │   │   └── json.py           # JSON/YAML conversion
│   │   └── rendercv/
│   │       └── functions.py      # RenderCV wrapper
│   ├── manage.py
│   ├── db.sqlite3
│   ├── requirements.txt
│   └── media/                    # Generated CVs storage
│       └── jobs/
├── ui/                           # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── ui/               # shadcn UI components
│   │   ├── pages/
│   │   │   ├── GeneratePage.tsx  # CV input form
│   │   │   └── DownloadPage.tsx  # File download page
│   │   ├── lib/
│   │   │   └── utils.ts          # Utility functions
│   │   ├── App.tsx               # Main app with routing
│   │   ├── main.tsx              # React entry point
│   │   ├── index.css             # Tailwind + theme
│   │   └── App.css
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── package.json
│   └── dist/                     # Build output
├── app.py                        # Legacy CLI interface
└── README.md
```

## Prerequisites

- **Python 3.8+** - For Django backend
- **Node.js 16+** - For React frontend
- **Ollama** - For running local LLM (install from [ollama.ai](https://ollama.ai))
- **RenderCV** - For CV rendering (installed via pip)

## Installation

### 1. Clone and Setup Backend

```bash
# Install Python dependencies
cd api
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Django development server
python manage.py runserver 0.0.0.0:5555
```

The API will be available at `http://localhost:5555`

### 2. Setup Frontend

```bash
cd ui

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```

The UI will be available at `http://localhost:5173` (or next available port)

### 3. Setup Ollama

```bash
# Install Ollama from https://ollama.ai
# Pull the Qwen3 model
ollama pull qwen3:0.6b

# Start Ollama server (runs on port 11434)
ollama serve
```

## Configuration

### Environment Variables

Create a `.env` file in the `api/` directory:

```env
# Ollama settings
OLLAMA_HOST=http://127.0.0.1:11434
MODEL_NAME=qwen3:0.6b

# Django settings (from api/api/settings.py)
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*
```

### Django Settings

Key settings in `api/api/settings.py`:

- `DEBUG` - Development mode flag
- `ALLOWED_HOSTS` - List of allowed hosts
- `INSTALLED_APPS` - Installed Django apps
- `DATABASES` - SQLite database configuration
- `MEDIA_ROOT` - Directory for generated CVs

## API Endpoints

### Generate CV

**POST** `/api/resume/`

Request:

```json
{
  "prompt": "John Doe\nEmail: john@example.com\n\nExperience:\n- Senior Developer at TechCorp (2021–Present)..."
}
```

Response:

```json
{
  "job_id": "uuid-here",
  "message": "CV generated successfully"
}
```

### Get Generated Files

**GET** `/api/resume/<job_id>/files/`

Response:

```json
{
  "files": [
    {
      "name": "John_Doe_CV.pdf",
      "ext": "pdf",
      "ext_upper": "PDF",
      "url": "/download/<job_id>/John_Doe_CV.pdf"
    },
    ...
  ],
  "job_id": "uuid-here"
}
```

### Download File

**GET** `/download/<job_id>/<filename>`

Downloads the generated CV file with proper security checks.

## Usage

### Web UI

1. Navigate to `http://localhost:5173` in your browser
2. Enter your career details in the textarea (name, experience, education, skills, etc.)
3. Click "Generate CV"
4. Wait for processing (30-60 seconds depending on model and input)
5. Download your CV in multiple formats

### CLI (Legacy)

```bash
python app.py
```

This uses the hardcoded CV data in `app.py` for testing.

## LLM Prompt Flow

The CV generation process uses a two-stage prompt:

1. **Rephrase & Enhance** (`rephrase-enhance.md`)
   - Takes raw input
   - Enhances and structures the information
   - Outputs enhanced career narrative

2. **Complete Prompt** (`complete-prompt.md`)
   - Takes enhanced narrative
   - Generates structured JSON output
   - Enforces JSON-only response

The JSON is then converted to YAML and passed to RenderCV for rendering.

## File Storage

Generated CVs are stored in `api/media/jobs/<job_id>/` with the following files:

- `cv.yaml` - Structured CV data
- `*.pdf` - PDF rendering
- `*.html` - HTML rendering
- `*.md` - Markdown rendering
- `*.typ` - Typst rendering
- `*.png` - PNG preview (if enabled)

## Development

### Hot Reload

- **Frontend**: Vite provides instant HMR (Hot Module Replacement)
- **Backend**: Django dev server auto-reloads on file changes

### Building for Production

```bash
# Frontend
cd ui
npm run build  # Creates dist/ directory

# Backend uses Django's default collectstatic
python manage.py collectstatic
```

### Linting & Type Checking

```bash
# Frontend
cd ui
npm run lint              # ESLint
npx tsc --noEmit         # TypeScript type checking
```

## Deployment

### Docker (Recommended)

Create `Dockerfile`:

```dockerfile
# Multi-stage build for frontend
FROM node:18-alpine AS frontend
WORKDIR /app/ui
COPY ui/package*.json ./
RUN npm install
COPY ui .
RUN npm run build

# Django backend
FROM python:3.11-slim
WORKDIR /app
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY api .
COPY --from=frontend /app/ui/dist ./static/
EXPOSE 5555
CMD ["python", "manage.py", "runserver", "0.0.0.0:5555"]
```

### Environment-Specific Settings

For production, update `api/api/settings.py`:

- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS` with your domain
- Set a strong `SECRET_KEY`
- Use a production database (PostgreSQL recommended)
- Enable HTTPS/SSL

## Troubleshooting

### Ollama Connection Failed

- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_HOST` environment variable
- Verify model is installed: `ollama list`

### CV Generation Timeout

- Increase timeout in API view settings
- Consider using a larger/faster model than qwen3:0.6b
- Check Ollama server logs for errors

### PDF Generation Failed

- Ensure RenderCV is properly installed
- Check YAML format is valid
- Verify all required fields are present in the YAML

### Port Already in Use

- Django: `python manage.py runserver 0.0.0.0:5556`
- Vite: `npm run dev -- --port 5174`

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly (both frontend and backend)
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please open a GitHub issue.

## Acknowledgments

- [RenderCV](https://github.com/simonkurtz-inomad/rendercv) - CV rendering
- [Ollama](https://ollama.ai) - Local LLM inference
- [Qwen3](https://github.com/QwenLM/Qwen3) - Language model
- [shadcn/ui](https://ui.shadcn.com) - UI component library
- [Tailwind CSS](https://tailwindcss.com) - Styling framework
