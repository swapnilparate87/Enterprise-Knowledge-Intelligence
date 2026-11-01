---
doc_id: OPS-009
title: Invoice Processing and Payment SOP
department: Operations and Procurement
doc_type: SOP
owner: Finance Controller
version: 0.9
status: draft
effective_date: 2026-09-15
audience: Budget owners, managers and Finance/Procurement staff
related: OPS-002, OPS-004, OPS-005
---

# Invoice Processing and Payment SOP

| Field | Value |
|---|---|
| Document ID | OPS-009 |
| Department | Operations and Procurement |
| Document type | SOP |
| Owner | Finance Controller |
| Version | 0.9 |
| Status | DRAFT |
| Effective / last reviewed | 2026-09-15 |
| Audience | Budget owners, managers and Finance/Procurement staff |
| Related documents | OPS-002, OPS-004, OPS-005 |

**Summary.** Draft standard operating procedure for receiving, matching, approving and paying supplier invoices at Northstar Systems. It is not in force; current practice follows the approved procurement and payment rules, and several changes are proposed for review.

*SYNTHETIC DOCUMENT - Northstar Systems is a fictional company. This document exists for development, testing and demonstration only and is not real legal, employment, security or compliance advice.*

## 1. Purpose and Scope

**This document is a DRAFT (version 0.9) and is not yet in force.** The approved current practice for invoices and payments is whatever the related approved documents say, namely OPS-001 (Delegation of Authority and purchasing rules), OPS-002, OPS-004 (vendor onboarding) and OPS-005 (contract management). Where this draft differs from those documents, the approved documents prevail. Nobody should change their working practice because of this draft. Items that differ from current practice are labelled "Proposed" in the text below.

The draft describes how Finance would process supplier invoices from receipt to payment in NorthBuy and NorthPay, including the three-way match, exception handling, payment runs and vendor queries. Its goal is to put the existing rules into one operating procedure for the Finance team and budget owners. It covers invoices for goods and services bought under a purchase order. It does not cover employee expense claims, corporate card statements or petty cash, which are covered by other policies.

The effective date shown for this draft, 15 September 2026, is the date of the circulated version for review and not a date from which it applies.

## 2. Definitions

- **Invoice**: a request for payment from a vendor that is onboarded in the NorthBuy vendor master.
- **Purchase order (PO)**: the approved commitment created in NorthBuy before any purchase is made.
- **Goods receipt or service acceptance**: confirmation by the requester that goods were received or services were delivered as ordered.
- **Three-way match**: comparison of the PO, the goods receipt or service acceptance, and the invoice.
- **Tolerance**: the permitted difference between the invoice and the matched PO and receipt.
- **Payment run**: the scheduled batch in which Finance releases approved supplier payments.
- **MSME vendor**: a vendor with a valid micro, small or medium enterprise registration (illustrative; to be verified by Legal before external use).

## 3. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Finance Controller | Owns the SOP, approves exceptions, signs off payment runs |
| Accounts Payable team | Registers invoices, performs matching, prepares runs |
| Budget owner or requester | Confirms goods receipt or service acceptance, resolves disputes |
| Procurement Desk | Maintains vendor master, supports PO corrections |
| Finance Desk | Answers vendor and internal questions at finance@northstar-systems.example |

## 4. Current Rules the Draft Restates

The following rules are already in force through approved documents. The draft restates them for convenience:

- A PO must exist before any commitment is made. Invoices without a PO are not paid, except pre-approved utilities and statutory payments.
- The vendor must be onboarded in the NorthBuy vendor master before a PO is issued.
- Payment terms are Net 45 days from invoice receipt. MSME-registered vendors are on Net 30 terms.
- Payment runs take place every Tuesday and Friday.
- The three-way match applies, with a tolerance of 2% or INR 500, whichever is lower.
- Advance payments up to 30% of PO value need CFO approval and are only for onboarded vendors.
- Approval of payments follows the Delegation of Authority, and nobody may approve their own request.

## 5. Proposed Invoice Processing Steps

