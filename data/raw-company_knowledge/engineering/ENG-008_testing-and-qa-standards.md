---
doc_id: ENG-008
title: Testing and QA Standards
department: Engineering
doc_type: Standard
owner: QA Lead
version: 4.3
status: approved
effective_date: 2025-04-12
audience: Engineering staff
related: ENG-001, ENG-007, ENG-003
---

# Testing and QA Standards

| Field | Value |
|---|---|
| Document ID | ENG-008 |
| Department | Engineering |
| Document type | Standard |
| Owner | QA Lead |
| Version | 4.3 |
| Status | APPROVED |
| Effective / last reviewed | 2025-04-12 |
| Audience | Engineering staff |
| Related documents | ENG-001, ENG-007, ENG-003 |

**Summary.** Sets testing and quality assurance standards for Northstar engineering. Covers the test pyramid, 80 percent coverage for new code, release gating on integration smoke tests, performance testing before major releases, flaky test quarantine, test data rules and defect handling.

*SYNTHETIC DOCUMENT - Northstar Systems is a fictional company. This document exists for development, testing and demonstration only and is not real legal, employment, security or compliance advice.*

## 1. Purpose and Scope

This standard defines the minimum testing and quality assurance expectations for software built by Northstar Systems Private Limited engineering teams, including the Northstar Nexus Platform, Nexus Connect, Nexus Insight and internal services. It applies to developers, QA engineers, release managers and reviewers. It describes what must be tested, how much, where tests run, which results block a release and how defects and flaky tests are handled.

The pipeline that enforces these rules is described in ENG-007, the review rules are in ENG-001, and the deployment process is in ENG-003. Teams may exceed this standard but must not fall below it.

## 2. Definitions

- **Unit test**: a fast, isolated test of a small piece of code, without network, database or file system dependencies.
- **Integration test**: a test that exercises several components together, for example a service with its database or a Connector with a stub endpoint.
- **Smoke test**: a small, fast subset of integration tests that confirms the critical paths work.
- **End-to-end (E2E) test**: a test of a complete user journey through the console or API.
- **Test pyramid**: the principle of having many unit tests, fewer integration tests and the fewest E2E tests.
- **New-code coverage**: the percentage of lines added or changed in a pull request that are executed by tests.
- **Flaky test**: a test that sometimes passes and sometimes fails on the same code.
- **Quarantine**: moving a flaky test into a non-blocking job so it cannot hold up unrelated work.
- **QA Lead**: the engineering role that owns this standard and the test tooling.

## 3. Roles and Responsibilities

| Role | Responsibilities |
|---|---|
| Developer | Writes unit and integration tests with each change, fixes failing tests |
| QA engineer | Designs test plans, maintains E2E and performance suites, triages defects |
| QA Lead | Owns this standard, reports quality metrics monthly, manages flaky test list |
| Reviewer | Checks that tests are meaningful, not only present |
| Release manager | Confirms release gates are green before each release train |
| Security Champion | Reviews tests for security-sensitive changes |

## 4. The Test Pyramid

Teams must follow the test pyramid. A healthy repository has a large base of unit tests, a smaller layer of integration tests and a thin layer of E2E tests. As a guide, around 70% of automated tests should be unit tests, 20% integration tests and 10% or fewer E2E tests. A team whose suite is dominated by E2E tests should rebalance, because E2E tests are slow and fragile.

### 4.1 Unit tests

Every change to logic must include unit tests that would fail if the change were wrong. Unit tests must run in under 10 minutes for the whole repository on the pipeline. Mocks may be used for external dependencies, but business rules must be tested with real objects where practical.

### 4.2 Integration tests

Integration tests cover service boundaries: database access, queue handling, Connector behaviour, authentication flows and API contract tests against the specification in ENG-002. They run against the test environment with synthetic data. Contract tests must be added for every new public API endpoint.

### 4.3 End-to-end tests

E2E tests cover a small set of critical journeys, for example creating a Workspace, building a Pipeline, receiving a Webhook and viewing a Nexus Insight report. They run in staging after deployment and should complete in under 30 minutes in total.

## 5. Coverage Requirements

New code coverage must be at least 80%. This is a gate in the pipeline: a PR whose changed lines are covered below 80% cannot be merged. Coverage is measured on changed lines, not on the whole repository, so teams are not penalised for old code, but they are expected to raise coverage over time when touching legacy files.

