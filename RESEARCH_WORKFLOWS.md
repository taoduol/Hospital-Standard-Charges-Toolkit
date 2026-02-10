# Research Workflows & Data Extraction

This is a space for researchers to share how they extract, clean, and analyze hospital billing data.

## Why This Matters

Hospital billing files are inconsistently formatted:
- Different column names across hospitals
- Missing data handled differently
- Error records that need filtering
- Different data quality standards

**There's no "one way" to clean this data** — it depends on your research question.

This document collects real workflows so other researchers can:
- See what others are doing
- Adapt approaches to their needs
- Share code and techniques
- Contribute improvements

---

## Template: Share Your Workflow

**Post in GitHub Discussions with this format:**

### Title
"Extracting [drug prices/equipment costs/etc] from [hospital type/region]"

### Your Approach
What are you trying to extract? Why?
```
Example: Extracting chemotherapy drug prices from NCI-designated cancer centers
to compare costs across institutions for a policy analysis.
```

### Data Quality Issues You Found
What problems did you encounter?
```
Example:
- Yale New Haven includes bundled procedure codes mixed with drug codes
- Missing units for 30% of entries
- Price ranges instead of single prices in some entries
```

### Your Solution
How did you handle it?
```
Example Python pseudocode:
1. Filter by procedure code prefix (e.g., "J" = injectable)
2. For missing units, infer from hospital coding standards
3. For price ranges, use midpoint or exclude from analysis
4. Document all filtering decisions in audit log
```

### Code/Tools
Share a link to your code or a code snippet

### Lessons Learned
What would you do differently? What worked well?

---

## Example Workflows (To Be Added By Community)

### Example 1: Cancer Drug Prices (Oncology Research)

**Researcher:** [Your name]  
**Hospitals:** NCI-designated centers  
**Goal:** Compare chemotherapy costs

**Approach:**
- Filtered for J-codes (drugs) only
- Excluded outliers >3 SD from mean
- Created hospital comparison matrix
- Validated against prior published data

**Key Issues Found:**
- Hospital A doesn't list unit prices (bundle only)
- Hospital B includes markup percentages  
- Hospital C has duplicate entries

**Solution Code:**
[Link to GitHub Gist or file]

---

## General Tips

### Data Integrity Checklist
- [ ] Document your data source (hospital + download date)
- [ ] Record original file hash or size
- [ ] Keep a copy of the original CSV
- [ ] Log all filtering/transformation decisions
- [ ] Note which records you excluded and why
- [ ] Validate your output against a sample of originals

### Common Pitfalls
- **Aggregating without checking units** — Some prices are per unit, others are bundles
- **Assuming consistent structure** — Each hospital names columns differently
- **Ignoring error flags** — Hospitals often include quality/source indicators
- **Merging across different dates** — Prices change frequently

### Tools Researchers Are Using
- Python (pandas): Most common for batch processing
- R (readr, tidyr): For statistical validation
- Spreadsheet + careful manual checking: For smaller datasets
- SQL: For cross-hospital comparisons

---

## Contributing Your Workflow

1. **Create a GitHub Discussion** (Discussions tab)
2. **Use the template above**
3. **Include code** (as GitHub Gist or inline)
4. **Share your challenges** — this helps others

---

## FAQ: Data Cleaning

**Q: Should I include the original files in my repo?**  
A: No. Keep your analysis code + metadata. Original files should come from this tool for reproducibility.

**Q: The hospital updated their file. Should I re-download?**  
A: Yes. Document the old vs new in your audit log. This is why download dates matter.

**Q: How do I validate my extraction?**  
A: Compare your output against the original file for a sample of rows. Document your validation approach.

**Q: Can I combine data from multiple hospitals?**  
A: Yes, but carefully. Document any transformations. Never assume column meanings are identical across hospitals.

---

## Becoming a Contributor

If you develop a general-purpose extraction tool (e.g., "Extract all drug prices from any hospital file"), consider:
1. Creating a separate repository (e.g., `hospital-data-extractor`)
2. Link it here in this file
3. Make it modular so others can adapt it

---

**Questions?** Open an issue or start a Discussion.

**Want to add your workflow?** Submit a Pull Request editing this file!
