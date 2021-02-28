from PIL import Image, ImageFont, ImageDraw

def make_image(question, answer):
        ### import resources
        background = Image.open("resources/background.png", "r").convert("RGBA").resize((1080, 1920), Image.BICUBIC)
        print("Background:", background.size, background.mode)

        logo = Image.open("resources/tellonym-logo.png", "r").convert("RGBA")
        print("Logo:", logo.size, logo.mode)

        button = Image.open("resources/send_btn.png", "r").convert("RGBA").resize((100, 100), Image.BICUBIC)
        print("Button:", button.size, button.mode)

        ### create layers
        text_layer = Image.new("RGBA", background.size, (255, 255, 255, 0))
        background_additions = Image.new("RGBA", background.size, (255, 255, 255, 0))

        ### draw background additions
        logo_position = (int(background.size[0] / 2) - int(logo.size[0] / 2), 70)
        logo_area = (logo_position[0], logo_position[1], logo_position[0] + logo.size[0], logo_position[1] + logo.size[1])
        background_additions.paste(logo, logo_area)
        btn_position = (background.size[0] - button.size[0] - 100,
                background.size[1] - button.size[1] - 200)
        btn_area = (btn_position[0], btn_position[1], btn_position[0] + button.size[0], btn_position[1] + button.size[1])
        background_additions.paste(button, btn_area)
        tell_font_size = 80
        tell_font = ImageFont.truetype("resources/Goldman/Goldman-Regular.ttf", tell_font_size)
        tell_text = "Link in der Bio"
        tell_color = (226, 226, 226)
        image_tell = ImageDraw.Draw(background_additions)
        tell_position = (int(background.size[0] / 2) - image_tell.textsize(tell_text, font=tell_font, spacing=4)[0] / 2,
                background.size[1] - 300)
        image_tell.text(tell_position, tell_text, tell_color, font=tell_font, anchor="mm",
                spacing=4, align="center", stroke_width=0, stroke_fill=None, embedded_color=False)

        ### draw text
        if not question.endswith("?"):
                question += "?"
        count = 0
        for i in range(len(question)):
                if count >= 20 and question[i-1] == " ":
                        split_strings = [question[index : index + i] for index in range(0, len(question), i)]
                        question = f"{split_strings[0]}\n"
                        for x in range(len(split_strings) - 1):
                                question += split_strings[x + 1]
                        count = 0
                count += 1
        count = 0
        for i in range(len(answer)):
                if count >= 20 and answer[i-1] == " ":
                        split_strings = [answer[index : index + i] for index in range(0, len(answer), i)]
                        answer = f"{split_strings[0]}\n"
                        for x in range(len(split_strings) - 1):
                                answer += split_strings[x + 1]
                        count = 0
                count += 1

        card_font_size = 70
        card_font = ImageFont.truetype("resources/Balsamiq_Sans/BalsamiqSans-Regular.ttf", card_font_size)
        question_color = (226, 226, 226)
        answer_color = (255, 1, 123)

        image_card = ImageDraw.Draw(text_layer)
        question_height = image_card.multiline_textsize(question, font=card_font, spacing=4)[1]
        answer_height = image_card.multiline_textsize(answer, font=card_font, spacing=4)[1]

        question_position = (100, int(background.size[1] / 2) - int((question_height + answer_height) / 2) - 200)
        image_card.multiline_text(question_position, question, fill=question_color, font=card_font, anchor=None,
                        spacing=4, align="left", stroke_width=0, stroke_fill=None)
        answer_position = (100, question_position[1] + question_height + 70)
        image_card.multiline_text(answer_position, answer, fill=answer_color, font=card_font, anchor=None,
                        spacing=4, align="left", stroke_width=0, stroke_fill=None)

        ### put the layers together
        background_layer = Image.alpha_composite(background, background_additions)

        output_image = Image.alpha_composite(background_layer, text_layer)

        output_image.show()
        return output_image

def save_image(image, name):
        image.save(f"output/{name}.png")
        print(f"saved image {name}.png")

if __name__ == "__main__":
    q = input("Question: ")
    a = input("Answer: ")
    im = make_image(q, a)
    save_image(im, "tellonym")