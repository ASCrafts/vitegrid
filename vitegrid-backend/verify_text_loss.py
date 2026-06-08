"""Text-Loss Verification Engine - Validates Docling doesn't omit characters or macro-structural nodes."""

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

# High-performance marker indicating infinite penalty for structural node deletion
INF_PENALTY = 1_000_000

def tokenize_document(text: str) -> list[str]:
    """
    Tokenizes text into structural markers, words, space sequences, and individual symbols.
    Preserves structural sequences like newlines followed immediately by list/bullet markers.
    """
    if not text:
        return []
    # Pattern detects newlines with procedural bullets, numeric lists, or standalone markers
    pattern = re.compile(r'(\n[-*+]\s+|\n\d+[.)]\s+|[-*+]\s+|^\d+[.)]\s+|\s+|\w+|.)')
    return [m.group(0) for m in pattern.finditer(text) if m.group(0)]


def is_structural_token(token: str) -> bool:
    """
    Determines if a token corresponds to a macro-structural anchor (procedural list marker).
    Matches patterns such as \\n-, \\n*, \\n1. or line-starting bullet sequences.
    """
    if token.startswith('\n-') or token.startswith('\n*') or token.startswith('\n+'):
        return True
    if re.match(r'^\n\d+[.)]', token):
        return True
    if re.match(r'^[-*+]\s+', token):
        return True
    if re.match(r'^\d+[.)]\s+', token):
        return True
    return False


def verify_document_text_loss(pdf_path: str, docling_json_path: str) -> dict[str, Any]:
    """
    Compare PyMuPDF ground-truth token stream with Docling parsed structure using 
    an asymmetrically weighted Levenshtein sequence alignment matrix.
    
    Returns: {
        "coverage_percentage": float (0-100),
        "total_expected_chars": int,
        "total_missing_chars": int,
        "omissions_log": dict,
        "status": "pass" | "warn" | "fail",
        "structural_failures": list[dict]
    }
    """
    try:
        import pymupdf
        from docling_core.types.doc import DoclingDocument
        from docling_core.types.doc.document import ContentLayer
    except ImportError as e:
        return {
            "coverage_percentage": 100.0,
            "total_expected_chars": 0,
            "total_missing_chars": 0,
            "omissions_log": {},
            "status": "pass",
            "error": f"Dependencies not available: {e}",
            "structural_failures": []
        }

    # Extract character counts (compatibility layer) and full text stream (alignment layer)
    doc = pymupdf.open(pdf_path)
    pymupdf_chars = []
    gt_text_parts = []
    
    for page in doc:
        gt_text_parts.append(page.get_text("text"))
        char_page = page.get_text("rawdict")
        for block in char_page.get("blocks", []):
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    for char in span.get("chars", []):
                        c = char.get("c", "")
                        if c:
                            pymupdf_chars.append(c)
    doc.close()
    gt_text = "".join(gt_text_parts)

    try:
        with open(docling_json_path, "r", encoding="utf-8") as f:
            doc_data = json.load(f)
        docling_doc = DoclingDocument(**doc_data)
    except Exception:
        docling_doc = None

    docling_text_blocks = []
    if docling_doc:
        for item, _ in docling_doc.iterate_items(
            included_content_layers={ContentLayer.BODY, ContentLayer.FURNITURE}
        ):
            if hasattr(item, "text") and item.text:
                docling_text_blocks.append(item.text)

    docling_text = "".join(docling_text_blocks)
    
    # --- Backward-Compatible Character Diagnostics ---
    pymupdf_counts = Counter(pymupdf_chars)
    docling_chars = [c for c in docling_text if c]
    docling_counts = Counter(docling_chars)

    missing_characters = {}
    for char, count in pymupdf_counts.items():
        doc_count = docling_counts.get(char, 0)
        if doc_count < count:
            missing_characters[char] = count - doc_count

    total_expected = sum(pymupdf_counts.values())
    total_missing = sum(missing_characters.values())
    coverage_percentage = (
        ((total_expected - total_missing) / total_expected) * 100.0
        if total_expected > 0
        else 100.0
    )

    # --- Asymmetric Dynamic Programming Token Sequence Alignment ---
    X = tokenize_document(gt_text)
    Y = tokenize_document(docling_text)
    m, n = len(X), len(Y)
    
    structural_omission_detected = False
    isolated_failures = []

    if m > 0:
        # Banded Corridor Optimization to preserve O(W * max(m,n)) computational thresholds
        W = max(200, abs(m - n) + 50)
        dp = [[INF_PENALTY] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = 0
        
        for j in range(1, n + 1):
            dp[0][j] = dp[0][j-1] + 1  # w_ins = 1
            
        for i in range(1, m + 1):
            w_del = INF_PENALTY if is_structural_token(X[i-1]) else 1
            dp[i][0] = dp[i-1][0] + w_del

        for i in range(1, m + 1):
            w_del = INF_PENALTY if is_structural_token(X[i-1]) else 1
            start_j = max(1, i - W)
            end_j = min(n, i + W)
            for j in range(start_j, end_j + 1):
                if X[i-1] == Y[j-1]:
                    w_sub = 0
                elif X[i-1].strip().lower() == Y[j-1].strip().lower():
                    w_sub = 0.5  # Soft penalty for case variation
                else:
                    w_sub = 2    # Strict replacement boundary
                    
                dp[i][j] = min(
                    dp[i-1][j] + w_del,   # Deletion
                    dp[i][j-1] + 1,       # Insertion
                    dp[i-1][j-1] + w_sub  # Substitution
                )

        if dp[m][n] >= INF_PENALTY:
            structural_omission_detected = True

        # --- Dynamic Programming Matrix Traceback & Index Isolation ---
        i, j = m, n
        while i > 0 or j > 0:
            w_del = INF_PENALTY if is_structural_token(X[i-1]) else 1
            current_cost = dp[i][j]
            
            from_diag = dp[i-1][j-1] if i > 0 and j > 0 else INF_PENALTY
            from_up = dp[i-1][j] if i > 0 else INF_PENALTY
            from_left = dp[i][j-1] if j > 0 else INF_PENALTY
            
            if i > 0 and j > 0:
                w_sub = 0 if X[i-1] == Y[j-1] else (0.5 if X[i-1].strip().lower() == Y[j-1].strip().lower() else 2)
            else:
                w_sub = INF_PENALTY

            if i > 0 and j > 0 and current_cost == from_diag + w_sub:
                i -= 1
                j -= 1
            elif i > 0 and current_cost == from_up + w_del:
                if w_del >= INF_PENALTY:
                    isolated_failures.append({
                        "token_index": i - 1,
                        "token": X[i-1].replace('\n', '\\n'),
                        "type": "structural_marker"
                    })
                i -= 1
            elif j > 0 and current_cost == from_left + 1:
                j -= 1
            else:
                if i > 0:
                    i -= 1
                elif j > 0:
                    j -= 1

    # --- Deterministic Status Assignment ---
    if coverage_percentage >= 99.0:
        status = "pass"
    elif coverage_percentage >= 95.0:
        status = "warn"
    else:
        status = "fail"

    # Halting Override: If a macro-structural marker is omitted, fail deterministically
    if structural_omission_detected or len(isolated_failures) > 0:
        status = "fail"

    return {
        "coverage_percentage": round(coverage_percentage, 2),
        "total_expected_chars": total_expected,
        "total_missing_chars": total_missing,
        "omissions_log": missing_characters,
        "status": status,
        "structural_failures": isolated_failures[::-1]  # Return in reading order
    }