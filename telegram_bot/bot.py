import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from api_client import ApiClient

# Загрузка переменных окружения
load_dotenv()

# Включение логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена из переменных окружения
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Состояния для разговора
TITLE, DESCRIPTION = range(2)

# Инициализация API клиента
api_client = ApiClient()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при команде /start."""
    user = update.effective_user
    await update.message.reply_text(
        f'Привет, {user.first_name}! Я бот для системы AKFADesk.\n\n'
        f'Используйте /tasks для просмотра задач\n'
        f'Используйте /newtask для создания новой задачи\n'
        f'Используйте /help для просмотра доступных команд'
    )

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с помощью при команде /help."""
    await update.message.reply_text(
        'Доступные команды:\n'
        '/start - начать работу с ботом\n'
        '/help - показать список команд\n'
        '/tasks - показать список всех задач\n'
        '/newtask - создать новую задачу\n'
    )

# Обработчик команды /tasks
async def tasks_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает список всех задач."""
    await update.message.reply_text('Загрузка списка задач...')
    
    tasks = await api_client.get_tasks()
    
    if not tasks:
        await update.message.reply_text('Задачи не найдены. Используйте /newtask для создания новой задачи.')
        return
    
    for task in tasks:
        status = "✅ Выполнено" if task['completed'] else "⏳ В процессе"
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Отметить выполненной" if not task['completed'] else "⏳ Отметить невыполненной", 
                                    callback_data=f"toggle_{task['id']}"),
                InlineKeyboardButton("❌ Удалить", callback_data=f"delete_{task['id']}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🔹 *{task['title']}*\n"
            f"{task['description'] if task['description'] else '-'}\n"
            f"Статус: {status}\n"
            f"ID: {task['id']}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

# Начало создания новой задачи
async def newtask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало процесса создания новой задачи."""
    await update.message.reply_text(
        'Давайте создадим новую задачу!\n'
        'Введите название задачи:'
    )
    return TITLE

# Получение названия задачи
async def title_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет название и запрашивает описание задачи."""
    context.user_data['title'] = update.message.text
    await update.message.reply_text(
        'Отлично! Теперь введите описание задачи (или отправьте "-" для пропуска):'
    )
    return DESCRIPTION

# Получение описания и создание задачи
async def description_step(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Сохраняет описание и создает задачу."""
    description = update.message.text
    title = context.user_data['title']
    
    if description == "-":
        description = None
    
    await update.message.reply_text('Создание задачи...')
    
    task = await api_client.create_task(title, description)
    
    if task:
        await update.message.reply_text(
            f'✅ Задача успешно создана!\n'
            f'Название: {task["title"]}\n'
            f'ID: {task["id"]}'
        )
    else:
        await update.message.reply_text('❌ Ошибка при создании задачи.')
    
    return ConversationHandler.END

# Отмена создания задачи
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Отменяет создание задачи."""
    await update.message.reply_text('Создание задачи отменено.')
    return ConversationHandler.END

# Обработчик кнопок
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатия на кнопки."""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data.startswith('toggle_'):
        task_id = int(data.split('_')[1])
        task = await api_client.get_task(task_id)
        
        if task:
            new_status = not task['completed']
            result = await api_client.update_task(task_id, {'completed': new_status})
            
            if result:
                await query.edit_message_text(
                    text=f"🔹 *{task['title']}*\n"
                        f"{task['description'] if task['description'] else '-'}\n"
                        f"Статус: {'✅ Выполнено' if new_status else '⏳ В процессе'}\n"
                        f"ID: {task['id']}",
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                "✅ Отметить выполненной" if not new_status else "⏳ Отметить невыполненной", 
                                callback_data=f"toggle_{task_id}"),
                            InlineKeyboardButton("❌ Удалить", callback_data=f"delete_{task_id}")
                        ]
                    ]),
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(text=f"❌ Ошибка при обновлении задачи.")
    
    elif data.startswith('delete_'):
        task_id = int(data.split('_')[1])
        success = await api_client.delete_task(task_id)
        
        if success:
            await query.edit_message_text(text=f"✅ Задача с ID {task_id} успешно удалена!")
        else:
            await query.edit_message_text(text=f"❌ Ошибка при удалении задачи с ID {task_id}.")

def main() -> None:
    """Запускает бота."""
    # Создание приложения
    application = Application.builder().token(TOKEN).build()
    
    # Создание обработчика разговора для создания задачи
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('newtask', newtask_command)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, title_step)],
            DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, description_step)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("tasks", tasks_command))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 