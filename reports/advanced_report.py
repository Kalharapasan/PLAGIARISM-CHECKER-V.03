from datetime import datetime
from typing import Dict, List
import json

def generate_advanced_report(results: Dict, filename: str, 
                           algorithms: List[str]) -> str:
    score = results['overall_similarity']
    stats = results.get('statistics', {})
    
    report = []
    report.append("=" * 80)
    report.append("ADVANCED PLAGIARISM DETECTION REPORT")
    report.append("=" * 80)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Document: {filename}")
    report.append(f"Analysis Algorithms: {', '.join(algorithms)}")
    report.append("")