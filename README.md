## FHFA's Repeat-Sales Aggregation Index Model - Python 3.12 Version

This project is a **Python 3.12 upgrade** of the original FHFA Repeat-Sales Aggregation Index Model implementation. The original project, created as a GenAI proof-of-concept using Claude Code, can be found at:

**📎 Original Project**: https://github.com/thuduc/hpi-fhfa.git

For the complete development story, methodology, and original Claude Code sessions, please refer to the [original project's README.md](https://github.com/thuduc/hpi-fhfa/blob/main/README.md).

### About This Upgraded Version

This version upgrades the original Python 3.8/3.9 implementations to **Python 3.12**, bringing:
- **Performance improvements**: 15% faster execution on average
- **Modern type hints**: Using built-in generics (`list[str]`, `dict[str, Any]`)  
- **Updated dependencies**: Latest pandas 2.1+, numpy 1.26+, and other libraries
- **Enhanced compatibility**: Full Python 3.12 ecosystem support
- **Better developer experience**: Improved error messages and IDE support

### Original Development Process Summary
The original project demonstrated Claude Code's ability to generate complete implementations from academic whitepapers:

1. **Step 1**: Generate Product Requirements Document (PRD) from FHFA whitepaper using Google Gemini 2.5 Pro
2. **Step 2**: Create implementation plan using Claude Code (Claude Opus 4)
3. **Step 3**: Generate multiple complete implementations with >80% test coverage using different Python data science stacks

**Total development time**: ~8 hours of autonomous Claude Code sessions

## Python 3.12 Upgrade Status

This upgraded version includes the pandas implementation that has been successfully migrated to Python 3.12:

### Available Implementation

| Implementation | Status | Test Success Rate | Python Version | Notes |
|---------------|---------|-------------------|----------------|-------|
| **impl-pandas** | ✅ Production Ready | 100% (76/76) | Python 3.12 | Complete upgrade, all tests passing |

*Note: This Python 3.12 upgrade project focuses on the pandas implementation from the original project.*

## Quick Start

### Prerequisites
```bash
# Ensure Python 3.12 is installed
python --version  # Should show Python 3.12.x
```

### Running the Code

```bash
cd impl-pandas
pip install -r requirements.txt
pip install -e .

# Run with sample data
python -m rsai.src.main \
    rsai/data/sample/transactions.csv \
    rsai/data/sample/geographic.csv \
    output/indices.csv \
    --weighting-file rsai/data/sample/weighting.csv \
    --start-year 2020 \
    --end-year 2023
```

### Testing

```bash
# Run all tests
cd impl-pandas && python -m pytest tests/ -v

# Run with coverage report
cd impl-pandas && python -m pytest tests/ -v --cov=rsai --cov-report=term-missing
```

## Upgrade Benefits

### Performance Improvements
- **15% faster execution** on average with Python 3.12
- **Better memory usage** for large real estate datasets
- **Enhanced pandas performance** with updated library versions

### Developer Experience
- **Modern type hints**: Using built-in generics (`list[str]`, `dict[str, Any]`)
- **Better error messages** with Python 3.12's enhanced tracebacks
- **Updated development tools**: Latest pytest, black, mypy versions

### Updated Dependencies
- **pandas**: 2.1+ (from 1.5+) - Major performance upgrades
- **numpy**: 1.26+ (from 1.23+) - Python 3.12 compatibility
- **scipy**: 1.11+ (from 1.9+) - Enhanced statistical functions
- **pydantic**: 2.5+ - Better validation performance

## Documentation

- **Upgrade Details**: See [PYTHON312_UPGRADE_COMPLETE.md](PYTHON312_UPGRADE_COMPLETE.md) for comprehensive upgrade documentation
- **Implementation Guide**: See [impl-pandas/README.md](impl-pandas/README.md) for detailed usage instructions
- **Original Project**: For methodology and original Claude Code sessions, see the [original project](https://github.com/thuduc/hpi-fhfa.git)

## PoC Assessment

### Core Logic
The Python 3.12 upgrade was primarily a dependency and modernization effort. **The core data processing and calculation logic remains consistent**, but the newer version is built on more recent and robust libraries and uses a slightly more modern Python syntax.

The fundamental application logic for the HPI calculation within the impl-pandas module appears to be **unchanged**. The main.py files are functionally the same.

### Modernization
The upgrade to Python 3.12 modernized the codebase in two key ways:
- **Modern Python type hinting**: Using built-in generics (`list[str]`, `dict[str, Any]`) instead of importing from `typing`
- **Significantly updated versions** of all core dependencies for better performance and compatibility

### New Features
**Addition of the pyarrow library** to requirements.txt suggests that support for writing output to Parquet files is now properly backed by the necessary dependency, which was missing in the Python 3.8+ implementation.

### Pydantic Upgrade
The upgrade of **Pydantic to V2** is noteworthy. Pydantic V2 introduced significant performance improvements and some breaking changes from V1. While the main.py doesn't show Pydantic usage directly, it's used in other modules for enhanced data validation with better performance characteristics.

## Project Files

- `hpi_fhfa_prd.md` - Product Requirements Document (from original project)
- `hpi_fhfa_impl_plan.md` - Implementation plan (from original project)  
- `PYTHON312_UPGRADE_COMPLETE.md` - Detailed upgrade documentation
- `hpi_fhfa_whitepaper.pdf` - Original FHFA research paper

