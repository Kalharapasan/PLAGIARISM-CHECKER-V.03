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
    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 80)
    report.append(f"Overall Similarity Score: {score}%")
    report.append(f"Total Words: {results['total_words']}")
    report.append(f"Total Sentences: {results['total_sentences']}")
    report.append(f"Citations Detected: {results.get('citations_found', 0)}")
    report.append(f"Sources Matched: {len(results['matches'])}")
    report.append(f"Matched Words: {stats.get('matched_words', 0)}")
    report.append(f"Unique Content: {stats.get('unique_percentage', 0)}%")
    report.append(f"Longest Match: {stats.get('longest_sequence', 0)} words")
    report.append("")
    report.append("RISK ASSESSMENT")
    report.append("-" * 80)
    if score < 15:
        risk_level = "LOW RISK"
        interpretation = "The document shows minimal similarity to reference sources. This level is generally acceptable for academic submissions."
        recommendation = "Continue maintaining good citation practices."
    elif score < 30:
        risk_level = "MODERATE RISK"
        interpretation = "The document shows moderate similarity to reference sources. Review recommended to ensure proper attribution."
        recommendation = "Review all matched sections. Verify citations are present and paraphrasing is adequate."
    else:
        risk_level = "HIGH RISK"
        interpretation = "The document shows substantial similarity to reference sources. Significant concerns regarding originality."
        recommendation = "Comprehensive revision required. Review all matches carefully and ensure proper citation or rewrite in your own words."
    
    report.append(f"Risk Level: {risk_level}")
    report.append(f"\nInterpretation: {interpretation}")
    report.append(f"\nRecommendation: {recommendation}")
    report.append("")
    report.append("ALGORITHM ANALYSIS")
    report.append("-" * 80)
    if results.get('algorithm_scores'):
        for algo, perf in results['algorithm_scores'].items():
            report.append(f"{algo.capitalize()} Similarity: {perf.get('average', 0):.2f}% (avg across matches)")
    report.append("")