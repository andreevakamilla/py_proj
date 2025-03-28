import subprocess
from gtts import gTTS
from aiogram import Bot, Dispatcher, types
import telebot
from telebot import types
import helper
from googletrans import Translator
import base64
from transliterate import translit
from deepface import DeepFace
from mytoken import TG_TOKEN
import json
import os



bot = telebot.TeleBot(TG_TOKEN)
translator = Translator()

user_states = {}
def convert_ogg_to_wav(ogg_filename, wav_filename):
    command = ['ffmpeg', '-y', '-i', ogg_filename, wav_filename]
    subprocess.run(command)


def handle_command(chat_id, text):
    bot.send_message(chat_id, "??????")


def convert_video_to_gif(video_filename, gif_filename):
    command = ['ffmpeg', '-y', '-i', video_filename, '-vf', 'scale=320:-1', '-t', '15', gif_filename]
    subprocess.run(command)


@bot.message_handler(commands=['start'])
def welcome(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    to_sound = types.InlineKeyboardButton("конвертация текста в аудио", callback_data="tosound")
    to_text = types.InlineKeyboardButton("конвертация аудио в текст", callback_data="totext")
    to_gif = types.InlineKeyboardButton("конвертация видео в гиф", callback_data="togif")
    encode_button = types.InlineKeyboardButton("Кодировать текст", callback_data="encode")
    decode_button = types.InlineKeyboardButton("Декодировать текст", callback_data="decode")
    translate_button = types.InlineKeyboardButton("Перевод текста", callback_data="translate")
    face_button = types.InlineKeyboardButton("Анализ фото", callback_data="face")



    markup.add(to_sound, to_text, to_gif, encode_button, decode_button, translate_button, face_button)
    bot.send_message(message.chat.id, "Привет, я бот, который может делать много разных функций", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def to_sound_callback_handler(call):
    chat_id = call.message.chat.id
    if call.data == "tosound":
        bot.send_message(chat_id, "Введите текст для конвертации в аудио:")
        user_states[chat_id] = "tosound"
    elif call.data == "totext":
        bot.send_message(chat_id, "Введите аудио для конвертации в текст:")
        user_states[chat_id] = "totext"
    elif call.data == "togif":
        bot.send_message(chat_id, "Вставьте видео для конвертации в гиф-изображение:")
        user_states[chat_id] = "togif"
    elif call.data == "encode":
        bot.send_message(chat_id, "Введите текст для кодирования:")
        user_states[chat_id] = "encode"
    elif call.data == "decode":
        bot.send_message(chat_id, "Введите текст для декодирования:")
        user_states[chat_id] = "decode"
    elif call.data == "translate":
        bot.send_message(chat_id, "Введите текст для перевода:")
        user_states[chat_id] = "translate"
    elif call.data == "face":
        bot.send_message(chat_id, "Вставьте изображение для анализа:")
        user_states[chat_id] = "face"


@bot.message_handler(func=lambda message: True)
def handle_user_text(message):
    chat_id = message.chat.id
    if chat_id in user_states:
        state = user_states[chat_id]
        if state == "tosound":
            text_to_convert = message.text
            tts = gTTS(text_to_convert, lang='ru')
            tts.save("output.mp3")
            with open("output.mp3", "rb") as audio:
                bot.send_voice(message.chat.id, audio.read())
        elif state == "encode":
            text_to_encode = message.text
            encoded_text = base64.b64encode(text_to_encode.encode('utf-8')).decode('utf-8')
            bot.send_message(chat_id, f"Закодированный текст: {encoded_text}")
        elif state == "decode":
            text_to_decode = message.text
            decoded_text = base64.b64decode(text_to_decode).decode('utf-8')
            bot.send_message(chat_id, f"Декодированный текст: {decoded_text}")
        elif state == "translate":
            translated_text = translit(translator.translate(message.text, src='ru', dest='ar').text, 'ru', reversed=True)
            bot.send_message(chat_id, f"Текст на арабском:\n{translated_text}")

    del user_states[chat_id]


@bot.message_handler(content_types=['voice'])
def handle_user_audio(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    ogg_filename = 'voice.ogg'
    with open(ogg_filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    wav_filename = 'voice.wav'
    convert_ogg_to_wav(ogg_filename, wav_filename)
    text = helper.speech_to_text(wav_filename)
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['video'])
def handle_user_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    video_filename = 'input_video.mp4'
    gif_filename = 'output_gif.gif'
    with open(video_filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    convert_video_to_gif(video_filename, gif_filename)
    with open(gif_filename, 'rb') as gif_file:
        bot.send_document(message.chat.id, gif_file)


@bot.message_handler(content_types=['photo'])
def handle_user_photo(message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    photo_filename = 'user_photo.jpg'
    with open(photo_filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    with open(photo_filename, 'rb') as image_file:
        try:
            result_list = DeepFace.analyze(img_path=os.path.abspath(photo_filename), actions=['age', 'gender', 'race', 'emotion'])
            for i, face_result in enumerate(result_list, start=1):
                bot.send_message(chat_id, f'Analysis for Face #{i}:')
                bot.send_message(chat_id, f'[+] Age: {face_result.get("age")}')
                bot.send_message(chat_id, f'[+] Gender: {face_result.get("gender")}')
                bot.send_message(chat_id, f'[+] Race: {json.dumps(face_result.get("race"), indent=4, ensure_ascii=False)}')

                # Iterate over emotions and send them
                bot.send_message(chat_id, '[+] Emotions:')
                for k, v in face_result.get("emotion").items():
                    bot.send_message(chat_id, f'{k} - {round(v, 2)}%')

        except Exception as _ex:
            bot.send_message(chat_id, f'Error processing photo: {_ex}')



if __name__ == "__main__":
    bot.polling(none_stop=True)
