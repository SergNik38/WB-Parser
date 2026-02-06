import pandas as pd
import os
from datetime import datetime
from typing import List, Dict, Any

def save_to_excel(data: List[Dict[str, Any]], filename_prefix: str = "wb_data") -> str:
    """
    Saves a list of dictionaries to an Excel file.
    Returns the absolute path to the saved file.
    """
    if not data:
        return ""
    
    # Ensure exports directory exists
    export_dir = os.path.join(os.path.dirname(__file__), "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}_{timestamp}.xlsx"
    filepath = os.path.join(export_dir, filename)
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    
    # Rename columns for better readability (optional, but good for end user)
    column_mapping = {
        "id": "Артикул",
        "name": "Название",
        "brand": "Бренд",
        "price": "Цена (руб)",
        "rating": "Рейтинг",
        "url": "Ссылка"
    }
    df = df.rename(columns=column_mapping)
    
    # Reorder columns to make 'Артикул' first
    cols = ["Артикул", "Бренд", "Название", "Цена (руб)", "Рейтинг", "Ссылка"]
    # Filter only columns that exist (in case scraper changes)
    cols = [c for c in cols if c in df.columns]
    df = df[cols]
    
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Товары')
        
        # Access the openpyxl worksheet
        worksheet = writer.sheets['Товары']
        
        # Auto-adjust column widths
        for i, col in enumerate(df.columns):
            # Calculate max length of data in column or header
            max_len = max(
                df[col].astype(str).map(len).max(),
                len(str(col))
            )
            
            # Add a little padding
            worksheet.column_dimensions[chr(65 + i)].width = min(max_len + 2, 50) # Cap at 50 chars
    
    return filename
