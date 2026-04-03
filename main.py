#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
def main():
    parser = argparse.ArgumentParser(
        description="Plagiarism Checker Pro - Complete Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode cli --document essay.txt
  %(prog)s --mode basic
  %(prog)s --mode advanced
  %(prog)s --mode ultimate
  %(prog)s --mode batch --input-dir ./documents
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["cli", "basic", "advanced", "ultimate", "batch", "server"],
        default="basic",
        help="Interface mode (default: basic)"
    )
    
    parser.add_argument(
        "--document",
        type=str,
        help="Document to check (for CLI mode)"
    )
    
    parser.add_argument(
        "--input-dir",
        type=str,
        help="Input directory (for batch mode)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output file/directory for results"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Configuration file"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Plagiarism Checker Pro v3.0"
    )
    
    args = parser.parse_args()

    from core.utils import load_config
    config = load_config(args.config)