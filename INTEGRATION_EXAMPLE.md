# Integration Example - Optional Enhancement

This document shows how to optionally integrate the Bigdabach scraper into the existing Flask application.

## Current Structure

The repository has two independent functionalities:
1. **Flask App** (`app.py`) - Excel to XML converter
2. **Scraper** (`bigdabach_scraper.py`) - Web scraper for promotions

## Optional: Add Scraper Route to Flask App

If you want to trigger the scraper from a web interface, here's how:

### 1. Add Route to app.py

```python
from bigdabach_scraper import run_scraper

@app.route('/scrape-promotions', methods=['POST'])
def scrape_promotions():
    try:
        result = run_scraper()
        if result['status'] == 'completed':
            message = f"✓ Scraping completed! Found {result['items_found']} items, saved {result['items_saved']}, skipped {result['items_skipped']}."
        else:
            message = f"✗ Error: {result.get('error_message', 'Unknown error')}"
        return render_template('index.html', message=message)
    except Exception as e:
        return render_template('index.html', message=f"Error running scraper: {str(e)}")

@app.route('/view-promotions')
def view_promotions():
    import sqlite3
    conn = sqlite3.connect('promotions.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_name, price, date FROM promotions ORDER BY date DESC LIMIT 50")
    promotions = cursor.fetchall()
    conn.close()
    return render_template('promotions.html', promotions=promotions)
```

### 2. Add Button to templates/index.html

```html
<!-- Add after the existing form -->
<hr>
<h2>Scrape Promotions</h2>
<form action="/scrape-promotions" method="post">
    <button type="submit">Run Bigdabach Scraper</button>
</form>
<br>
<a href="/view-promotions">View Promotions Database</a>
```

### 3. Create templates/promotions.html

```html
<!DOCTYPE html>
<html>
<head>
    <title>Promotions Database</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <style>
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: right; }
        th { background-color: #4CAF50; color: white; }
        tr:nth-child(even) { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>Promotions Database - Dabach</h1>
    <a href="/">← Back to Home</a>
    
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Product Name</th>
                <th>Price (₪)</th>
                <th>Date</th>
            </tr>
        </thead>
        <tbody>
            {% for promo in promotions %}
            <tr>
                <td>{{ promo[0] }}</td>
                <td style="text-align: right;">{{ promo[1] }}</td>
                <td>{{ promo[2] }}</td>
                <td>{{ promo[3] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    {% if not promotions %}
    <p>No promotions found. Run the scraper first!</p>
    {% endif %}
</body>
</html>
```

## Standalone Usage (Recommended)

The scraper works perfectly as a standalone script:

```bash
# Run manually
python bigdabach_scraper.py

# Run on schedule (Linux/Mac cron)
# Add to crontab: 0 9 * * * /usr/bin/python /path/to/bigdabach_scraper.py

# Run on schedule (Windows Task Scheduler)
# Create task to run: python C:\path\to\bigdabach_scraper.py
```

## Recommendation

**Keep the scraper standalone** for now. This provides:
- ✅ Separation of concerns
- ✅ Easier testing and debugging
- ✅ Simpler deployment
- ✅ Can be scheduled independently
- ✅ No impact on existing Flask app

**Integrate later** if needed for:
- Unified web interface
- User-triggered scraping
- Real-time results display
- Admin dashboard

---

**Note**: This integration is **optional** and **not required** for the current ticket. The scraper fully meets all requirements as a standalone script.
