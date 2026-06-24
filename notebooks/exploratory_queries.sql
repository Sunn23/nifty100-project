SELECT COUNT(*) FROM companies;

SELECT COUNT(*) FROM profitandloss;

SELECT COUNT(*) FROM balancesheet;

SELECT COUNT(*) FROM cashflow;

SELECT company_id, COUNT(*)
FROM profitandloss
GROUP BY company_id
ORDER BY COUNT(*) DESC;

SELECT company_id, AVG(return_on_equity_pct)
FROM financial_ratios
GROUP BY company_id;

SELECT company_id, SUM(net_profit)
FROM profitandloss
GROUP BY company_id
ORDER BY SUM(net_profit) DESC;

SELECT company_id, MAX(market_cap_crore)
FROM market_cap
GROUP BY company_id
ORDER BY MAX(market_cap_crore) DESC;

SELECT company_id, MIN(year), MAX(year)
FROM profitandloss
GROUP BY company_id;

SELECT COUNT(*)
FROM stock_prices;
