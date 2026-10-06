# Reproducibility & Data Consistency Guide

**For Capstone Submission**

---

## Problem Statement

After manually updating the JSON with 4 new entries:
- ✅ `shopunow_qa_dataset.json` has 52 Q&As
- ⚠️ `data_generation.py` would generate NEW random data (not the same 52)
- ⚠️ `database.py` reads from JSON (OK if JSON is current)

**Goal:** Ensure reviewers can reproduce your exact work.

---

## Solution: JSON is the Source of Truth

### What This Means

```
┌─────────────────────────────────────────┐
│  shopunow_qa_dataset.json (Source)      │ ← MANUALLY CURATED
│  - 52 Q&As (4 custom + 48 original)     │ ← THIS IS GOLDEN
│  - Department metadata                   │
│  - Audience classification               │
└────────────────────────────────────────┘
              ↓
        (Read by)
              ↓
┌─────────────────────────────────────────┐
│  database.py                             │ ← DETERMINISTIC
│  (Embeds JSON into ChromaDB)             │ ← REPRODUCIBLE
└────────────────────────────────────────┘
```

**Key Point:** JSON file is what gets committed. It's the single source of truth.

---

## What to Document in Your Capstone

### 1. Data Generation Approach

In your capstone README, add:

```markdown
## Knowledge Base

The knowledge base consists of **52 Q&As** across 4 departments:
- **HR (15 Q&As):** Vacation, sick leave, PTO, maternity, health insurance, etc.
- **IT Support (13 Q&As):** Laptop, VPN, monitor, phishing, email, etc.
- **Billing & Payments (12 Q&As):** Invoices, refunds, payments, disputes
- **Shipping & Delivery (12 Q&As):** Tracking, returns, delivery, shipping

### Data Source

The dataset is stored in `data/shopunow_qa_dataset.json`. 

**Note on reproducibility:**
- The initial 48 Q&As were generated using `data_generation.py` with Groq LLM
- 4 additional Q&As were manually curated to address data gaps:
  - Sick leave policy
  - PTO/Personal time off policy
  - Maternity/Paternity leave policy
  - Hardware/Monitor request process

The JSON file is the authoritative source. To regenerate the database:
```bash
python database.py
```

This reads the JSON and embeds all 52 Q&As into ChromaDB.
```

---

## Verification Checklist

Create a file: `VERIFICATION_STEPS.md`

```markdown
# How to Verify the System Works

## Step 1: Verify JSON Data Exists
```bash
python -c "import json; data=json.load(open('data/shopunow_qa_dataset.json')); print(f'Total Q&As: {len(data)}')"
# Expected: Total Q&As: 52
```

## Step 2: Verify Specific New Entries
```bash
python -c "
import json
data = json.load(open('data/shopunow_qa_dataset.json'))
for item in data:
    if 'sick' in item['question'].lower():
        print('✓ Sick leave entry found')
    if 'pto' in item['question'].lower() or 'personal time' in item['question'].lower():
        print('✓ PTO entry found')
    if 'maternity' in item['question'].lower():
        print('✓ Maternity leave entry found')
    if 'monitor' in item['question'].lower() or 'hardware' in item['question'].lower():
        print('✓ Hardware request entry found')
"
```

## Step 3: Count by Department
```bash
python -c "
import json
from collections import Counter
data = json.load(open('data/shopunow_qa_dataset.json'))
depts = Counter(item['department'] for item in data)
for dept, count in sorted(depts.items()):
    print(f'{dept}: {count}')
"
# Expected output:
# Billing & Payments: 12
# HR: 15
# IT Support: 13
# Shipping & Delivery: 12
```

## Step 4: Regenerate Database
```bash
python database.py
# Should output: Successfully initialized ChromaDB with 52 documents
```

## Step 5: Run Local Test
```bash
python local_test.py "How do I apply for sick leave?"
# Should return the sick leave policy answer
```
```

---

## How to Handle Capstone Submission

### What to Include in Submission

```
shopnow/
├── data/
│   └── shopunow_qa_dataset.json          ← INCLUDE (52 Q&As, final version)
├── database.py                            ← INCLUDE (reads JSON → ChromaDB)
├── data_generation.py                     ← INCLUDE (documents original approach)
├── local_test.py                          ← INCLUDE (demonstrates system works)
├── REPRODUCIBILITY_GUIDE.md               ← INCLUDE (this file)
├── VERIFICATION_STEPS.md                  ← INCLUDE (how to verify)
└── README.md                              ← INCLUDE (with note about data sources)
```

### What to Tell Reviewers

In your capstone writeup:

