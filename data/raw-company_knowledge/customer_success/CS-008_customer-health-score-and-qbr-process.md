---
doc_id: CS-008
title: Customer Health Score and QBR Process
department: Product and Customer Support
doc_type: Process
owner: VP Customer Success
version: 4.4
status: approved
effective_date: 2026-01-13
audience: Customer Success, Support and Engineering staff
related: CS-004, CS-003, CS-009
---

# Customer Health Score and QBR Process

| Field | Value |
|---|---|
| Document ID | CS-008 |
| Department | Product and Customer Support |
| Document type | Process |
| Owner | VP Customer Success |
| Version | 4.4 |
| Status | APPROVED |
| Effective / last reviewed | 2026-01-13 |
| Audience | Customer Success, Support and Engineering staff |
| Related documents | CS-004, CS-003, CS-009 |

**Summary.** Defines the customer health score at Northstar Systems, its five weighted components, Green, Yellow and Red bands, the recovery plan for Red accounts, QBR frequency by tier, and the renewal motion that starts 120 days before renewal, with calculation examples.

*SYNTHETIC DOCUMENT - Northstar Systems is a fictional company. This document exists for development, testing and demonstration only and is not real legal, employment, security or compliance advice.*

## 1. Purpose and Scope

This process describes how Northstar Systems Private Limited measures the health of each customer account, what must happen when an account turns Red, how Quarterly Business Reviews (QBRs) are run, and when the renewal motion begins. It gives Customer Success Managers (CSMs) a single, consistent view of risk and opportunity, and gives the VP Customer Success a basis for resourcing and executive attention.

It applies to all customers of the Northstar Nexus Platform, Nexus Connect and Nexus Insight, and to the CSMs, Support Leads, Directors of Customer Success and account executives who work with them. Implementation projects are covered by CS-004, which ends with handover to the CSM; this process starts at that handover. Support targets are in CS-003 and escalations in CS-001.

## 2. Definitions

- **Health score**: a number from 0 to 100 that summarises the condition of a customer account.
- **Component**: one of the five weighted measures that make up the score.
- **Recovery plan**: a written plan with actions, owners and dates to bring a Red account back to Yellow or Green.
- **QBR**: Quarterly Business Review, a structured meeting with the customer on value delivered, issues and plans.
- **Renewal motion**: the set of activities that prepare and secure a renewal.
- **NPS and CSAT**: Net Promoter Score and Customer Satisfaction survey results.

## 3. Health Score Components and Weights

The health score is the weighted sum of five component scores, each rated from 0 to 100.

| Component | Weight | What it measures |
|---|---|---|
| Product usage | 30% | Active users, Pipeline runs, feature adoption, trend against the customer's plan |
| Support experience | 20% | Case volume, P1 and P2 history, time to resolution, escalations, CSAT of cases |
| Sentiment | 20% | NPS and CSAT survey results, tone of interactions |
| Executive engagement | 15% | Contact with the customer's sponsor and decision makers, attendance at QBRs |
| Commercial | 15% | Renewal status, payment history, expansion or contraction |

The weights add up to 100%. The CSM reviews and updates the inputs at least monthly, and Support and Finance supply data by the fifth business day of each month. The score is recorded in the customer success records and is visible to the Director of Customer Success.

Example: A Premier customer has component scores of usage 80, support 60, sentiment 70, executive engagement 50 and commercial 90. The score is 0.30 x 80 + 0.20 x 60 + 0.20 x 70 + 0.15 x 50 + 0.15 x 90 = 24 + 12 + 14 + 7.5 + 13.5 = 71. The account is Yellow.

## 4. Score Bands

| Band | Score | Meaning |
|---|---|---|
| Green | 75 and above | Healthy; focus on value and growth |
| Yellow | 50 to 74 | Needs attention; CSM watches closely and acts on weak components |
| Red | Below 50 | At risk; recovery plan required |

