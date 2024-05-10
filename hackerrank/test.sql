-- house = [BUYER_ID, HOUSE_ID]
-- price = [HOUSE_ID, PRICE]
-- return BUYER_ID's of buyers with > 1 house and total price > 100000000

-- SELECT FROM JOIN WHERE GROUPBY HAVING ORDERBY LIMIT syntactic order
-- FROM JOIN WHERE GROUPBY HAVING SELECT ORDERBY LIMIT execution order

SELECT H.BUYER_ID
FROM house AS H 
     JOIN price AS P ON H.HOUSE_ID = p.HOUSE_ID
     GROUP BY H.BUYER_ID
     HAVING COUNT(H.HOUSE_ID) > 1 AND SUM(P.price) > 100000000
     