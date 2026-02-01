# AI-Powered Test Case Generator 🤖

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

An intelligent test case generation tool that automatically creates comprehensive test cases based on your codebase, function signatures, and user stories using AI and machine learning.

## 🌟 Features

- **Automatic Test Generation**: Analyze Python functions and generate pytest test cases automatically
- **Edge Case Detection**: AI-powered analysis to identify potential edge cases and boundary conditions
- **User Story Analysis**: Convert user stories into actionable test scenarios
- **Multiple Test Types**: Generate unit tests, integration tests, and edge case tests
- **CI/CD Integration**: Seamless integration with GitHub Actions, Jenkins, and other CI systems
- **Code Coverage Analysis**: Identify untested code paths
- **Customizable Templates**: Flexible test generation with customizable templates
- **CLI & API Interface**: Use via command line or integrate into your workflow programmatically

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Install from Source

```bash
# Clone the repository
git clone https://github.com/Naysrania18/ai-test-generator.git
cd ai-test-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Install from PyPI (Coming Soon)

```bash
pip install ai-test-generator
```

## ⚡ Quick Start

### Generate Tests for a Python File

```bash
# Basic usage
ai-test-gen analyze path/to/your/file.py

# Generate tests with edge cases
ai-test-gen analyze path/to/your/file.py --include-edge-cases

# Specify output directory
ai-test-gen analyze path/to/your/file.py --output tests/
```

### Generate Tests from User Stories

```bash
# From a file
ai-test-gen user-story path/to/stories.txt

# From stdin
echo "As a user, I want to login with email and password" | ai-test-gen user-story -
```

### Python API Usage

```python
from ai_test_generator import TestGenerator

# Initialize the generator
generator = TestGenerator()

# Analyze a file and generate tests
test_cases = generator.analyze_file('path/to/your/file.py')

# Generate test file
generator.generate_test_file(
    'path/to/your/file.py',
    output_path='tests/test_generated.py',
    include_edge_cases=True
)
```

## 📖 Usage

### Command Line Interface

```bash
# Show help
ai-test-gen --help

# Analyze entire project
ai-test-gen analyze-project ./src --output ./tests

# Train custom model (advanced)
ai-test-gen train --dataset ./training_data --epochs 50

# Evaluate model
ai-test-gen evaluate --model ./models/custom_model.h5
```

### Configuration

Create a `.ai-test-gen.yml` file in your project root:

```yaml
# Test generation settings
test_framework: pytest  # Options: pytest, unittest
include_edge_cases: true
include_mocks: true
max_tests_per_function: 10

# AI model settings
model_path: models/test_generator_v1.h5
confidence_threshold: 0.7

# Output settings
output_directory: tests/
file_naming: test_{filename}.py
```

## 🏗️ Architecture

### Components

1. **Code Analyzer**: Parses Python code using AST to extract function signatures, types, and complexity
2. **ML Model**: TensorFlow-based model trained on patterns from existing test suites
3. **Edge Case Detector**: Identifies boundary conditions, null cases, and exceptional scenarios
4. **Test Generator**: Creates pytest-compatible test code from analyzed patterns
5. **User Story Parser**: NLP-based parser to convert user stories into test scenarios

### ML Model

The model uses a hybrid architecture:
- **LSTM** for sequence analysis of code patterns
- **Transformer** for understanding code context
- **Classification Head** for test type prediction

Training data includes:
- 50,000+ open-source test cases
- Code-test pairs from popular Python projects
- Manually curated edge cases

## 🔧 Configuration

### Environment Variables

```bash
export AI_TEST_GEN_MODEL_PATH=/path/to/model
export AI_TEST_GEN_API_KEY=your_api_key  # For cloud features
export AI_TEST_GEN_LOG_LEVEL=INFO
```

### Advanced Configuration

See [docs/configuration.md](docs/configuration.md) for detailed configuration options.

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
name: AI Test Generation

on: [push, pull_request]

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install AI Test Generator
        run: pip install ai-test-generator
      - name: Generate Tests
        run: ai-test-gen analyze-project ./src --output ./tests
      - name: Run Generated Tests
        run: pytest tests/
```

### Jenkins

```groovy
pipeline {
    agent any
    stages {
        stage('Generate Tests') {
            steps {
                sh 'ai-test-gen analyze-project ./src --output ./tests'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest tests/'
            }
        }
    }
}
```

## 📊 Examples

### Input: Python Function

```python
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate discounted price."""
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

### Output: Generated Tests

```python
import pytest

def test_calculate_discount_normal_case():
    assert calculate_discount(100.0, 10.0) == 90.0

def test_calculate_discount_zero_discount():
    assert calculate_discount(100.0, 0.0) == 100.0

def test_calculate_discount_full_discount():
    assert calculate_discount(100.0, 100.0) == 0.0

def test_calculate_discount_invalid_negative():
    with pytest.raises(ValueError):
        calculate_discount(100.0, -10.0)

def test_calculate_discount_invalid_over_100():
    with pytest.raises(ValueError):
        calculate_discount(100.0, 150.0)

def test_calculate_discount_zero_price():
    assert calculate_discount(0.0, 50.0) == 0.0
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and install dev dependencies
git clone https://github.com/yourusername/ai-test-generator.git
cd ai-test-generator
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linters
black src/
flake8 src/
mypy src/

# Run full test suite with coverage
pytest --cov=ai_test_generator --cov-report=html
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with TensorFlow and PyTorch
- Inspired by research in automated testing and program synthesis
- Training data from open-source projects (with proper attribution)



