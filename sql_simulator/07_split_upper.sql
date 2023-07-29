-- Примените последовательно функции UPPER и SPLIT_PART к колонке name и преобразуйте наименования товаров в таблице products так,
-- чтобы от названий осталось только первое слово, записанное в верхнем регистре.
-- Колонку с новым названием, состоящим из первого слова, назовите first_word.
-- В результат включите исходные наименования товаров, новые наименования из первого слова, а также цену товаров.
-- Результат отсортируйте по возрастанию исходного наименования товара в колонке name.
-- Поля в результирующей таблице: name, first_word, price
-- SELECT * FROM products LIMIT 10
SELECT
  name,
  UPPER(SPLIT_PART(name, ' ', 1)) AS first_word,
  price
FROM
  products
ORDER BY(name)