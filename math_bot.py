import telebot
import re
from sympy import symbols, solve

# 🔑 Токен бота
TOKEN = '8392751195:AAGFtjuRGxQTBMrV8xOsIalLHBhal2ugPMo'
bot = telebot.TeleBot(TOKEN)

# -------------------- /start --------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
<b>🤖 Привет! Я MathBot — твой помощник в решении уравнений!</b>

<b>📝 Что я умею:</b>
• Решать уравнения
• Показывать алгоритм решения
• Приводить примеры

<b>📌 Основные команды:</b>
/solve — решить уравнение  
/algorithm — алгоритмы решений  
/example — показать пример  
/help — инструкция  
/about — информация о боте  

<b>💡 Просто напиши уравнение в чат!</b>
"""
    bot.send_message(message.chat.id, welcome_text, parse_mode="HTML")


# -------------------- /algorithm --------------------
@bot.message_handler(commands=['algorithm'])
def send_algorithm(message):
    text = """
<b>📘 АЛГОРИТМЫ РЕШЕНИЯ УРАВНЕНИЙ</b>

<b>🔹 ЛИНЕЙНОЕ (ax + b = 0)</b>
1️⃣ Раскрыть скобки  
2️⃣ Перенести x в одну сторону  
3️⃣ Числа в другую  
4️⃣ Найти x  

<b>🔹 КВАДРАТНОЕ (ax² + bx + c = 0)</b>
1️⃣ Привести к виду ax² + bx + c  
2️⃣ D = b² - 4ac  
3️⃣ Найти корни по формуле  

<b>🔹 СО СКОБКАМИ</b>
1️⃣ Раскрыть скобки  
2️⃣ Упростить  
3️⃣ Привести к стандартному виду  
4️⃣ Решить  

<b>🔹 ДРОБНОЕ</b>
1️⃣ Найти общий знаменатель  
2️⃣ Умножить уравнение  
3️⃣ Решить  
4️⃣ Проверить ОДЗ  

<b>🎯 Главное — определить тип уравнения!</b>
"""
    bot.send_message(message.chat.id, text, parse_mode="HTML")


# -------------------- /help --------------------
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
<b>📘 КАК ПРАВИЛЬНО ВВОДИТЬ УРАВНЕНИЯ</b>

<b>✅ Правильный формат:</b>
• <code>2x + 5 = 13</code>
• <code>x**2 - 5x + 6 = 0</code>
• <code>3*(x - 2) = 15</code>

<b>⚠️ Важно:</b>
• Используйте <code>*</code> для умножения  
• Используйте <code>**</code> для степени  
• Перед скобками ставьте <code>*</code>
"""
    bot.send_message(message.chat.id, help_text, parse_mode="HTML")


# -------------------- /example --------------------
@bot.message_handler(commands=['example'])
def send_example(message):
    examples_text = """
<b>📚 ПРИМЕРЫ УРАВНЕНИЙ</b>

<b>Линейные:</b>
• <code>2x + 3 = 11</code> → x = 4  

<b>Квадратные:</b>
• <code>x**2 - 5x + 6 = 0</code> → x1 = 2, x2 = 3  
"""
    bot.send_message(message.chat.id, examples_text, parse_mode="HTML")


# -------------------- /about --------------------
@bot.message_handler(commands=['about'])
def send_about(message):
    about_text = """
<b>📖 О БОТЕ</b>

Учебный проект для помощи в математике.
"""
    bot.send_message(message.chat.id, about_text, parse_mode="HTML")


# -------------------- /solve --------------------
@bot.message_handler(commands=['solve'])
def ask_equation(message):
    bot.send_message(
        message.chat.id,
        "🔢 <b>Введите уравнение:</b>\nПример: <code>2*x + 5 = 13</code>",
        parse_mode="HTML"
    )


# -------------------- Обработка текста --------------------
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    text = message.text.strip()

    if '=' in text and 'x' in text.lower():
        process_equation(message)
    elif text.startswith('/'):
        bot.send_message(message.chat.id, "❌ Неизвестная команда. Используйте /help")
    else:
        bot.send_message(
            message.chat.id,
            "🤔 Это не похоже на уравнение.",
            parse_mode="HTML"
        )


# -------------------- Алгоритм для конкретного уравнения --------------------
def get_algorithm(eq_text):
    steps = []

    left, right = eq_text.split('=')

    # Определяем тип уравнения
    if "x**2" in eq_text or "x^2" in eq_text:
        # Квадратное
        steps.append("🔹 Тип: квадратное уравнение")

        steps.append("1️⃣ Переносим всё в одну сторону")
        steps.append(f"{left} - ({right}) = 0")

        steps.append("2️⃣ Приводим к виду ax² + bx + c")
        steps.append("3️⃣ Находим дискриминант: D = b² - 4ac")
        steps.append("4️⃣ Вычисляем корни по формуле")
        steps.append("5️⃣ Записываем ответ")

    else:
        # Линейное
        steps.append("🔹 Тип: линейное уравнение")

        steps.append("1️⃣ Раскрываем скобки (если есть)")
        steps.append("2️⃣ Переносим все x в одну сторону")
        steps.append("3️⃣ Переносим числа в другую сторону")
        steps.append("4️⃣ Делим на коэффициент при x")
        steps.append("5️⃣ Получаем ответ")

    return "\n".join(steps)


# -------------------- Решение --------------------
def process_equation(message):
    try:
        equation = message.text.replace(' ', '')
        solution = solve_equation(equation)
        algorithm = get_algorithm(equation)

        response = f"""
<b>✅ Уравнение решено!</b>

<b>📝 Уравнение:</b>
<code>{equation}</code>

<b>📘 Алгоритм:</b>
{algorithm}

<b>🎯 Ответ:</b>
{solution}
"""
        bot.send_message(message.chat.id, response, parse_mode="HTML")

    except Exception:
        bot.send_message(
            message.chat.id,
            "❌ Не удалось решить уравнение.",
            parse_mode="HTML"
        )


def solve_equation(eq_text):
    x = symbols('x')

    eq_text = eq_text.replace(' ', '')
    eq_text = eq_text.replace('^', '**')

    if '=' not in eq_text:
        raise ValueError("Нет =")

    left, right = eq_text.split('=')

    left = re.sub(r'(\d)(x)', r'\1*\2', left)
    right = re.sub(r'(\d)(x)', r'\1*\2', right)

    left = re.sub(r'(\d)\(', r'\1*(', left)
    right = re.sub(r'(\d)\(', r'\1*(', right)

    left = re.sub(r'\)\(', r')*(', left)
    right = re.sub(r'\)\(', r')*(', right)

    equation = left + "-(" + right + ")"

    solutions = solve(equation, x)

    if not solutions:
        raise ValueError("Нет решений")

    if len(solutions) == 1:
        return f"x = {solutions[0]}"
    else:
        return f"x1 = {solutions[0]}, x2 = {solutions[1]}"


# -------------------- Запуск --------------------
if __name__ == "__main__":
    print("🤖 Бот запущен")
    bot.polling(none_stop=True)