# Python — Agent Instructions

## Stack
- **Python:** 3.12
- **Gestor:** uv
- **Linting:** Black, Flake8, Pylint
- **Testing:** Pytest
- **Types:** MyPy

## Comandos Clave
| Comando | Descripción |
|---------|-------------|
| `nix develop` | Activar entorno (crea .venv con uv) |
| `uv venv` | Crear virtual environment |
| `uv pip install <pkg>` | Instalar paquete |
| `uv pip sync` | Sincronizar dependencias |
| `uv run python script.py` | Ejecutar con uv |
| `pytest` | Ejecutar tests |
| `pytest --cov` | Tests con cobertura |
| `black .` | Formatear código |
| `flake8 .` | Linting |
| `mypy .` | Verificación de tipos |

## Convenciones
- **Gestor:** uv (nunca pip directamente)
- **Estructura:** `src/<package>/`, `tests/`
- **PEP 8:** seguir guías oficiales de estilo
- **Docstrings:** formato Google o NumPy
- **Imports:** stdlib → third-party → local (separados por líneas)
- **Testing:** archivos `test_*.py`, funciones `test_*`

## Templates Disponibles
| Template | Uso |
|----------|-----|
| `template-python-basic` | Desarrollo Python general |
| `template-python-fastapi` | APIs REST con FastAPI |
| `template-python-datascience` | Data Science con Jupyter + Pandas |
| `template-python-flet` | Apps desktop con Flet + NVIDIA |
