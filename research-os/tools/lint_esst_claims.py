#!/usr/bin/env python3
"""Conservative claim-boundary lint for the ESST manuscript.

The lint is intentionally small: it flags high-risk terms unless nearby text
explicitly negates, prohibits, or bounds the claim. It is not a substitute for
human review.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERNS = [
    r"\baffected\b",
    r"\bnot_affected\b",
    r"artifact safety",
    r"artifact 安全",
    r"漏洞状态",
    r"数据泄漏",
    r"重大创新",
    r"已获得录用",
    r"投稿录用",
    r"新方法",
]
SAFE_MARKERS = (
    "不", "不能", "不得", "禁止", "不输出", "不判断", "不把", "不确认", "不声称",
    "不构建", "不检索", "停止", "若出现", "not", "no", "without", "never",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    args = ap.parse_args()
    lines = Path(args.path).read_text(encoding="utf-8").splitlines()
    findings = []
    for index, line in enumerate(lines):
        for pattern in PATTERNS:
            if re.search(pattern, line, flags=re.IGNORECASE):
                context = " ".join(lines[max(0, index - 8): min(len(lines), index + 3)])
                bounded = any(marker in context for marker in SAFE_MARKERS)
                findings.append({"line": index + 1, "pattern": pattern, "bounded": bounded, "text": line.strip()})
    unsafe = [item for item in findings if not item["bounded"]]
    print({"path": args.path, "findings": len(findings), "unsafe": len(unsafe)})
    for item in findings:
        print(f"{item['line']}: {'OK' if item['bounded'] else 'REVIEW'} {item['pattern']} :: {item['text']}")
    return 1 if unsafe else 0


if __name__ == "__main__":
    raise SystemExit(main())
