# Freelancer Contract & Milestone Payment Tracker

A production-style backend system for managing freelance contracts, milestone lifecycles, staged payments, deadlines, and disputes.

The project was inspired by a real problem I experienced while freelancing: generic invoicing tools can record invoices and payments, but they usually do not model the actual lifecycle of freelance work — milestone approval, partial payments, overdue delivery, disputes, and contract-value reconciliation.

This project focuses on those business rules rather than being a simple CRUD application.

---

## Problem

Freelance contracts often involve:

- Multiple delivery milestones
- Different deadlines
- Partial or staged payments
- Approval before final payment
- Client disputes and revisions
- Contract-value reconciliation
- Overdue work tracking

A normal invoice table does not represent these rules well.

This application models the contract as a lifecycle with explicit business invariants.

---

## Key Features

### Contract Management

Create contracts containing:

- Client
- Freelancer
- Contract title
- Total contract value
- Start date
- Multiple milestones

Milestone allocation is validated against the contract value.

For example:

```text
Contract value: $5,000

Milestone 1: $2,000
Milestone 2: $2,000
Milestone 3: $1,000

Total allocated: $5,000
