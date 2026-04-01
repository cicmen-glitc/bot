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

    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        markup.add('/coin', '/emoji', '/quiz')
        markup.add('/score', '/reset', '/mem')
        markup.add('/random', '/password', '/games')
        markup.add('/eco')  
        return markup
    
    def get_coin_menu(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('🟡 Heads', '🔴 Tails')
        return markup
    
    def get_eco_menu(self):
        """Инлайн-клавиатура для экологических советов"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton("♻️ Сортировка отходов", callback_data="eco_sort")
        btn2 = types.InlineKeyboardButton("💡 Как начать", callback_data="eco_start")
        btn3 = types.InlineKeyboardButton("⏳ Время разложения", callback_data="eco_decompose")
        btn4 = types.InlineKeyboardButton("🏠 Домашние лайфхаки", callback_data="eco_tips")
        markup.add(btn1, btn2, btn3, btn4)
        return markup
    
    def start_help(self, chat_id):
        help_text = ("🎮 *Играй в мини-игры!*\n"
                     "/coin 🪙 – угадай орла или решку\n"
                     "/emoji 🎲 – случайный эмодзи\n"
                     "/quiz ❓ – угадай число от 1 до 10\n"
                     "/mem 🖼️ – случайный мем\n"
                     "/random 🎲 – случайное число от 1 до 100\n"
                     "/password 🔐 – сгенерировать 8-значный пароль\n"
                     "/games 🎮 – актуальные игры\n"
                     "/eco 🌱 – советы по экологии и уменьшению отходов\n"
                     "/score 📊 – твой счёт\n"
                     "/reset 🔄 – сброс счёта")
        bot.send_message(chat_id, help_text, parse_mode='Markdown', reply_markup=self.get_main_menu())
    
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
    
    # ========== ЭКОЛОГИЯ ==========
    def show_eco_info(self, chat_id):
        """Главное экологическое меню"""
        text = ("🌱 *Экологический помощник*\n\n"
                "Я помогу тебе уменьшить количество отходов и начать экологичный образ жизни!\n"
                "Выбери, что тебя интересует:")
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=self.get_eco_menu())
    
    def eco_sort_tips(self, chat_id):
        text = ("♻️ *Как сортировать отходы:*\n\n"
                "• Пластик: бутылки, флаконы (с маркировкой 1, 2, 5) – сжать, снять крышки.\n"
                "• Стекло: банки, бутылки – промыть, снять крышки.\n"
                "• Бумага: картон, тетради, газеты – чистая и сухая.\n"
                "• Металл: алюминиевые банки, крышки.\n"
                "• Опасные отходы: батарейки, лампы – сдавать отдельно.\n"
                "❌ Не выбрасывай в общий контейнер: пищевые отходы, грязную упаковку, чеки.\n\n"
                "🌟 *Совет*: установи дома два ведра – для смешанных отходов и для вторсырья.")
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=self.get_eco_menu())
    
    def eco_start_tips(self, chat_id):
        text = ("💡 *С чего начать эко-привычки:*\n\n"
                "1️⃣ Многоразовая сумка вместо пакетов.\n"
                "2️⃣ Бутылка для воды – откажись от пластиковых.\n"
                "3️⃣ Сортируй хотя бы пластик и бумагу.\n"
                "4️⃣ Используй эко-средства для уборки (уксус, сода).\n"
                "5️⃣ Не бери лишнюю упаковку.\n"
                "6️⃣ Сдавай батарейки в специальные пункты.\n\n"
                "✨ Начни с одного пункта – это уже вклад!")
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=self.get_eco_menu())
    
    def eco_decompose_info(self, chat_id):
        text = ("⏳ *Время разложения отходов:*\n\n"
                "• Стекло – более 1000 лет\n"
                "• Алюминиевая банка – 200–500 лет\n"
                "• Пластиковая бутылка – 450 лет\n"
                "• Полиэтиленовый пакет – 20–200 лет\n"
                "• Окурок – 10–15 лет\n"
                "• Батарейка – 100 лет (опасна для почвы!)\n"
                "• Бумага – 2–6 месяцев\n"
                "• Пищевые отходы – 1–2 месяца\n\n"
                "📌 *Помни*: переработка сокращает время разложения и сохраняет ресурсы!")
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=self.get_eco_menu())
    
    def eco_home_tips(self, chat_id):
        text = ("🏠 *Эко-лайфхаки для дома:*\n\n"
                "🌿 Используй многоразовые губки для посуды.\n"
                "🌿 Компостируй пищевые отходы (даже в квартире).\n"
                "🌿 Покупай продукты на развес.\n"
                "🌿 Замени пленку на восковые салфетки.\n"
                "🌿 Ремонтируй вещи вместо покупки новых.\n"
                "🌿 Участвуй в акциях по раздельному сбору.\n\n"
                "🧠 Маленькие шаги ведут к большим изменениям!")
        bot.send_message(chat_id, text, parse_mode='Markdown', reply_markup=self.get_eco_menu())
    
    def eco_question_answer(self, chat_id, message_text):
        """Обработка вопросов пользователя об экологии"""
        text_lower = message_text.lower()
        if "пластик" in text_lower or "бутылка" in text_lower:
            answer = ("♻️ *Пластик*: большинство бутылок с маркировкой 1 (PET) и 2 (HDPE) перерабатываются. "
                      "Сними крышку, сожми бутылку. Крышки тоже можно сдавать отдельно. "
                      "Пакеты и плёнку сдавай в специальные контейнеры.")
        elif "батарейк" in text_lower:
            answer = ("🔋 *Батарейки*: никогда не выбрасывай в мусорное ведро! "
                      "Они содержат тяжёлые металлы. Сдавай в магазинах (Media Markt, Икеа, Леруа Мерлен) "
                      "или в пунктах приёма опасных отходов.")
        elif "стекло" in text_lower:
            answer = ("🥃 *Стекло*: перерабатывается бесконечно. Снимай крышки, промывай, "
                      "складывай в контейнеры для стекла. Бьётся – не страшно, его тоже принимают.")
        elif "бумаг" in text_lower or "картон" in text_lower:
            answer = ("📄 *Бумага и картон*: принимаются чистыми и сухими. "
                      "Удаляй скрепки, скотч. Чеки, влажная бумага, втулки от туалетной бумаги – идут в общий мусор.")
        elif "сортировк" in text_lower or "раздельный сбор" in text_lower:
            answer = ("🗑️ *Сортировка*: обычно выделяют 4 фракции – пластик, стекло, бумага, металл. "
                      "Узнай, какие контейнеры есть в твоём дворе. Для опасных отходов – отдельные пункты.")
        elif "разлагается" in text_lower or "разложение" in text_lower:
            answer = ("⏳ *Время разложения*: пластиковая бутылка ~450 лет, алюминиевая банка ~200–500 лет, "
                      "стекло >1000 лет, батарейка ~100 лет. Лучше сдавать на переработку!")
        elif "начать" in text_lower:
            answer = ("💡 *Как начать*: выбери одну привычку – например, носить с собой эко-сумку, "
                      "или начать собирать пластик. Постепенно добавляй новые шаги. Главное – не пытаться всё сразу.")
        elif "одежд" in text_lower or "вещи" in text_lower:
            answer = ("👕 *Текстиль*: старую одежду можно сдать в контейнеры для вещей, отдать в благотворительные магазины "
                      "или использовать как тряпки. Не выбрасывай в мусор – текстиль почти не разлагается.")
        else:
            answer = ("🌱 *Эко-совет*: старайся уменьшать количество отходов: выбирай товары без упаковки, "
                      "используй многоразовые вещи, сортируй мусор. Если есть конкретный вопрос – спроси, я помогу!")
        
        bot.send_message(chat_id, answer, parse_mode='Markdown', reply_markup=self.get_eco_menu())

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


@bot.message_handler(commands=['eco'])
def eco_handler(message):
    logic.show_eco_info(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('eco_'))
def eco_callback(call):
    chat_id = call.message.chat.id
    if call.data == 'eco_sort':
        logic.eco_sort_tips(chat_id)
    elif call.data == 'eco_start':
        logic.eco_start_tips(chat_id)
    elif call.data == 'eco_decompose':
        logic.eco_decompose_info(chat_id)
    elif call.data == 'eco_tips':
        logic.eco_home_tips(chat_id)
    bot.answer_callback_query(call.id)

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


@bot.message_handler(func=lambda message: True, content_types=['text'])
def eco_question_handler(message):
    
    if message.from_user.id in user_states:
        return
    
    eco_keywords = ['экологи', 'отход', 'мусор', 'сортировк', 'переработк', 'пластик', 'батарейк', 
                    'стекло', 'бумаг', 'картон', 'разлагается', 'разложение', 'начать', 'одежд', 'вещи',
                    'эко', 'эко-', 'эко ', 'сбор', 'контейнер']
    if any(keyword in message.text.lower() for keyword in eco_keywords):
        logic.eco_question_answer(message.chat.id, message.text)
    else:
        
        
        bot.send_message(message.chat.id, "Я бот-помощник. Используй /help для списка команд. Если есть вопросы по экологии – задавай, я отвечу!")

print(" Бот запущен!")
bot.infinity_polling()
