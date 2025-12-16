#!/usr/bin/env python3
"""Test script for the etf_profile module."""

from justetf_scraping import get_etf_overview, get_gettex_quote

# Test get_etf_overview
isin = 'IE00B3RBWM25'
print(f"Fetching ETF overview for {isin}...")
overview = get_etf_overview(isin)

print('\n' + '='*60)
print('=== ETF OVERVIEW ===')
print('='*60)
print(f'Name: {overview["name"]}')
print(f'ISIN: {overview["isin"]}')
print(f'TER: {overview["ter"]}%')
print(f'Fund Size: EUR {overview["fund_size_eur"]}m')
print(f'Description: {overview["description"][:100]}...')

print(f'\n=== COUNTRIES ({len(overview["countries"])}) ===')
for c in overview['countries']:
    print(f'  {c["name"]}: {c["percentage"]}%')

print(f'\n=== SECTORS ({len(overview["sectors"])}) ===')
for s in overview['sectors']:
    print(f'  {s["name"]}: {s["percentage"]}%')

print(f'\n=== TOP HOLDINGS ({len(overview["top_holdings"])}) ===')
for h in overview['top_holdings'][:5]:
    print(f'  {h["name"]} ({h["isin"]}): {h["percentage"]}%')

print(f'\n=== GETTEX QUOTE ===')
g = overview['gettex']
if g:
    print(f'  Bid: {g["bid"]} {g["currency"]}')
    print(f'  Ask: {g["ask"]} {g["currency"]}')
    print(f'  Day Change: {g["day_change_percent"]}%')
    print(f'  Timestamp: {g["timestamp"]}')
