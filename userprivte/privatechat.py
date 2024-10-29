from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from userprivte.keyboards import main, inline
from db.models import Databaseconnect, save_write, show, counts, delete_note, create_user
from adminbot.admin_user import createuser, regstr, checkreg
import emoji


router = Router()

class States(StatesGroup):
    write = State()
    delete = State()
    nameuser = State()
    passuser = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    async with Databaseconnect() as conn:
        await create_user(message.from_user.id,
                          message.from_user.first_name,
                          message.from_user.last_name,
                          conn)
        await message.reply(f'hello {message.from_user.first_name} {emoji.emojize("👋")}', reply_markup=inline)

@router.message(Command('reg'))
async def register(message: Message, state: FSMContext):
    async with Databaseconnect() as conn:
        try:
            bols = await checkreg(message.from_user.id, conn)
            if bols:
                await message.answer(f'you aldery regstation! {emoji.emojize("❤️")}')
                

            else:
                await message.answer('name')
                await state.set_state(States.nameuser)
        except Exception:
            await message.asnwer('error')
        

@router.message(States.nameuser)
async def register(message: Message, state: FSMContext):
    nameuser = message.text
    await state.update_data(name=nameuser)
    await message.answer('password')
    await state.set_state(States.passuser)

@router.message(States.passuser)
async def register(message: Message, state: FSMContext):
    passuser = message.text
    data = await state.get_data()
    nameuser = data.get('name')
    async with Databaseconnect() as conn:
        try:

            await createuser(nameuser, passuser, conn) 
            await regstr(message.from_user.id, conn) # Pass conn here
            await message.answer('you reg!')
            await state.clear()
        
        except Exception:
            await message.answer('такой пользователь с таким ником уже существует введите новое')
            await state.set_state(States.nameuser)


    

@router.callback_query(F.data.startswith('_profile_'))
async def profile(call: CallbackQuery):
    async with Databaseconnect() as conn:
        count = await counts(call.from_user.id, conn)
        value = await checkreg(call.from_user.id, conn)
        await call.message.answer(f' ID: {call.message.from_user.id} {emoji.emojize("🎃")} \n NAME: {call.message.from_user.first_name} \n NOTES: {count} \n REG: {value}')

@router.callback_query(F.data.startswith('_show_'))
async def show_note(call: CallbackQuery):
    async with Databaseconnect() as conn:
        user_id = call.from_user.id
        notes = await show(user_id, conn)
        if notes:
            message_text = "\n".join(f"{i + 1} - {note[2]}" for i, note in enumerate(notes))  # Assuming your tuple has elements [id, notes]
            await call.message.answer(message_text)
        else:
            await call.message.asnwer('нет заметок ' + emoji.emojize("😭"))

@router.callback_query(F.data.startswith('_write_'))
async def inf(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Напишите запись')
    await state.set_state(States.write)

@router.callback_query(F.data.startswith('_delete_note_'))
async def deleted(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите заметку которую хотите удалить ' + emoji.emojize("❌"))
    await state.set_state(States.delete)

@router.message(States.delete)
async def deleted_note(message: Message, state: FSMContext):
    async with Databaseconnect() as conn:
        num = message.text
        user_id = message.from_user.id
        result = await conn.fetchrow('''SELECT 1 FROM python_notes_user
                               WHERE user_id = $1 and notes = $2''',
                               user_id,
                               num)

        if result:
            await delete_note(message.from_user.id, num, conn)
            await message.answer(f'{num} - удалено ' + emoji.emojize("✔️"))
        else:
            await message.answer(f'{num} - не найдено ' + emoji.emojize("❌"))

    await state.clear()
    
    

@router.message(States.write)
async def writer(message: Message, state: FSMContext):
    notes = message.text
    async with Databaseconnect() as conn:
        await save_write(message.from_user.id, notes, conn)

    await message.answer(f'save: {notes}')
    await state.clear()