import telebot
import random
import os
import string
from telebot import types

TOKEN = '...'
bot = telebot.TeleBot(TOKEN)

user_states = {}
user_data = {}

class BotLogic:
    def __init__(self):
        self.emojis = ['🚀', '⭐', '🌙', '🎮', '🔥', '💫', '🪐', '⚡', '🎲', '❤️']
    
    def get_main_menu(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        markup.add('/coin', '/emoji', '/quiz')
        markup.add('/score', '/reset', '/mem')
        markup.add('/random', '/password', '/games')
        return markup
    
    def get_coin_menu(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('🟡 Heads', '🔴 Tails')
        return markup
    
    def start_help(self, chat_id):
        help_text = ("🎮 Играй в мини-игры!\n"
                    "/coin 🪙 – угадай орла или решку\n"
                    "/emoji 🎲 – случайный эмодзи\n"
                    "/quiz ❓ – угадай число от 1 до 10\n"
                    "/mem 🖼️ – случайный мем\n"
                    "/random 🎲 – случайное число от 1 до 100\n"
                    "/password 🔐 – сгенерировать 8-значный пароль\n"
                    "/games 🎮 – актуальные игры\n"
                    "/score 📊 – твой счёт\n"
                    "/reset 🔄 – сброс счёта")
        bot.send_message(chat_id, help_text, reply_markup=self.get_main_menu())
    
    def coin_game(self, chat_id, user_id, text):
        guess = 'Heads' if 'Heads' in text else 'Tails'
        result = random.choice(['Heads', 'Tails'])
        
        if guess == result:
            score = user_data.get(user_id, {}).get('score', 0) + 10
            user_data[user_id] = user_data.get(user_id, {})
            user_data[user_id]['score'] = score
            bot.send_message(chat_id, f"✅ Угадал! {result}! +10 очков. Счёт: {score}", reply_markup=self.get_main_menu())
        else:
            bot.send_message(chat_id, f"❌ {result}", reply_markup=self.get_main_menu())
    
    def emoji_game(self, chat_id):
        emoji = random.choice(self.emojis)
        bot.send_message(chat_id, f" {emoji}", reply_markup=self.get_main_menu())
    
    def quiz_game(self, chat_id, user_id):
        number = random.randint(1, 10)
        user_data[user_id] = user_data.get(user_id, {})
        user_data[user_id]['quiz_number'] = number
        bot.send_message(chat_id, "❓ Угадай число 1-10:", reply_markup=None)
        return number
    
    def check_quiz(self, chat_id, user_id, guess):
        correct = user_data[user_id]['quiz_number']
        if guess == correct:
            score = user_data[user_id].get('score', 0) + 20
            user_data[user_id]['score'] = score
            bot.send_message(chat_id, f"✅ {correct}! +20 очков. Счёт: {score}", reply_markup=self.get_main_menu())
        else:
            bot.send_message(chat_id, f"😔 Было {correct}", reply_markup=self.get_main_menu())
    
    def show_score(self, chat_id, user_id):
        score = user_data.get(user_id, {}).get('score', 0)
        bot.send_message(chat_id, f"📊 Твои очки: {score}", reply_markup=self.get_main_menu())
    
    def reset_score(self, chat_id, user_id):
        user_data[user_id] = {'score': 0}
        bot.send_message(chat_id, "🔄 Счёт сброшен!", reply_markup=self.get_main_menu())
    
    def send_random_mem(self, chat_id):
        try:
            all_images = os.listdir('images')
            image_files = [f for f in all_images if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
            
            if image_files:
                img_name = random.choice(image_files)
                with open(f'images/{img_name}', 'rb') as f:
                    bot.send_photo(chat_id, f, caption=f"😂 Мем: {img_name}")
                bot.send_message(chat_id, "🎮 Главное меню:", reply_markup=self.get_main_menu())
            else:
                bot.send_message(chat_id, "❌ В папке images нет картинок!", reply_markup=self.get_main_menu())
        except FileNotFoundError:
            bot.send_message(chat_id, "❌ Создай папку 'images' и добавь мемы!", reply_markup=self.get_main_menu())
        except Exception as e:
            bot.send_message(chat_id, f"❌ Ошибка с мемами: {e}", reply_markup=self.get_main_menu())
    
    # Новые методы
    def random_number(self, chat_id):
        num = random.randint(1, 100)
        bot.send_message(chat_id, f"🎲 Случайное число от 1 до 100: {num}", reply_markup=self.get_main_menu())
    
    def generate_password(self, chat_id):
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for _ in range(8))
        bot.send_message(chat_id, f"🔐 Ваш 8-значный пароль: `{password}`", parse_mode='Markdown', reply_markup=self.get_main_menu())
    
    def suggest_games(self, chat_id):
        games = [
            "🎮 *Among Us* – всё ещё популярная игра на логику и обман.",
            "🎮 *Minecraft* – классика, актуальна для творческих личностей.",
            "🎮 *Genshin Impact* – отличный выбор для любителей аниме и открытого мира.",
            "🎮 *CS:GO* – для любителей динамичных шутеров.",
            "🎮 *Dota 2* – если нравятся сложные стратегии.",
            "🎮 *Valorant* – тактический шутер с уникальными персонажами.",
            "🎮 *Stardew Valley* – расслабляющая ферма, всегда актуальна."
        ]
        text = "🌟 *Актуальные игры сейчас:*\n\n" + "\n".join(games)
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=self.get_main_menu())

logic = BotLogic()

@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    logic.start_help(message.chat.id)

@bot.message_handler(commands=['coin'])
def coin_handler(message):
    user_id = message.from_user.id
    user_states[user_id] = 'coin_wait'
    bot.send_message(message.chat.id, "🪙 Heads или Tails?", reply_markup=logic.get_coin_menu())

@bot.message_handler(commands=['emoji'])
def emoji_handler(message):
    logic.emoji_game(message.chat.id)

@bot.message_handler(commands=['quiz'])
def quiz_handler(message):
    user_id = message.from_user.id
    user_states[user_id] = 'quiz_wait'
    logic.quiz_game(message.chat.id, user_id)

@bot.message_handler(commands=['score'])
def score_handler(message):
    logic.show_score(message.chat.id, message.from_user.id)

@bot.message_handler(commands=['reset'])
def reset_handler(message):
    logic.reset_score(message.chat.id, message.from_user.id)

@bot.message_handler(commands=['mem'])
def mem_handler(message):
    logic.send_random_mem(message.chat.id)

@bot.message_handler(commands=['random'])
def random_handler(message):
    logic.random_number(message.chat.id)

@bot.message_handler(commands=['password'])
def password_handler(message):
    logic.generate_password(message.chat.id)

@bot.message_handler(commands=['games'])
def games_handler(message):
    logic.suggest_games(message.chat.id)

@bot.message_handler(func=lambda m: m.from_user.id in user_states and user_states[m.from_user.id] == 'coin_wait')
def coin_response(message):
    user_id = message.from_user.id
    logic.coin_game(message.chat.id, user_id, message.text)
    del user_states[user_id]

@bot.message_handler(func=lambda m: m.text.isdigit() and len(m.text) == 1 and m.from_user.id in user_states and user_states[m.from_user.id] == 'quiz_wait')
def quiz_response(message):
    user_id = message.from_user.id
    logic.check_quiz(message.chat.id, user_id, int(message.text))
    del user_states[user_id]

@bot.message_handler(func=lambda message: True)
def default_handler(message):
    logic.start_help(message.chat.id)

print("🚀 Бот запущен!")
bot.infinity_polling()
