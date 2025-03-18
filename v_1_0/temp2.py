import flet as ft
from flet import (Dropdown,TextField,ElevatedButton)
import time  
import win32api
import pygtrie
from rapidfuzz import process
from Model.items import Item 
import asyncio
import random 
import time
class text_filed_style(TextField):
    def __init__(self, label=None, capitalizationn=None, hint_text=None, 
                 prefix_text=None, leng=None, col1=None, on_change=None, 
                 value=None, input_filter=None,on_click=None, suffix=None, prefix_icon=None, 
                 kbtype=None, **kwargs):  # Add **kwargs
        super().__init__(**kwargs)
        self.label = label
        self.keyboard_type = kbtype
        self.input_filter=input_filter
        self.capitalization = capitalizationn
        self.hint_text = hint_text
        self.prefix_text = prefix_text
        self.max_length = leng
        self.value = value
        self.col = col1
        self.on_change = on_change
        self.on_click = on_click
        self.suffix = suffix
        self.prefix_icon = prefix_icon
        
        # Style properties
        # self.width = 200
        self.cursor_color = "#1A1A1D"
        self.focused_color = "#3B1E54"
        self.focused_bgcolor = "#C6E7FF"
        self.border_color = "#1A1A1D"
        self.color = "#1A1A1D"
        self.bgcolor = "#EBEAFF"
        self.border_radius = ft.border_radius.all(10)
        
        # Label style
        self.label_style = ft.TextStyle(
            word_spacing=5,
            color="#6A1E55",
            size=16,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.BLUE_GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.SOLID,
            ),
        )
class button_style(ElevatedButton):
    def __init__(self, on_click=None, text=None, bgcolor=None,**kwargs):  # Fix kwargs
        super().__init__(**kwargs)
        self.on_click = on_click
        self.text = text
        
        # Button style
        self.style = ft.ButtonStyle(
            animation_duration=290,
            color={
                ft.ControlState.HOVERED: "#3D3BF3",  # Light blue text on hover
                ft.ControlState.FOCUSED: "#000000",  # Cyan text on focus
            },
            bgcolor={
                "": bgcolor if bgcolor else "#FF2929",  # Default background color
                ft.ControlState.HOVERED: "#000000",  # Black background on hover
            },
            elevation={"pressed": 0, "": 1},
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(1, "#1D24CA"),
                ft.ControlState.HOVERED: ft.BorderSide(1, "#40A2D8"),
            },
            shape={
                ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=5),
                ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=12),
            },
        )


class dropdown(Dropdown):
    def __init__(self,label,  **kwargs):
        super().__init__(**kwargs)
        self.label=label
        self.counter_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,))
        self.border_radius=ft.border_radius.all(10)
        self.border_color="#1A1A1D"
        self.bgcolor="#EBEAFF"
        self.color="#1A1A1D"
        self.focused_bgcolor="#C6E7FF"
        self.focused_color="#3B1E54"
        # self.icon_enabled_color="red"
        self.label_style=ft.TextStyle( word_spacing=5,color="#6A1E55",size=18,shadow=ft.BoxShadow(
                                                spread_radius=1,
                                                blur_radius=15,
                                                color=ft.Colors.BLUE_GREY_300,
                                                offset=ft.Offset(0,0),
                                                blur_style=ft.ShadowBlurStyle.SOLID,))
