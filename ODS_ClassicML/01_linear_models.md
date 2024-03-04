# Тема 1. Линейные модели: 1. Линейная регрессия
В первой теме поговорим о нескольких моментах:

* Нужна ли еще линейная регрессия?
* Эконометрика и машинное обучение
* Предпосылки - зачем они, есть ли важные?
* Проблемы с Х, регуляризация
* Коэффициенты: интерпретация, значимость

<br>

* [Видео](https://www.youtube.com/watch?v=n7mdqY-dDKI)
* [Презентация](https://storage.yandexcloud.net/ds-ods/files/content/2023/09/15/e5cae218/1_linear_models_0923.pptx)
* [Ноутбук](https://disk.yandex.ru/d/Ctlf86FsDVQhpg)

**Перессказ от YandexGPT**

Линейные модели 2023 | Линейная регрессия

00:00 Введение в линейную регрессию

* Иван Комаров, ведущий курса по линейным моделям, объясняет, что линейная регрессия используется в науке, экономике и финансах.
* Он приводит примеры использования линейной регрессии в определении лучшего сотрудника и выборе квартиры.

10:41 Два подхода к линейной регрессии

* Параметрический подход: проверка гипотезы и теории.
* Непараметрический подход: машинное обучение и агрессия(?).
* Оба подхода используются для решения задач, связанных с данными.

13:36 Линейная регрессия и машинное обучение

* Линейная регрессия может использоваться для определения эффекта изменения цены на количество покупок.
* Машинное обучение может использоваться для определения вероятности передачи пропуска сотрудником другому сотруднику.
* Оба подхода используют функцию потерь и ошибку для определения коэффициентов и свободного члена.

16:31 Линейная регрессия

* Линейная регрессия - это метод машинного обучения, который используется для предсказания значений на основе имеющихся данных.
* Линейная регрессия предполагает, что между переменными существует линейная связь.
* В процессе обучения модели, мы минимизируем ошибку между предсказанными и истинными значениями.

20:23 Предположения и ошибки

* Важно убедиться, что данные, которые мы используем, соответствуют нашим предположениям.
* Линейная регрессия предполагает линейную связь между переменными, но в реальности это не всегда так.
* Необходимо убедиться, что выборка репрезентативна и отражает всю генеральную совокупность.

31:10 Коэффициенты и ошибки

* Коэффициенты показывают влияние факторов на зависимую переменную.
* Важно проверить, насколько значимы коэффициенты и соответствуют ли они нашим предположениям.
* Если коэффициенты не значимы, это может указывать на проблемы с данными или моделью.

35:03 Обсуждение регрессии и ее свойств

* В видео обсуждаются проблемы мультиеоллинеарности и как их обойти в регрессии.
* Также обсуждаются переменные-факторы и их влияние на коэффициенты.

47:46 Использование регуляризации для борьбы с коллинеальностью

* Регуляризация используется для упрощения модели и борьбы с коллинеальностью.
* Она может быть основана на сумме квадратов или сумме модулей коэффициентов.

50:40 Влияние регуляризации на коэффициенты и прогноз

* Регуляризация может уменьшить коэффициенты, что улучшает прогноз.
* Функция потерь обычно хорошо определена и решение находится практически всегда.

52:36 Коллинеарность и регуляризация

* Коллинеарность возникает, когда несколько признаков имеют сильную корреляцию, что может привести к проблемам с интерпретацией коэффициентов.
* Регуляризация решает эту проблему, минимизируя сумму коэффициентов по модулю или в квадрате.
* Нормирование данных перед регуляризацией позволяет избежать проблем с коллинеарностью.

58:18 Замены отсутствующих наблюдений

* Если некоторые наблюдения отсутствуют, можно заменить их средними значениями других наблюдений.
* Это может привести к переобучению модели, поэтому важно выбрать репрезентативную выборку.

01:01:14 Интерпретация коэффициентов

* Без регуляризации коэффициенты означают, что изменение X на 1% приведет к изменению Y на коэффициент процентов.
* С регуляризацией коэффициенты теряют свое значение, но можно определить, какой признак важнее.

01:03:10 Минимальное количество наблюдений

* Рекомендуется минимум 30 наблюдений для получения точных результатов.
* Если Y ограничен, можно использовать специальные виды регрессии, такие как Тоби регрессия.
