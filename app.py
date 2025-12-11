from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import xml.etree.ElementTree as ET
import os

from database import init_db
from parser import run_parser

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'xml_output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return render_template('index.html', message="Файл не загружен.")

    filepath = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(filepath)

    try:
        # ----------------------------------------
        # df = pd.read_excel(filepath)
        #
        # # Трансформация: оставляем только нужные столбцы
        # field_map = {
        #     'имя': 'name',
        #     'цена': 'Price',
        #     'количество': 'cont'
        # }
        #
        # df = df[[*field_map.keys()]]
        # xml_rows = []
        #
        # for _, row in df.iterrows():
        #     row_xml = "  <row>\n"
        #     for orig, tag in field_map.items():
        #         val = str(row[orig]).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        #         row_xml += f"    <{tag}>{val}</{tag}>\n"
        #     row_xml += "  </row>"
        #     xml_rows.append(row_xml)
        #
        # xml_content = "<root>\n" + "\n".join(xml_rows) + "\n</root>"
        #
        # output_filename = os.path.splitext(uploaded_file.filename)[0] + ".xml"
        # output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        #
        # with open(output_path, "w", encoding="utf-8") as f:
        #     f.write(xml_content)
        # ------------------------------------------------------
        column_map = {
            "name": "Название товара *",
            "price": "Цена *",
            "picture": "Ссылка на изображение *",
            "description": "Описание товара *",
            "categoryId": "Категория на Маркете *",
            "vendor": "Бренд *",
            "weight": "Вес с упаковкой, кг",
            "vendorCode": "Артикул производителя",
            "oldprice": "Зачёркнутая цена",
            "barcode": "Штрихкод *",
            "country_of_origin": "Страна производства",
            "dimensions": "Габариты с упаковкой, см"
        }

        # Загрузка Excel с нужного листа и пропущенных строк
        df = pd.read_excel(filepath, sheet_name="Список товаров", header=1, skiprows=[2])
        # print("Колонки в Excel-файле:")
        # for col in df.columns:
        #     print(f"'{col}'")

        # Создание XML-структуры
        yml = ET.Element("yml_catalog", date=datetime.now().strftime("%Y-%m-%d %H:%M"))
        shop = ET.SubElement(yml, "shop")
        ET.SubElement(shop, "name").text = "Магазин"
        ET.SubElement(shop, "company").text = "Star Store"

        # Валюта
        currencies = ET.SubElement(shop, "currencies")
        ET.SubElement(currencies, "currency", id="RUR", rate="1")

        # Категории
        categories = ET.SubElement(shop, "categories")
        ET.SubElement(categories, "category", id="1").text = "электроника / телефоны / мобильные телефоны"
        ET.SubElement(categories, "category", id="2").text = "компьютерная техника / комплектующие / видеокарты"
        ET.SubElement(categories, "category",
                      id="3").text = "электроника / игровые приставки и аксессуары / игровые приставки"
        ET.SubElement(categories, "category", id="4").text = "электроника / телефоны / умные часы и браслеты"

        # Товары
        offers = ET.SubElement(shop, "offers")

        # Генерация офферов
        for idx, row in df.iterrows():
            offer = ET.SubElement(offers, "offer", id=str(idx + 1), available="true")

            for tag, column in column_map.items():
                value = row.get(column)
                catId = ''
                if pd.notna(value):
                    if tag == "picture":
                        for pic in str(value).split(","):
                            ET.SubElement(offer, "picture").text = pic.strip()
                    elif tag == "dimensions":
                        dims = str(value).replace(" ", "").replace("х", "/").replace("x", "/")
                        ET.SubElement(offer, "dimensions").text = dims
                    elif tag == "description":
                        ET.SubElement(offer, "description").text = f"<![CDATA[{str(value)}]]>"
                    elif tag == "categoryId":
                        if str(value) == "электроника / телефоны / мобильные телефоны":
                            catId = "1"
                        if str(value) == "компьютерная техника / комплектующие / видеокарты":
                            catId = "2"
                        if str(value) == "электроника / игровые приставки и аксессуары / игровые приставки":
                            catId = "3"
                        if str(value) == "электроника / телефоны / умные часы и браслеты":
                            catId = "4"
                        ET.SubElement(offer, "categoryId").text = catId
                    else:
                        ET.SubElement(offer, tag).text = str(value)

            ET.SubElement(offer, "currencyId").text = "RUR"

        # Сохраняем как XML
        tree = ET.ElementTree(yml)
        tree.write(r"xml\output\output.xml", encoding="utf-8", xml_declaration=True)
        # ------------------------------------------------------

        return render_template('index.html', message='Файл успешно преобразован в XML')

    except Exception as e:
        return render_template('index.html', message=f"Ошибка: {str(e)}")


@app.route('/run-parser', methods=['POST'])
def run_parser_route():
    try:
        data = request.get_json() or {}
        url = data.get('url')
        use_selenium = data.get('use_selenium', False)
        store_name = data.get('store_name', 'BigDaBach')
        
        stats = run_parser(
            url=url,
            use_selenium=use_selenium,
            store_name=store_name
        )
        
        return jsonify({
            'success': True,
            'stats': {
                'items_parsed': stats['items_parsed'],
                'items_saved': stats['items_saved'],
                'items_updated': stats['items_updated'],
                'errors': stats['errors'],
                'duration': stats['duration']
            },
            'message': f"Successfully parsed {stats['items_parsed']} products"
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': f"Parser failed: {str(e)}"
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
