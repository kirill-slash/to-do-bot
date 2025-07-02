from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.keys_tasks import keys_menu, cancellations_task
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
import sqlite3

router = Router()


connection = sqlite3.connect('task.bd')
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Task(
id INTEGER PRIMARY KEY AUTOINCREMENT,  
user_id INTEGER NOT NULL,
task_text TEXT NOT NULL         
)
""")
connection.commit()
connection.close()


class Task(StatesGroup):
    create_task = State()
    name_task = State()
    id_del_task = State()



@router.message(F.text.lower() == "❌ отмена")
async def cancellation(message: Message, state: FSMContext):
    await message.answer("Действие отменено", reply_markup=keys_menu())
    await state.clear()



@router.message(F.text.lower() == "✏️ добавить задачу")
async def add_tasks(message: Message, state: FSMContext):
    text_add_task_1 = """✨ *Давайте создадим задачу!*  

Как вам удобнее её назвать?  
Можете просто написать в чат — что вы хотите сделать.  

Я всё запомню! 😊"""
    await message.answer(text_add_task_1, reply_markup=cancellations_task())
    await state.set_state(Task.create_task)



@router.message(Task.create_task)
async def total_add_task(message: Message, state: FSMContext):
    connection = sqlite3.connect('task.bd')
    cursor = connection.cursor()

    cursor.execute("""
INSERT INTO Task (user_id, task_text) VALUES (?, ?)
""", (message.from_user.id, message.text))

    connection.commit()
    connection.close()

    text_add_task_2 = f'''📌 Отлично! Задача сохранена:

"{message.text}" 😉'''
    await message.answer(text_add_task_2, reply_markup=keys_menu())
    await state.set_state(Task.name_task)

    

@router.message(F.text.lower() == "📃 все задачи")
async def show_task(message: Message):
    text_show_tasks = "📋 *Ваши текущие задачи:*\n"
    connection = sqlite3.connect('task.bd')
    cursor = connection.cursor()

    cursor.execute("""
SELECT task_text FROM Task WHERE user_id = ?
""", (message.from_user.id,))

    list_task = cursor.fetchall() 
    
    if len(list_task) >= 1:
        list_task = list_task[0]
        for i in range(len(list_task)):
            text_show_tasks += f"\n{i+1}. {list_task[i]}"
        await message.answer(text_show_tasks)
    else:
        await message.answer("🎉 У вас пока нет задач!")

    connection.commit()
    connection.close()



@router.message(F.text.lower() == "❌ удалить задачу")
async def del_task(message: Message, state: FSMContext):
    connection = sqlite3.connect('task.bd')
    cursor = connection.cursor()

    cursor.execute("""
SELECT task_text FROM Task WHERE user_id = ?
""", (message.from_user.id,))
    
    list_task = cursor.fetchall()

    if len(list_task) >= 1:
        list_task = list_task[0]

        text_del = """🗑️ *Удаление задачи*
        
Ваши текущие задачи:
"""
        
        for i in range(len(list_task)):
            text_del += f'{i+1}. {list_task[i]}\n'
        text_del += """
Введите номер задачи для удаления:
(или нажмите "Отмена")"""

        await message.answer(text_del, reply_markup=cancellations_task())
        await state.set_state(Task.id_del_task)  

    else:
        await message.answer("🎉 У вас пока нет задач!")



@router.message(Task.id_del_task)
async def del_id(message: Message, state: FSMContext):
    connection = sqlite3.connect('task.bd')
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM Task")
    id_task = cursor.fetchall()

    try:
        cursor.execute("""
DELETE FROM Task WHERE user_id = ? AND id = ?
""", (message.from_user.id, id_task[int(message.text)-1][0]))
        await message.answer("✅ Задача удалена!", reply_markup=keys_menu())
    except:
        await message.answer("⛔ Вы ввели не корректное значение 😢", reply_markup=keys_menu())

    connection.commit()
    connection.close()