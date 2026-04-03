from pathlib import Path

from core.base_engine import BasePlagiarismEngine
from core.database import DatabaseManager
from reports.basic_report import generate_basic_report


class BatchProcessor:
    def __init__(self, config):
        self.config = config
        self.engine = BasePlagiarismEngine(config)
        self.db_manager = DatabaseManager(config)

    def process_directory(self, input_dir, output_dir=None):
        if input_dir:
            input_path = Path(input_dir)
        else:
            default_input = self.config.get("paths.sample_documents", "data/sample_documents")
            input_path = Path(default_input)
            print(f"No input directory provided. Using default: {input_path}")

        if not input_path.exists() or not input_path.is_dir():
            print(f"Invalid input directory: {input_path}")
            print("Use --input-dir <folder> for batch mode.")
            return []

        out_path = Path(output_dir) if output_dir else Path("exports/batch_reports")
        out_path.mkdir(parents=True, exist_ok=True)

        database = self.db_manager.get_all_documents()
        if not database:
            database = [
                {
                    "source": "Built-in Reference",
                    "url": "",
                    "text": "Sample reference content for baseline plagiarism detection.",
                }
            ]

        supported = {".txt", ".docx", ".pdf"}
        files = [p for p in input_path.rglob("*") if p.is_file() and p.suffix.lower() in supported]

        if not files:
            print("No supported files found for batch processing.")
            return []

        produced = []
        for file_path in files:
            try:
                text = self.engine.extract_text(str(file_path))
                results = self.engine.analyze_basic(text, database)
                report_text = generate_basic_report(results, file_path.name)
                report_file = out_path / f"report_{file_path.stem}.txt"
                report_file.write_text(report_text, encoding="utf-8")
                produced.append(str(report_file))
                print(f"Processed: {file_path.name} -> {report_file.name}")
            except Exception as exc:
                print(f"Failed: {file_path} ({exc})")

        print(f"Batch complete. Reports: {len(produced)}")
        return produced
