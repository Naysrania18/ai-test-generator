"""
Command Line Interface for AI Test Generator
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from . import TestGenerator, __version__
from .config import load_config


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AI-Powered Test Case Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate tests for a single file
  ai-test-gen analyze path/to/file.py

  # Generate tests for entire project
  ai-test-gen analyze-project ./src --output ./tests

  # Generate tests from user story
  ai-test-gen user-story "As a user, I want to login"

  # Train custom model
  ai-test-gen train --dataset ./data --epochs 50
        '''
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'AI Test Generator {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze a Python file')
    analyze_parser.add_argument('file', help='Python file to analyze')
    analyze_parser.add_argument(
        '--output', '-o',
        help='Output file path for generated tests'
    )
    analyze_parser.add_argument(
        '--include-edge-cases',
        action='store_true',
        default=True,
        help='Include edge case detection (default: True)'
    )
    analyze_parser.add_argument(
        '--no-edge-cases',
        action='store_true',
        help='Disable edge case detection'
    )
    analyze_parser.add_argument(
        '--config', '-c',
        help='Path to configuration file'
    )
    
    # Analyze project command
    project_parser = subparsers.add_parser(
        'analyze-project',
        help='Analyze entire project'
    )
    project_parser.add_argument('path', help='Project root path')
    project_parser.add_argument(
        '--output', '-o',
        default='tests/',
        help='Output directory for tests (default: tests/)'
    )
    project_parser.add_argument(
        '--pattern', '-p',
        action='append',
        help='File pattern to match (can be used multiple times)'
    )
    project_parser.add_argument(
        '--config', '-c',
        help='Path to configuration file'
    )
    
    # User story command
    story_parser = subparsers.add_parser(
        'user-story',
        help='Generate tests from user story'
    )
    story_parser.add_argument(
        'story',
        help='User story text or file path (use - for stdin)'
    )
    story_parser.add_argument(
        '--output', '-o',
        help='Output file path'
    )
    story_parser.add_argument(
        '--config', '-c',
        help='Path to configuration file'
    )
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train ML model')
    train_parser.add_argument(
        '--dataset',
        required=True,
        help='Path to training dataset'
    )
    train_parser.add_argument(
        '--epochs',
        type=int,
        default=50,
        help='Number of training epochs (default: 50)'
    )
    train_parser.add_argument(
        '--output', '-o',
        default='models/trained_model.h5',
        help='Output path for trained model'
    )
    train_parser.add_argument(
        '--validation-split',
        type=float,
        default=0.2,
        help='Validation split ratio (default: 0.2)'
    )
    
    # Evaluate command
    eval_parser = subparsers.add_parser('evaluate', help='Evaluate model')
    eval_parser.add_argument(
        '--model',
        required=True,
        help='Path to model file'
    )
    eval_parser.add_argument(
        '--test-data',
        required=True,
        help='Path to test dataset'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == 'analyze':
            analyze_file(args)
        elif args.command == 'analyze-project':
            analyze_project(args)
        elif args.command == 'user-story':
            generate_from_user_story(args)
        elif args.command == 'train':
            train_model(args)
        elif args.command == 'evaluate':
            evaluate_model(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def analyze_file(args):
    """Analyze a single Python file."""
    # Load configuration
    config = load_config(args.config) if hasattr(args, 'config') and args.config else None
    
    # Initialize generator
    generator = TestGenerator(config=config)
    
    # Determine edge case setting
    include_edge_cases = not args.no_edge_cases if hasattr(args, 'no_edge_cases') else True
    
    print(f"Analyzing {args.file}...")
    
    # Generate tests
    output_path = generator.generate_test_file(
        args.file,
        output_path=args.output,
        include_edge_cases=include_edge_cases
    )
    
    print(f"✓ Test file generated: {output_path}")


def analyze_project(args):
    """Analyze entire project."""
    # Load configuration
    config = load_config(args.config) if hasattr(args, 'config') and args.config else None
    
    # Initialize generator
    generator = TestGenerator(config=config)
    
    print(f"Analyzing project at {args.path}...")
    
    # Analyze project
    results = generator.analyze_project(
        args.path,
        output_dir=args.output,
        file_patterns=args.pattern
    )
    
    print(f"\n✓ Generated {len(results)} test files:")
    for source, test_file in results.items():
        print(f"  {source} -> {test_file}")


def generate_from_user_story(args):
    """Generate tests from user story."""
    # Load configuration
    config = load_config(args.config) if hasattr(args, 'config') and args.config else None
    
    # Initialize generator
    generator = TestGenerator(config=config)
    
    # Read user story
    if args.story == '-':
        # Read from stdin
        user_story = sys.stdin.read()
    elif Path(args.story).exists():
        # Read from file
        with open(args.story, 'r') as f:
            user_story = f.read()
    else:
        # Treat as direct text
        user_story = args.story
    
    print("Generating tests from user story...")
    
    # Generate tests
    output_path = generator.generate_from_user_story(
        user_story,
        output_path=args.output
    )
    
    print(f"✓ Test file generated: {output_path}")


def train_model(args):
    """Train ML model."""
    print(f"Training model with dataset: {args.dataset}")
    print(f"Epochs: {args.epochs}")
    print(f"Validation split: {args.validation_split}")
    
    # TODO: Implement training logic
    print("\nTraining not yet implemented in this version.")
    print("This feature will allow you to train custom models on your test data.")


def evaluate_model(args):
    """Evaluate model performance."""
    print(f"Evaluating model: {args.model}")
    print(f"Test data: {args.test_data}")
    
    # TODO: Implement evaluation logic
    print("\nEvaluation not yet implemented in this version.")


if __name__ == '__main__':
    main()
