import asyncio
from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from openai import AsyncOpenAI
from config import OPENAI_API_KEY

async def stream_openai_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка запроса с OpenAI streaming mode."""
    response_message = await update.message.reply_text("⌛ Генерирую ответ...")
    collected_chunks = []

    try:
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        # Запуск стриминга ответа
        stream = await client.chat.completions.create(
            model="gpt-4.5",  # Используем модель GPT-4.5
            messages=[{"role": "user", "content": update.message.text}],
            stream=True
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                collected_chunks.append(chunk.choices[0].delta.content)
                # Обновление сообщения каждые 20 чанков или по окончании предложения
                if len(collected_chunks) % 20 == 0 or chunk.choices[0].delta.content.endswith(('.', '!', '?')):
                    current_response = ''.join(collected_chunks)
                    try:
                        await response_message.edit_text(current_response)
                    except Exception:
                        continue
        final_response = ''.join(collected_chunks)
        await response_message.edit_text(final_response)
    except Exception as e:
        await response_message.edit_text(f"❌ Произошла ошибка: {str(e)}")

def setup_handlers(app):
    """Регистрация обработчика для сообщений, инициирующих OpenAI streaming."""
    # Используем группу 3 для самого низкого приоритета
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, stream_openai_response), group=3) 