> **Data Reproducibility**
>
> The knowledge base is stored in `data/shopunow_qa_dataset.json` and contains 52 Q&As:
>
> - Initial 48 Q&As were generated using LLM-assisted generation (`data_generation.py`)
> - 4 additional Q&As were manually curated to address identified data gaps in HR policies and IT hardware requests
>
> To verify the system with the exact dataset:
> ```bash
> python database.py          # Initialize ChromaDB
> python local_test.py "Your test query"  # Test locally
> ```
>
> The JSON file is the authoritative source for all knowledge base content.

---

## Why This Approach is Best

### ✅ Reproducibility
- Reviewers can clone your repo and run `python database.py`
- Same JSON → Same embeddings → Same system behavior

### ✅ Transparency
- JSON is human-readable
- Reviewers can inspect exact Q&As
- Shows domain knowledge curation

### ✅ Credibility
- Honest about manual curation vs. generated content
- Shows thoughtfulness in addressing data gaps
- Documents methodology clearly

### ✅ Future-Proof
- New entries are documented and preserved
- Easy to trace which Q&As were added/modified
- Reviewers can validate your improvements

---

## Git Commit Message Template

When committing the final JSON:

```
Add 4 curated Q&A entries for missing HR and IT policies

- Add sick leave policy (HR department)
- Add PTO/personal time off policy (HR department)  
- Add maternity/paternity leave policy (HR department)
- Add hardware request process (IT Support department)

Total Q&As: 48 → 52

These entries address identified data gaps revealed during initial testing.
The JSON file serves as the authoritative source for all knowledge base
content. To regenerate the embedded database, run:
  python database.py

Reproducibility verified:
- python database.py creates ChromaDB with 52 documents
- python local_test.py validates routing and retrieval logic
- All 4 new entries tested and working
```

---

## Data Integrity Check Script

Create: `verify_data_integrity.py`

```python
#!/usr/bin/env python3
"""Verify data consistency for capstone submission"""

import json
from collections import Counter

def verify_qa_data():
    """Verify JSON data structure and completeness"""
    
    with open('data/shopunow_qa_dataset.json', 'r') as f:
        data = json.load(f)
    
    print("="*80)
    print("DATA INTEGRITY VERIFICATION")
    print("="*80)
    
    # Check count
    print(f"\n✓ Total Q&As: {len(data)} (expected: 52)")
    assert len(data) == 52, f"Expected 52 Q&As, got {len(data)}"
    
    # Check departments
    depts = Counter(item['department'] for item in data)
    print(f"\n✓ Department Distribution:")
    for dept, count in sorted(depts.items()):
        print(f"  - {dept}: {count}")
    
    expected_depts = {
        "HR": 15,
        "IT Support": 13,
        "Billing & Payments": 12,
        "Shipping & Delivery": 12
    }
    
    for dept, expected_count in expected_depts.items():
        assert depts[dept] == expected_count, \
            f"{dept} has {depts[dept]}, expected {expected_count}"
    
    # Check new entries
    print(f"\n✓ New Curated Entries:")
    new_entries = {
        "sick leave": False,
        "pto": False,
        "personal time off": False,
        "maternity": False,
        "monitor": False,
        "hardware": False
    }
    
    for item in data:
        q_lower = item['question'].lower()
        for key in new_entries.keys():
            if key in q_lower:
                new_entries[key] = True
    
    for entry, found in new_entries.items():
        status = "✓" if found else "✗"
        print(f"  {status} {entry}")
        assert found, f"Missing entry: {entry}"
    
    # Check required fields
    print(f"\n✓ Data Structure:")
    for item in data:
        assert 'question' in item, "Missing 'question' field"
        assert 'answer' in item, "Missing 'answer' field"
        assert 'department' in item, "Missing 'department' field"
        assert 'audience' in item, "Missing 'audience' field"
    print("  All items have required fields")
    
    print("\n" + "="*80)
    print("✅ DATA INTEGRITY CHECK PASSED")
    print("="*80)
    print("\nReady for capstone submission!")

if __name__ == "__main__":
    verify_qa_data()
```

Run it:
```bash
python verify_data_integrity.py
```

---

## Summary for Capstone Submission

### Files to Include
- ✅ `shopunow_qa_dataset.json` (52 Q&As - final version)
- ✅ `database.py` (reproducibly creates ChromaDB)
- ✅ `REPRODUCIBILITY_GUIDE.md` (this file)
- ✅ `verify_data_integrity.py` (automated verification)
- ✅ Updated `README.md` (documents data sources)

### What Reviewers Can Do
```bash
# 1. Verify data
python verify_data_integrity.py

# 2. Regenerate database
python database.py

# 3. Test the system
python local_test.py "How do I apply for sick leave?"
```

### Bottom Line
**The JSON file is your source of truth. Everything flows from there.**
- Reproducible ✅
- Transparent ✅
- Professional ✅
- Honest about manual curation ✅

This approach shows you did thoughtful work and can prove it!
