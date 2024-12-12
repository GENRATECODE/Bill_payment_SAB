# views.view_about
import math
import time
import base64
import flet as ft
from zhipuai import ZhipuAI


class AccountCard(ft.Container):
    def __init__(self):
        super().__init__()
        self.t = ft.Text()
        self.content = self.t

    def did_mount(self):
        self.running = True
        self.page.run_thread(self.update_weather)

    def will_unmount(self):
        self.running = False

    def update_weather(self):
        x = 0
        while self.running:
            x += 1
            self.t.value = x
            self.t.update()
            time.sleep(1)


def AboutView(page):

    def ocr_message(e):

        client = ZhipuAI(
            api_key="83de700906eb01fba2d1dc980d98ebbf.MhjzywbFar2RCWPW"
        )  # 填写您自己的APIKey
        if inputURL.value != "":
            with open(rf"{inputURL.value}", "rb") as img_file:
                img_base = base64.b64encode(img_file.read()).decode("utf-8")
            message=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "image_url", "image_url": {"url": img_base}},
                            {"type": "text", "text": "请提取这个图片的文字"},
                        ],
                    }
            ]
            


            response = client.chat.completions.create(
                model="glm-4v-plus",  # 填写需要调用的模型名称
                messages=message,
                stream=True,
                top_p=0.1,
                temperature=0.55,
                tools=[{"type": "web_search", "web_search": {"search_result": True}}],
            )
            # print(response.choices[0].message)
            ocrText.value = ""
            ocrText.update()
            for chunk in response:
                ocrText.value += chunk.choices[0].delta.content  # 实时流输出
                ocrText.update()
    inputURL = ft.TextField(
        label="Input your text here",
        multiline=True,
        shift_enter=True,
        bgcolor=ft.colors.BLACK45,
    )
    ocrText = ft.TextField(
        multiline=True,
        shift_enter=True,
        expand=True,
        min_lines=100,
        border=ft.InputBorder.NONE,
        bgcolor=ft.colors.BLACK45,
    )
    content = ft.Row(
        [
            ft.Column(
                [
                    inputURL,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Translate",
                                on_click=lambda e: ocr_message(e),
                                expand=True,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(1))
                            )
                        ]
                    ),
                    ocrText,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,spacing=2
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )

    return content
