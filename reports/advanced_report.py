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
    if score < 15:
        color = '#48bb78'
        status = 'Low Risk'
    elif score < 30:
        color = '#ed8936'
        status = 'Moderate Risk'
    else:
        color = '#f56565'
        status = 'High Risk'
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Plagiarism Report - {filename}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        .score-card {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .score {{
            font-size: 72px;
            font-weight: bold;
            color: {color};
        }}
        .status {{
            font-size: 24px;
            color: {color};
            font-weight: bold;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .stat-box {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }}
        .match {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 5px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .match-header {{
            font-size: 18px;
            font-weight: bold;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        .matched-text {{
            background: #fef5e7;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 3px solid #f39c12;
        }}
        .recommendation {{
            background: #e8f5e9;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #4caf50;
        }}
        .warning {{
            background: #fff3cd;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #ffc107;
        }}
        .critical {{
            background: #f8d7da;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #dc3545;
        }}
        @media print {{
            body {{ background: white; }}
            .score-card, .stat-box, .match {{ box-shadow: none; border: 1px solid #ddd; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Advanced Plagiarism Detection Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Document: {filename}</p>
        <p>Algorithms: {', '.join(algorithms)}</p>
    </div>
    
    <div class="score-card">
        <div class="score">{score}%</div>
        <div class="status">{status}</div>
        <p>Overall Similarity Score</p>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{results['total_words']}</div>
            <div class="stat-label">Total Words</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{stats.get('matched_words', 0)}</div>
            <div class="stat-label">Matched Words</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{len(results['matches'])}</div>
            <div class="stat-label">Sources Found</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{stats.get('unique_percentage', 0)}%</div>
            <div class="stat-label">Unique Content</div>
        </div>
    </div>
    
    <h2>Risk Assessment</h2>
    <div class="{{
        'recommendation' if score < 15 else 
        'warning' if score < 30 else 
        'critical'
    }}">
        <h3>{status}</h3>
        <p>"""
    
    if score < 15:
        html += "The document shows minimal similarity to reference sources. This level is generally acceptable for academic submissions."
    elif score < 30:
        html += "The document shows moderate similarity to reference sources. Review recommended to ensure proper attribution."
    else:
        html += "The document shows substantial similarity to reference sources. Significant concerns regarding originality."
    
    html += """</p>
    </div>
    
    <h2>Matched Sources</h2>
"""
    
    if results['matches']:
        for idx, match in enumerate(results['matches'], 1):
            html += f"""
    <div class="match">
        <div class="match-header">Match #{idx}: {match['source']}</div>
        <p><strong>Similarity:</strong> {match['similarity']}% | <strong>Confidence:</strong> {match.get('confidence', 'N/A')} | <strong>Risk:</strong> {match.get('risk_level', 'N/A')}</p>
        {f"<p><strong>URL:</strong> <a href='{match['url']}'>{match['url']}</a></p>" if match.get('url') else ''}
        <p><strong>Algorithm Scores:</strong></p>
        <ul>
"""
            for algo, algo_score in match.get('algorithm_scores', {}).items():
                html += f"            <li>{algo.capitalize()}: {algo_score}%</li>\n"
            
            html += "        </ul>\n"
            
            if match.get('matched_sequences'):
                html += f"        <p><strong>Matched Sequences ({len(match['matched_sequences'])}):</strong></p>\n"
                for seq in match['matched_sequences'][:3]:
                    truncated = seq['text'][:200] + '...' if len(seq['text']) > 200 else seq['text']
                    html += f"        <div class='matched-text'>\"{truncated}\" ({seq['length']} words)</div>\n"
            
            html += "    </div>\n"
    else:
        html += """
    <div class="recommendation">
        <h3>✓ No Significant Matches Found</h3>
        <p>The document appears to contain primarily original content.</p>
    </div>
"""

    html += f"""
    <h2>Statistical Analysis</h2>
    <div class="stats">
        <div class="stat-box">
            <div class="stat-value">{stats.get('total_words', 0)}</div>
            <div class="stat-label">Total Words</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{stats.get('matched_words', 0)}</div>
            <div class="stat-label">Matched Words</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{stats.get('unique_words', 0)}</div>
            <div class="stat-label">Unique Words</div>
        </div>
        <div class="stat-box">
            <div class="stat-value">{stats.get('longest_sequence', 0)}</div>
            <div class="stat-label">Longest Match</div>
        </div>
    </div>
    
    <h2>Recommendations</h2>
    <div class="recommendation">
"""
    
    if score < 15:
        html += """
        <p>✓ Document is acceptable for submission</p>
        <p>✓ Continue maintaining good academic practices</p>
        <p>• Double-check that all citations are properly formatted</p>
"""
    elif score < 30:
        html += """
        <p>⚠ Review all highlighted matches carefully</p>
        <p>⚠ Verify that all borrowed content is properly cited</p>
        <p>⚠ Consider paraphrasing matched sections more thoroughly</p>
        <p>• Ensure quotation marks are used for direct quotes</p>
        <p>• Add citations for paraphrased content</p>
"""
    else:
        html += """
        <p>✗ Significant revision required before submission</p>
        <p>✗ Review ALL matched sections with source material</p>
        <p>✗ Ensure proper citation for all borrowed content</p>
        <p>✗ Rewrite highly similar sections in your own words</p>
        <p>• Consult with instructor or writing center</p>
        <p>• Review institutional plagiarism policies</p>
"""
    
    html += """
    </div>
    
    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px;">
        <p><strong>Disclaimer:</strong> This is an automated analysis tool. Results should be reviewed by a human. 
        Proper citation, quotation, and paraphrasing are essential for academic integrity. 
        This tool is for educational purposes and should not be the sole basis for 
        academic integrity decisions. Always consult institutional policies and guidelines.</p>
        <p>Generated by Plagiarism Checker Pro - Advanced Version</p>
    </div>
</body>
</html>
"""
    return html

def generate_json_report(results: Dict, filename: str, algorithms: List[str]) -> str:
    