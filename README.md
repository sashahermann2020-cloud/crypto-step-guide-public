# Crypto Step Guide

**An independent information guide that helps beginners buy, store and transfer cryptocurrency legally and with fewer mistakes.**

Website: <https://crypto-step-guide.com> (Russian) · Language guides: [Español](https://crypto-step-guide.com/es/) · [Português](https://crypto-step-guide.com/pt/) · [English](https://crypto-step-guide.com/en/)
Contact: hello@crypto-step-guide.com

## What it is

Crypto Step Guide is a free, static educational website. It explains in plain language what cryptocurrency is, how wallets and networks differ, and how to buy USDT (and USDC where required by local rules) step by step, country by country. Every route points to the **official** website, registry or regulator of the service, with the date it was last reviewed.

## What it is not

- It does not open accounts, take payments, hold or send money or crypto assets, or execute transactions.
- It gives no financial, legal or tax advice, and no investment recommendations.
- It currently has no affiliate links. The services it names are independent companies.

## How routes are described

- Each route has a status: **ready** (described from official sources) or **conditional** (conditions must be checked before paying).
- A registry entry is never presented as a licence. For example, an Argentine CNV PSAV registration, a Brazilian central-bank "under review" status and a Nigerian SEC approval in principle are each described exactly as the regulator describes them.
- No route has been tested with a real transaction, and the site says so. Fees and limits are shown only when an official source states them, with its date.
- What could not be verified is listed next to each route.

## Coverage

| Language | Countries |
|---|---|
| Russian | Kazakhstan, Kyrgyzstan, Uzbekistan, Serbia, Russia, Ukraine, Belarus (18 routes) |
| Spanish | Argentina, Venezuela, Spain |
| Portuguese (Brazil) | Brazil |
| English | India, Nigeria |

Also: a glossary of crypto terms, articles on USDT networks and address freezes, and a route for selling USDT back to local currency.

## How it is built

A dependency-free Python generator (`generate.py`) renders a static site from JSON content models and hosts it on Cloudflare Pages. Validators check routes, SEO metadata, structured data, links and the wizard logic before every release. Pages declare `isAccessibleForFree: true` in JSON-LD and are crawlable.

## Editorial principles

Action → check → reason → consequence. Official sources first; no unverified numbers; clear separation between "described", "checked" and "not checked".

## Build locally

```bash
mkdir -p dist
python3 generate.py
python3 scripts/validate_routes.py && python3 scripts/validate_build.py && python3 scripts/validate_seo.py && python3 scripts/validate_sell_routes.py
```

Python 3 only, no dependencies. Page sources are the `*-page.html` files; data lives in `content/*.json`.

This repository is a public mirror of the site sources. Route data is informational: check every condition on the service's official website before paying.
