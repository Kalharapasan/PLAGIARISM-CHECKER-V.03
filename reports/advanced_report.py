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
    report.append("DETAILED MATCH ANALYSIS")
    report.append("-" * 80)
    
    if results['matches']:
        for idx, match in enumerate(results['matches'], 1):
            report.append(f"\n{'='*80}")
            report.append(f"MATCH #{idx}")
            report.append(f"{'='*80}")
            report.append(f"Source: {match['source']}")
            if match.get('url'):
                report.append(f"URL: {match['url']}")
            report.append(f"Overall Similarity: {match['similarity']}%")
            report.append(f"Confidence: {match.get('confidence', 'N/A')}")
            report.append(f"Risk Level: {match.get('risk_level', 'N/A')}")
            
            report.append("\nAlgorithm Scores:")
            for algo, score in match.get('algorithm_scores', {}).items():
                report.append(f"  • {algo.capitalize()}: {score}%")
            
            if match.get('matched_sequences'):
                report.append(f"\nMatched Sequences ({len(match['matched_sequences'])} found):")
                for seq_idx, seq in enumerate(match['matched_sequences'][:3], 1):
                    report.append(f"\n  Sequence {seq_idx} ({seq['length']} words):")
                    truncated = seq['text'][:150] + '...' if len(seq['text']) > 150 else seq['text']
                    report.append(f"  \"{truncated}\"")
            
            report.append(f"\n{'-'*80}")
    else:
        report.append("\n✓ No significant matches found.")
        report.append("The document appears to contain primarily original content.")
        
    report.append("\n\nSTATISTICAL ANALYSIS")
    report.append("-" * 80)
    report.append(f"Total Words Analyzed: {stats.get('total_words', 0)}")
    report.append(f"Matched Words: {stats.get('matched_words', 0)}")
    report.append(f"Unique Words: {stats.get('unique_words', 0)}")
    report.append(f"Unique Percentage: {stats.get('unique_percentage', 0)}%")
    report.append(f"Average Match Length: {stats.get('average_sequence_length', 0)} words")
    report.append(f"Longest Single Match: {stats.get('longest_sequence', 0)} words")
    report.append(f"Total Sources Found: {stats.get('total_sources', 0)}")
    report.append(f"High Risk Sources: {stats.get('high_risk_sources', 0)}")
    report.append("\n\nRECOMMENDATIONS")
    report.append("-" * 80)
    if score < 15:
        report.append("✓ Document is acceptable for submission")
        report.append("✓ Continue maintaining good academic practices")
        report.append("• Double-check that all citations are properly formatted")
    elif score < 30:
        report.append("⚠ Review all highlighted matches carefully")
        report.append("⚠ Verify that all borrowed content is properly cited")
        report.append("⚠ Consider paraphrasing matched sections more thoroughly")
        report.append("• Ensure quotation marks are used for direct quotes")
        report.append("• Add citations for paraphrased content")
    else:
        report.append("✗ Significant revision required before submission")
        report.append("✗ Review ALL matched sections with source material")
        report.append("✗ Ensure proper citation for all borrowed content")
        report.append("✗ Rewrite highly similar sections in your own words")
        report.append("• Consult with instructor or writing center")
        report.append("• Review institutional plagiarism policies")
    
    report.append("\n\nANALYSIS METADATA")
    report.append("-" * 80)
    metadata = results.get('metadata', {})
    report.append(f"Database Size: {metadata.get('database_size', 0)} documents")
    report.append(f"Algorithms Used: {', '.join(metadata.get('algorithms_used', []))}")
    report.append(f"Analysis Timestamp: {datetime.now().isoformat()}")
    report.append("\n" + "=" * 80)
    report.append("DISCLAIMER")
    report.append("-" * 80)
    report.append("This is an automated analysis tool. Results should be reviewed by a human.")
    report.append("Proper citation, quotation, and paraphrasing are essential for academic integrity.")
    report.append("This tool is for educational purposes and should not be the sole basis for")
    report.append("academic integrity decisions. Always consult institutional policies and guidelines.")
    report.append("=" * 80)
    
    return '\n'.join(report)

def generate_html_report(results: Dict, filename: str, algorithms: List[str]) -> str:
    score = results['overall_similarity']
    stats = results.get('statistics', {})