from __future__ import annotations
import fitz  # PyMuPDF
import logging
from typing import Literal

# Setup logging for the triage system
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("ViteGrid.Stage1")

class TriageStatus:
    """Enum-like constants for document classification states."""
    NATIVE_TEXT = "NATIVE_TEXT"
    SCANNED_IMAGE = "SCANNED_IMAGE"
    GARBLED_CORRUPTION = "GARBLED_CORRUPTION"
    
    # Backward compatibility aliases
    NATIVE = "NATIVE_TEXT"
    SCANNED = "SCANNED_IMAGE"
    GARBLED = "GARBLED_CORRUPTION"

def is_scanned(page: fitz.Page) -> bool:
    """
    The core heuristic function that determines if a page is a rasterized scan.
    """
    # 1. Character Count Thresholds
    extracted_text = page.get_text("text").strip()
    text_len = len(extracted_text)
    if text_len < 45:
        return True
        
    # 2. Image Density Mapping
    page_area = page.rect.width * page.rect.height
    max_image_area = 0.0
    
    # Get image info using page.get_image_info() to get bounding boxes (bbox)
    for img in page.get_image_info():
        bbox = fitz.Rect(img["bbox"])
        img_area = bbox.width * bbox.height
        if img_area > max_image_area:
            max_image_area = img_area
            
    if page_area > 0 and (max_image_area / page_area) > 0.95:
        return True
        
    # 3. Microscopic Vector Graphics Detection
    vector_drawings = page.get_drawings()
    if len(vector_drawings) > 1000:
        return True
        
    return False

class AlgorithmicTriage:
    """
    Stage 1: Algorithmic Triage and Heuristic Detection.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def _check_library_warnings(self) -> bool:
        """Intercepts background library warnings to detect CID corruption."""
        warnings = fitz.TOOLS.mupdf_warnings(True)
        if not warnings:
            return False
            
        corruption_flags = [
            "unknown cid collection", "broken table", "ignored error when loading embedded font"
        ]
        warnings_lower = warnings.lower()
        for flag in corruption_flags:
            if flag in warnings_lower:
                logger.error(f"Corruption flag triggered: {flag}")
                return True
        return False

    def execute(self) -> Literal["NATIVE_TEXT", "SCANNED_IMAGE", "GARBLED_CORRUPTION"]:
        fitz.TOOLS.mupdf_warnings(True)
        try:
            doc = fitz.open(self.file_path)
        except Exception as e:
            logger.error(f"Failed to open document: {e}")
            return TriageStatus.GARBLED_CORRUPTION
            
        if self._check_library_warnings():
            doc.close()
            logger.warning("Garbled document detected via MUPDF warnings at open. Aborting digital extraction.")
            return TriageStatus.GARBLED_CORRUPTION
            
        page_count = len(doc)
        if page_count == 0:
            doc.close()
            return TriageStatus.NATIVE_TEXT
            
        total_text_length = 0
        try:
            for page in doc:
                page_text = page.get_text("text").strip()
                total_text_length += len(page_text)
                
                # Check library warnings during text extraction
                if self._check_library_warnings():
                    logger.warning(f"Garbled document detected via MUPDF warnings on page {page.number}. Aborting.")
                    return TriageStatus.GARBLED_CORRUPTION
                
                # 4. Corruption Detection (U+FFFD and TOFU density)
                replacement_char_count = page_text.count("\ufffd")
                
                # Count unreadable/TOFU symbols (control chars except whitespaces, and PUA range)
                tofu_count = 0
                for char in page_text:
                    if (ord(char) < 32 and char not in "\n\r\t") or (0xe000 <= ord(char) <= 0xf8ff):
                        tofu_count += 1
                        
                total_len = len(page_text)
                if total_len > 0:
                    tofu_density = tofu_count / total_len
                    fffd_density = replacement_char_count / total_len
                    if replacement_char_count > 10 or tofu_density > 0.15 or fffd_density > 0.10:
                        logger.warning(
                            f"Extreme TOFU/U+FFFD density detected on page {page.number} "
                            f"(TOFU density: {tofu_density:.2f}, FFFD count: {replacement_char_count})."
                        )
                        return TriageStatus.GARBLED_CORRUPTION
                    
                if is_scanned(page):
                    logger.info(f"Page {page.number} flagged as scanned/heuristic mismatch.")
                    return TriageStatus.SCANNED_IMAGE
        finally:
            doc.close()
            
        if (total_text_length / page_count) < 45:
            return TriageStatus.SCANNED_IMAGE
            
        logger.info("Document classified as Digital-Native Text.")
        return TriageStatus.NATIVE_TEXT