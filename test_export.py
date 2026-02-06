from exporter import save_to_excel
import os

def test_export():
    mock_data = [
        {
            "id": 123456,
            "name": "Тестовый товар с очень длинным названием для проверки ширины колонки",
            "brand": "TestBrand",
            "price": 1234.56,
            "rating": 4.8,
            "url": "https://www.wildberries.ru/catalog/123456/detail.aspx"
        },
        {
            "id": 654321,
            "name": "Короткое имя",
            "brand": "Brand2",
            "price": 500.0,
            "rating": 3.5,
            "url": "https://www.wildberries.ru/catalog/654321/detail.aspx"
        }
    ]
    
    print("Generating mock Excel file...")
    filename = save_to_excel(mock_data, "mock_test")
    print(f"File created: {filename}")
    
    # Verify file exists
    path = os.path.join("exports", filename)
    if os.path.exists(path):
        print("✅ File exists")
    else:
        print("❌ File was not created")

if __name__ == "__main__":
    test_export()
