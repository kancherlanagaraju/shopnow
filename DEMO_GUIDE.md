# ShopUNow Demo Guide

## Knowledge base at a glance

The current source dataset is `data/shopunow_qa_dataset.json`. It contains **52 synthetic FAQ records across four departments**. There is no Facilities & Admin department in the current dataset.

| Department | Audience | FAQ records |
|---|---|---:|
| HR | Internal employees | 15 |
| IT Support | Internal employees | 13 |
| Billing & Payments | External customers | 12 |
| Shipping & Delivery | External customers | 12 |
| **Total** | | **52** |

The questions below are the questions represented in the dataset. They are good starting points for a demo, but they are not a guarantee that every paraphrase will retrieve the same record or produce an identical answer. Retrieval depends on the live vector index and configuration.

### HR — 15 records

1. What is the process for applying for a vacation day at ShopUNow?
2. How do I apply for sick leave at ShopUNow?
3. What about PTO or personal time off at ShopUNow?
4. How does ShopUNow handle health insurance for full-time employees?
5. What are the guidelines for remote work eligibility?
6. How can I access my performance review feedback?
7. What is the policy on overtime pay for retail associates?
8. How do I enroll in the ShopUNow Employee Assistance Program?
9. What steps should I take if I notice a violation of the code of conduct?
10. Can I transfer to a different store location?
11. What is the policy on employee referrals?
12. How do I update my personal contact information in the HR system?
13. What training resources are available for career development?
14. How does ShopUNow handle payroll deductions for union dues?
15. What is the maternity and paternity leave policy at ShopUNow?

### IT Support — 13 records

1. How do I reset my ShopUNow employee VPN password?
2. What should I do if my laptop is running slow after the latest Windows update?
3. How can I access the ShopUNow internal wiki from my mobile device?
4. I received a phishing email claiming to be from the Finance department. What steps should I take?
5. How do I set up a shared printer for the Marketing team?
6. What is the procedure for requesting a new software license for a design tool?
7. How do I request a new monitor or additional hardware for my workstation?
8. My email client is not syncing new messages. How can I fix it?
9. How do I enable two-factor authentication for my ShopUNow account?
10. I need to backup my project files to the company cloud. What steps should I follow?
11. Why am I receiving repeated error 0x80070005 when installing updates?
12. How can I configure my laptop to automatically lock after 15 minutes of inactivity?
13. What should I do if I suspect a coworker is accessing my shared folder without permission?

### Billing & Payments — 12 records

1. How do I view my recent invoices on ShopUNow?
2. How do I update my ShopUNow payment method?
3. I was charged twice for the same order. How can I get a refund?
4. Can I set up automatic recurring payments for my monthly subscription?
5. What is the refund policy for digital products purchased on ShopUNow?
6. How do I update my billing address?
7. I received a partial refund that doesn’t match the original amount. What should I do?
8. Can I pay my invoice in installments?
9. What should I do if my credit card was declined during checkout?
10. How can I export my purchase history for tax purposes?
11. Is there a discount for paying annually instead of monthly?
12. How do I dispute a charge that I don’t recognize?

### Shipping & Delivery — 12 records

1. What shipping options does ShopUNow offer for my order?
2. How can I track my shipment once it has shipped?
3. What happens if I’m not home when my package arrives?
4. Can I change my shipping address after placing an order?
5. What is ShopUNow’s return policy for items that arrive damaged?
6. Do you ship internationally?
7. What should I do if my package is delayed?
8. Can I choose a pickup location instead of home delivery?
9. What is the estimated delivery time for a Standard shipment to Denver?
10. How do I cancel a shipment that hasn’t shipped yet?
11. Do you offer free shipping for first-time customers?
12. What happens if I miss the delivery window for Same-Day shipping?

## Recommended demo sequence

Use direct questions represented by the dataset first:

1. “How do I apply for a vacation day at ShopUNow?” — HR retrieval.
2. “How do I reset my ShopUNow employee VPN password?” — IT retrieval.
3. “How do I update my ShopUNow payment method?” — Billing retrieval. The corresponding FAQ describes updating a method in Billing Settings.
4. “How can I track my shipment once it has shipped?” — Shipping retrieval.
5. “I’m furious that I was charged twice for the same order!” — negative-sentiment escalation.
6. “Who is the president of Canada?” — unknown department / out-of-scope response, unless the categorizer labels the query negative.

