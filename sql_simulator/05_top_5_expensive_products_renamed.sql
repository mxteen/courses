-- Используя операторы SELECT, FROM, ORDER BY и LIMIT, определите 5 самых дорогих товаров в таблице products, которые доставляет наш сервис.
-- Выведите их наименования и цену.
-- Поля в результирующей таблице: name, price

-- Повторите запрос из предыдущего задания, но теперь колонки name и price переименуйте соответственно в product_name и product_price.
-- Поля в результирующей таблице: product_name, product_price

SELECT
  name AS product_name,
  price AS product_price
FROM
  products
ORDER BY
  price DESC
LIMIT 5