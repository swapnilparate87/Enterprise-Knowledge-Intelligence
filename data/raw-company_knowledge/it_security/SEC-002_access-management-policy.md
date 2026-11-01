---
doc_id: SEC-002
title: Access Management Policy
department: IT and Information Security
doc_type: Policy
owner: Chief Information Security Officer
version: 2.1
status: approved
effective_date: 2025-10-01
audience: All employees and contractors
related: SEC-003, HR-005, HR-006, SEC-015
---

# Access Management Policy

| Field | Value |
|---|---|
| Document ID | SEC-002 |
| Department | IT and Information Security |
| Document type | Policy |
| Owner | Chief Information Security Officer |
| Version | 2.1 |
| Status | APPROVED |
| Effective / last reviewed | 2025-10-01 |
| Audience | All employees and contractors |
| Related documents | SEC-003, HR-005, HR-006, SEC-015 |

**Summary.** Rules for requesting, approving, reviewing and removing access to Northstar systems. Covers role-based least privilege, the NorthDesk Access Request form, privileged just-in-time access, joiner-mover-leaver timelines, quarterly access reviews, dormant and break-glass accounts.

*SYNTHETIC DOCUMENT - Northstar Systems is a fictional company. This document exists for development, testing and demonstration only and is not real legal, employment, security or compliance advice.*

## 1. Purpose and Scope

This policy defines how access to Northstar information systems is requested, approved, granted, reviewed and removed. It supports SEC-001 (Information Security Policy) and applies to all employees, contractors and third parties who hold or request an account on any Northstar system, including NorthPeople, NorthPay, NorthBuy, NorthDesk, NorthShip, NorthWatch, NorthAssist, cloud consoles and production environments.

## 2. Definitions

- **Least privilege**: the minimum access needed to perform the current job.
- **System owner**: the named business or technical owner of an application who decides who may use it.
- **Privileged access**: administrator-level or production access that can change systems, data or security controls.
- **Just-in-time (JIT) access**: privileged access granted for a limited time and removed automatically.
- **Break-glass account**: an emergency account used only when normal access paths fail.
- **Dormant account**: an account with no sign-in for a defined period.
- **NorthDesk Access Request form**: the only approved channel to ask for access.
- **NorthID**: the single sign-on and MFA platform through which access is granted.

## 3. Principles

Access is role-based and follows least privilege. Each person has an individual account. Shared accounts are prohibited, without exception. Access is granted for a business need and removed when the need ends. Every grant, change and removal must be traceable to a NorthDesk ticket.

## 4. Requesting and Approving Access

### 4.1 Standard access

1. The requester, or the reporting manager on their behalf, submits the NorthDesk Access Request form naming the system, the role needed and the business reason.
2. The reporting manager approves.
3. The system owner approves.
4. IT Operations provisions the access through NorthID, and the requester is notified in NorthDesk.

Standard access needs two approvals: the reporting manager and the system owner. Nobody may approve their own request, and an approver must be at least Band B4.

### 4.2 Privileged and production access

Privileged access to production, including access through the NorthGate bastion, needs the reporting manager and system owner approvals plus approval from a Director (Band B6) and a CISO delegate. It is granted just-in-time for a maximum of 8 hours. When the window ends, access is removed automatically and a new request is needed to continue. All sessions on NorthGate are recorded, and privileged actions are always logged in NorthWatch. Admin consoles have a session timeout of 1 hour, and accounts that hold privileged rights must use a hardware security key as described in SEC-003.

Example: A Site Reliability Engineer needs to inspect a database on a Tier-1 production service during a SEV2 incident. She raises the Access Request form, her manager and the database owner approve, the on-call Director approves and the CISO delegate confirms. She receives 8 hours of access through NorthGate. If the work is not finished at the end of the window, she raises a fresh request.

### 4.3 Contractors and third parties

Contractors receive accounts only after the sponsoring manager confirms the engagement end date, and the account expires on that date unless extended in NorthDesk. Vendor staff who reach Confidential or Restricted data need a completed vendor security assessment first (see SEC-001).

## 5. Joiner, Mover, Leaver

| Event | Requirement | Deadline |
|---|---|---|
| Joiner | Baseline role access ready, laptop enrolled in NorthGuard | Day 1 |
| Mover (role or team change) | New access added and old access no longer needed removed | Within 2 business days |
| Leaver | All accounts disabled | By 18:30 IST on the last working day |
| Contractor end | Accounts disabled | On the engagement end date |

HR triggers joiner, mover and leaver events from NorthPeople. A manager who learns of a change before HR does must raise a NorthDesk ticket without waiting. For leavers, IT Operations also revokes VPN, tokens, API keys and shared secrets the person could use, and the manager must reassign any credentials the person owned in NorthVault.

Example: An employee moves from Customer Success to Engineering on 14 July. Her Support lead access in NorthAssist must be removed and her new access granted by 16 July, which is 2 business days.

## 6. Periodic Access Reviews

User access reviews run every quarter in January, April, July and October. System owners and reporting managers receive a list of accounts and entitlements from NorthID, and must confirm or revoke each one. The review must be completed within 15 business days. Entitlements not confirmed by the deadline are removed. The Security team reports completion rates at the quarterly security review. Findings of excessive access are corrected within 5 business days of discovery.

## 7. Dormant, Break-Glass and Service Accounts

- **Dormant accounts**: disabled after 60 days of inactivity and deleted after 180 days. Managers are notified at day 45.
- **Break-glass accounts**: kept in sealed storage, monitored continuously, and every use must be reviewed within 1 business day. The use needs a ticket explaining the reason.
- **Service accounts**: must have a named owner, credentials in NorthVault or a KMS-backed secret store, and credentials rotated every 90 days.
- **Shared accounts**: not allowed. Where a tool cannot support individual accounts, an exception must be raised in NorthDesk under SEC-001.

## 8. Exceptions and Edge Cases

- Emergency access when the approvers cannot be reached: the Engineering Director on call may approve, and the request is reviewed retrospectively within 1 business day.
- Temporary elevated access for a project: granted with an end date of at most 90 days and reviewed at the next quarterly review.
- An approver on leave: the reporting manager's department head acts as delegate, recorded in NorthDesk.
- An employee working outside the registered city for more than 10 working days in a year needs HR and Security approval before access from that location is permitted.

## 9. Related Documents

Password and MFA requirements are in SEC-003. Employee exit steps are in HR-005 and HR-006. Monitoring of access activity is described in SEC-015.

## 10. Revision History

| Version | Date | Change |
|---|---|---|
| 2.0 | 2025-03-10 | Introduced just-in-time privileged access |
| 2.1 | 2025-10-01 | Clarified review deadline and dormant account timeline |
