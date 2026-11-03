---
name: openbook-market-contracts
description: Choose and explain OpenBook Betting, OpenExchange or OpenVenue contracts for coverage, order lifecycle, exchange depth, fees, tokenized equivalence and all-in quotes without assuming interoperability.
---

# Market and venue contracts

## Sources

Read the [betting profile](https://github.com/openbook-data-standards/openbook-betting/blob/main/README.md), [OpenExchange specification](https://github.com/openbook-data-standards/openexchange/blob/main/spec/openexchange.md), [OpenVenue specification](https://github.com/openbook-data-standards/openvenue/blob/main/spec/openvenue.md) and [readiness catalog](https://github.com/openbook-data-standards/openbook/blob/main/docs/ecosystem.json). Select the actual project's schemas and examples at a reviewed revision.

## Workflow

1. Identify the user's required information before selecting a contract: venue acceptance/order lifecycle uses Betting; exchange state/runners/back-lay depth uses OpenExchange; tokenized instrument equivalence and fee-adjusted quotes uses OpenVenue. Core OpenBook supplies sportsbook document identity and changes, not all these surfaces.
2. Explain overlap without declaring wire interchangeability. Check each project's normative precedence independently: OpenVenue says its prose wins; OpenExchange says its schemas win. Do not silently reconcile differences.
3. Gate betting profile compatibility: its objects do not fit core's closed object enum and use a profile envelope (ONB-005). Do not modify core or promise compatibility with openbook-js without evidence.
4. Read synthetic Betting/OpenVenue documents. OpenExchange lacks a supplied example corpus at catalog review (ONB-006); provide schema orientation rather than inventing a supported end-to-end adapter.
5. Preserve native runner/venue identity, original back/lay semantics, exact decimal amounts, timestamps, fees and lifecycle states. Equivalence requires evidence; similar names do not establish the same instrument. Source quotes are not accepted executable orders.
6. For any authorized implementation, propose a bounded adapter and CI validation using the selected contract/version. Obtain separate approval for changes to normative contracts.

## Evidence

Report the selected contract, exact revision, relevant schema/example, preserved semantics and any compatibility blocker. Explain why the other contracts do not solve the same problem. For quote comparisons state whether fees and units are comparable; do not claim a working router or execution service.

## Boundaries

Do not run tests locally; CI owns test execution. No bets, transfers, payments, accounts, wallets or venue connections are needed for contract onboarding. Do not invent complement-price conversions, venue mappings, enum values or cross-project compatibility. Skills provide guidance, not permission to execute or change the standard.
