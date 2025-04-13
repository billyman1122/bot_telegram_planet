import telebot
from telebot.types import Message
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def detect_image(input_path, model):
    np.set_printoptions(suppress=True)
    model = load_model(model, compile=False)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(input_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    confidence_score = prediction[0][index]
    return index, confidence_score


bot = telebot.TeleBot('*your telegramm token*')

@bot.message_handler(commands=['start'])
def start_cmd(message:Message):
    bot.send_message(message.chat.id, 'Привет, я бот ИИ, который может отличать планеты и давать о них небольшую информацию')


@bot.message_handler(content_types='photo')
def photo_cmd(message: Message):
    if not message.photo:
        return bot.send_message(message.chat.id, 'Вы отправили не картинку')
    
    filename = f'photo_{message.from_user.id}.png'
    fileinfo = bot.get_file(message.photo[-1].file_id)

    file = bot.download_file(fileinfo.file_path)
    with open(filename, 'wb') as new_file:
        new_file.write(file)

    old_message = bot.send_message(message.chat.id, 'Ваша картинка загружена, пожалуйста подождите')

    index, score = detect_image(filename, 'keras_model.h5')
    if score > 0.9:
        if index == 0:
         bot.send_message(message.chat.id, f'Меркурий (я уверен в этом на {round(score * 100, 1)}%) это ближайшая планета к Солнцу, и она имеет очень тонкую атмосферу. Это маленькая и каменистая планета, с большими температурными колебаниями между днем и ночью')
        elif index == 1:
         bot.send_message(message.chat.id, f'Венера (я уверен в этом на {round(score * 100, 1)}%) похожая на Землю по размеру, но с очень плотной и токсичной атмосферой, богатой углекислым газом. Поверхность Венеры очень горячая из-за парникового эффекта')
        elif index == 2:
         bot.send_message(message.chat.id, f'Земля (я уверен в этом на {round(score * 100, 1)}%) единственная известная планета с жизнью. У Земли есть атмосфера, океаны и континенты. Она вращается вокруг своей оси и движется по орбите вокруг Солнца')
        elif index == 3:
         bot.send_message(message.chat.id, f'Марс (я уверен в этом на {round(score * 100, 1)}%) известен как "красная планета" из-за своего железного оксида на поверхности. Марс обладает тонкой атмосферой и имеет полюса замороженной воды')
        elif index == 4:
         bot.send_message(message.chat.id, f'Юпитер (я уверен в этом на {round(score * 100, 1)}%) самая большая планета в солнечной системе. Это газовый гигант с характерными полосами облаков и знаменитым Большим красным пятном — бурей, существующей уже сотни лет')
        elif index == 5:
         bot.send_message(message.chat.id, f'Сатурн (я уверен в этом на {round(score * 100, 1)}%) известен своими великолепными кольцами, состоящими из льда и камней. Также является газовым гигантом и имеет множество спутников')
        elif index == 6:
         bot.send_message(message.chat.id, f'Уран (я уверен в этом на {round(score * 100, 1)}%) это газовый гигант, который имеет уникальное наклонение оси вращения, почти лежа на боку. Уран также имеет кольца и множество лун')
        elif index == 7:
         bot.send_message(message.chat.id, f'Нептун (я уверен в этом на {round(score * 100, 1)}%) это самая удаленная планета от Солнца, также газовый гигант. Известен своими сильными ветрами и характерным синим цветом из-за присутствия метана в атмосфере')
        else:
         bot.send_message(message.chat.id, 'Извините, я не уверен, что это на картинке')
        bot.delete_message(old_message.chat.id, old_message.id)

  
bot.infinity_polling()
