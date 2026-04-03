from pathlib import Path

from core.base_engine import BasePlagiarismEngine
from core.database import DatabaseManager
from reports.basic_report import generate_basic_report


class CLIMode:
    def __init__(self, config):
        self.config = config
        self.engine = BasePlagiarismEngine(config)
        self.db_manager = DatabaseManager(config)

    def _database_docs(self):
        docs = self.db_manager.get_all_documents()
        if docs:
            return docs
        return [
            {
                "source": "Built-in Reference",
                "url": "",
                "text": (
                    "Plagiarism is presenting someone else's work as your own. "
                    "Proper citation and paraphrasing are essential for academic integrity."
                ),
            }
        ]

    def check_document(self, document_path, output_path=None):
        path = Path(document_path)
        if not path.exists():
            print(f"Error: file not found: {document_path}")
            return

        text = self.engine.extract_text(str(path))
        results = self.engine.analyze_basic(text, self._database_docs())

        print(f"Document: {path.name}")
        print(f"Overall similarity: {results['overall_similarity']}%")
        print(f"Sources matched: {len(results['matches'])}")

        if output_path:
            report = generate_basic_report(results, path.name)
            out = Path(output_path)
            if out.is_dir() or str(out).endswith("/") or str(out).endswith("\\"):
                out.mkdir(parents=True, exist_ok=True)
                out = out / f"report_{path.stem}.txt"
            else:
                out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(report, encoding="utf-8")
            print(f"Report saved: {out}")

    def interactive_mode(self):
        print("CLI mode interactive session")
        print("Type document path, or 'quit' to exit.")
        while True:
            user_input = input("document> ").strip()
            if user_input.lower() in {"quit", "exit", "q"}:
                break
            if not user_input:
                continue
            try:
                self.check_document(user_input)
            except Exception as exc:
                print(f"Error: {exc}")
