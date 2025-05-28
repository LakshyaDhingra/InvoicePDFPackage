import os
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, product_id, product_name,
             amount_purchased, price_per_unit, total_price):
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        # Creation of PDF
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        # Extracting invoice number and date from filename
        filename = Path(filepath).stem
        invoice_number = filename.split("-")[0]
        date = filename.split("-")[1]
        # Setting font of the title invoice
        pdf.set_font(family="Helvetica", size=34, style="B")
        pdf.cell(w=0, h=16, txt="Invoice", align="R")
        # Setting font of the invoice number
        pdf.set_font(family="Helvetica", size=16)
        pdf.cell(w=0, h=32, txt=f"#{invoice_number}", align="R")
        # Setting font of the date
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=0, h=56, txt=f"Date: {date}", align="R", ln=1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Creation of headers
        columns = list(df.columns)
        columns = [item.replace("_", " ").title() for item in columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(r=80, g=80, b=80)
        pdf.cell(w=30, h=8, txt=(columns[0]), border=1)
        pdf.cell(w=50, h=8, txt=(columns[1]), border=1)
        pdf.cell(w=40, h=8, txt=(columns[2]), border=1)
        pdf.cell(w=30, h=8, txt=(columns[3]), border=1)
        pdf.cell(w=30, h=8, txt=(columns[4]), border=1, ln=1)

        # Creation of rows
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(r=80, g=80, b=80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=50, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=40, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        # Total price calculation and display
        total_sum = df["total_price"].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(r=80, g=80, b=80)
        pdf.cell(w=30, h=10, txt=f"The total amount is {total_sum} Rupees")

        # Generation of PDF
        os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")

