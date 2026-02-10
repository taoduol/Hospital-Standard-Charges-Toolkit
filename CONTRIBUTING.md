# Contributing Guide

Thank you for helping maintain this resource! Here's how to contribute.

## 🏥 Updating or Adding Hospital Data

### For Researchers: Report Broken Links

**See an outdated link?** Create an Issue:

1. Go to Issues tab
2. Title: "Update needed: [Hospital Name]"
3. Include:
   - Hospital name
   - Current URL (if you found it)
   - When you last verified it worked
   - Screenshot of the billing page (optional)

**We'll update it and credit you!**

---

### For Contributors: Update Hospitals Config

#### Step 1: Verify the Hospital's Billing Page

1. Go to hospital website
2. Find: Billing → Insurance → Pricing/Standard Charges
3. Copy the billing page URL

#### Step 2: Find the Direct File Link

1. On the billing page, look for a button/link to download the machine-readable file (JSON, CSV, or .ashx)
2. Right-click → "Copy Link"
3. Test the link in your browser to confirm it works
4. **Important:** If the file downloads as CSV but the URL ends in .ashx/.json, that's normal — note both

#### Step 3: Edit hospitals_config.json

Add your hospital entry:

```json
{
  "name": "Hospital Full Legal Name",
  "short_name": "hospital-abbreviation",
  "billing_page": "https://hospital.com/billing-pricing-page",
  "file_url": "https://hospital.com/path/to/standard-charges.csv",
  "last_verified": "2024-02-10",
  "notes": "CSV format, includes bundled codes. Contact: billing@hospital.com"
}
```

**Rules:**
- `short_name`: lowercase, hyphens only (no spaces/underscores)
- `billing_page`: The human-readable page where you found the link
- `file_url`: The direct download link
- `last_verified`: Today's date (YYYY-MM-DD)
- `notes`: Any quirks about the data (format, known issues, contact info)

#### Step 4: Test It

```bash
python3 download_charges.py hospital-short-name
```

You should see:
```
✓ Downloaded file to hospital_charges_data/hospital-short-name/2024-02-10/...
```

#### Step 5: Submit a Pull Request

1. Fork this repository
2. Create a branch: `git checkout -b add-hospital-name`
3. Edit `hospitals_config.json` with your hospital(s)
4. Commit: `git commit -m "Add: Hospital Name - verified 2024-02-10"`
5. Push and create a Pull Request

---

## 🔍 What Makes a Good Contribution

**Include in your PR:**
- [ ] The hospital's name is clearly spelled
- [ ] The billing page URL is public (no login required)
- [ ] The file URL is tested and works
- [ ] You used today's date in `last_verified`
- [ ] The `short_name` follows naming conventions
- [ ] You added any relevant notes about data quirks

**Common Issues to Note:**
- "Hospital doesn't publish machine-readable prices" ← That's okay! Mark as `file_url: null`
- "File is behind a form/registration" ← Note this in `notes` field
- "Prices are by diagnosis, not by item" ← Helpful for researchers to know
- "File updates monthly on X day" ← Note the update frequency

---

## 📋 Data Integrity Standards

When adding/updating hospitals:

### Test Checklist
- [ ] Downloaded file is not empty
- [ ] File opens in Excel or text editor without errors
- [ ] File size seems reasonable (not a web page)
- [ ] File contains pricing data (not just instructions)
- [ ] URL works when you paste it directly in browser

### Documentation
- [ ] Note any known data quality issues
- [ ] Include hospital contact/billing info if available
- [ ] Mention if this is a new hospital or an update
- [ ] Flag if file format changed from previous version

---

## 🐛 Reporting Issues

**Found a broken link?**
- Create an Issue with title: "Broken: [Hospital Name]"
- Include: URL, error message, date you tried

**Hospital changed their file format?**
- Create an Issue: "Format change: [Hospital Name]"
- Include: Old format, new format, date noticed

**Data looks wrong?**
- Create an Issue: "Data quality: [Hospital Name]"
- Include: Specific example of the problem
- Note: We don't validate data — you might need to research if the hospital's data is actually wrong

---

## 💡 Future Contributions

**Things that help:**
- [ ] Curated lists of hospitals by region/type (e.g., "All NCI cancer centers")
- [ ] Automated URL checker script (periodically tests if links still work)
- [ ] Better documentation of hospital-specific quirks
- [ ] Integration with health databases for hospital metadata

**Things we don't do here:**
- Extraction code (see RESEARCH_WORKFLOWS.md instead)
- Data validation/cleaning logic
- Analysis or comparisons
- Hosted data downloads

---

## ❓ Questions?

- Read [README.md](README.md) for usage questions
- See [RESEARCH_WORKFLOWS.md](RESEARCH_WORKFLOWS.md) for extraction help
- Create an Issue for anything else

**Thank you for helping researchers access this data!** ✓