1. **Receipt.** Vendors send invoices to a dedicated Accounts Payable mailbox or upload them to NorthBuy. The date of receipt is the date the invoice arrives, and the Net 45 or Net 30 clock starts from that date. Proposed: invoices received by other routes, such as directly by a requester, must be forwarded to Accounts Payable within 1 business day.
2. **Registration.** Accounts Payable logs the invoice in NorthBuy with the PO number, vendor, invoice number, date, amount, tax details and cost-centre code. Duplicate invoice numbers from the same vendor are blocked.
3. **Validation.** Accounts Payable checks the vendor against the vendor master, the GSTIN and the bank details held, and that the invoice carries the required fields.
4. **Matching.** The invoice is matched with the PO and the goods receipt or service acceptance. If the difference is within tolerance, which is 2% or INR 500, whichever is lower, the invoice passes. If it is outside tolerance, it is placed on hold and the budget owner is notified.
5. **Approval.** Approval follows the Delegation of Authority by invoice amount. The budget owner confirms acceptance, and the DoA approver authorises payment.
6. **Scheduling.** The invoice is scheduled for the next payment run on or after its due date, using Net 45 or Net 30 terms.
7. **Payment and filing.** After the run, Accounts Payable records payment details, sends a remittance advice to the vendor and files the documents.

## 6. Proposed Changes Under Review

The following are proposals and are not in force. They are drafted for discussion with Finance, Procurement and Legal.

| Topic | Current approved practice | Proposal in this draft |
|---|---|---|
| Match tolerance | 2% or INR 500, whichever is lower | Keep unchanged; add a rule that cumulative tolerance on one PO cannot exceed INR 2,000 |
| Payment run days | Tuesday and Friday | Add a weekly Wednesday run for MSME invoices due within 3 days |
| Invoice receipt routes | No fixed route | Single mailbox plus NorthBuy upload |
| Invoice query response | No fixed target | Accounts Payable replies to vendor queries within 3 business days |

Until the draft is approved, only the current approved practice in the middle column applies. The proposals are not authorised, and no payment may be made on the Wednesday run.

## 7. Exceptions and Holds

### 7.1 Mismatch outside tolerance

If an invoice is more than the PO plus tolerance, Accounts Payable asks the requester to confirm the reason. The requester may ask Procurement to amend the PO, which must be approved by the same level as the original approval, or the vendor issues a credit note. A PO amendment that increases the value is approved at the DoA level for the new total.

### 7.2 Missing goods receipt

If the requester has not confirmed receipt within 5 business days, Accounts Payable reminds the requester and informs the department head. Payment may not be released without acceptance.

### 7.3 Invoice without a PO

Invoices without a PO are not paid. The vendor is told to wait while the requester follows the retrospective approval process in OPS-001. The only exceptions are pre-approved utilities and statutory payments.

### 7.4 Duplicate or suspicious invoices

Accounts Payable must stop payment on any invoice that appears duplicated, has altered bank details or looks unusual, and must tell the Finance Controller. Bank detail changes follow the verification process in OPS-004 and are never accepted by email alone.

### 7.5 Advance payments

An advance of up to 30% of PO value needs CFO approval and is available only to onboarded vendors. Advance payments are recorded against the PO, and the balance invoice is net of the advance.

## 8. Worked Examples

Example 1: A PO for INR 2,00,000 covers a software implementation. The vendor invoices INR 2,03,000. The difference is INR 3,000, which is 1.5%. The tolerance is 2% or INR 500, whichever is lower, so the tolerance is INR 500. The difference exceeds the tolerance, so the invoice goes on hold.

Example 2: An MSME-registered vendor invoices INR 85,000 on 1 October and Finance receives it the same day. Net 30 gives a due date of 31 October. The invoice is scheduled for the last Tuesday or Friday payment run on or before that date.

Example 3: A non-MSME vendor invoice received on 10 November has a due date of 25 December under Net 45. The invoice amount is INR 3,50,000. Payment approval needs the CFO because the amount is in the INR 2,00,001 to 10,00,000 band.

## 9. Related Documents

See OPS-001 for the Delegation of Authority and purchasing rules, OPS-002 for related operational procedures, OPS-004 for vendor onboarding and bank detail verification, and OPS-005 for contract management and renewal.

## 10. Revision History

| Version | Date | Change |
|---|---|---|
| 0.5 | 2026-07-20 | First internal draft |
| 0.9 | 2026-09-15 | Circulated for Finance and Procurement review; not approved |
