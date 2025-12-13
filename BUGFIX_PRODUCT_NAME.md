# Bug Fix: Product Name Extraction

## Проблема (Issue)

Название товара определялось неправильно. Текст в элементе обрезается многоточием, а полное название находится в атрибуте `title`.

**Пример HTML:**
```html
<div class="name" ellipsis="" title="ליפטון תה שחור יילו לייבל">
    ליפטון תה שחור יילו ליי...
</div>
```

**Неправильный результат:** "ליפטון תה שחור יילו ליי..." (обрезанное название)  
**Правильный результат:** "ליפטון תה שחור יילו לייבל" (полное название из title)

---

## Решение (Solution)

Изменён приоритет извлечения названия товара:
1. **Сначала**: проверяется атрибут `title` (полное название)
2. **Потом**: если title отсутствует или пустой, используется текст элемента
3. **Fallback**: если ничего нет, используется "Unknown Product"

### Код ДО (Before)

```python
# Extract product name
product_name = product_name_elem.text.strip()
if not product_name:
    product_name = product_name_elem.get_attribute('title') or 'Unknown Product'
```

**Проблема:** Сначала берётся текст (который обрезан), и только если текста нет, проверяется title.

### Код ПОСЛЕ (After)

```python
# Extract product name
# First try title attribute (full name), then text (may be truncated)
product_name = product_name_elem.get_attribute('title')
if not product_name or product_name.strip() == '':
    product_name = product_name_elem.text.strip()
if not product_name:
    product_name = 'Unknown Product'
else:
    product_name = product_name.strip()
```

**Решение:** Сначала проверяется title (полное название), затем text, затем fallback.

---

## Тестирование (Testing)

### Тест 1: Title с полным именем, text обрезанный
```python
elem = MockElement(
    title="ליפטון תה שחור יילו לייבל",
    text="ליפטון תה שחור יילו ליי..."
)
result = extract_product_name(elem)
# Результат: "ליפטון תה שחור יילו לייבל" ✓
```

### Тест 2: Только text, без title
```python
elem = MockElement(title=None, text="Product Name")
result = extract_product_name(elem)
# Результат: "Product Name" ✓
```

### Тест 3: Оба доступны, приоритет у title
```python
elem = MockElement(title="Full Product Name", text="Short Name")
result = extract_product_name(elem)
# Результат: "Full Product Name" ✓
```

### Запуск тестов:
```bash
python test_product_name_extraction.py
```

**Результат:**
```
✓ All product name extraction tests passed!

Key behavior:
  1. Title attribute is checked FIRST (full product name)
  2. If title is empty/None, falls back to text content
  3. Handles Hebrew text correctly
  4. Strips extra whitespace
```

---

## Влияние на функциональность (Impact)

### ✅ Улучшения (Improvements)
- **Полные названия товаров**: Теперь извлекаются полные названия из атрибута title
- **Правильная работа с Hebrew**: Корректная обработка ивритских символов
- **Обратная совместимость**: Если title отсутствует, используется текст (старая логика работает)

### ✅ Без breaking changes
- Все существующие тесты проходят
- База данных не требует изменений
- API остаётся таким же

---

## Проверка в реальной работе (Production Check)

При запуске скрапера теперь будет:

```python
python bigdabach_scraper.py
```

**Ожидаемый вывод:**
```
INFO - Extracted item 1: ליפטון תה שחור יילו לייבל - ₪XX.XX
```

А не:
```
INFO - Extracted item 1: ליפטון תה שחור יילו ליי... - ₪XX.XX
```

---

## Статус (Status)

✅ **ИСПРАВЛЕНО (FIXED)**

- Дата: 13 декабря 2024
- Файл: `bigdabach_scraper.py` (строки 202-210)
- Тест: `test_product_name_extraction.py`
- Приоритет: Высокий (влияет на качество данных)

---

## Дополнительная информация (Additional Info)

### Структура HTML на bigdabach.co.il
```html
<div class="product-item">
    <div class="sp-sale-icon fixed-sale sale-icon">מבצע</div>
    <div class="name" ellipsis="" title="[ПОЛНОЕ НАЗВАНИЕ]">
        [ОБРЕЗАННОЕ НАЗВАНИЕ]...
    </div>
    <div class="price">₪XX.XX</div>
</div>
```

### Селектор для названия
Скрапер ищет элемент с классом `.name` и теперь правильно извлекает данные из атрибута `title`.

---

**Автор:** AI Assistant  
**Проверено:** Unit tests passed ✓  
**Готово к продакшену:** ✅ Yes
