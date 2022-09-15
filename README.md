# SVI-Crypto

In this notebook, we look at constructing a BTC volatility surface using the SVI method. We determine our parameters by performing a least mean squared optimistation using market data from deribit. A penalty factor is included for both calender and butterfly arbitrage to ensure our volatility surface is arbitrage free.
