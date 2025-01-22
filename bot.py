from playwright.sync_api import sync_playwright
import telebot

API_TOKEN = '7277573409:AAHGUx0Mfh4DB31R8VR4SlT2eA1gy2o9vik'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحبًا! أنا بوت يقدم الفتاوى. اكتب سؤالك، وسأبحث عن الفتوى المناسبة.")

@bot.message_handler(func=lambda message: True)
def get_fatwa(message):
    query = message.text.strip().replace(" ", "+")
    url = f"https://www.e-cfr.org/?s={query}"
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            
            # البحث عن النتائج
            results = page.locator("h2.entry-title a")  # تحديث بناءً على هيكل الصفحة
            if results.count() > 0:
                title = results.nth(0).text_content()
                link = results.nth(0).get_attribute('href')
                bot.send_message(
                    message.chat.id,
                    f"*{title}*\n\n[للقراءة الكاملة اضغط هنا]({link})",
                    parse_mode='Markdown'
                )
            else:
                bot.send_message(message.chat.id, "عذرًا، لم أتمكن من العثور على فتوى ذات صلة بسؤالك.")
            
            browser.close()
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء جلب الفتوى: {e}")

print("Bot is running...")
bot.polling()