A score exactly at 75 is Green and a score exactly at 50 is Yellow. A CSM may place an account in Red regardless of the calculation if there is a clear risk, such as a written notice of non-renewal, but must record the reason and the Director of Customer Success must confirm it.

## 5. Red Account Recovery

When an account turns Red, the CSM must create a recovery plan within 5 business days. The plan contains:

1. The reasons for the low score, by component.
2. The customer's main concerns, in their words where possible.
3. Specific actions, each with an owner and a date.
4. The executive sponsor on the Northstar side (Director of Customer Success or VP Customer Success).
5. The target date and score for returning to Yellow.
6. A review rhythm, at least every two weeks until the account is Yellow.

The Director of Customer Success approves the plan. If Support or Engineering actions are needed, the CSM must raise them through the escalation route in CS-001. The VP Customer Success reviews all Red accounts monthly. An account leaves Red only when its score is 50 or above for two consecutive monthly calculations.

Example: An Enterprise customer falls to 42 after two SEV1 incidents, a falling usage trend and a missed QBR. The CSM drafts the recovery plan in 4 business days: an executive call with the customer CTO, delivery of the RCA, a performance review by Engineering, and a re-baselined success plan. Two months later the score reaches 58 and 61 and the account moves to Yellow.

## 6. Quarterly Business Reviews

QBR frequency depends on the support tier.

| Tier | QBR frequency |
|---|---|
| Enterprise | Quarterly |
| Premier | Twice a year |
| Standard | Annually, on request |

A QBR agenda should include: value delivered against the success criteria, usage and adoption trends, support summary including P1 and P2 cases, service levels and any credits, roadmap items relevant to the customer, risks, and agreed actions with owners. The CSM sends the agenda 5 business days before and a summary with actions within 3 business days after. Executive attendance on both sides is expected for Enterprise QBRs. For Red accounts a QBR should be held, even if the tier would not normally include one.

## 7. Renewal Motion

The renewal motion starts 120 days before the renewal date. Activities include:

- Review of the health score and the open risks at day 120.
- Confirmation of the renewal scope, seats, products and version in use. For example, customers on 4.2 LTS (supported until 2027-01-20) should have an upgrade conversation well before their support ends.
- A pre-renewal meeting with the customer sponsor.
- Preparation of the quotation and the contract. Legal review is needed for contracts above INR 5,00,000, any multi-year term or any non-standard terms. Auto-renewal clauses need General Counsel approval.
- A renewal alert 90 days before expiry from the contracts repository.
- Approval of price and terms under the Delegation of Authority.

A Red account at day 120 requires the Director of Customer Success to join the renewal planning and confirm the risk and the plan.

## 8. Roles and Responsibilities

- **CSM**: updates the score, runs QBRs, owns recovery plans and the renewal motion.
- **Support Lead**: supplies support data, flags cases that affect health.
- **Director of Customer Success**: approves recovery plans, reviews Red accounts and joins renewals of Red accounts.
- **VP Customer Success**: monthly review of Red accounts and ownership of this process.
- **Finance**: provides payment and invoice data.

## 9. Exceptions and Edge Cases

- **New customers**: during hypercare (30 days after go-live) the account is tracked by the Implementation Manager, and the first score is calculated at handover.
- **Missing data**: if a component cannot be measured, the CSM uses the last known value for up to two months and records the gap. After two months the Director of Customer Success decides how to treat it.
- **Multiple products**: if a customer has several products, one overall score is held for the account, with product-level notes.
- **Disagreement**: a CSM who disagrees with the calculated band may ask the Director of Customer Success for an override and must record the reason.

## 10. Related Documents

CS-004 (Customer Onboarding and Implementation Playbook), CS-003 (Service-Level Objectives and Support Procedures) and CS-009.

## 11. Revision History

| Version | Date | Change |
|---|---|---|
| 4.2 | 2025-04-02 | Adjusted component weights |
| 4.3 | 2025-09-17 | Added QBR frequency by tier |
| 4.4 | 2026-01-13 | Added 120-day renewal motion and recovery plan timing |
