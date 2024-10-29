import asyncpg
from config import database, host, username, password, port


class Databaseconnect:
    async def __aenter__(self):
        self.conn = await asyncpg.connect(database=database,
                               user=username,
                               password=password,
                               host=host,
                               port=port)
        return self.conn
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()


async def create_table(conn):
    await conn.execute('''CREATE TABLE IF NOT EXISTS pythonbot(
                    user_id BIGINT PRIMARY KEY,
                    firstname VARCHAR(30),
                    lastname VARCHAR(30),
                    reg BOOLEAN DEFAULT FALSE);''')
    print(f'Table created.')

async def counts(user_id, conn):
    count_note = await conn.fetchrow('''SELECT COUNT(*)
                       FROM python_notes_user
                       WHERE user_id = $1''',
                       user_id)
    return count_note['count']

async def delete_note(user_id, num, conn):
    await conn.execute('''DELETE FROM python_notes_user
                       WHERE user_id = $1 AND notes = $2''',
                       user_id,
                       num)
    

async def create_note(conn):
    await conn.execute('''CREATE TABLE IF NOT EXISTS python_notes_user(
                       user_id_note SERIAL PRIMARY KEY,
                       user_id BIGINT,
                       notes VARCHAR(100),
                       FOREIGN KEY (user_id) REFERENCES pythonbot(user_id));''')
    print('create note table')

async def save_write(user_id, notes, conn):
    await conn.execute('''INSERT INTO python_notes_user(user_id, notes)
                       VALUES($1, $2)''',
                       user_id,
                       notes)
    
async def show(user_id, conn):
    notes = await conn.fetch('''SELECT *
                       FROM python_notes_user
                       WHERE user_id = $1''',
                       user_id)
    return notes

async def create_user(user_id, first, last, conn):
    try:
        await conn.execute('''INSERT INTO pythonbot(user_id, firstname, lastname)
                           VALUES($1, $2, $3)''',
                           user_id,
                           first,
                           last)
        print(f'user {user_id} created')
    except Exception as ex:
        print('user aldery created {user_id} or error  {ex}')

    
async def mainsql():
    async with Databaseconnect() as conn:
        await create_table(conn)
        await create_note(conn)