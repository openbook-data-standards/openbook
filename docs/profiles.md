# Profile specifications (Q172)

Regulator reporting, a prediction-market bridge, integrity alerts, and
the register live in **their own repositories**. Each pins a core major
and a vocabulary release. None redefine a core field. Core stays the
public odds wire.

This page is a pointer. It is not those specifications.

| Planned repository | Audience | Status |
| --- | --- | --- |
| openbook-register | Prefix allocation, join key, anchors | Recipe today: [`../register/`](../register/) in this repo. Separate repo waits. |
| openbook-pm | Event-contract ↔ market / selection | Not created. |
| openbook-reg | Bet-level reporting that carries OpenBook ids | Not created. |
| openbook-integrity | CAP-shaped alert envelope | Not created. |

Q96 stands: vendor mapping / starter / translate packages are not this
spec. Planned names openbook-starter and openbook-translate are also
not created here.

Do not put those shapes in [`../spec/openbook.md`](../spec/openbook.md)
or as `x_` extensions.
