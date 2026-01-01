# CLAUDE.md Template: Data Science / ML Project

> Copy this file to your project root as `CLAUDE.md` and customize.

---

# Project Name

## Overview
[Description of the data science/ML project - what problem it solves, what data it uses]

## Tech Stack
- **Language:** Python 3.11+
- **Package Manager:** [uv / poetry / pip]
- **ML Framework:** [PyTorch / TensorFlow / scikit-learn / JAX]
- **Experiment Tracking:** [MLflow / Weights & Biases / Neptune]
- **Data Processing:** pandas, polars, numpy
- **Notebooks:** Jupyter Lab

## Project Structure
```
├── data/
│   ├── raw/                  # Original, immutable data
│   ├── processed/            # Cleaned, transformed data
│   ├── features/             # Feature-engineered data
│   └── external/             # External data sources
├── notebooks/
│   ├── 01_exploration.ipynb  # Initial EDA
│   ├── 02_preprocessing.ipynb
│   ├── 03_modeling.ipynb
│   └── 04_evaluation.ipynb
├── src/
│   ├── data/                 # Data loading and processing
│   │   ├── load.py
│   │   └── preprocess.py
│   ├── features/             # Feature engineering
│   │   └── build_features.py
│   ├── models/               # Model definitions
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── evaluate.py
│   ├── visualization/        # Plotting utilities
│   │   └── plots.py
│   └── utils/                # Helper functions
├── configs/
│   ├── config.yaml           # Main configuration
│   └── model_config.yaml     # Model hyperparameters
├── models/                   # Saved model artifacts
├── outputs/
│   ├── figures/              # Generated plots
│   └── reports/              # Generated reports
├── tests/
├── requirements.txt          # or pyproject.toml
└── README.md
```

## Common Commands
```bash
# Environment Setup
python -m venv .venv
source .venv/bin/activate     # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Using uv (faster)
uv venv
uv pip install -r requirements.txt

# Jupyter
jupyter lab                   # Start Jupyter Lab
jupyter notebook              # Start Jupyter Notebook

# Data Pipeline
python -m src.data.load       # Load raw data
python -m src.data.preprocess # Preprocess data
python -m src.features.build_features  # Build features

# Training
python -m src.models.train    # Train model
python -m src.models.evaluate # Evaluate model

# Testing
pytest                        # Run all tests
pytest -v tests/test_models.py  # Specific test file

# Code Quality
ruff check .                  # Linting
ruff format .                 # Formatting
mypy src/                     # Type checking
```

## Data Guidelines

### Data Versioning
- Raw data is immutable - never modify `data/raw/`
- Use DVC or git-lfs for large files
- Document data sources in `data/README.md`

### Data Loading
```python
# Preferred pattern
from src.data.load import load_dataset

df = load_dataset("train")  # Loads from configured path
```

### Feature Engineering
- All feature code in `src/features/`
- Document feature definitions
- Use consistent naming: `feature_name_v1`

## Model Guidelines

### Configuration
Use YAML configs for reproducibility:
```yaml
# configs/model_config.yaml
model:
  name: "random_forest"
  params:
    n_estimators: 100
    max_depth: 10
training:
  epochs: 50
  batch_size: 32
```

### Experiment Tracking
```python
import mlflow

with mlflow.start_run():
    mlflow.log_params(config["model"]["params"])
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")
```

### Model Artifacts
- Save models to `models/` with descriptive names
- Include timestamp and metrics: `model_rf_acc0.95_20260101.pkl`
- Log model cards with performance metrics

## Notebook Guidelines

### Naming Convention
```
01_initial_exploration.ipynb
02_data_cleaning.ipynb
03_feature_engineering.ipynb
04_baseline_model.ipynb
05_model_tuning.ipynb
06_final_evaluation.ipynb
```

### Structure
1. **Title and description** at top
2. **Imports** in first cell
3. **Configuration** (paths, params)
4. **Main content** with markdown sections
5. **Summary** at bottom

### Best Practices
- Clear markdown explanations between code
- Don't commit notebooks with outputs (use `nbstripout`)
- Extract reusable code to `src/`
- Use `%load_ext autoreload` for development

## Environment Variables
```bash
# .env
DATA_PATH=/path/to/data
MODEL_PATH=/path/to/models
MLFLOW_TRACKING_URI=http://localhost:5000
WANDB_API_KEY=your-key
```

## Key Files
- `configs/config.yaml` - Main project configuration
- `src/data/load.py` - Data loading utilities
- `src/models/train.py` - Training pipeline
- `notebooks/01_exploration.ipynb` - Initial analysis

## Don't
- Don't commit large data files - use DVC or git-lfs
- Don't hardcode paths - use config files
- Don't skip experiment tracking - log everything
- Don't leave notebooks with outputs - strip before commit
- Don't duplicate preprocessing - centralize in `src/data/`
- Don't train without setting random seeds
