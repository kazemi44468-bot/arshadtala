# ArshadTala Architecture

## 1. Shared UI runtime
All public pages use one shared runtime for Header, Navigation, Market Ticker, Footer and Back-to-Top. Do not duplicate these sections in page HTML. Shared assets live under `components/`, global styles under `css/`, and page-specific markup remains inside its domain folder.

## 2. Design system
- Persian RTL first
- Central design tokens in `css/tokens.css`
- Shared primitives in `css/base.css`, `css/shared.css` and `css/components.css`
- Domain-specific visual systems in dedicated CSS files such as `css/terminal.css`
- Component reuse before page-specific styling
- Responsive behavior is part of the base contract, not a later patch

## 3. Data integrity contract
- No fabricated market prices, percentages, members, licenses, certificates or transactions
- Empty states are explicit and distinguish `no data`, `not authenticated` and `service not connected`
- Market UI accepts data only from an authoritative connected source
- Member-market records must originate from real authenticated accounts
- Trust information must originate from real verification/credential records

## 4. Product surfaces
- `index.html`: public product entry point
- `pages/market/`: Market Terminal and market discovery
- `pages/gold/`, `pages/currency/`, `pages/gemstones/`: domain markets
- `pages/members/`: private member market
- `pages/trust/`: trust profile and public trust lookup
- `pages/verification/`: verification service surface
- `pages/licenses/`: license and credential registry
- `dashboard/`: authenticated member workspace

## 5. Future backend boundaries
Authentication, identity verification, market data ingestion, offers, trade requests, matching, settlement, documents, notifications, audit logs and administration are separate service boundaries. The static frontend must not invent persistence or pretend a backend operation succeeded.

## 6. Market data boundary
The Market Terminal is intentionally data-source agnostic at this stage. The next implementation should define a stable market-data contract before wiring a provider: asset identifier, market, timestamp, last price, bid, ask, change, unit, source and source-status metadata. Provider-specific logic should remain outside page markup.

## 7. Trust boundary
Trust Profile is the presentation layer for identity and credential evidence. Verification status, license validity, credential metadata and trust events must be returned by authoritative services; the frontend only renders the returned state.

## 8. License registry
The licenses page is a registry surface. Real license images, identifiers, issuing authority, validity dates and verification links will be added only from owner-provided authoritative records.
