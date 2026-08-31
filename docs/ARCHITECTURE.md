# ArshadTala Architecture

## Shared UI
All public pages use one shared runtime for Header, Navigation, Market Ticker, Footer and Back-to-Top. Do not duplicate these sections in page HTML.

## Design principles
- Persian RTL first
- Central design tokens
- Component reuse before page-specific styling
- No fabricated market data, licenses, certificates or transaction records
- Public market UI is informational until a compliant data/trading backend is connected
- Member-only features are permission-gated

## Domain modules
Market / Gold / Coins / Currency / Gemstones / Members / Referral / Verification / Education / Analysis / Licenses / Trading

## Future backend boundaries
Authentication, identity verification, market data, offers, trade requests, matching, settlement, documents, notifications, audit logs and administration are separate service boundaries.

## License registry
The licenses page is a placeholder registry. Real license images, identifiers and verification links will be added only from owner-provided authoritative records.
