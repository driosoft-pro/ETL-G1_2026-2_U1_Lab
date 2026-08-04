# Work Plan - Lab 1B ETL Pipeline

## Team

| Member | Role | Responsibilities |
|---|---|---|
| Deyton Riascos Ortiz | Project Manager & Technical Lead | Architecture, main.py, module integration, Git, PR review, final validations, and SQLite |
| Samuel Izquierdo Bonilla | ETL - Extract & Profile | extract.py, profile.py, CSV/JSON/XML reading, profiling, and findings documentation |
| Daniel David Garcia Restrepo | ETL - Clean & Transform | clean.py, transform.py, master table integration, and metrics calculation |
| Mauricio Taborda Gongora | Quality & Analytics | validate.py, load.py, queries.py, README, testing, and compliance evidence |

## Sprint 1 - Setup
- [ ] Repository setup
- [ ] Project structure
- [ ] Pipeline diagram
- [ ] Selection of 6 business requirements from Lab 1A

## Sprint 2 - Extract & Profile
- [ ] Extract (CSV, JSON, XML)
- [ ] Profile
- [ ] Clean

## Sprint 3 - Transform & Load
- [ ] Transform
- [ ] Validate
- [ ] Load to SQLite

## Sprint 4 - Queries & Documentation
- [ ] SQL queries
- [ ] README
- [ ] Testing
- [ ] Presentation
- [ ] Bug fixes

## Git Workflow
```
main
│
develop
├── feature/extract-profile
├── feature/clean-transform
├── feature/validate-load-queries
└── feature/docs
```
- No one develops directly on main.
- Everything is integrated into develop first.
- Changes are made via Pull Requests reviewed by Deyton.

## Technologies
- Python 3.12+
- pandas
- SQLite (sqlite3)
- xml.etree.ElementTree
- json
- logging
- pathlib
- python-dotenv
- pytest (optional)
- Git + GitHub
