# Contributing to Crypto Arbitrage Platform

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a new branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/crypto-arb-engine.git
cd crypto-arb-engine

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install -r requirements-dev.txt
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Add unit tests

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Run linting
flake8 src tests
```

## Pull Request Process

1. Update documentation
2. Add tests
3. Update CHANGELOG.md
4. Request review

## Code Review

- Code quality
- Test coverage
- Documentation
- Performance impact