The category and sentiment are LLM-classified, so paraphrases and emotional wording can change routing. For reliable comparisons, use the same exact input and verify the displayed department, sentiment, and response.

## Routing and response behavior

The current workflow in `agent.py` uses these routes:

| Categorization result | Route | Expected behavior |
|---|---|---|
| Negative sentiment | Human escalation | Returns the escalation message |
| Non-negative sentiment and a known department (HR, IT Support, Billing & Payments, Shipping & Delivery) | RAG | Retrieves only that department’s FAQ documents; answers from retrieved context or abstains |
| Non-negative sentiment and an unknown department | Out of scope | Says the request is outside ShopUNow support and lists supported departments |

Negative sentiment takes precedence over department classification. Therefore, a negative out-of-scope question can still be escalated. The escalation node only returns a message; this project does not currently create a support ticket or notify a human agent. Do not present that message as proof that a real handoff occurred.

RAG uses a department metadata filter, retrieves up to `TOP_K` documents, and applies a relevance threshold. If no retrieved document passes the threshold, it returns:

> I don't have enough information in the ShopUNow knowledge base to answer this accurately.

The configured default `RELEVANCE_THRESHOLD` is **0.35** and `TOP_K` defaults to **3**. Environment variables can override these values, so check the deployment environment when behavior differs from local configuration. The threshold is not a guarantee that every phrasing will match, and lowering it can admit less relevant context. The LLM is instructed to use only retrieved context and abstain when that context does not answer the question.

## Known coverage gaps and caveats

The dataset is synthetic and intentionally limited. Examples of questions without a direct FAQ include:

- HR: salary bands, office locations, gym membership, or benefits beyond the documented health plan, EAP, and leave policies.
- IT: initial VPN access, IT helpdesk phone number, or laptop purchasing beyond the documented monitor/additional hardware request process.
- Billing: applying a discount code, a general refund policy for all product types, and exact subscription billing-cycle details.
- Shipping: reshipments for lost packages, packages that never arrived, and a general return policy beyond damaged-item handling.
- General business questions: product catalog, store hours, store count, CEO identity, or product recommendations.

Related topics are not interchangeable policies. For example, the dataset contains a refund FAQ for digital products; it should not be treated as a universal refund policy. Similarly, a lost-package reshipment process is not explicitly documented. The assistant should abstain rather than infer missing rules.

## Index synchronization

The JSON dataset is the source of truth. `database.py` stores a hash of the dataset with the Chroma collection and rebuilds the collection when the dataset changes. When testing a deployed app, make sure the latest code and dataset are deployed and that the app has initialized the index from that dataset. If the deployment has a separate persistent Chroma volume or overrides configuration, verify those as well.

## Evaluation and demo claims

`evaluation.py` currently contains a small number of workflow examples; it is **not** an evaluation of all 52 FAQ records and does not establish a 100% retrieval or answer-accuracy rate. Do not claim that every paraphrase works or that all questions have passed. A robust evaluation should test each FAQ and important paraphrase against expected department, retrieved source, required answer facts, and abstention/routing behavior.

For the demo, describe the project as a capstone prototype that demonstrates department routing, metadata-filtered RAG, grounded generation, controlled abstention, and an escalation path. Avoid describing it as production-ready customer support: it has synthetic content, LLM-dependent classification and generation, and no implemented human ticket handoff.

## Pre-demo checklist

- Confirm the deployment is running the intended commit.
- Confirm `GROQ_API_KEY` is configured in the runtime without displaying or sharing the key.
- Confirm `RELEVANCE_THRESHOLD` is `0.35` or intentionally overridden, and check `TOP_K`.
- Confirm Chroma initialized from the current `data/shopunow_qa_dataset.json`.
- Test at least one direct question from each department.
- Test an unsupported neutral question and a negative-sentiment support complaint separately.
- Explain that retrieval can fail for paraphrases and that the current evaluation suite does not cover all 52 questions.

## Useful project files

- `README.md` — setup and project overview
- `architecture.md` — architecture summary
- `data/shopunow_qa_dataset.json` — current FAQ source data
- `agent.py` — categorization and graph routing
- `retrieval.py` — retrieval and relevance threshold logic
- `database.py` — Chroma collection initialization and synchronization
- `evaluation.py` — current workflow evaluation examples
