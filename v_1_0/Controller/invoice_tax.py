from fpdf import FPDF
from time import gmtime,strftime
import os 
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
# from  Controller.bill_number_generator import generate_bill_number as bill_gen

global bill_nums
bill_nums=1#bill_gen()
class PDF(FPDF):
    def header(self):
        # Font
        self.set_font('helvetica','B',7)
        self.cell(40,10,'GSTIN: 09AUZPS3017HZV')
        self.cell(50)
        self.cell(70,10,'TAX INVOICE')
        self.image("assets\logo\whatsapp.png",x=165,y=14,w=3,h=3,type='png')
        self.cell(80,10,'9415863731, 9794144305')
        self.set_font('times','B',7)
        # logo
        self.ln(5)
        # filename ="Model\assests\logo\Raj Distributor.jpg"
        # with open(filename,'r') as file:
        self.image("assets\logo\Raj_distributos.png",x=45,y=15,w=20,h=20,type='png')
        
        #title
        self.set_font('times','I',28)
        self.cell(50)
        self.cell(100,20,'RAJ DISTRIBUTORS',align='C',ln=True)
        self.set_font('times','B',10)
        self.cell(180,5,'Behind Pakka Kuwa in North Side Behind Gramin Bank',align='C',ln=True)
        self.cell(180,5,'Front of Main Road Saidpur, Ghazipur-233304',align='C',ln=True)
        # self.ln(14)
        self.set_font('times','',10)
        samay=strftime("%d-%m-%Y ",gmtime())
        self.cell(40,10,f"Invoice Date:{samay}")
        # bill_number=generator_bill_number()
        # bill_number=1
        self.cell(150,10,f'Bill Number: {bill_nums}',align='R',ln=True)
    def footer(self):
        self.set_y(-40)
        self.set_font('times','U',6)
        self.cell(20,5,'Terms & Condition',ln=True)
        self.set_font('times','B',8)
        self.cell(20,5,'E.&O.E.',ln=True)
        self.cell(20,5,'1.Goods once Sold Will not be taken back',ln=True)
        self.cell(20,5,'2.Interest @18% p.a. will be charged if the payment is not made with in the stipulated only',ln=True)
        self.cell(20,5,'3.Subject to Ghzipur Jurisdiction only',ln=True)
        self.cell(20,5,'4.No Exchange No Refund.',ln=True)
        self.cell(60,6,'Receiver\'s Signature : ....................................',border=1)
        
        self.image('assets\logo\Payment.jpg',x=160,y=240,w=30,h=30,type='jpg')
        self.cell(94)
        self.cell(20,10,'Scan & Pay (*_*)')

class Invoice(PDF):
    def __init__(self):
        super().__init__('P','mm','Letter')
        self.set_auto_page_break(auto=True,margin=40)
        self.add_page()
        self.count=1
    def customer_detail(self,name_field,address,mobile_number,gst,aadhar):
        self.set_font('times','B',14)
        self.output_name=name_field
        self.cell(10,10,'Customer Detail',ln=True)
        self.set_font('times','',12)
        self.cell(70,10,f'Customer Name: {name_field}')
        self.cell(70,10,f'Address: {address}')
        self.cell(70,10,f'Mobile Number: {mobile_number}',ln=True)
        self.cell(70,10,f'Gst No: {name_field}')
        self.cell(70,10,f'Aadhar Number: {address}',ln=True)
        self.set_font('times','B',14)
        self.cell(10,10,'Goods Details',ln=True)
    def item_description(self):
        self.set_font('times','',12)
        self.ln(2)
        self.cell(15,10,'SR.NO',border=1)
        self.cell(50,10,'Description of Goods',border=1)
        self.cell(20,10,'Qty',border=1)
        self.cell(20,10,'Unit',border=1)
        self.cell(30,10,'Rate',border=1)
        self.cell(30,10,'IGST',border=1)
        self.cell(29,10,'Amount(Rs)',border=1,ln=True)
    def item(self,item_name,qty,unit,rate,gst,amount):  
        self.set_font('times','',12)
        self.cell(15,10,f'{self.count}',border=1)
        self.count+=1
        self.cell(50,10,f'{item_name}',border=1)
        self.cell(20,10,f'{qty}',border=1)
        self.cell(20,10,f'{unit}',border=1)
        self.cell(30,10,f'{rate}',border=1)
        self.cell(30,10,f'{gst}',border=1)
        self.cell(29,10,f'{amount}',border=1,ln=True)           
    def generate_bill(self,pdf_path,grand_total,discound,payable_amount):
        self.ln(4)  
        self.count=1
        self.cell(125)   
        self.cell( 40,10,str("Grand Total Amount"), border=1, align='C')
        self.cell( 30,10,str(grand_total), border=1,ln=True, align='C')
        self.cell(125)   
        self.cell( 40,10,str("Discount"), border=1, align='C')
        self.cell( 30,10,str(discound), border=1,ln=True, align='C')
        self.cell(125)   
        self.cell( 40,10,str("Payable Amount Rs."), border=1, align='C')
        self.cell( 30,10,str(payable_amount), border=1,ln=True, align='C')
        self.output(os.path.join("D:\\", "Bill_payment_SAB", "test", f"{self.output_name}.pdf"))
