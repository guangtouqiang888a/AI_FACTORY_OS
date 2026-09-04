# 11_CONTENT_FACTORY/artifact_generators/excel_generator.py — 真实 XLSX 生成

from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_excel(title: str, sheets: list[dict], output_path: Path) -> dict[str, Any]:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ImportError as exc:
        return {"status": "error", "file_path": "", "error": f"openpyxl not installed: {exc}"}

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)

    for sheet_def in sheets:
        ws = wb.create_sheet(title=sheet_def.get("name", "Sheet")[:31])
        columns = sheet_def.get("columns", [])
        ws.append(columns)
        for cell in ws[1]:
            cell.font = Font(bold=True)

        sample_rows = sheet_def.get("sample_rows", 3)
        for i in range(1, sample_rows + 1):
            row = []
            for col in columns:
                if col in ("金额", "数值", "合计"):
                    row.append(i * 100)
                elif col == "日期":
                    row.append(f"2026-07-{i:02d}")
                else:
                    row.append(f"示例{i}")
            ws.append(row)

        formulas = sheet_def.get("formulas", [])
        if "SUM" in formulas and len(columns) >= 2:
            sum_col = 2 if len(columns) > 1 else 1
            ws.cell(row=sample_rows + 3, column=1, value="合计")
            col_letter = chr(64 + sum_col) if sum_col <= 26 else "B"
            ws.cell(row=sample_rows + 3, column=sum_col, value=f"=SUM({col_letter}2:{col_letter}{sample_rows + 1})")

        for col_idx, col_name in enumerate(columns, 1):
            ws.column_dimensions[chr(64 + col_idx) if col_idx <= 26 else "A"].width = max(12, len(str(col_name)) + 4)

    if not wb.sheetnames:
        wb.create_sheet("数据")

    wb.properties.title = title
    wb.save(str(output_path))
    return {"status": "ok", "file_path": str(output_path)}
