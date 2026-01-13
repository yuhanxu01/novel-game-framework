# Novel Game Framework

A universal framework for converting long novels into interactive text-based games.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Code Agent                                   │
│  (Uses prompts to analyze novel and generate game content)          │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Prompts Framework                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐               │
│  │ Analyzer │→│ Builder  │→│ Designer │→│ Writer   │               │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘               │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Game Data (JSON)                                │
│  story.json / characters.json / world.json / items.json             │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────┬─────────────────────────────────────────────┐
│   Django Backend      │              Frontend                        │
│  ┌─────────────────┐  │  ┌─────────────────────────────────────┐   │
│  │ Game API        │◄─┼──│ Game Engine (Pure JS)               │   │
│  │ Creative API    │  │  │ - Story System                      │   │
│  │ Save/Load       │  │  │ - Attribute System                  │   │
│  └─────────────────┘  │  │ - Exploration System                │   │
│                       │  │ - Inventory System                  │   │
│                       │  │ - Creative Mode                     │   │
│                       │  └─────────────────────────────────────┘   │
└───────────────────────┴─────────────────────────────────────────────┘
```

## Quick Start

### 1. Setup Backend
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Process Novel (Code Agent)
```bash
cd tools
python novel_processor.py --novel path/to/novel.txt --output ../data/
```

### 3. Run Game
Open `frontend/index.html` or serve via Django

## For Code Agent

### Processing Pipeline
1. Read `prompts/README.md` for workflow
2. Use `prompts/01_novel_analyzer.md` to analyze novel in 3000-char chunks
3. Build world with `prompts/02_world_