from fpdf import FPDF
import os
from datetime import datetime

class PriceTagGenerator:
    PAGE_WIDTH = 210  # mm (A4 width)
    PAGE_HEIGHT = 297  # mm (A4 height)
    TAG_WIDTH = 66  # Adjusted width to fit properly
    TAG_HEIGHT = 36  # Adjusted height to fit properly
    MARGIN_X = 0.5  # Minimal horizontal margin
    MARGIN_Y = 0.5  # Minimal vertical margin
    COLUMNS = 3  # Number of columns per row
    ROWS = (PAGE_HEIGHT - 2 * MARGIN_Y) // (TAG_HEIGHT + MARGIN_Y)  # Adjusted row fitting
    TAG_BG_COLOR = (255, 255, 204)  # Light Yellow Background

    def __init__(self, tags_data):
        self.tags_data = tags_data
        self.pdf = FPDF("P", "mm", "A4")
        self.bg_image=r"assets\background\price_tag_backgroud.png"
    def add_price_tag(self, x, y, product_name, mrp, price, discount):
        """Draws a price tag at the given coordinates with better text wrapping and alignment."""
        # Background color
        # self.pdf.set_fill_color(*self.TAG_BG_COLOR)
        self.pdf.image(self.bg_image,x,y,self.TAG_WIDTH,self.TAG_HEIGHT)
        self.pdf.rect(x,y,self.TAG_WIDTH,self.TAG_HEIGHT)
        self.pdf.rect(x, y, self.TAG_WIDTH, self.TAG_HEIGHT, )#'F')  # Fill background

        # Border
        self.pdf.set_draw_color(0, 0, 0)
        self.pdf.rect(x, y, self.TAG_WIDTH, self.TAG_HEIGHT)

        # Product Name (Multi-line Fix)
        self.pdf.set_font("Arial", "B", 9)
        self.pdf.set_text_color(0, 0, 139)  # Dark Blue
        max_width = self.TAG_WIDTH - 10
        self.pdf.set_xy(x + 5, y + 5)  # Positioning slightly above
        self.pdf.multi_cell(max_width, 4, product_name, align="L")  # Wrap text properly

        # Adjust MRP Position Based on Text Height
        text_height = self.pdf.get_y()  # Get Y position after product name
        self.pdf.set_font("Arial", "B", 18)
        self.pdf.set_text_color(139, 0, 0)  # Dark Red
        mrp_text = f"MRP: Rs.{mrp}"
        text_width = self.pdf.get_string_width(mrp_text)
        self.pdf.text(x + 5, text_height + 3+4, mrp_text)  # Adjust position
        self.pdf.set_draw_color(255, 0, 0)  # Red line for strikethrough
        self.pdf.line(x + 5, text_height + 2+4, x + 5 + text_width, text_height + 2)  # Strikethrough line

        # Selling Price
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.set_text_color(0, 100, 0)  # Dark Green
        self.pdf.text(x + 5, text_height + 12+2, f"Rs.{price}")  # Adjusted position

        # Extra Discount
        self.pdf.set_font("Arial", "B", 9)
        self.pdf.set_text_color(255, 140, 0)  # Orange
        self.pdf.text(x + 40, text_height + 12+2, f"Extra OFF: {discount}%")
    def generate_pdf(self):
        """Generates the price tag PDF and saves it to the desktop."""
        self.pdf.add_page()
        
        for i, (product_name, mrp, price, discount, _) in enumerate(self.tags_data):
            col = i % self.COLUMNS
            row = (i // self.COLUMNS) % self.ROWS
            x = self.MARGIN_X + col * (self.TAG_WIDTH + self.MARGIN_X)
            y = self.MARGIN_Y + row * (self.TAG_HEIGHT + self.MARGIN_Y)
            
            if row == 0 and col == 0 and i != 0:
                self.pdf.add_page()
            
            self.add_price_tag(x, y, product_name, mrp, price, discount)
        base_filename = 'price_tags.pdf'
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        new_filename = f"{base_filename.split('.')[0]}_{timestamp}.{base_filename.split('.')[-1]}"

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", new_filename )
        self.pdf.output(desktop_path)
        return desktop_path
