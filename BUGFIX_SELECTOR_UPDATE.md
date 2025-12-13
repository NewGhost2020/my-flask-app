# Bug Fix #3 - Correct CSS Selector for Product Name

## Проблема (Issue)

Неправильная структура селекторов для поиска названия товара. Название находится в специфической структуре HTML.

## Правильная HTML структура (Correct HTML Structure)

```html
<div class="product-item">
    <div class="sp-sale-icon fixed-sale sale-icon">מבצע</div>
    <div class="data">
        <div class="name" ellipsis="" title="ליפטון תה שחור יילו לייבל">
            ליפטון תה שחור יילו ליי...
        </div>
        <div class="description highlight">
            <!-- NOT HERE - это описание, не название -->
        </div>
    </div>
    <div class="price">₪XX.XX</div>
</div>
```

**Важно:**
- Название товара находится в: `div.data > div.name`
- НЕ в: `div.description.highlight`

## Решение (Solution)

Обновлена логика поиска элемента с названием товара:

1. **Сначала** ищем контейнер `div.data`
2. **Внутри** `div.data` ищем `div.name`
3. **Fallback** на прямые селекторы если структура отличается

### Код ДО (Before)

```python
# Look for product name - common selectors
if not product_name_elem:
    product_name_elem = (
        safe_select(product_container, '.product-title') or
        safe_select(product_container, '.product-name') or
        safe_select(product_container, 'h2') or
        safe_select(product_container, 'h3') or
        safe_select(product_container, '.name') or
        safe_select(product_container, 'a[href*="product"]')
    )
```

**Проблема:** Общие селекторы могли находить неправильные элементы (например, description вместо name).

### Код ПОСЛЕ (After)

```python
# Look for product name in the correct structure:
# div.data -> div.name (not div.description)
if not product_name_elem:
    # First try to find div.data container
    data_container = safe_select(product_container, 'div.data')
    if data_container:
        # Inside div.data, look for div.name
        product_name_elem = safe_select(data_container, 'div.name')
    
    # If not found, try direct selectors as fallback
    if not product_name_elem:
        product_name_elem = (
            safe_select(product_container, 'div.data div.name') or
            safe_select(product_container, '.name') or
            safe_select(product_container, '.product-title') or
            safe_select(product_container, '.product-name')
        )
```

**Решение:** 
- Специфический путь: `div.data` → `div.name`
- Избегаем случайного нахождения `div.description`
- Сохранены fallback селекторы для других структур

## Приоритет селекторов (Selector Priority)

### Для названия товара (Product Name)
1. `div.data > div.name` - **основной путь**
2. `div.data div.name` - прямой комбинированный селектор
3. `.name` - fallback для других структур
4. `.product-title` - дополнительный fallback
5. `.product-name` - дополнительный fallback

### Преимущества нового подхода

✅ **Точность** - Находим именно div.name внутри div.data  
✅ **Избегаем ошибок** - Не путаем с div.description  
✅ **Обратная совместимость** - Fallback селекторы на случай других структур  
✅ **Логичная структура** - Следуем реальной DOM структуре сайта  

## Тестирование (Testing)

### Синтаксис
```bash
python -m py_compile bigdabach_scraper.py
✓ Синтаксис правильный
```

### Unit тесты
```bash
python test_scraper.py
✓ All 7 tests passed
```

### Проверка импорта
```bash
python -c "from bigdabach_scraper import scrape_bigdabach; print('OK')"
✓ OK
```

## Ожидаемое поведение (Expected Behavior)

При запуске скрапера:

```python
python bigdabach_scraper.py
```

Теперь будет:
1. Найден элемент с классом `sp-sale-icon` (акционный товар)
2. Поиск родительского контейнера
3. Внутри контейнера найден `div.data`
4. Внутри `div.data` найден `div.name` с названием товара
5. Извлечено полное название из атрибута `title`

**Результат:**
```
INFO - Extracted item 1: ליפטון תה שחור יילו לייבל - ₪XX.XX
```

## Связанные исправления (Related Fixes)

Это исправление работает вместе с Bug Fix #2 (приоритет title над text):
- **Bug Fix #2**: Извлекает полное название из атрибута `title`
- **Bug Fix #3 (это)**: Находит правильный элемент `div.name` в `div.data`

Вместе они обеспечивают:
- Правильный элемент (`div.data > div.name`)
- Полное название (атрибут `title`)

## Статус (Status)

✅ **ИСПРАВЛЕНО (FIXED)**

- Дата: 13 декабря 2024
- Файл: `bigdabach_scraper.py` (строки 168-184)
- Тип: Улучшение селекторов
- Приоритет: Высокий (точность извлечения данных)

## Дополнительная информация (Additional Info)

### CSS Селекторы для bigdabach.co.il

```css
/* Акционный товар */
.sp-sale-icon.fixed-sale.sale-icon

/* Контейнер данных */
div.data

/* Название товара (правильно) */
div.data > div.name

/* НЕ ИСПОЛЬЗОВАТЬ */
div.data > div.description.highlight  /* Это описание! */

/* Цена */
.price
```

### Отладка (Debugging)

Если названия всё ещё извлекаются неправильно:

1. Проверьте HTML структуру на сайте
2. Убедитесь что `div.data` существует
3. Убедитесь что `div.name` находится внутри `div.data`
4. Проверьте логи скрапера:
   ```bash
   python bigdabach_scraper.py 2>&1 | grep "Could not find product name"
   ```

---

**Автор:** AI Assistant  
**Проверено:** Unit tests passed ✓  
**Готово к продакшену:** ✅ Yes
