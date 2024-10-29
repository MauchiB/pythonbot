from aiogram.filters import Command
from aiogram import F, Router
from aiogram.types import Message
from adminbot.admin_user import check_admin, admin_append, admin_select, createuser
from db.models import Databaseconnect, show
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import code
import emoji


admin_router = Router()

class admins(StatesGroup):
    admin = State()
    admin2 = State()


@admin_router.message(Command('code'))
async def createad(message: Message, state: FSMContext):
    async with Databaseconnect() as conn:
        check = await check_admin(message.from_user.id, conn)
        if check:
            await message.answer('you are admin')
        else:
    
            await message.answer('code:')
            await state.set_state(admins.admin)

@admin_router.message(Command('nu'))
async def selectuser2(message: Message, state: FSMContext):
    async with Databaseconnect() as conn:
        check = await check_admin(message.from_user.id, conn)  # Await the result
        if check:
            await message.answer('ID user')
            await state.set_state(admins.admin2)
        else:
            await message.answer('you not admin')

@admin_router.message(admins.admin2)
async def selectuser(message: Message, state: FSMContext):
    async with Databaseconnect() as conn:
        user_id = int(message.text)
        if user_id:
            try:
                info = await show(user_id, conn)
                if info:
                    message_text = "\n".join(f"ID: {user_id} \n {i + 1} - {note[2]}" for i, note in enumerate(info))
                    await message.answer(message_text)
                else:
                    await message.answer('ID is not search in database')
            
            except Exception as _ex:
                await print('{_ex}')
    
    await state.clear() 

        
        

@admin_router.message(admins.admin)
async def checks(message: Message, state: FSMContext):
    async with Databaseconnect() as conn:
        if message.text == code:
            await admin_append(message.from_user.id, conn)
            await message.answer('nice you admin')

        else:
            message.answer('error code')
    await state.clear()



@admin_router.message(F.text == '/cu')
async def checkad(message: Message):
    async with Databaseconnect() as conn:
        check = await check_admin(message.from_user.id, conn)
        if check:
            user_data = await admin_select(conn)
            if user_data:
                user_info = f'ID: {user_data["user_id"]} firstname: {user_data["firstname"]} lastname: {user_data["lastname"]}'
                await message.answer(user_info)
            else:
                await message.answer('error table data')
        
        else:
            await message.answer('you not admin')
            