class PriceTagContainer(ft.Container):
    def __init__(self):
        super().__init__()
        self.tags=dict()
        self.expand=True   
        self.field_value_section_name_id={
            '0':["Ids","CY,CT,AT"],    
           '1':["Name","Hercules,ATLAS,HERO"]  
        } 
        # item -> id and name
        self.debounce_task=None # Task to handle debouncing
        self.items_database = Item() # database connection
        self.items = self.items_database.list_items()# item
        self.items_database.close_connection()
        self.item_id_search = self.items
        # id search requirement                   
        self.list_items = {  
            name['item_id'].lower(): ft.ListTile(
                title=ft.Text(f"{name['item_id']} Stock->{name['stock']}"),
                leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                trailing=ft.Text(f"{name['item_description']}"),
                on_click=self.printer,
                hover_color='pink',
                style=ft.ListTileStyle.LIST,
                text_color='white',
                data=name
            )
            for name in self.item_id_search
        }
        self.trie_for_id=self.build_trie(self.list_items)
        # name requirement
        self.list_items_description = {
            "".join((name['item_description'].lower()).split()): ft.ListTile(
                title=ft.Text(f"{name['item_description']}"),
                leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                on_click=self.printer,
                trailing=ft.Text(f"{name['item_id']} Stock->{name['stock']}"),
                data=name,
                hover_color='pink',
                style=ft.ListTileStyle.LIST,
                text_color='white'
            )
            for name in self.items
        }
        self.trie=self.build_trie(self.list_items_description)
        # some import variable as like button and drop down 
        self.item_id=text_filed_style(label='Search BY ID Name',
                                    capitalizationn=ft.TextCapitalization.CHARACTERS,
                                    kbtype=ft.KeyboardType.STREET_ADDRESS,
                                    on_change=self.textbox_changed,
                                      # Matching column width
                                      expand=True,
                                    )
        self.drop_down=dropdown(value='0', width=100,on_change=self.feild_name_change,label="Search by!",options=[ft.dropdown.Option(key=0,text="IDs"),ft.dropdown.Option(key=1,text="Names")])
        self.search_description=ft.ListView(expand=1,spacing=2,item_extent=300,padding=2,auto_scroll=False)
        # ID name container for search 
        self.item_name_container=ft.Container(expand=False,
                                            height=0  ,
                                            # width =200,
                                              
                                            bgcolor="red",
                                            border_radius=15,
                                            padding=ft.padding.only(top=15,left=21,right=21,bottom=15),
                                            # clip behv. makes sure there' no overflow
                                            animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
                                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                            content=ft.Column(
                                                controls=[
                        
                                                    # there will be data display
                                                    self.search_description,
                                                    # ft.Column(scroll="auto",expand=True,)
                                                    # next 
                                                ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                                alignment=ft.MainAxisAlignment.START
                                            ))
        #tag detail here defin 
        self.discount_value = text_filed_style(
                                width=100,
                                label="Discount",
                                    kbtype=ft.KeyboardType.NUMBER,
                                    input_filter=ft.NumbersOnlyInputFilter(),
                                    suffix_text="%",
                                    # expand=True,
                                    hint_text="3-10%",
                                )

        self.Amount_value = text_filed_style(
                                    label="Amount",
                                    hint_text="",
                                    kbtype=ft.KeyboardType.NUMBER,
                                    input_filter=ft.NumbersOnlyInputFilter(),
                                    expand=True,
                                )

        self.MRP_value = text_filed_style(
                                    label="MRP",  # Corrected label
                                    hint_text="",
                                    kbtype=ft.KeyboardType.NUMBER,
                                   input_filter=ft.NumbersOnlyInputFilter(),
                                    expand=True,
                                )

        self.Product_name_value = text_filed_style(
                                    label="Product Name",   
                                    capitalization=ft.TextCapitalization.WORDS,  # Fixed typo
                                    kbtype=ft.KeyboardType.NAME,  # Changed from STREET_ADDRESS
                                    # input_filter=ft.TextOnlyInputFilter(),
                                    hint_text="ATLAS/Hero/Hercules/SunCross",
                                        )
        # button  here define 
        self.reset_all=button_style(text="Reset",on_click=self.reset_all)
        self.Add_all=button_style(text="Add Tag",on_click=self.add_tag)     
        self.generate_all=button_style(text="Generate Tag",bgcolor='Green',on_click=self.generate_tag)
        # Column define for action reaction and list_tag
        self.list_view_tag=ft.ListView(expand=True,auto_scroll=True,divider_thickness=2,spacing=10,padding=15,clip_behavior=ft.ClipBehavior.HARD_EDGE)
        # action 
        action_field =ft.Column([ft.Divider(),
            ft.Row([ft.Text("Tag Detail Entry",color="BLACK",size=18),],alignment=ft.MainAxisAlignment.CENTER),
                                 ft.Divider(),
                                 ft.Text("Search Area",color="BLACK",size=14),
                    
                                 ft.Row([self.drop_down,self.item_id,]),
                                 self.item_name_container,   
                                 ft.Divider(),
                                self.Product_name_value,
                                ft.Row([self.MRP_value,self.Amount_value,]),  
                                ft.Row([self.discount_value, self.Add_all,self.reset_all,self.generate_all   ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                 
                                 ]
                                ,alignment=ft.MainAxisAlignment.START)
        
        # reaction 
        
        # list_tag 
        list_tag_filed=ft.Column([ft.Divider(),
            ft.Row([ft.Text("List Tag Detail",color="BLACK",size=18),],alignment=ft.MainAxisAlignment.CENTER),
            ft.Divider(),
            ft.Divider(),
            self.list_view_tag,  
            ft.Divider(),
            ],alignment=ft.MainAxisAlignment.START)
        # Container
        action=ft.Container(bgcolor="#c1d3fe",
                            content=action_field,
                            expand=3,
                            alignment=ft.alignment.center,
                            border_radius=10,
                            ink=True,
                            margin=10,
                            padding=10 
                            )
        
        self.reaction=ft.Container(bgcolor="#c1d3fe",
                                    
                                   expand=True,alignment=ft.alignment.center,
                            border_radius=10,
                            ink=True,)
        self.list_tag=ft.Container(bgcolor="#c1d3fe",
                                   content=list_tag_filed,
                                   expand=True,
                                   alignment=ft.alignment.center,
                            border_radius=10,
                            ink=True,)
        divider_section=ft.Container(bgcolor="#c1d3fe",
                                   content=ft.Row([ft.Text("         Preview Area",size=15,color='black'),]),
                                   expand=True,
                                   alignment=ft.alignment.center,
                            border_radius=10,
                            ink=True,)
        self.content=ft.Row([action,ft.Column([
                                                ft.Row([self.list_tag,],expand=5,alignment=ft.MainAxisAlignment.CENTER),
                                                ft.Row([divider_section,],expand=1,alignment=ft.MainAxisAlignment.CENTER),
                                                 ft.Row([self.reaction,],expand=3,alignment=ft.MainAxisAlignment.CENTER),
                                            ],expand=5),])
    def handle_close_name_filed(self,e):
        self.item_name_container.height=0
        self.item_id.value=""
        self.search_description.controls.clear()
        self.item_name_container.update()
    def printer(self,e):
        pass
    def generate_unique_id(self):
        timestamp = int(time.time() * 1000)
        random_number = random.randint(1000, 9999)
        return f"{timestamp}{random_number}"
    def build_trie(self,data):
        """ Build a trie with item description"""
        trie=pygtrie.CharTrie()
        for key, value in data.items():
            trie[key.lower()]=value
        return trie
    def feild_name_change(self,e):    
        print(f"changes call function call{self.drop_down.value}")
       
        self.item_id.label=self.field_value_section_name_id[self.drop_down.value][0]
        self.item_id.hint_text=self.field_value_section_name_id[self.drop_down.value][1]
        self.item_id.update()
        return
    def textbox_changed(self,e):
        str_number = e.control.value.lower()
        if not str_number:
            self.item_name_container.height=0
            self.item_name_container.update()
        if self.drop_down.value == '1':
            try:
                result=[value for key, value in self.trie.items(prefix=str_number)]
                self.search_description.controls = result if str_number else []
                if len(self.search_description.controls)==0:
                    self.item_name_container.height=0
                else: 
                    self.item_name_container.height=min(90+(len(self.search_description.controls)*50),190)
            except:
                self.search_description.controls.clear()
                self.search_description.controls.append(
                    ft.ListTile(
                    title=ft.Text("Sorry"),
                    leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                    # on_click=self.printer,
                    trailing=ft.Text(f"No Matches found"),
                    data="Not_found",  
                    hover_color='pink',
                    style=ft.ListTileStyle.LIST,
                    text_color='white'
                )
                )
                self.item_name_container.height=90
        elif self.drop_down.value == '0':
            try:
                result=[value for key, value in self.trie_for_id.items(prefix=str_number)]
                self.search_description.controls = result if str_number else []
                if len(self.search_description.controls)==0:
                    self.item_name_container.height=0
                else: 
                    self.item_name_container.height=min(90+(len(self.search_description.controls)*50),190)
            except:
                self.search_description.controls.clear()
                self.search_description.controls.append(
                    ft.ListTile(
                    title=ft.Text("Sorry"),
                    leading=ft.Image(src="invoice_logo.png", color_blend_mode=ft.BlendMode.SRC_IN, width=24, height=24),
                    # on_click=self.printer,
                    trailing=ft.Text(f"No Matches found"),
                    data="Not_found",  
                    hover_color='pink',
                    style=ft.ListTileStyle.LIST,
                    text_color='white'
                )
                )
                self.item_name_container.height=90
        
        self.item_name_container.update()
    def increment(self,e):
        tag_id = e.control.data  # Get the tag ID from the button's data attribute
        if tag_id in self.tags:
            self.tags[tag_id]["copy"] += 1  # Increase the quantity
            self.update_tag_display(tag_id)  # Update UI display
    def decrement(self,e):
        tag_id = e.control.data
        if tag_id in self.tags and self.tags[tag_id]["copy"] > 1:
            self.tags[tag_id]["copy"] -= 1  # Decrease the quantity, ensuring it's at least 1
            self.update_tag_display(tag_id)  # Update UI display
    def update_tag_display(self, tag_id):
        for tile in self.list_view_tag.controls:
            if isinstance(tile, ft.Dismissible) and tile.data == tag_id:
                list_tile = tile.content  # Get the ListTile inside Dismissible
                list_tile.trailing.controls[1].value = str(self.tags[tag_id]["copy"])  # Update count
                list_tile.trailing.update()  # Refresh the UI
                break
    def preview_fun(self,e):
        id=e.control.data
        tag_data = self.tags[id]
        self.reaction.content=ft.Card(
            content=ft.Container(
                alignment=ft.alignment.center,
                padding=ft.Padding(16, 16, 16, 16),
                image=ft.DecorationImage(
                    src="background/price_tag_backgroud.png",
                    fit=ft.ImageFit.FILL,
                    # color_filter=ft.FilterQuality.HIGH
                ),
                width=400,
                height=200,
                content=ft.Column([ft.Row([]),
                    ft.Row([ft.Text(f"Product: {tag_data['item_name']}", size=20,color="black", weight=ft.FontWeight.BOLD)],wrap=True,alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Text(f"MRP:",color="black",size=16),ft.Text(spans=[ft.TextSpan(
                    f"{tag_data['mrp']}",
                    ft.TextStyle(color='black',size=18,    
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=1,decoration_color="red"
                    ),
                ),])],alignment=ft.MainAxisAlignment.CENTER)
                         
                ])
            )    ,elevation=4,   
        )
        self.reaction.update()
        
    def add_tag(self,e):
        if not( self.Product_name_value and self.MRP_value and self.Amount_value and self.discount_value):
            return
        
        data_v={
            'item_name':self.Product_name_value.value,
            'mrp':self.MRP_value.value,
            'amount':self.Amount_value.value,
            'discount':self.discount_value.value,
            'copy':1,
        }
        id = self.generate_unique_id()            
        lv=ft.ListTile(
            leading=ft.Icon(ft.Icons.FILTER_VINTAGE_ROUNDED),
            title=ft.Text(f"{data_v['item_name']}",expand=True),
            subtitle=ft.Text(f"MRP:{data_v['mrp']}, Amount:{data_v['amount']}  ,Discount:{data_v['discount']}",expand=True),
            trailing=ft.Row([
                ft.IconButton(icon=ft.Icons.ADD_ROUNDED,data=id,on_click=self.increment),
                ft.Text(f"{data_v['copy']}"),
                ft.IconButton(icon=ft.Icons.REMOVE_OUTLINED,data=id,on_click=self.decrement),  
            ],wrap=False,width=100),
            data=id,
            on_click=self.preview_fun
        )
        self.list_view_tag.controls.append(
            ft.Dismissible(
                dismiss_thresholds={
                    ft.DismissDirection.END_TO_START:0.2  
                },
                on_dismiss=self.handle_dismiss_tag,
                dismiss_direction=ft.DismissDirection.END_TO_START,
                secondary_background=ft.Container(bgcolor="red",content=ft.Text("REMOVE TAG        ",size=19,color='black'),alignment=ft.alignment.center_right),
                content=lv,
                data=id  
                
            )
        )
        self.tags[id]=data_v
        self.list_view_tag.update()    
    def generate_tag(self,e):
        pass
    def reset_all(self,e):
        pass
    def handle_dismiss_tag(self,e):  
        if e.control.data in self.tags:
            del self.tags[e.control.data]
        self.list_view_tag.controls.remove(e.control)
        self.list_view_tag.update()
        
class PriceTagApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.tags = []  # Store added price tags
        self.preview_text = ft.Text("TAG PREVIEW", color="white", size=18)
    
    async def build(self):
        # Entry Fields
        self.item_name = ft.TextField(label="ITEM NAME")
        self.mrp = ft.TextField(label="MRP")
        self.price = ft.TextField(label="PRICE")
        self.discount = ft.TextField(label="DISCOUNT")
        
        # Buttons
        self.empty_btn = ft.ElevatedButton(text="EMPTY", bgcolor="red", color="white", on_click=self.clear_fields)
        self.add_btn = ft.ElevatedButton(text="ADD", bgcolor="red", color="white", on_click=self.add_tag)
        self.generate_btn = ft.ElevatedButton(text="GENERATE", bgcolor="black", color="white", on_click=self.generate_pdf)

        # Tags List
        self.tag_list = ft.Column(spacing=10, expand=True)
        
        # UI Layout
        return ft.Row(
            controls=[
                # Left Panel (Entry Area)
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("ENTRY AREA", size=20, color="white"),
                            ft.Text("SEARCH AREA", color="white"),
                            ft.Row([ft.TextField(label="SEARCH BY ID"), ft.TextField(label="SEARCH BY NAME")]),
                            self.item_name, self.mrp, self.price, self.discount,
                            ft.Row([self.empty_btn, self.add_btn]),
                            self.generate_btn,
                        ],
                        spacing=10,
                    ),
                    bgcolor="#0B2A47",
                    padding=20,
                    expand=2,
                    border_radius=10,
                ),
                
                # Right Panel (Tag List + Preview)
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("LIST TAG", size=20, color="white"),
                            self.tag_list,
                            ft.Text("PRICE TAG PREVIEW", size=16),
                            ft.Container(
                                content=self.preview_text,
                                bgcolor="green",
                                width=200,
                                height=100,
                                alignment=ft.alignment.center,
                            ),
                        ],
                        spacing=10,
                    ),
                    bgcolor="lightgray",
                    padding=20,
                    expand=3,
                    border_radius=10,
                ),
            ],
            expand=True
        )
    
    async def clear_fields(self, e):
        """ Clears input fields """
        self.item_name.value = ""
        self.mrp.value = ""
        self.price.value = ""
        self.discount.value = ""
        await self.update_async()

    async def add_tag(self, e):
        """ Adds a new tag to the list """
        tag_text = f"{self.item_name.value} - Rs.{self.price.value} (OFF: {self.discount.value}%)"
        new_tag = ft.Text(tag_text, color="white", bgcolor="teal", width=300, height=40, alignment=ft.alignment.center)
        self.tags.append(new_tag)
        self.tag_list.controls.append(new_tag)
        await self.update_async()
    
    async def generate_pdf(self, e):
        """ Placeholder for PDF generation """
        print("Generating PDF...")  # Implement PDF logic here
    
async def main(page: ft.Page):
    page.title = "Price Tag Generator"
    page.add(PriceTagContainer())

ft.app(target=main,assets_dir="../assets")
