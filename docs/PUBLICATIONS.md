# Automated Publication Management

This repository now includes an automated system for managing publications using BibTeX format.

## Overview

Instead of manually maintaining the publication list in `_includes/all_publications.md`, you can now:

1. Add publications to `_data/publications.bib` in standard BibTeX format
2. Run the generation script to automatically create the formatted markdown
3. Easily include links to arXiv, code repositories, and paper PDFs

## Quick Start

1. **Install dependencies:**
   ```bash
   make install
   ```

2. **Edit publications:**
   Add your publications to `_data/publications.bib`

3. **Generate the publication list:**
   ```bash
   make publications
   ```

4. **Optional: Set up Git hook for automatic generation:**
   ```bash
   git config core.hooksPath .githooks
   ```

## BibTeX Format

### Standard Fields
- `title`: Paper title
- `author`: Authors (standard BibTeX format)
- `year`: Publication year
- `booktitle`: Conference name (for @inproceedings)
- `journal`: Journal name (for @article)

### Custom Fields for Links
- `arxiv`: URL to arXiv preprint
- `paperurl`: URL to official paper (PDF/DOI)
- `code`: URL to code repository
- `status`: Either "preprint" or "accepted" (defaults to "accepted")

### Example Entry

```bibtex
@inproceedings{my_paper_2024,
  title={My Amazing Paper Title},
  author={Smith, John and Doe, Jane},
  booktitle={ICML},
  year={2024},
  arxiv={https://arxiv.org/abs/2401.00000},
  code={https://github.com/user/repo},
  status={accepted}
}
```

## Venue Mapping

The system automatically maps venue names to the proper format:
- `ACL` → `ACL'25`
- `KDD` → `KDD'24` or `KDD'25` (based on year)
- `IJCAI` → `IJCAI'25`
- `NeurIPS` → `Neurips'24`
- etc.

## File Structure

```
_data/
  publications.bib          # BibTeX source file
_includes/
  all_publications.md       # Generated markdown (don't edit manually)
scripts/
  generate_publications.py  # Generation script
requirements.txt            # Python dependencies
Makefile                   # Convenient commands
```

## Adding New Publications

1. Open `_data/publications.bib`
2. Add your new publication in BibTeX format
3. Set the `status` field to "preprint" or "accepted"
4. Add URLs for `arxiv`, `code`, and `paperurl` as needed
5. Run `make publications` to regenerate the list

## Customization

To modify the output format, edit `scripts/generate_publications.py`:

- **Venue mapping:** Update the `venue_map` dictionary in `format_venue()`
- **Link formatting:** Modify the `format_links()` function
- **Section organization:** Adjust the `generate_markdown()` function

## Troubleshooting

### Missing Dependencies
```bash
pip install bibtexparser==1.4.0
```

### BibTeX Parsing Errors
- Ensure proper BibTeX syntax
- Check for unmatched braces `{}`
- Verify all required fields are present

### Custom Venues
Add new venue mappings in the `venue_map` dictionary in `scripts/generate_publications.py`.

## Git Hook (Optional)

A pre-commit hook is provided that automatically regenerates the publication list when `_data/publications.bib` is modified:

1. **Enable the hook:**
   ```bash
   git config core.hooksPath .githooks
   ```

2. **How it works:**
   - When you commit changes to `_data/publications.bib`
   - The hook automatically runs `scripts/generate_publications.py`
   - The updated `_includes/all_publications.md` is added to your commit

This ensures the publication list is always up-to-date with your BibTeX file. 