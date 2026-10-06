#!/usr/bin/env python3
"""
Data Integrity Verification Script
For capstone submission reproducibility
"""

import json
import sys
from collections import Counter

def verify_qa_data():
    """Verify JSON data structure and completeness"""

    print("\n" + "="*80)
    print("📊 DATA INTEGRITY VERIFICATION FOR CAPSTONE SUBMISSION")
    print("="*80)

    try:
        with open('data/shopunow_qa_dataset.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ ERROR: data/shopunow_qa_dataset.json not found")
        return False
    except json.JSONDecodeError:
        print("❌ ERROR: JSON file is malformed")
        return False

    all_passed = True

    # Check 1: Total count
    print(f"\n✓ CHECK 1: Total Q&A Count")
    print(f"  Found: {len(data)} Q&As")
    print(f"  Expected: 52 Q&As")
    if len(data) == 52:
        print("  Status: ✅ PASS")
    else:
        print(f"  Status: ❌ FAIL (Expected 52, got {len(data)})")
        all_passed = False

    # Check 2: Department distribution
    depts = Counter(item['department'] for item in data)
    print(f"\n✓ CHECK 2: Department Distribution")

    expected_depts = {
        "HR": 15,
        "IT Support": 13,
        "Billing & Payments": 12,
        "Shipping & Delivery": 12
    }

    dept_pass = True
    for dept, expected_count in expected_depts.items():
        actual_count = depts.get(dept, 0)
        status = "✅" if actual_count == expected_count else "❌"
        print(f"  {status} {dept}: {actual_count} (expected {expected_count})")
        if actual_count != expected_count:
            dept_pass = False
            all_passed = False

    if dept_pass:
        print("  Status: ✅ PASS")
    else:
        print("  Status: ❌ FAIL")

    # Check 3: New curated entries
    print(f"\n✓ CHECK 3: New Curated Entries (4 additions)")

    new_entries = {
        "sick leave": {
            "keywords": ["sick leave"],
            "department": "HR",
            "found": False
        },
        "pto": {
            "keywords": ["pto", "personal time off"],
            "department": "HR",
            "found": False
        },
        "maternity": {
            "keywords": ["maternity", "paternity"],
            "department": "HR",
            "found": False
        },
        "hardware": {
            "keywords": ["monitor", "hardware"],
            "department": "IT Support",
            "found": False
        }
    }

    for item in data:
        q_lower = item['question'].lower()
        for entry_name, entry_info in new_entries.items():
            for keyword in entry_info['keywords']:
                if keyword in q_lower and item['department'] == entry_info['department']:
                    entry_info['found'] = True

    new_entries_pass = True
    for entry_name, entry_info in new_entries.items():
        status = "✅" if entry_info['found'] else "❌"
        print(f"  {status} {entry_name.upper()}: {entry_info['department']}")
        if not entry_info['found']:
            new_entries_pass = False
            all_passed = False

    if new_entries_pass:
        print("  Status: ✅ PASS (All 4 curated entries present)")
    else:
        print("  Status: ❌ FAIL (Some curated entries missing)")

    # Check 4: Required fields
    print(f"\n✓ CHECK 4: Data Structure Validation")

    required_fields = ['question', 'answer', 'department', 'audience']
    fields_pass = True

    for i, item in enumerate(data):
        for field in required_fields:
            if field not in item:
                print(f"  ❌ Item {i}: Missing field '{field}'")
                fields_pass = False
                all_passed = False

    if fields_pass:
        print(f"  ✅ All {len(data)} items have required fields")
        print("  Status: ✅ PASS")
    else:
        print("  Status: ❌ FAIL")

    # Check 5: Audience distribution
    print(f"\n✓ CHECK 5: Audience Distribution")
    audiences = Counter(item['audience'] for item in data)
    for audience, count in sorted(audiences.items()):
        print(f"  - {audience}: {count}")
    print("  Status: ✅ PASS")

    # Check 6: Department-audience mapping
    print(f"\n✓ CHECK 6: Department-Audience Mapping Consistency")

    expected_audience = {
        "HR": "Internal",
        "IT Support": "Internal",
        "Billing & Payments": "External",
        "Shipping & Delivery": "External"
    }

    mapping_pass = True
    for item in data:
        dept = item['department']
        audience = item['audience']
        expected = expected_audience[dept]

        if expected not in audience:
            print(f"  ❌ {dept}: has '{audience}', expected '{expected}'")
            mapping_pass = False
            all_passed = False

    if mapping_pass:
        print("  ✅ All departments match expected audiences")
        print("  Status: ✅ PASS")
    else:
        print("  Status: ❌ FAIL")

    # Final summary
    print("\n" + "="*80)
    if all_passed:
        print("✅ ALL CHECKS PASSED - DATA READY FOR CAPSTONE SUBMISSION")
        print("="*80)
        print("\nYou can confidently submit with this knowledge base:")
        print("  • 52 Q&As verified")
        print("  • 4 new curated entries confirmed")
        print("  • Proper department/audience mapping")
        print("  • All required fields present")
        print("  • Reproducible and transparent")
        return True
    else:
        print("❌ SOME CHECKS FAILED - FIX BEFORE SUBMISSION")
        print("="*80)
        return False

if __name__ == "__main__":
    success = verify_qa_data()
    sys.exit(0 if success else 1)
