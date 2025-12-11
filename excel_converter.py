from datetime import datetime
import pandas as pd
import xml.etree.ElementTree as ET
import os
from typing import Dict, Optional


def convert_excel_to_yml_xml(
    filepath: str,
    output_path: str = None,
    shop_name: str = "Магазин",
    company_name: str = "Star Store"
) -> Dict:
    """
    Converts an Excel file with product list to YML-compatible XML format.
    
    Args:
        filepath: Path to the Excel file
        output_path: Path for output XML file (optional)
        shop_name: Shop name for XML
        company_name: Company name for XML
        
    Returns:
        Dict with status and output file path
    """
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
    
    df = pd.read_excel(filepath, sheet_name="Список товаров", header=1, skiprows=[2])
    
    yml = ET.Element("yml_catalog", date=datetime.now().strftime("%Y-%m-%d %H:%M"))
    shop = ET.SubElement(yml, "shop")
    ET.SubElement(shop, "name").text = shop_name
    ET.SubElement(shop, "company").text = company_name
    
    currencies = ET.SubElement(shop, "currencies")
    ET.SubElement(currencies, "currency", id="RUR", rate="1")
    
    categories = ET.SubElement(shop, "categories")
    ET.SubElement(categories, "category", id="1").text = "электроника / телефоны / мобильные телефоны"
    ET.SubElement(categories, "category", id="2").text = "компьютерная техника / комплектующие / видеокарты"
    ET.SubElement(categories, "category", id="3").text = "электроника / игровые приставки и аксессуары / игровые приставки"
    ET.SubElement(categories, "category", id="4").text = "электроника / телефоны / умные часы и браслеты"
    
    offers = ET.SubElement(shop, "offers")
    
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
    
    if output_path is None:
        output_folder = "xml_output"
        os.makedirs(output_folder, exist_ok=True)
        filename = os.path.splitext(os.path.basename(filepath))[0]
        output_path = os.path.join(output_folder, f"{filename}_output.xml")
    
    tree = ET.ElementTree(yml)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    
    return {
        "success": True,
        "output_path": output_path,
        "products_count": len(df)
    }


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python excel_converter.py <input_excel_file> [output_xml_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        result = convert_excel_to_yml_xml(input_file, output_file)
        print(f"✅ Success! Converted {result['products_count']} products")
        print(f"Output: {result['output_path']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
