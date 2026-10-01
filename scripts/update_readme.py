#!/usr/bin/env python3
"""Atualiza os campos dinâmicos do README.md com base em datas.

Os valores ficam entre marcadores invisíveis no Markdown:
    <!--dyn:chave-->valor<!--/dyn:chave-->
A idade do Typing SVG é atualizada direto na URL.
"""

import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

README = Path(__file__).resolve().parent.parent / "README.md"

BIRTH_DATE = date(2001, 7, 16)
STUDY_START = date(2017, 7, 1)
IT_START = date(2020, 10, 21)
DEV_START = date(2021, 8, 9)

# Progresso do curso: estimativa linear entre um ponto conhecido e a previsão de fim.
COURSE_ANCHOR_DATE = date(2026, 10, 1)
COURSE_ANCHOR_DONE = 74  # matérias concluídas na data acima (faltavam 6)
COURSE_TOTAL = 80
COURSE_END = date(2027, 7, 1)


def years_since(start: date, today: date) -> int:
    return today.year - start.year - ((today.month, today.day) < (start.month, start.day))


def course_percent(today: date) -> int:
    if today >= COURSE_END:
        return 100
    anchor_pct = COURSE_ANCHOR_DONE / COURSE_TOTAL * 100
    if today <= COURSE_ANCHOR_DATE:
        return int(anchor_pct)
    elapsed = (today - COURSE_ANCHOR_DATE).days / (COURSE_END - COURSE_ANCHOR_DATE).days
    return int(anchor_pct + (100 - anchor_pct) * elapsed)


def build_values(today: date) -> dict[str, str]:
    pct = course_percent(today)
    if pct >= 100:
        course_pt = "e em **Engenharia da Computação**."
        course_en = "and a **Computer Engineering degree**."
    else:
        course_pt = f"e estou cursando **Engenharia da Computação**, já com {pct}% do curso concluído."
        course_en = (
            f"and I'm currently pursuing a **Computer Engineering degree**, "
            f"with {pct}% of the program already completed."
        )
    return {
        "study_years": str(years_since(STUDY_START, today)),
        "it_years": str(years_since(IT_START, today)),
        "dev_years": str(years_since(DEV_START, today)),
        "course_pt": course_pt,
        "course_en": course_en,
    }


def render(text: str, today: date) -> str:
    values = build_values(today)

    def replace_marker(m: re.Match) -> str:
        key = m.group(1)
        return f"<!--dyn:{key}-->{values[key]}<!--/dyn:{key}-->"

    text = re.sub(r"<!--dyn:(\w+)-->.*?<!--/dyn:\1-->", replace_marker, text)
    age = years_since(BIRTH_DATE, today)
    return re.sub(r"I'm\+\d+\+years\+old", f"I'm+{age}+years+old", text)


def main() -> None:
    today = datetime.now(ZoneInfo("America/Sao_Paulo")).date()
    original = README.read_text(encoding="utf-8")
    updated = render(original, today)
    if updated != original:
        README.write_text(updated, encoding="utf-8")
        print("README.md atualizado.")
    else:
        print("Nada para atualizar.")


if __name__ == "__main__":
    main()
