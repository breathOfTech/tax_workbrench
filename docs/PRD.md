# Tax Workbench - Product Requirements Document

Version: 0.1
Status: Draft for implementation agent
Date: 2026-07-20

## 1. Product identity

Product name: Tax Workbench
GitHub repository: `tax-workbench`
Python package name: `tax_workbench`
Suggested GitHub description: Agentic tax planning workspace for U.S. individual tax scenarios with source-grounded research, deterministic calculations, human review, and a live task plan.

Tagline: Understand your tax situation, compare scenarios, and know what to do next.

Note: Tax Workbench is a working title for a side project. Perform trademark and domain checks before commercial launch.

## 2. Product summary

Tax Workbench is an AI-assisted tax planning workspace for U.S. individuals with moderately complex finances. It helps users collect facts and documents, identify federal and state tax obligations, compare planning scenarios, discover lawful tax-saving opportunities, and create a clear to-do list.

The primary user is a W-2 employee who may be single or married, own a home, receive RSUs, trade stocks, receive dividends or interest, and optionally own one rental property in another state.

The product is not a tax filing service in the MVP. It does not submit returns, initiate payments, sign forms, or replace a CPA, enrolled agent, tax attorney, or financial adviser. It is a planning, education, evidence, and workflow product.

Use the phrase "lawful tax-planning opportunities" rather than "loopholes" in product copy.

## 3. Product thesis

Existing tax tools often force users through forms or answer isolated questions. Tax Workbench should instead act like a tax project manager:

1. Understand the user's goal.
2. Build a visible plan.
3. Collect the required evidence.
4. Delegate bounded work to specialized agents.
5. Run calculations in deterministic code.
6. explain findings with authoritative citations.
7. Ask the user only for missing facts or approvals.
8. Produce a scenario report and actionable to-do list.

The chat interface is a command surface. The task plan is the system of work.

## 4. Target persona

### Primary persona

A U.S. tax resident with the following profile:

- One or two W-2 jobs in the household.
- Filing status of single or married filing jointly.
- One primary residence.
- One taxable brokerage account.
- Interest, dividends, short-term gains, and long-term gains.
- RSU vesting and stock sales from one employer.
- Optional ownership of one residential rental property.
- Resident in one state and potentially earning rental income sourced to a second state.
- Wants to understand estimated liability, withholding gaps, filing obligations, and legal planning opportunities.

### Secondary use case

The user exports an organized package to share with their CPA or enrolled agent, containing:

- Confirmed taxpayer facts.
- Source documents.
- Open questions.
- Calculation inputs and outputs.
- Federal and state jurisdiction analysis.
- Candidate planning opportunities.
- Authoritative citations.
- A complete audit trail of user confirmations.

## 5. MVP scope

### Tax year strategy

Implement tax year 2025 first because complete federal publications and forms are available and outputs can be validated against completed returns. Add a 2026 planning mode after the source versioning and calculation framework are stable.

### Supported in MVP

- Federal individual income tax planning for tax year 2025.
- California resident state module.
- One additional nonresident state module selected for the demo scenario.
- Single and married filing jointly.
- W-2 income and federal/state withholding.
- Interest and dividends.
- Stock purchases and sales from Form 1099-B data.
- Short-term and long-term capital gains and losses.
- RSU vest and sale reconciliation.
- Primary residence and Form 1098 mortgage interest.
- Standard deduction versus itemized deduction comparison.
- One residential rental property.
- Rental income, common expenses, basis, and depreciation inputs.
- State residency and source-income analysis.
- Resident-state credit analysis where supported by the implemented state modules.
- Estimated federal and state liability.
- Withholding gap or over-withholding estimate.
- Scenario comparisons.
- Source-grounded tax-planning opportunities.
- User-visible task plan.
- Human approval and confirmation checkpoints.
- Accountant-ready report export.

### Explicitly excluded from MVP

- Electronic filing.
- Tax payment initiation.
- Return signing.
- Audit representation.
- Partnerships, S corporations, C corporations, trusts, or estates.
- Self-employment and Schedule C.
- Crypto assets.
- Foreign income, foreign accounts, or tax treaties.
- Incentive stock options, employee stock purchase plans, and complex equity derivatives.
- More than one rental property.
- Short-term rentals with material services.
- Depreciation recapture on a property sale.
- 1031 exchanges.
- Cost segregation.
- Alternative minimum tax optimization beyond a warning that professional review is needed.
- Full support for all 50 states in the first release.

## 6. Primary user goals

The system must support these user goals:

1. "Estimate what I may owe federally and in my state."
2. "Tell me whether my W-2 and RSU withholding appears sufficient."
3. "Explain the tax impact if I sell a specific stock or vested RSU position."
4. "Compare selling this year versus next year."
5. "Identify legal tax-planning opportunities before year-end."
6. "Explain whether I may need to file in another state because I own a rental property there."
7. "Show how rental income may affect federal, resident-state, and property-state taxes."
8. "Give me a prioritized to-do list and tell me which documents are missing."
9. "Prepare a report I can review with my CPA."

## 7. Core demo scenario

The demo taxpayer is a California resident with the following facts:

- Married filing jointly.
- Taxpayer and spouse each have a W-2.
- Taxpayer receives RSUs from an employer.
- Household has one brokerage account with dividends and stock sales.
- Household owns a primary residence with mortgage interest and property tax.
- Household owns one rental property in a second state.
- Some RSU sales have an apparent cost-basis mismatch between broker records and vest records.
- The user asks: "What might I owe, where might I need to file, and what can I still do before year-end to reduce taxes legally?"

