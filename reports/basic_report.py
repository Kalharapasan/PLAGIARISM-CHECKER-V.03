from datetime import datetime
from typing import Dict


def generate_basic_report(results: Dict, filename: str) -> str:
	"""Generate a concise plain-text plagiarism summary report."""
	score = results.get("overall_similarity", 0)
	matches = results.get("matches", [])

	lines = [
		"=" * 70,
		"BASIC PLAGIARISM REPORT",
		"=" * 70,
		f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
		f"Document: {filename}",
		"",
		f"Overall Similarity: {score}%",
		f"Total Words: {results.get('total_words', 0)}",
		f"Total Sentences: {results.get('total_sentences', 0)}",
		f"Citations Found: {results.get('citations_found', 0)}",
		f"Sources Matched: {len(matches)}",
		"",
	]

	if score < 15:
		lines.append("Assessment: Low similarity")
	elif score < 30:
		lines.append("Assessment: Moderate similarity")
	else:
		lines.append("Assessment: High similarity")

	lines.append("")
	lines.append("MATCH DETAILS")
	lines.append("-" * 70)

	if not matches:
		lines.append("No significant matches found.")
	else:
		for idx, match in enumerate(matches, start=1):
			lines.append(f"{idx}. Source: {match.get('source', 'Unknown')}")
			if match.get("url"):
				lines.append(f"   URL: {match['url']}")
			lines.append(f"   Similarity: {match.get('similarity', 0)}%")

			sequences = match.get("matched_sequences", [])
			if sequences:
				lines.append("   Matched Sequences:")
				for seq in sequences[:3]:
					seq_text = seq.get("text", "")
					snippet = seq_text[:100] + ("..." if len(seq_text) > 100 else "")
					lines.append(
						f"   - \"{snippet}\" ({seq.get('length', 0)} words)"
					)
			lines.append("")

	lines.append("=" * 70)
	lines.append("End of Report")
	return "\n".join(lines)

