"""
Coordinate Projection Transforms & Structural-Relative Node Tracking

Manages bidirectional mapping and structural stabilization between three coordinate spaces:
1. PDF space: Absolute unrotated page pixels (0,0 = bottom-left, Y increases upward)
2. VLM space: Normalized integer [0-1000]² representing virtual canvas (0,0 = top-left)
3. CSS space: Physical pixels in web viewport (0,0 = top-left)

References: High-Fidelity Document Reconstruction specification, Phase 3 Spatiotemporal Alignment
"""

from typing import Tuple, Dict, Any, Optional, List
from dataclasses import dataclass
import math


@dataclass
class StructuralNodeInterval:
    """Represents a genomic-style zero-based, half-open interval for a document node."""
    node_id: str
    start_token_idx: int
    end_token_idx: int
    
    def contains_index(self, idx: int) -> bool:
        # Zero-based, half-open interval logic: inclusive of start, exclusive of end
        return self.start_token_idx <= idx < self.end_token_idx

    def shift_interval(self, offset: int) -> None:
        """Adjusts boundaries cleanly to isolate upstream sequence mutations."""
        self.start_token_idx += offset
        self.end_token_idx += offset


class StructuralRelativeTracker:
    """
    Firewalls Layout Space from token modifications by mapping physical canvas 
    coordinates directly to discrete structural node identifiers rather than volatile string indices.
    """
    def __init__(self, page_width_px: float = 816.0, page_height_px: float = 1056.0):
        self.page_width_px = page_width_px
        self.page_height_px = page_height_px
        self.registry: Dict[str, StructuralNodeInterval] = {}
        self.node_order: List[str] = []

    def register_node(self, node_id: str, start_idx: int, end_idx: int) -> None:
        """Maps an immutable Node ID to a zero-based half-open text interval."""
        interval = StructuralNodeInterval(node_id, start_idx, end_idx)
        self.registry[node_id] = interval
        if node_id not in self.node_order:
            self.node_order.append(node_id)

    def handle_sequence_mutation(self, failing_node_id: str, new_length: int) -> None:
        """
        Adjusts subsequent tracking intervals when a localized node updates its content length,
        permanently preventing downstream index shifting and layout corruption.
        """
        if failing_node_id not in self.registry:
            return
            
        current_interval = self.registry[failing_node_id]
        old_length = current_interval.end_token_idx - current_interval.start_token_idx
        delta = new_length - old_length
        
        # Update target node boundary
        current_interval.end_token_idx = current_interval.start_token_idx + new_length
        
        # Cascade transformation shift exclusively to downstream nodes
        start_shifting = False
        for node_id in self.node_order:
            if start_shifting:
                self.registry[node_id].shift_interval(delta)
            if node_id == failing_node_id:
                start_shifting = True


def apply_affine_projection(
    bbox_coords: Tuple[float, float, float, float], 
    scale_x: float, 
    scale_y: float, 
    translation_vector: Tuple[float, float]
) -> Tuple[float, float, float, float]:
    """
    Executes a 2D affine transformation matrix over matched node coordinates 
    to convert structural geometries smoothly into final layout canvases.
    
    [x_new]   [scale_x     0    ] [x_old]   [trans_x]
    [y_new] = [   0     scale_y ] [y_old] + [trans_y]
    """
    x0, y0, x1, y1 = bbox_coords
    tx, ty = translation_vector
    
    x0_new = (x0 * scale_x) + tx
    y0_new = (y0 * scale_y) + ty
    x1_new = (x1 * scale_x) + tx
    y1_new = (y1 * scale_y) + ty
    
    return x0_new, y0_new, x1_new, y1_new


def pdf_to_vlm_coords(
    x_pdf: float, y_pdf: float, page_width_pt: float, page_height_pt: float
) -> Tuple[int, int]:
    """Convert PDF page coordinates to VLM normalized space [0-1000]²."""
    y_flipped = page_height_pt - y_pdf
    x_norm = (x_pdf / page_width_pt) * 1000
    y_norm = (y_flipped / page_height_pt) * 1000
    x_int = round(max(0, min(1000, x_norm)))
    y_int = round(max(0, min(1000, y_norm)))
    return x_int, y_int


def vlm_to_css_coords(
    x_norm: int, y_norm: int, viewport_width_px: float, viewport_height_px: float
) -> Tuple[float, float]:
    """Convert VLM normalized coordinates to CSS pixel space."""
    x_css = (x_norm / 1000.0) * viewport_width_px
    y_css = (y_norm / 1000.0) * viewport_height_px
    return x_css, y_css


def css_to_vlm_coords(
    x_css: float, y_css: float, viewport_width_px: float, viewport_height_px: float
) -> Tuple[int, int]:
    """Convert CSS pixel coordinates to VLM normalized space."""
    x_norm = (x_css / viewport_width_px) * 1000
    y_norm = (y_css / viewport_height_px) * 1000
    x_int = round(max(0, min(1000, x_norm)))
    y_int = round(max(0, min(1000, y_norm)))
    return x_int, y_int


def ioa_score(
    bbox1: Tuple[float, float, float, float], bbox2: Tuple[float, float, float, float]
) -> float:
    """Compute Intersection-over-Area (IoA) metric for two bounding boxes."""
    x0_1, y0_1, x1_1, y1_1 = bbox1
    x0_2, y0_2, x1_2, y1_2 = bbox2
    inter_x0 = max(x0_1, x0_2)
    inter_y0 = max(y0_1, y0_2)
    inter_x1 = min(x1_1, x1_2)
    inter_y1 = min(y1_1, y1_2)
    if inter_x1 <= inter_x0 or inter_y1 <= inter_y0:
        return 0.0
    inter_area = (inter_x1 - inter_x0) * (inter_y1 - inter_y0)
    bbox2_area = (x1_2 - x0_2) * (y1_2 - y0_2)
    if bbox2_area == 0:
        return 0.0
    return inter_area / bbox2_area