# Graph Report - vitegrid-main  (2026-06-06)

## Corpus Check
- 41 files · ~357,265 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 674 nodes · 1735 edges · 38 communities (29 shown, 9 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 183 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5a14eaa7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Agent Layout & Style Pipeline|Agent Layout & Style Pipeline]]
- [[_COMMUNITY_Document PDFDocx Parser Engine|Document PDF/Docx Parser Engine]]
- [[_COMMUNITY_Frontend UI Components & State|Frontend UI Components & State]]
- [[_COMMUNITY_Backend FastAPI API & DB Storage|Backend FastAPI API & DB Storage]]
- [[_COMMUNITY_Layout Audit Programmatic Tests|Layout Audit Programmatic Tests]]
- [[_COMMUNITY_Frontend Package Configuration|Frontend Package Configuration]]
- [[_COMMUNITY_Frontend TypeScript Config|Frontend TypeScript Config]]
- [[_COMMUNITY_Image Pipeline Integration Tests|Image Pipeline Integration Tests]]
- [[_COMMUNITY_Remediation & Correction Tests|Remediation & Correction Tests]]
- [[_COMMUNITY_Parser V2 PDF Parsing Tests|Parser V2 PDF Parsing Tests]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Frontend Node build tsconfig|Frontend Node build tsconfig]]
- [[_COMMUNITY_VLM Coordinate Transformations|VLM Coordinate Transformations]]
- [[_COMMUNITY_Frontend Docx Validation Metrics|Frontend Docx Validation Metrics]]
- [[_COMMUNITY_Margin Verification Scripts|Margin Verification Scripts]]
- [[_COMMUNITY_Backend Core Library Dependencies|Backend Core Library Dependencies]]
- [[_COMMUNITY_SSE Live Streaming Response|SSE Live Streaming Response]]
- [[_COMMUNITY_Document Text Loss Verification|Document Text Loss Verification]]
- [[_COMMUNITY_Workspace Pyright Settings|Workspace Pyright Settings]]
- [[_COMMUNITY_Backend Pyright Config|Backend Pyright Config]]
- [[_COMMUNITY_Backend VS Code Config|Backend VS Code Config]]
- [[_COMMUNITY_Workspace VS Code Config|Workspace VS Code Config]]
- [[_COMMUNITY_Graphify Rule Config|Graphify Rule Config]]
- [[_COMMUNITY_Frontend HTML Entrypoint|Frontend HTML Entrypoint]]
- [[_COMMUNITY_Uploaded Image Assets|Uploaded Image Assets]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]

## God Nodes (most connected - your core abstractions)
1. `str` - 37 edges
2. `StructuralRelativeTracker` - 37 edges
3. `BaseModel` - 33 edges
4. `DocumentLayout` - 31 edges
5. `TextSpan` - 26 edges
6. `Any` - 24 edges
7. `Template` - 23 edges
8. `ImageAsset` - 23 edges
9. `str` - 23 edges
10. `classify_pdf_layout()` - 23 edges

## Surprising Connections (you probably didn't know these)
- `DocumentBlock` --uses--> `BlockType`  [INFERRED]
  D:/vitegrid/vitegrid-backend/tests/test_audit_programmatic.py → vitegrid-backend/agent.py
- `DocumentBlock` --uses--> `StyleTokens`  [INFERRED]
  D:/vitegrid/vitegrid-backend/tests/test_audit_programmatic.py → vitegrid-backend/agent.py
- `DocumentBlock` --uses--> `BoundingBox`  [INFERRED]
  D:/vitegrid/vitegrid-backend/tests/test_audit_programmatic.py → vitegrid-backend/agent.py
- `DocumentBlock` --uses--> `DocumentBlock`  [INFERRED]
  D:/vitegrid/vitegrid-backend/tests/test_audit_programmatic.py → vitegrid-backend/agent.py
- `DocumentBlock` --uses--> `DocumentLayout`  [INFERRED]
  D:/vitegrid/vitegrid-backend/tests/test_audit_programmatic.py → vitegrid-backend/agent.py

## Communities (38 total, 9 thin omitted)

### Community 0 - "Agent Layout & Style Pipeline"
Cohesion: 0.05
Nodes (134): Client, DocumentLayout, Enum, GenerateContentConfig, generateFromPrompt(), str, agent1_structural_parse(), agent2_style_evaluate() (+126 more)

### Community 1 - "Document PDF/Docx Parser Engine"
Cohesion: 0.05
Nodes (111): bool, float, str, DocumentConverter, PageLayout, PdfExtraction, RGBColor, case_column_collision_prevention() (+103 more)

### Community 2 - "Frontend UI Components & State"
Cohesion: 0.13
Nodes (22): alignmentFor(), ASTNode, blockToChildren(), cellPaddingFor(), CodeBlockNode, compileToDocx(), createSafeParagraph(), CustomFonts (+14 more)

### Community 3 - "Backend FastAPI API & DB Storage"
Cohesion: 0.09
Nodes (53): Dashboard(), Props, Session, DeclarativeBase, FastAPI, getTemplate(), importLayout(), jsonOrThrow() (+45 more)

### Community 4 - "Layout Audit Programmatic Tests"
Cohesion: 0.15
Nodes (33): bool, int, str, DocumentBlock, case_clean_layout(), case_color_standardization(), case_filter_strips_llm_bottom_edge_messages(), case_font_bounds() (+25 more)

### Community 5 - "Frontend Package Configuration"
Cohesion: 0.08
Nodes (25): dependencies, docx, file-saver, highlight.js, react, react-dom, devDependencies, autoprefixer (+17 more)

### Community 6 - "Frontend TypeScript Config"
Cohesion: 0.10
Nodes (19): compilerOptions, allowSyntheticDefaultImports, esModuleInterop, isolatedModules, jsx, lib, module, moduleResolution (+11 more)

