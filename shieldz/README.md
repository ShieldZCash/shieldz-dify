# Shieldz Swap Quotes

**Author:** shieldzcash
**Version:** 0.1.0
**Type:** tool
**Source:** https://github.com/ShieldZCash/shieldz-dify
**Contact:** support@shieldz.cash

Live cross-chain crypto swap quotes for Dify apps and agents. Read-only, no API key, no account.

## Tools

| Tool | What it does |
| --- | --- |
| Get cross-chain swap quote | Best route, expected output, all-in cost and ETA for swapping one asset for another across chains. Compares NEAR Intents, Chainflip, Relay, MAYAChain, BOB Gateway and Garden. |
| List swappable assets | Search the 340+ quotable assets on 40+ chains by symbol or chain, with exact ids and USD prices. |

Assets use `CHAIN.SYMBOL`, for example `BTC.BTC`, `ETH.ETH`, `SOL.SOL`, `ZEC.ZEC`, `BASE.USDC`, `TRON.USDT`.

## Setup and connection

Install the plugin. There is nothing to configure: no credentials, no API key. The tools call the public quote API at https://swap.shieldz.cash over HTTPS.

## Example

"How much ZEC do I get for 0.01 BTC?" calls Get cross-chain swap quote with `BTC.BTC`, `ZEC.ZEC`, `0.01` and returns the best route (for example MAYAChain), the expected ZEC and the all-in cost.

## Notes

- Quotes are informational and change with the market. They include the flat 0.15% Shieldz Swap fee.
- The plugin never moves funds, signs anything or asks for keys.

## Links

- Shieldz Swap: https://swap.shieldz.cash
- Fee data and method: https://swap.shieldz.cash/fees
- Privacy: [PRIVACY.md](PRIVACY.md)
