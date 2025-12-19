# Implementation Notes

## Approach

I began by reviewing the BOQ Excel files to understand how work items are structured in practice. While the column layout was consistent across files, the meaning of a single work item was often spread across multiple rows. Headings, sub headings, and descriptive scope frequently appeared above the quantified line rather than on it.

To handle this correctly, I implemented a context aware parser with the following rules.

1. Rows with numeric QTY values are treated as the only actionable work items.
2. Rows without QTY are treated as contextual information rather than standalone items.
3. Fully uppercase descriptions are treated as sticky headings that apply to all subsequent quantified rows until replaced.
4. All context rows immediately preceding a quantified row are appended to that row’s description.

This results in one prediction per QTY row, while preserving the full semantic meaning that a quantity surveyor would naturally infer when reading the BOQ.

---

## Tag Normalization via LLM (Preprocessing Step)

Before performing final BOQ item classification, I introduced an explicit **tag normalization stage** using `tags_classification.py`. This step converts noisy, project-specific TAG values into a **clean, canonical trade taxonomy** using an LLM under strict constraints.

### Why this step exists

The raw `TAG` column in BOQs is inconsistent across projects:

* Vendor- or project-specific naming
* Abbreviations and shorthand
* Combined or overlapping scopes
* Missing or ambiguous values

Using these tags directly would reduce robustness and leak project-specific assumptions. Instead, they are treated as *weak signals* and normalized once into a stable vocabulary.

### How `tags_classification.py` works

1. **Extraction**
   All unique raw TAG values across BOQ files are collected.

2. **LLM Classification**
   Each tag is sent to the LLM with:

   * The same **fixed allowed trade list** used in final classification
   * Explicit instructions to return **exactly one trade**
   * A deterministic fallback to `General / Preliminaries`

3. **Output Artifact**
   The script outputs:

   `tags_classification_by_llm.csv`

   which contains:

   * `original_tag`
   * `normalized_trade`

4. **Frozen Lookup Table**
   This CSV is generated once and reused. It ensures that tag interpretation is:

   * Deterministic
   * Auditable
   * Decoupled from item-level inference

---

## Item-Level Trade Classification (main.py)

In `main.py`, each enriched BOQ item is classified as follows:

1. Context-aware description is constructed (headings + scope + line item)
2. The normalized tag lookup (`tags_classification_by_llm.csv`) is loaded
3. The LLM predicts **one trade** from the allowed list
4. The prediction is validated against the allowed taxonomy
5. Invalid outputs are safely mapped to `General / Preliminaries`

This two-stage design separates:

* **Taxonomy normalization** (tags)
* **Semantic understanding** (item descriptions)

---

## Technical Decisions

### Context Aware Parsing

Instead of treating each row independently, the parser accumulates headings and descriptive lines so that every quantified item carries its full scope and trade intent.

### Sticky Heading Detection

Uppercase-only rows are treated as section headers and retained until replaced. This mirrors how BOQs are structured and avoids losing high-level trade context.

### Fixed Trade List

A predefined trade list is used consistently across:

* Tag normalization
* Item classification
* Validation

This guarantees output consistency and prevents uncontrolled label drift.

### Deterministic LLM Usage

* Prompts are restrictive and schema-like
* Outputs are validated programmatically
* No free-form reasoning is consumed

This keeps the system explainable and production-safe.

---

## Trade-offs

1. Longer descriptions increase token usage but improve accuracy
2. A two-stage pipeline adds complexity but improves robustness
3. Items are processed independently to preserve traceability

---

## Ideas for Improvement

1. Add few-shot examples for very short descriptions
2. Add lightweight heuristics using units or materials
3. Batch LLM calls with strict output parsing to reduce cost
4. Introduce confidence scoring for human review

---

## Time Spent

* Data exploration & BOQ analysis: ~45 min
* Parsing & context modeling: ~50 min
* Tag normalization pipeline: ~40 min
* LLM integration & validation: ~90 min
* Testing & documentation: ~35 min

**Total: ~4 hours 20 minutes**
