from fpdf import FPDF
from datetime import datetime, timedelta
import os 
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
# from  Controller.bill_number_generator import generate_bill_number as bill_gen
# from hindiwsd import hindi_wsd
global bill_nums
bill_nums=1#bill_gen()


class WInvoice(FPDF):
    def __init__(self):
        super().__init__('P','mm','A5')
        self.set_auto_page_break(auto=True,margin=20)
        self.add_page()
        self.add_font('NotoSansDevanagari', '', r'assets\font\NotoSansDevanagari-VariableFont_wdth.ttf',uni=True)
        self.count=1
        self.set_font('helvetica','B',12)
        self.cell(40,10,'Rough Estimate')
        self.cell(50)
        self.cell(40,10,f'Bill Number: {bill_nums}',align='R',ln=True)
    def customer_detail(self,name_field,address,mobile_number):
        current_date=datetime.now()
        years_to_subtract=10
        ten_year_ago=current_date.replace(year=current_date.year-years_to_subtract)
        self.set_font('times','B',12)
        self.output_name=name_field
        self.cell(10,10,'Customer Detail',ln=True)
        self.set_font('times','',10)
        self.cell(50,10,f'Customer Name: {name_field}')
        self.cell(30)
        self.cell(50,10,f'Mobile Number: {mobile_number}',ln=True)
        self.cell(50,10,f'Date: {ten_year_ago.strftime("%d-%m-%Y")}')
        self.cell(30)
        self.cell(50,10,f"No.{1}",ln=True)# for bill number showing
        self.set_font('times','B',12)
        self.cell(10,10,'Goods Details',ln=True)
    def item_description(self):
        self.set_font('times','',10)
        self.ln(2)
        self.cell(15,10,'SR.NO',border=1)
        self.cell(40,10,'Description of Goods',border=1)
        self.cell(15,10,'Qty',border=1)
        self.cell(17,10,'Unit',border=1)
        self.cell(18,10,'Rate',border=1)
        self.cell(25,10,'Amount(Rs)',border=1,ln=True)
    def function(self,text):
        # hindi_converter=EngtoHindi(text)
        return text  
    def item(self, item_name, qty, unit, rate, amount):
        line_height = 4  # Line height for text
        col_widths = [15, 40, 15, 17, 18, 25]  # Widths of columns
        desc_width = col_widths[1]  # Width of Description column
    
    # Step 1: Save the current position
        current_y = self.get_y()
        start_x = self.get_x()
        self.set_text_color(255, 255, 255) 
    # Step 2: Determine the height required for the "Description" column
        self.set_font('NotoSansDevanagari', '', 8)
        self.multi_cell(desc_width, line_height, item_name, border=0)
        row_height = self.get_y() - current_y  # Calculate the height of the row
        self.set_text_color(0, 0, 0) 
    # Step 3: Reset position and draw all cells with the calculated height
        self.set_xy(start_x, current_y)
    
    # Column 1: SR.NO
        self.set_font('times', '', 8)
        self.cell(col_widths[0], row_height, str(self.count), border=1)
        self.count += 1
    
    # Column 2: Description
        self.set_font('NotoSansDevanagari', '', 8)
        self.set_xy(start_x + col_widths[0], current_y)  # Move to Description column
        self.multi_cell(desc_width, line_height, item_name, border=1)
    
    # Reset Y position to match the start of the row
        self.set_xy(start_x + col_widths[0] + desc_width, current_y)
    
    # Column 3: Qty
        self.set_font('times', '', 8)
        self.cell(col_widths[2], row_height, str(qty), border=1)
    # Column 4: Unit
        self.cell(col_widths[3], row_height, str(unit), border=1)
    # Column 5: Rate
        self.cell(col_widths[4], row_height, f"{rate:.4f}", border=1)
    # Column 6: Amount
        self.cell(col_widths[5], row_height, f"{amount:.4f}", border=1, ln=True)
    
    def generate_bill(self,name,grand_total,CD_amt,trans_charge,payable_amt):
        self.ln(2)
        self.count=1

        self.cell(60)   
        self.cell( 40,10,str("Grand Total Amount"), border=1, align='C')
        self.cell( 30,10,str(grand_total), border=1,ln=True, align='C')
        self.cell(60)   
        self.cell( 40,10,str("CD"), border=1, align='C')
        self.cell( 30,10,str(float(CD_amt)/100), border=1,ln=True, align='C')
        self.cell(60)
        self.cell( 40,10,str("Transport Charge"), border=1, align='C')
        self.cell( 30,10,str(trans_charge), border=1,ln=True, align='C')
        self.cell(60)
        self.cell( 40,10,str("Bill Amount"), border=1, align='C')
        self.cell( 30,10,str(f"{((float(payable_amt)+float(trans_charge))/100):.4f}"), border=1,ln=True, align='C')


        self.output(os.path.join("D:\\", "Bill_payment_SAB", "test", f"{name}.pdf"))