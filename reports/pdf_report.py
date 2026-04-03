from pathlib import Path

from reports.advanced_report import generate_advanced_report


def generate_pdf_report(results, filename, algorithms, output_path):
    """Generate a PDF report when reportlab is available.

    Falls back with a clear ImportError message when reportlab is missing.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
    except ImportError as exc:
        raise ImportError(
            "PDF export requires reportlab. Install it with: pip install reportlab"
        ) from exc

    report_text = generate_advanced_report(results, filename, algorithms)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(output), pagesize=A4)
    width, height = A4
    x = 40
    y = height - 40

    for raw_line in report_text.splitlines():
        line = raw_line if raw_line else " "
        if len(line) > 120:
            chunks = [line[i:i + 120] for i in range(0, len(line), 120)]
        else:
            chunks = [line]

        for chunk in chunks:
            c.drawString(x, y, chunk)
            y -= 14
            if y < 40:
                c.showPage()
                y = height - 40

    c.save()
    return str(output)