### 5.1 Exemptions

Generated code, trivial configuration files and code that cannot be tested without hardware may be excluded from coverage in a documented exclusion list approved by the QA Lead. Exclusions of business logic are not allowed. Coverage is a minimum, not a goal: reviewers must reject tests that execute lines without asserting behaviour.

Example: A developer changes 150 lines in a Connector. Test coverage on those lines is 72%, so the pipeline blocks the PR. The developer adds tests for the retry and timeout branches, raising new-code coverage to 85%, and the gate passes.

## 6. Release Gating

A release is promoted only when all of the following are green:

1. Unit tests pass with new-code coverage at least 80%.
2. Integration smoke tests pass in the test and staging environments. Release gating on integration smoke tests means no promotion proceeds if even one smoke test fails.
3. Security scans meet the thresholds set in ENG-007.
4. For major releases, a performance test has been run and compared with the agreed budget.
5. There are no open defects of critical severity against the release scope.

Known failures may not be waived by the developer. A waiver for a non-critical defect needs the QA Lead and the engineering manager to agree and record it in the NorthDesk change ticket.

## 7. Performance Testing

A performance test must be run before every major release (a MAJOR version increase under semantic versioning, as in ENG-006) and before any change that alters query patterns, caching or Pipeline execution. The test should run in staging with production-like data volume, using anonymised or synthetic data.

Performance budgets for Tier-1 services are defined by the service owner and must at least ensure that p95 latency does not exceed 1.5x the current baseline, since this is the same threshold that triggers automatic rollback in production. The test report must be attached to the change ticket. Capacity tests for the API default rate limit of 1,000 requests per minute per tenant must confirm that excess requests receive HTTP 429 with a Retry-After header.

## 8. Flaky Tests

A flaky test must be quarantined within 2 business days of being identified. The QA Lead tracks quarantined tests in NorthDesk with an owner. Quarantined tests are not ignored: they run in a non-blocking job and must be fixed or deleted within 30 days. Developers must not add automatic retries to hide flakiness; retries are limited to one attempt for diagnosing purposes.

Example: A test of webhook delivery fails on Monday and passes on retry. The developer reports it to the QA Lead on Monday. If the cause is not fixed by Wednesday, the test is moved to quarantine within the 2 business day limit, and the owner has until the 30-day mark to repair or delete it.

## 9. Test Data

- Test data must be synthetic or properly anonymised. Customer production data, personal data of employees and credentials must never be used in test environments.
- Test accounts must use corporate test domains and not real customer addresses.
- Test data sets for Nexus Insight must include edge cases such as empty datasets, very large datasets and unusual character sets.
- Secrets in tests must be fake values or injected from NorthVault, never committed to source.

## 10. Defect Management

Defects are recorded in NorthDesk with severity, steps to reproduce, environment and version. Severity maps to action as follows.

| Severity | Meaning | Required action |
|---|---|---|
| Critical | Data loss, security flaw or complete feature failure | Blocks release, fix immediately |
| High | Major feature impaired, no workaround | Fix in the next release train |
| Medium | Impaired with workaround | Planned within 2 sprints |
| Low | Cosmetic | Backlog |

Defects found in production are checked against the incident rules in ENG-004 to decide whether an incident should be declared. Every production defect must have a regression test added with the fix.

## 11. Exceptions and Edge Cases

- Prototypes and spikes marked as non-production may skip coverage requirements, but must not be deployed to production or promoted to a Tier-1 or Tier-2 service without meeting this standard.
- Emergency changes under hotfix procedures must still have a regression test. If it cannot be written before deployment, it must be added within 1 business day.
- Third-party code is not tested by Northstar teams, but the way Northstar uses it must be covered by integration tests.
- Where a test requires an external partner system unavailable in test, a contract stub is acceptable if the contract is reviewed every quarter.

## 12. Related Documents

- ENG-001 Code Review Standards.
- ENG-007 CI/CD Pipeline Reference.
- ENG-003 Software Deployment Runbook.
- ENG-002 API Development Standards.
- ENG-004 Production Incident Management Procedure.

## 13. Revision History

| Version | Date | Change |
|---|---|---|
| 4.0 | 2024-11-18 | Introduced 2 business day flaky test quarantine rule |
| 4.2 | 2025-02-24 | Clarified performance test triggers |
| 4.3 | 2025-04-12 | Added contract test requirement for new public endpoints |
