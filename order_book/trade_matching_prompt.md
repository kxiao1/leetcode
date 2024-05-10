_Excerpted from real HackerRank challenge, see `trade_matching_engine.py` for exact implementation and `trade_matching_engine.cpp` for approximate C++ alternative_

# Background

You've been tasked with writing a matching engine from scratch that will run the order book for this one stock.

- The "order book" is composed of any unfulfilled limit orders, and dictates the market price at any given moment.

- Market orders:
  - Are executed against any matching orders in the order book, regardless of price
  - Are executed starting with the best price available (lower prices first for buys, higher prices first
    for sells)
  - Can be filled via multiple orders on the order book
  - Can be partially filled, but any portion that isn't filled should be canceled
- Limit orders:
  - Are only executed against matching orders that are equal or better than their target price
    - For example, a limit order to buy at $5.00 will execute against a sell order at $4.50 (trading at $4.50), but not a sell order at $5.50
  - Are executed starting with the best price available (lower prices first for buys, higher prices first for sells)
  - Can be filled via multiple orders on the order book
  - Can be partially filled, but remain on the order book until they are completely filled
- In the event of multiple orders on the order book with the same price, priority goes to orders that were placed earlier

# Input Format

- A line with a single integer (1 <= N <= 20000) representing the number of orders (additional lines you will receive)
- Chronologically sorted (earlier orders first) list of orders with one line representing each order (see below for examples)
- Elements of a line are as follows and will each be separated by a single space:
  - TIME: HH:MM:SS (between 09:30:00 and 16:00:00)
  - CLIENT_ID: non-negative integer representing the ID of the entity placing the order
  - DIRECTION: single character representing buy or sell
    - b: buy order
    - s: sell order
  - SIZE: positive integer representing number of shares, e.g. 100
  - TYPE: single character representing the trade type
    - m: market order
    - l: limit order
  - PRICE: non-negative float value (specified to two decimal places) representing target price for limit orders, -1.00 will be provided for market orders

# Output Format

- A list of trades done in a given day (one per line), in the order the trades occurred. Note that it is possible for a single order to trigger multiple trades at the same time, as a large order may be partially or completely filled by multiple smaller orders. For trades occurring at the same time:
  - Print out the trades in order from best to worst price (i.e. the order of preference to be executed).
  - If multiple trades occur at the same time and the same price, sort by the lesser of the two order times involved in each trade.
    - For example if there is a buy order by client 1 at 9:31:00 for $5.00, another buy order by client 2 at 9:32:00 for $5.00, and then a sell order from client 3 that causes both buy orders to be filled at 9:35:00, the trade with client 1 should be printed before the trade with client 2.
- Elements of the output lines are as follows and should be separated by a single space
  - TIME: HH:MM:SS, time that the trade occurred
  - BUY_CLIENT_ID: integer, client id of the buyer
  - SELL_CLIENT_ID: integer, client id of the seller
  - PRICE: float, price the trade is executed at (specified to two decimal places)
  - SIZE: integer, number of shares traded
