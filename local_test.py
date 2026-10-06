#!/usr/bin/env python3
"""
Local Test Script - Tests routing and retrieval WITHOUT external API calls
Perfect for testing when network is blocked
"""

import json
import sys
from pathlib import Path

# Load the knowledge base
with open('data/shopunow_qa_dataset.json', 'r') as f:
    kb_data = json.load(f)

def test_query(query, expected_dept=None):
    """Test a query locally by matching against KB"""

    print("="*80)
    print(f"Testing Query: {query}")
    print("="*80)

    # Simple sentiment detection
    negative_keywords = ['furious', 'terrible', 'worst', 'angry', 'hate', 'horrible', 'awful']
    sentiment = "NEGATIVE" if any(word in query.lower() for word in negative_keywords) else "POSITIVE/NEUTRAL"

    print(f"\n1️⃣  SENTIMENT DETECTION:")
    print(f"   Input: {query}")
    print(f"   Detected: {sentiment}")

    # Simple department detection (keyword based for demo)
    dept_keywords = {
        "HR": ["vacation", "leave", "sick", "pto", "personal time", "health insurance", "maternity", "payroll", "performance review", "training"],
        "IT Support": ["laptop", "slow", "vpn", "password", "printer", "email", "phishing", "two-factor", "monitor", "hardware"],
        "Billing & Payments": ["invoice", "refund", "payment", "overcharge", "billing", "charge"],
        "Shipping & Delivery": ["track", "order", "delivery", "return", "ship", "address"],
    }

    detected_dept = None
    for dept, keywords in dept_keywords.items():
        if any(keyword in query.lower() for keyword in keywords):
            detected_dept = dept
            break

    if not detected_dept:
        detected_dept = "UNKNOWN"

    print(f"\n2️⃣  DEPARTMENT CLASSIFICATION:")
    print(f"   Detected: {detected_dept}")

    # Check escalation conditions
    should_escalate = False
    escalation_reason = None

    if sentiment == "NEGATIVE":
        should_escalate = True
        escalation_reason = "Negative sentiment detected"
    elif detected_dept == "UNKNOWN":
        should_escalate = True
        escalation_reason = "Department unknown/out of scope"

    print(f"\n3️⃣  ROUTING DECISION:")
    if should_escalate:
        print(f"   ✅ ESCALATE TO HUMAN AGENT")
        print(f"   Reason: {escalation_reason}")
        print(f"\n   Response: Your query has been escalated to a human support agent. They will reach out to you shortly.")
        return

    print(f"   ✅ ROUTE TO RAG (Retrieval-Augmented Generation)")

    # Search KB for matching answers
    print(f"\n4️⃣  KNOWLEDGE BASE RETRIEVAL:")
    print(f"   Department Filter: {detected_dept}")

    matching_answers = []
    for item in kb_data:
        if item['department'] == detected_dept:
            # Simple keyword matching
            query_words = set(query.lower().split())
            kb_words = set(item['question'].lower().split())

            # Calculate overlap
            overlap = len(query_words & kb_words) / len(query_words) if query_words else 0

            # Check for key term matches
            has_key_term = any(word in item['question'].lower() for word in query_words if len(word) > 4)

            if overlap > 0.3 or has_key_term:
                matching_answers.append({
                    'question': item['question'],
                    'answer': item['answer'],
                    'score': overlap
                })

    if matching_answers:
        best_match = sorted(matching_answers, key=lambda x: x['score'], reverse=True)[0]
        print(f"   ✅ MATCH FOUND:")
        print(f"   KB Question: {best_match['question']}")
        print(f"   Relevance: HIGH")

        print(f"\n5️⃣  RESPONSE:")
        print(f"   {best_match['answer']}")
    else:
        print(f"   ❌ NO MATCH IN KB")
        print(f"\n5️⃣  RESPONSE (ABSTENTION):")
        print(f"   I don't have enough information in the ShopUNow knowledge base to answer this accurately.")

    print("\n" + "="*80)


def main():
    if len(sys.argv) > 1:
        # If query provided as argument
        query = sys.argv[1]
        test_query(query)
    else:
        # Test suite
        print("\n🧪 LOCAL TEST SUITE (No external API calls needed)")
        print("="*80)

        test_cases = [
            ("How do I apply for a vacation day?", "HR"),
            ("What should I do if my laptop is running slow?", "IT Support"),
            ("I am furious! You overcharged me!", "ANY"),
            ("Do you sell dog food?", "Unknown"),
            ("How do I apply for sick leave?", "HR"),
        ]

        for query, expected_dept in test_cases:
            test_query(query, expected_dept)
            input("\nPress Enter to continue to next test...\n")


if __name__ == "__main__":
    main()