### Community 7 - "Image Pipeline Integration Tests"
Cohesion: 0.24
Nodes (21): Any, bool, Path, str, _approved_audit_json(), case_mime_detection(), case_missing_file(), case_partial_block_backfilled_by_defaults() (+13 more)

### Community 8 - "Remediation & Correction Tests"
Cohesion: 0.20
Nodes (19): bool, str, case_empty_inputs(), case_intra_word_merge_basic(), case_intra_word_merge_with_kerning_overlap(), case_line_breaks_preserved(), case_prompt_topology_constraints(), case_resume_skill_row_no_fragmentation() (+11 more)

### Community 10 - "Community 10"
Cohesion: 0.23
Nodes (13): ChatEditor(), ChatTurn, Props, chatWithAgent(), App(), EMPTY_LAYOUT, isImage(), isPdf() (+5 more)

### Community 11 - "Frontend Node build tsconfig"
Cohesion: 0.15
Nodes (12): compilerOptions, allowSyntheticDefaultImports, composite, emitDeclarationOnly, lib, module, moduleResolution, outDir (+4 more)

### Community 12 - "VLM Coordinate Transformations"
Cohesion: 0.10
Nodes (23): apply_affine_projection(), css_to_vlm_coords(), ioa_score(), pdf_to_vlm_coords(), bool, float, int, str (+15 more)

### Community 13 - "Frontend Docx Validation Metrics"
Cohesion: 0.23
Nodes (11): calculateColorMatch(), calculateFontMatch(), calculateSpacingDeviation(), calculateTextCoverage(), generateValidationReport(), MANUAL_REVIEW_CHECKLIST, NodeIntervalMap, PixelComparisonResult (+3 more)

### Community 14 - "Margin Verification Scripts"
Cohesion: 0.57
Nodes (6): assert(), caseFixedCompilerOutput(), caseMarginEmu(), pxToDxa(), pxToEmu(), unzipDocx()

### Community 15 - "Backend Core Library Dependencies"
Cohesion: 0.29
Nodes (7): Docling, FastAPI, Google GenAI, Playwright, Pydantic, Backend Requirements, SQLAlchemy

### Community 16 - "SSE Live Streaming Response"
Cohesion: 0.33
Nodes (6): demo_iteration_generator(), str, Server-Sent Events (SSE) Streaming for Document Reconstruction, Simulated optimization loop for demo purposes., Formats SSE event dicts as text according to SSE specification., sse_formatter()

### Community 17 - "Document Text Loss Verification"
Cohesion: 0.23
Nodes (11): is_structural_token(), Any, bool, str, Text-Loss Verification Engine - Validates Docling doesn't omit characters or mac, Compare PyMuPDF ground-truth character stream with Docling parsed structure., Tokenizes text into structural markers, words, space sequences, and individual s, Determines if a token corresponds to a macro-structural anchor (procedural list (+3 more)

### Community 18 - "Workspace Pyright Settings"
Cohesion: 0.60
Nodes (3): extraPaths, venv, venvPath

### Community 19 - "Backend Pyright Config"
Cohesion: 0.60
Nodes (3): extraPaths, venv, venvPath

### Community 30 - "Community 30"
Cohesion: 0.12
Nodes (15): Align, BlockType, BoundingBox, CellPaddingDxa, DEFAULT_SPACING_TOKENS, DEFAULT_STYLE_TOKENS, FontWeight, LineRule (+7 more)

### Community 31 - "Community 31"
Cohesion: 0.23
Nodes (7): HeadlessPreview(), BADGE_STYLES, BadgeProps, LiveRender(), Props, RenderedBlock(), styleToCss()

### Community 32 - "Community 32"
Cohesion: 0.35
Nodes (11): bool, int, Path, str, case_closed_loop_optimization(), case_visual_regression_differences(), case_visual_regression_identical(), create_solid_image() (+3 more)

### Community 33 - "Community 33"
Cohesion: 0.38
Nodes (9): HistoryPanel(), Props, clone(), EditorAction, editorReducer(), EditorState, initEditorState(), timelineIndex() (+1 more)

### Community 34 - "Community 34"
Cohesion: 0.48
Nodes (3): HoneyModule, load_script(), str

### Community 35 - "Community 35"
Cohesion: 0.80
Nodes (4): Props, TextEditor(), TYPE_LABEL, DocumentBlock

## Knowledge Gaps
- **111 isolated node(s):** `python.defaultInterpreterPath`, `python.analysis.extraPaths`, `bool`, `Session`, `DocumentConverter` (+106 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `generateFromPrompt()` connect `Agent Layout & Style Pipeline` to `Backend FastAPI API & DB Storage`?**
  _High betweenness centrality (0.153) - this node is a cross-community bridge._
- **Why does `optimize_template_closed_loop()` connect `Agent Layout & Style Pipeline` to `Document PDF/Docx Parser Engine`?**
  _High betweenness centrality (0.103) - this node is a cross-community bridge._
- **Why does `classify_pdf_layout()` connect `Document PDF/Docx Parser Engine` to `Agent Layout & Style Pipeline`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `StructuralRelativeTracker` (e.g. with `Client` and `GenerateContentConfig`) actually correct?**
  _`StructuralRelativeTracker` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `DocumentLayout` (e.g. with `DocumentBlock` and `DocumentLayout`) actually correct?**
  _`DocumentLayout` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `python.defaultInterpreterPath`, `python.analysis.extraPaths`, `Stateful Bidirectional Masking Pipeline for Algorithmic Interdiction.          U` to the rest of the system?**
  _205 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Agent Layout & Style Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.052890771200630356 - nodes in this community are weakly interconnected._