Expected output:

- Federal estimated liability.
- California estimated liability.
- Nonresident-state filing analysis for the rental property.
- Withholding gap.
- RSU basis reconciliation warning.
- Standard-versus-itemized comparison.
- Rental income and depreciation summary.
- Candidate planning opportunities with assumptions, citations, and risk levels.
- A user to-do list.
- A CPA review package.

## 8. User experience

### 8.1 Main workspace

Built on CopilotKit's component model. The layout adapts between chat-first (early intake) and dashboard (analysis phase).

#### Chat-first mode (intake and Q&A)

- Full-width CopilotKit chat panel.
- Streaming agent activity (what it's doing, what it found).
- Inline approval prompts (CopilotKit actions) for fact confirmation.
- Collapsible sidebar with taxpayer profile summary and fact confidence indicators.

#### Dashboard mode (analysis and planning)

Left panel:

- Taxpayer profile (auto-populated from fact ledger).
- Tax year.
- Filing status.
- Resident state.
- Other relevant states.
- Connected or uploaded data sources.
- Prior scenarios.

Center panel:

- Live task plan (rendered from TaxTask graph via CopilotKit steps).
- Parent and child tasks.
- Status, owner, due date, and dependencies.
- Streaming progress summaries.
- Completed artifacts.

Right panel:

- Current task details.
- Missing information.
- Evidence used.
- Source citations.
- Assumptions.
- User input controls.
- Approve, reject, or edit controls (CopilotKit human-in-the-loop components).

Top summary bar:

- Estimated federal liability.
- Estimated resident-state liability.
- Estimated nonresident-state liability.
- Withholding gap.
- Open questions.
- High-risk items.
- Tax readiness score.

### 8.2 CopilotKit integration points

- **`useCopilotAction`** — Register approval actions (confirm fact, approve scenario, accept recommendation).
- **`useCopilotReadable`** — Expose fact ledger state and task plan to the copilot context.
- **`CopilotTask`** — Map TaxTask execution to visible streaming steps.
- **LangGraph streaming** — Wire supervisor events to CopilotKit's event stream via `@copilotkit/sdk`.

### 8.2 Task statuses

Use the following product-level statuses:

- planned
- in_progress
- needs_user_input
- needs_user_review
- needs_professional_review
- blocked
- completed
- canceled

### 8.3 User-visible activity

Do not display private chain-of-thought reasoning. Display concise activity summaries such as:

- "Reviewing RSU vest records and broker cost basis."
- "Checking California treatment of rental income from another state."
- "Comparing standard and itemized deductions."
- "Waiting for confirmation of rental property placed-in-service date."

## 9. Functional requirements

### FR-001: Conversational intake (primary) and guided onboarding

The system must support two intake modes:

#### Conversational mode (primary)

The user may provide informal, incomplete information in natural language. Examples:

- "I make about 200k, my wife works part-time at a nonprofit"
- "I sold some RSUs last month, maybe 50 shares"
- "We have a rental in Texas but I'm not sure what we paid for it"

The intake agent must:

- Extract structured facts from casual statements.
- Assign confidence scores to inferred values.
- Identify what's missing and ask targeted follow-up questions.
- Work with partial information — produce estimates with stated assumptions rather than blocking on missing data.
- Progressively refine the fact ledger as more information arrives.

#### Document mode (enrichment)

When documents are uploaded, they enrich and override conversational facts with higher-confidence extracted data.

#### Common requirements

The system must eventually collect and confirm:

- Tax year.
- Filing status.
- Spouse information when applicable.
- State residency and residency dates.
- W-2 employers.
- Home ownership.
- Brokerage and equity compensation.
- Rental property ownership and location.
- Prior-year return availability.
- User goal.

Material facts must be confirmed by the user before they are treated as canonical. However, the system must be able to produce useful guidance even with unconfirmed, low-confidence facts — clearly labeling assumptions.

### FR-002: Document intake

The system must accept:

- W-2.
- 1099-INT.
- 1099-DIV.
- 1099-B.
- Brokerage transaction CSV.
- RSU vest statements.
- Form 1098.
- Property tax statement.
- Rental income and expense CSV.
- Closing statement or basis worksheet.
- Prior-year federal and state returns.

The system must extract structured data and preserve a link to the source page or row.

### FR-003: Tax profile and fact ledger

The system must maintain a canonical fact ledger. Each fact must include:

- Value.
- Tax year.
- Jurisdiction.
- Source document or user statement.
- Confirmation status.
- Confidence.
- Effective date.
- Last updated time.

### FR-004: Dynamic task planning

The planner must convert the user goal into a task graph. It must:

- Create parent and child tasks.
- Identify dependencies.
- Assign tasks to a user, agent, or deterministic service.
- Update task status as work progresses.
- Add new tasks when missing information or conflicts are found.
- Preserve the plan across sessions.

### FR-005: Source-grounded tax research

Every tax rule or recommendation must cite an authoritative source. The research layer must prioritize:

1. Internal Revenue Code, Treasury regulations, and official IRS guidance.
2. Current IRS forms and instructions.
3. Current IRS publications and official topic pages.
4. Official state tax authority statutes, forms, instructions, and guidance.
5. User-provided CPA guidance, clearly labeled as user-provided.

The system must not treat blogs, social media, or commercial tax sites as authoritative sources in the MVP.

### FR-006: Source versioning

Every ingested tax source must include:

- Authority.
- Jurisdiction.
- Tax year.
- Publication or form number.
- Effective date.
- Last reviewed date.
- Source URL.
- Content checksum.
- Superseded status.
- Section or page reference.

The retrieval system must exclude superseded rules unless the user is analyzing the matching historical tax year.

### FR-007: Deterministic calculations

LLMs must not calculate final tax liability from prose alone. A versioned calculation library must handle:

- Ordinary taxable income.
- Standard and itemized deductions.
- Qualified dividends.
- Short-term and long-term capital gains and losses.
- Federal income tax brackets.
- Net investment income tax when applicable.
- Federal withholding comparison.
- State taxable income adjustments.
- Resident and nonresident state liability for implemented modules.
- Rental income and expense totals.
- Depreciation inputs and schedules supported by the MVP.
- Credits for taxes paid to another state where supported.

Every calculation result must include an input snapshot and tax-rule version.

### FR-008: RSU reconciliation

The system must:

- Extract vest dates, shares, fair market value, and withholding.
- Identify whether vest income appears in W-2 wages.
- Match sold shares to vest lots where possible.
- Compare broker-reported basis with vest-derived basis.
- Flag potential double taxation caused by missing or incorrect basis.
- Require user review when lot matching is ambiguous.

### FR-009: State jurisdiction analysis

The jurisdiction service must determine:

- Resident state.
- Part-year or nonresident states.
- Income-source state for rental property.
- Which state modules are required.
- Whether resident-state credit analysis may apply.
- Which missing residency or property facts must be confirmed.

The system must not generalize one state's rules to another state.

### FR-010: Rental property analysis

For one residential rental property, the system must collect:

- Property state.
- Acquisition date.
- Placed-in-service date.
- Purchase price and basis allocation.
- Land value.
- Rental income.
- Mortgage interest.
- Property tax.
- Insurance.
- Repairs and maintenance.
- Management fees.
- Utilities.
- Personal use days.
- Improvements.
- Prior depreciation.

The system must identify questions that require professional review, including passive activity limitations, material participation, personal use, basis uncertainty, and state-specific treatment.

### FR-011: Scenario engine

Users must be able to compare scenarios such as:

- Sell a stock position this year versus next year.
- Realize a loss versus hold.
- Sell RSUs immediately versus hold.
- Adjust W-4 withholding.
- Increase eligible retirement or HSA contributions.
- Standard deduction versus itemized deduction.
- Apply or do not apply a candidate rental expense, pending evidence.

Each scenario must show:

- Changed assumptions.
- Estimated federal impact.
- Estimated state impact.
- Cash-flow effect.
- Uncertainty.
- Required actions.
- Source citations.

### FR-012: Tax-planning opportunity engine

The system may identify candidate lawful strategies, including:

- Withholding adjustment.
- Estimated payment planning.
- Eligible retirement contribution planning.
- HSA contribution planning when eligible.
- Tax-loss harvesting candidates with wash-sale warnings.
- Capital gain timing.
- Charitable contribution planning.
- Standard versus itemized deduction comparison.
- Mortgage interest and state/local tax documentation.
- RSU basis correction and sale timing analysis.
- Rental expense and depreciation record completeness.
- Passive loss carryforward awareness.

A recommendation must never be a bare instruction. It must include:

- Why it may apply.
- Required eligibility facts.
- Assumptions.
- Estimated impact range.
- Risks and tradeoffs.
- Federal and state citations.
- Deadline.
- Risk level.
- Whether CPA review is required.

### FR-013: Human-in-the-loop approval

Human confirmation is required before:

- Treating an inferred fact as canonical.
- Accepting filing status.
- Accepting residency dates.
- Accepting an RSU lot match.
- Accepting rental basis or placed-in-service date.
- Including a high-impact deduction in a scenario.
- Finalizing a tax-planning report.
- Sharing a report with a third party.

The MVP must not allow filing, payment, or external account changes.

### FR-014: Report export

The system must produce:

- Executive summary.
- Confirmed facts.
- Missing facts.
- Federal estimate.
- State estimates.
- Withholding analysis.
- Investment and RSU analysis.
- Home and itemization analysis.
- Rental property analysis.
- Candidate planning opportunities.
- Open professional-review items.
- Source citations.
- Calculation version and timestamp.
- User approvals.

Export formats:

- PDF.
- JSON.
- CSV for normalized tax inputs.

## 10. Agent architecture

### 10.1 Architecture principle

Use LangGraph as the durable workflow runtime and Deep Agents as a bounded planning and delegation harness.

LangGraph owns:

- Canonical state.
- Durable execution.
- Checkpoints.
- Interrupts.
- Human approval.
- Retries.
- Task dependencies.
- Workflow recovery.

Deep Agents owns:

- Initial planning.
- Task decomposition.
- Delegation to isolated subagents.
- Context offloading.
- Summarization of bounded work.

PostgreSQL, not agent memory, is the source of truth for taxpayer facts and calculation results.

### 10.2 Why subagents (not one big agent)

A single monolithic agent fails here because:

1. **Context window limits.** Tax research + RSU reconciliation + rental analysis + state rules cannot fit in one context. Subagents operate in bounded contexts and return structured summaries.
2. **Isolation of concerns.** The research agent should never call the calculator. The intake agent should never make recommendations. Tool access is scoped per subagent.
3. **Parallel execution.** Jurisdiction research and investment analysis are independent — they run concurrently.
4. **Failure isolation.** If the property agent fails, the investment analysis is unaffected. The supervisor retries only the failed branch.
5. **Testability.** Each subagent has a clear input/output contract that can be evaluated independently.

### 10.3 Supervisor graph

```text
START
  → route_input
      ├── [user message] → intake_agent → update_fact_ledger
      ├── [document upload] → document_agent → update_fact_ledger
      └── [goal/command] → planner
  → planner
      → assess_readiness (what facts do we have? what's missing?)
      → create_or_update_task_graph
      → decide: enough info to proceed? or ask user?
          ├── [insufficient] → generate_clarifying_questions → WAIT
          └── [sufficient] → delegate_analysis
  → delegate_analysis (parallel where possible)
      ├── jurisdiction_agent (which states? which rules?)
      ├── research_agent (retrieve relevant tax law via RAG)
      ├── investment_agent (RSU, capital gains, dividends)
      └── property_agent (rental, primary home)
  → merge_results
      → resolve_conflicts (flag contradictions)
      → assemble_calculation_inputs
  → run_deterministic_calculations
      → tax_engine (pure Python, no LLM)
  → strategy_agent
      → generate opportunities from calc results + facts + rules
  → verification_agent
      → check citations, consistency, calc provenance
  → human_review_interrupt (if high-risk items exist)
  → generate_response
      → synthesize findings into user-facing answer
      → include: estimates, assumptions, what's missing, next steps
  → persist_audit_record
  → END (or loop back for follow-up)
```

### 10.4 Subagents

#### Intake agent

Role: Convert casual user statements into structured tax facts.

Input: Natural language message from user.
Output: List of `TaxFact` objects with confidence scores.

Responsibilities:

- Parse informal income/expense/life-event statements.
- Map to fact types (W2_income, filing_status, state_residency, etc.).
- Assign confidence (user said "about 200k" → value=200000, confidence=0.7).
- Identify ambiguities and generate targeted follow-up questions.
- Handle corrections ("actually it was 180k not 200k").

Tools available:

- `fact_ledger.write` — persist extracted facts.
- `fact_ledger.read` — check existing facts to avoid duplicates.

Restrictions:

- No tax recommendations.
- No calculations.
- No document parsing (that's the document agent).

#### Document intake agent

Role: Extract structured data from uploaded tax documents.

Input: Document file + document type hint (optional).
Output: Extracted fields linked to source page/row.

Responsibilities:

- Classify document type (W-2, 1099-B, 1098, etc.).
- Extract structured fields.
- Link each field to source evidence (page, row, cell).
- Detect duplicates against existing facts.
- Report missing expected documents.
- Override conversational facts with higher-confidence extracted values.

Tools available:

- `document_parser.extract` — OCR/parse the document.
- `fact_ledger.write` — persist extracted facts.
- `fact_ledger.read` — check for duplicates.

Restrictions:

- No tax recommendations.
- No calculation of final liability.

#### Research agent

Role: Retrieve and synthesize authoritative tax rules via RAG.

Input: Specific tax question + jurisdiction + tax year.
Output: Structured rule summary with citations.

Responsibilities:

- Formulate retrieval queries from the tax question.
- Filter sources by tax year, jurisdiction, authority.
- Return relevant passages with full citation metadata.
- Synthesize rules into structured summaries.
- Flag when no authoritative source is found.

Tools available:

- `source_retriever.search` — semantic search over tax corpus.
- `source_retriever.get_document` — fetch full section.

Restrictions:

- No uncited conclusions.
- No unofficial sources as authority.
- Must return "insufficient authority" rather than guess.

#### Jurisdiction agent

Role: Determine filing obligations and applicable state rules.

Input: Taxpayer facts (residency, income sources, property locations).
Output: List of required filings + applicable state modules.

Responsibilities:

- Determine resident state.
- Identify nonresident/part-year filing obligations.
- Identify income-source states (rental property state, etc.).
- Determine which state modules are needed.
- Identify resident-state credit applicability.
- Flag missing residency or property facts.

Tools available:

- `fact_ledger.read` — get taxpayer facts.
- `source_retriever.search` — look up state filing thresholds.

Restrictions:

- Must not generalize one state's rules to another.
- Must cite state authority for each conclusion.

#### Investment and RSU agent

Role: Analyze investment income and RSU positions.

Input: Brokerage facts, 1099-B data, RSU vest records.
Output: Structured calculation inputs + discrepancy flags.

Responsibilities:

- Normalize dividends, interest, capital gains/losses.
- Match RSU vest records to sale transactions.
- Detect cost-basis discrepancies (broker vs. vest-derived).
- Classify gains as short-term or long-term.
- Identify tax-loss harvesting candidates.
- Prepare structured inputs for the calculation engine.

Tools available:

- `fact_ledger.read` — get investment facts.
- `tax_calculator.classify_gains` — determine gain type.
- `source_retriever.search` — RSU tax treatment rules.

Restrictions:

- Ambiguous lot matches require user review (cannot assume).
- Cannot calculate final liability (that's the tax engine).

#### Property agent

Role: Analyze primary residence and rental property tax implications.

Input: Property facts, mortgage info, rental income/expenses.
Output: Structured calculation inputs + missing-info flags.

Responsibilities:

- Normalize primary-home and rental-property facts.
- Validate depreciation inputs (basis, placed-in-service date, method).
- Identify missing evidence (basis allocation, land value, expenses).
- Retrieve federal and state property rules.
- Prepare Schedule E-style inputs for the calculation engine.

Tools available:

- `fact_ledger.read` — get property facts.
- `source_retriever.search` — rental/depreciation rules.

Restrictions:

- Passive activity limitations with uncertain participation → professional review.
- Property sale / 1031 exchange → professional review.

#### Strategy agent

Role: Generate actionable tax-planning opportunities.

Input: Calculation results + verified facts + retrieved rules.
Output: Ranked list of recommendations with citations.

Responsibilities:

- Identify candidate strategies from calc results and fact patterns.
- Rank by estimated impact, deadline, confidence, effort.
- Generate user to-do items with deadlines.
- Include required eligibility facts and assumptions.
- Assess risk level and whether CPA review is needed.

Tools available:

- `fact_ledger.read` — current facts.
- `tax_calculator.run_scenario` — model what-if impacts.
- `source_retriever.search` — cite authority for each strategy.

Restrictions:

- Cannot invent tax rules or rates.
- Cannot recommend evasion, concealment, sham transactions, or abusive shelters.
- Every recommendation must have a citation.

#### Verification agent

Role: Quality-check all agent outputs before presenting to user.

Input: Merged results from all other agents.
Output: Verified results or conflict/error flags.

Responsibilities:

- Check that every rule claim has a citation.
- Check that citations match the tax year and jurisdiction.
- Check that numerical results came from deterministic calculations.
- Detect conflicts between agent outputs.
- Route unresolved conflicts to human or professional review.

Tools available:

- `source_retriever.verify_citation` — confirm citation exists and matches claim.
- `fact_ledger.read` — cross-check facts used.

Restrictions:

- Cannot resolve conflicts by choosing — must escalate.

### 10.5 Agent communication pattern

Subagents do NOT talk to each other directly. All communication flows through the supervisor:

```text
Supervisor (LangGraph state)
    │
    ├── dispatches task → Subagent A
    │       └── returns structured result → Supervisor state
    ├── dispatches task → Subagent B
    │       └── returns structured result → Supervisor state
    │
    └── Supervisor merges results, resolves, dispatches next step
```

Shared state lives in PostgreSQL (fact ledger, task graph, calc results). Subagents read from and write to the database via their scoped tools — they never pass large payloads through the supervisor's context.

### 10.6 Context engineering strategy

The core challenge: tax analysis requires more information than fits in any single context window.

Principles:

1. **Fact ledger as external memory.** Agents don't carry all facts in context — they query the ledger for relevant facts per task.
2. **Scoped context per subagent.** Each subagent receives only the facts and instructions relevant to its task. The investment agent never sees rental property details.
3. **Progressive summarization.** When a subagent completes, its full reasoning is persisted to the audit log but only a structured summary enters the supervisor's state.
4. **Retrieval over recall.** Rather than stuffing the prompt with all IRS rules, agents retrieve specific passages on demand via RAG tools.
5. **Confidence-aware assembly.** The context assembler prioritizes confirmed facts over inferred ones, and flags low-confidence inputs in the agent's prompt.

## 11. Retrieval-augmented generation design

### 11.1 Initial federal corpus

Ingest and version at minimum:

- Form 1040 and instructions.
- Schedule A and instructions.
- Schedule D and instructions.
- Schedule E and instructions.
- Form 8960 and instructions.
- Publication 505, Tax Withholding and Estimated Tax.
- Publication 525, Taxable and Nontaxable Income.
- Publication 550, Investment Income and Expenses.
- Publication 523, Selling Your Home.
- Publication 527, Residential Rental Property.
- Publication 551, Basis of Assets.
- Publication 925, Passive Activity and At-Risk Rules.
- Publication 936, Home Mortgage Interest Deduction.
- Official IRS credits and deductions pages.
- Official IRS Tax Withholding Estimator guidance.

### 11.2 State corpus

For each implemented state, ingest only official tax authority sources:

- Resident return instructions.
- Nonresident or part-year return instructions.
- Rental income guidance.
- Credit-for-taxes-paid-to-another-state guidance.
- Capital gain treatment.
- Standard or itemized deduction rules.
- State-specific forms and schedules.

### 11.3 Retrieval metadata

Each chunk must include:

```json
{
  "authority": "IRS",
  "jurisdiction": "US-FED",
  "tax_year": 2025,
  "document_type": "publication",
  "document_id": "Publication 527",
  "topic": ["rental_income", "depreciation"],
  "effective_date": "2025-01-01",
  "source_url": "https://www.irs.gov/publications/p527",
  "section": "Depreciation of Rental Property",
  "page": 9,
  "superseded": false,
  "checksum": "sha256:..."
}
```

### 11.4 Retrieval safeguards

- Filter by tax year and jurisdiction before semantic ranking.
- Prefer exact form instructions over general publications for form-specific questions.
- Return source passages and section identifiers.
- Do not answer when no authoritative source is found.
- Mark uncertain interpretations for professional review.
- Re-ingest sources when checksums or last-reviewed dates change.

## 12. Data model

Minimum entities (single-user, no auth):

- TaxYearWorkspace
- Jurisdiction
- TaxFact
- SourceDocument
- ExtractedField
- IncomeItem
- EquityLot
- RSUVest
- SecuritySale
- Residence
- RentalProperty
- RentalIncomeItem
- RentalExpenseItem
- TaxTask
- TaskDependency
- CalculationRun
- Scenario
- Recommendation
- Citation
- Approval
- AuditEvent
- ExportArtifact

### 12.1 TaxTask schema

```json
{
  "id": "task_123",
  "workspace_id": "ws_2025_001",
  "title": "Reconcile RSU cost basis",
  "status": "needs_user_review",
  "owner_type": "user",
  "assigned_agent": "investment_and_rsu_agent",
  "risk_level": "high",
  "dependencies": ["task_120"],
  "evidence_ids": ["doc_broker_1099b", "doc_rsu_vests"],
  "missing_fields": ["lot_selection_method"],
  "approval_required": true,
  "result_summary": "Three sales have broker basis that may exclude compensation income.",
  "created_at": "2026-07-20T12:00:00Z"
}
```

### 12.2 Recommendation schema

```json
{
  "id": "rec_456",
  "title": "Review W-4 withholding",
  "category": "withholding",
  "tax_year": 2025,
  "jurisdictions": ["US-FED", "US-CA"],
  "status": "candidate",
  "estimated_impact_low": 0,
  "estimated_impact_high": 0,
  "cash_flow_effect": "Increase withholding to reduce projected balance due.",
  "assumptions": ["Current income remains unchanged"],
  "required_facts": ["Remaining pay periods"],
  "citations": ["citation_1", "citation_2"],
  "confidence": 0.86,
  "risk_level": "medium",
  "professional_review_required": false,
  "deadline": "2025-12-15"
}
```

## 13. Safety and compliance requirements

- Present the product as educational planning software, not a licensed tax adviser.
- Do not use the phrase "guaranteed savings."
- Do not claim the system found every deduction or credit.
- Require source citations for every tax-law claim.
- Require deterministic calculations for numerical tax outputs.
- Clearly label estimates and assumptions.
- Flag high-impact or ambiguous items for CPA or enrolled-agent review.
- Prohibit advice involving concealment, unreported income, false residency, sham entities, fabricated expenses, or abusive transactions.
- Never transmit a return or payment in the MVP.
- Never request or store Social Security numbers in the initial public demo.
- Redact account numbers and sensitive identifiers before model calls.
- Do not use customer data to train models by default.

## 14. Human-in-the-loop policy

### Automatic actions

- Read uploaded documents.
- Extract fields.
- Search authoritative sources.
- Run deterministic calculations.
- Create and update tasks.
- Generate draft scenarios.

### User confirmation required

- Filing status.
- Residency dates.
- Spouse data.
- RSU lot matching.
- Rental property basis.
- Rental placed-in-service date.
- Personal-use days.
- Material tax facts inferred from documents.

### Professional review recommended or required

- Conflicting state residency evidence.
- Significant multi-state income allocation.
- Passive activity limitations with uncertain participation.
- Large RSU basis discrepancies.
- Alternative minimum tax exposure.
- Property sale, depreciation recapture, or 1031 exchange.
- Any recommendation with incomplete authority or high financial impact.

## 15. Evaluation plan

### 15.1 Functional evaluations

- Correct workflow classification.
- Correct task plan generated.
- Correct subagent selected.
- Required facts identified.
- Dependencies respected.
- Workflow resumes after interrupt.
- User edits are preserved.

### 15.2 Retrieval evaluations

- Correct tax year.
- Correct jurisdiction.
- Correct source authority.
- Citation supports the claim.
- Superseded source is not used.
- No answer is produced without sufficient authority.

### 15.3 Calculation evaluations

Create golden test cases for:

- Single W-2 taxpayer.
- Married two-W-2 household.
- Qualified dividends.
- Short-term and long-term gains.
- Capital loss limitation and carryforward input.
- RSU vest and sale basis.
- Standard versus itemized deduction.
- Mortgage interest inputs.
- Rental income and depreciation.
- Resident and nonresident state modules.
- Credit for taxes paid to another state.

Expected output must match a reference implementation to the cent before rounding rules are applied.

### 15.4 Security evaluations

- Prompt injection inside an uploaded PDF is ignored.
- An agent cannot call an unauthorized tool.
- Approval cannot be bypassed.
- Sensitive identifiers are redacted before model calls.
- Unofficial web content cannot override official sources.

### 15.5 Agent quality metrics

- End-to-end task completion rate.
- Citation correctness rate.
- Deterministic calculation pass rate.
- User correction rate.
- Number of unnecessary clarification questions.
- Percentage of high-risk items correctly escalated.
- Tool-call failure rate.
- Workflow recovery rate.
- Median time to a complete scenario report.
- Cost per completed analysis.

## 16. Technology stack

Frontend:

- CopilotKit (React, open-source agent UI framework)
  - Chat panel with streaming agent responses
  - Task plan visualization via CopilotKit actions/steps
  - Human-in-the-loop approval components (fact confirmation, lot matching, etc.)
  - Native LangGraph integration via @copilotkit/sdk
  - Extensible React components for custom views (scenario comparison, report)
- Next.js as the host app (lightweight — CopilotKit does the heavy lifting)
- Tailwind CSS for any custom styling
- Markdown-based report rendering

Backend:

- Python 3.12+
- FastAPI
- Pydantic v2
- LangGraph (durable workflow runtime, checkpoints, interrupts)
- Deep Agents (planning, delegation, context offloading)
- PostgreSQL 16+ with pgvector extension
- JSONB columns for flexible agent outputs and extracted fields
- Redis for ephemeral pub-sub coordination only (optional, add when needed)
- Local filesystem or S3 for document storage

Tax engine:

- Versioned Python package under `packages/tax_engine`
- Decimal arithmetic (no floats for money)
- Property-based tests
- Golden test fixtures

Observability and evaluation:

- LangSmith
- OpenTelemetry
- Structured audit events in PostgreSQL
- Pytest

Authentication and security:

- Single-user only. No auth, no multi-tenancy, no user management.
- PII redaction middleware before model calls (SSN, account numbers)
- Local-first — runs on user's machine or personal server

## 17. Repository structure

```text
tax-workbench/
  README.md
  LICENSE
  .env.example
  docker-compose.yml
  pyproject.toml                      # root project config (uv/poetry workspace)

  apps/
    api/                              # FastAPI service
      main.py
      routes/
      dependencies.py
    web/                              # Next.js + CopilotKit frontend
      src/
        app/
        components/
          task-plan/                  # task graph visualization
          approval/                   # HIL confirmation dialogs
          scenarios/                  # scenario comparison view
          report/                     # report preview/export
        copilot/
          actions.ts                  # CopilotKit action definitions
          config.ts                   # CopilotKit + LangGraph wiring

  src/
    tax_workbench/                    # main Python package
      __init__.py
      config.py

      # ─── Agent layer ───
      agents/
        __init__.py
        supervisor.py                 # top-level LangGraph orchestrator
        planner.py                    # goal → task graph decomposition
        subagents/
          __init__.py
          intake_agent.py             # conversational fact extraction
          research_agent.py           # RAG over tax sources
          jurisdiction_agent.py       # state filing analysis
          investment_agent.py         # RSU, stocks, dividends
          property_agent.py           # rental + primary residence
          strategy_agent.py           # planning opportunities
          verification_agent.py       # citation + consistency checks
        tools/
          __init__.py
          fact_ledger.py              # read/write/query facts
          tax_calculator.py           # call deterministic engine
          source_retriever.py         # RAG search tool
          document_parser.py          # extract fields from uploads
          scenario_runner.py          # compare what-if scenarios
        prompts/
          system/                     # system prompts per agent
          few_shot/                   # example interactions

      # ─── Context engineering ───
      context/
        __init__.py
        fact_ledger.py                # canonical fact store logic
        confidence.py                 # scoring and resolution
        context_assembler.py          # build agent context from facts + history
        progressive_refinement.py     # handle partial info gracefully

      # ─── RAG layer ───
      rag/
        __init__.py
        ingestion.py                  # parse + chunk IRS/state sources
        embeddings.py                 # embedding generation
        retriever.py                  # filtered semantic search
        source_registry.py            # version/checksum tracking
        metadata.py                   # chunk metadata schema

      # ─── Tax engine (deterministic) ───
      tax_engine/
        __init__.py
        federal/
          __init__.py
          income.py                   # AGI, taxable income
          brackets.py                 # tax rate schedules
          deductions.py               # standard vs itemized
          credits.py
          capital_gains.py
          niit.py                     # net investment income tax
          withholding.py
        states/
          __init__.py
          california/
            __init__.py
            resident.py
            nonresident.py
          base.py                     # state module interface
        rental/
          __init__.py
          income_expense.py
          depreciation.py
        rsu/
          __init__.py
          reconciliation.py
          lot_matching.py
        scenarios/
          __init__.py
          engine.py                   # scenario comparison logic
          differ.py                   # diff two calculation runs

      # ─── Data models ───
      models/
        __init__.py
        workspace.py
        taxpayer.py
        facts.py
        documents.py
        tasks.py
        calculations.py
        scenarios.py
        recommendations.py
        audit.py

      # ─── Database ───
      db/
        __init__.py
        session.py
        migrations/                   # alembic
        repositories/                 # data access layer

  data/
    fixtures/                         # test data
    golden_cases/                     # validated tax scenarios
    source_manifests/                 # IRS/state source metadata
    sources/                          # downloaded/cached tax publications

  docs/
    PRD.md
    architecture.md
    agent-design.md
    threat-model.md

  scripts/
    ingest_sources.py
    run_evals.py
    seed_demo.py

  tests/
    unit/
      test_tax_engine/
      test_agents/
      test_rag/
      test_context/
    integration/
    e2e/
```

## 18. API outline

Minimum endpoints:

```text
POST   /v1/workspaces
GET    /v1/workspaces/{id}
POST   /v1/workspaces/{id}/documents
POST   /v1/workspaces/{id}/goals
GET    /v1/workspaces/{id}/tasks
PATCH  /v1/tasks/{id}
POST   /v1/tasks/{id}/approve
POST   /v1/tasks/{id}/reject
GET    /v1/workspaces/{id}/facts
PATCH  /v1/facts/{id}
POST   /v1/workspaces/{id}/scenarios
GET    /v1/scenarios/{id}
POST   /v1/workspaces/{id}/calculate
GET    /v1/workspaces/{id}/recommendations
POST   /v1/workspaces/{id}/exports
GET    /v1/runs/{id}/events
```

## 19. Implementation phases

### Phase 0: Agent foundation

- Create monorepo with `uv` workspace.
- PostgreSQL via docker-compose (with pgvector).
- Alembic migrations for core models (Workspace, TaxFact, TaxTask, AuditEvent).
- LangGraph supervisor skeleton with checkpoint persistence.
- Intake agent: parse casual user input → structured facts.
- Fact ledger: write/read/query facts with confidence scores.
- Planner: goal → task graph (stored in PostgreSQL).
- One subagent executing a trivial task (prove the delegation pattern works).
- Chainlit chat interface wired to the supervisor.
- Basic tests for agent routing and fact extraction.

Exit criteria:

- User types "I make 200k in California, married" → facts are extracted, stored, and a task plan is created. One subagent executes and returns a result.

### Phase 1: RAG + Research agent + Federal tax engine

- Ingest 3-5 core IRS publications (chunked, embedded, stored in pgvector).
- Source registry with version/checksum tracking.
- Research agent: answer tax questions with cited passages.
- Federal tax engine: income, brackets, standard deduction, withholding comparison.
- Deterministic calculation from fact ledger inputs.
- Golden test cases for single W-2 and married two-W-2.

Exit criteria:

- User says "I earn 200k, wife earns 80k, we're in CA" → system estimates federal liability with IRS citations, compares to rough withholding, identifies what info is still missing.

### Phase 2: Investment + RSU agent

- Investment agent with RSU reconciliation.
- Capital gains classification (short/long term).
- 1099-B and RSU vest record parsing.
- Basis discrepancy detection.
- Scenario tool: "what if I sell X shares now vs next year?"
- Extend tax engine: capital gains, NIIT, qualified dividends.

Exit criteria:

- System identifies a seeded RSU basis mismatch and routes for user review. Scenario comparison works.

### Phase 3: Property + multi-state

- Property agent for rental + primary residence.
- Jurisdiction agent for multi-state analysis.
- Schedule E inputs and depreciation.
- California state module.
- One nonresident state module.
- Resident-state credit analysis.

Exit criteria:

- Demo scenario produces federal + CA + nonresident-state estimates with rental analysis and citations.

### Phase 4: Strategy + verification + report

- Strategy agent with ranked opportunities.
- Verification agent (citation check, consistency check).
- Human-in-the-loop approval flow (LangGraph interrupts).
- Markdown/JSON report export.
- CPA handoff package.

Exit criteria:

- Complete seeded scenario runs from conversational input to verified, cited report with actionable recommendations.

## 20. Definition of done for MVP

The MVP is complete when:

- A seeded user can upload or enter W-2, brokerage, RSU, home, and rental data.
- The system produces a visible, persistent task plan.
- At least four specialized agents execute bounded tasks.
- Federal, California, and one nonresident-state calculation paths pass golden tests.
- Every legal or tax rule claim has an authoritative citation.
- Numerical tax outputs come from deterministic code.
- The system detects a seeded RSU basis mismatch.
- The system identifies the rental property's nonresident-state filing question.
- The system generates at least three source-grounded planning opportunities.
- High-risk items require user or professional review.
- The user can export an accountant-ready report.
- Prompt-injection and cross-tenant tests pass.

## 21. First implementation prompt for a coding agent

Use the following prompt after creating the repository:

```text
You are implementing Tax Workbench from docs/PRD.md.

Start with Phase 0 only. Focus on the agent architecture foundation.

Requirements:
1. Create a Python monorepo with uv workspace. Structure per section 17.
2. Use FastAPI for the API, Chainlit for the chat UI.
3. Add PostgreSQL 16 + pgvector via docker-compose.
4. Implement SQLAlchemy models: Workspace, TaxFact, TaxTask, TaskDependency, AuditEvent.
5. Implement the LangGraph supervisor graph with:
   - State management via Postgres checkpointer.
   - Router node that classifies user input (conversational fact, document, goal).
   - Intake agent subgraph that extracts facts from natural language.
   - Planner node that creates a task graph from a user goal.
   - One dummy subagent that proves delegation + structured return works.
   - Human interrupt point.
6. Implement the fact ledger with confidence scoring.
7. Wire Chainlit to the supervisor — user messages flow in, streamed responses flow out.
8. Implement agent tools as scoped functions (fact_ledger.read, fact_ledger.write).
9. Add unit tests for fact extraction and one e2e test: user says "I make 200k in CA, married" → facts stored, plan created.
10. Do not add tax calculations, RAG, or document OCR in this phase.

Before coding, produce:
- an implementation plan,
- the proposed file tree,
- database schema,
- agent state schema,
- tool definitions,
- and test plan.

Then implement incrementally and run tests after each milestone.
```

## 22. Authoritative source seeds

Federal sources:

- https://www.irs.gov/individuals/tax-withholding-estimator
- https://www.irs.gov/credits-and-deductions-for-individuals
- https://www.irs.gov/pub/irs-pdf/p525.pdf
- https://www.irs.gov/pub/irs-pdf/p550.pdf
- https://www.irs.gov/pub/irs-pdf/p523.pdf
- https://www.irs.gov/publications/p527
- https://www.irs.gov/pub/irs-pdf/p551.pdf
- https://www.irs.gov/publications/p925
- https://www.irs.gov/publications/p936

Example state source:

- https://www.ftb.ca.gov/file/personal/income-types/rental.html

Agent framework sources:

- https://docs.langchain.com/oss/python/langgraph/overview
- https://docs.langchain.com/oss/python/deepagents/overview

## 23. Product wording guidelines

Preferred wording:

- tax planning
- estimated tax impact
- candidate opportunity
- source-grounded guidance
- user-confirmed fact
- professional review recommended
- lawful tax strategy

Avoid:

- loophole
- guaranteed savings
- audit-proof
- zero hallucinations
- replaces your CPA
- fully autonomous tax adviser
- definitive legal advice
