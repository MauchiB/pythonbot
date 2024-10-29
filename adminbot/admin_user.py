from db.models import Databaseconnect


async def admin_create(conn):
    await conn.execute('''CREATE TABLE IF NOT EXISTS admin_user(
                            admin_id SERIAL PRIMARY KEY,
                            user_id BIGINT UNIQUE,
                            FOREIGN KEY (user_id) REFERENCES pythonbot(user_id))''')
    
async def reg_user(conn):
    await conn.execute('''CREATE TABLE IF NOT EXISTS reg_user(
                        username VARCHAR(20) PRIMARY KEY,
                        password_user VARCHAR(30) NOT NULL)''')
    
async def admin_append(user_id, conn):
    await conn.execute('''INSERT INTO admin_user(user_id)
                       VALUES($1)''',
                       user_id)
    
async def regstr(user_id, conn):
    await conn.execute('''UPDATE pythonbot
                       SET reg = TRUE
                       WHERE user_id = $1''',
                       user_id)
    
async def check_admin(user_id, conn):
    resultad = await conn.fetchrow('''SELECT * FROM admin_user
                       WHERE user_id = $1''',
                       user_id)
    return bool(resultad)

async def checkreg(user_id, conn):
    bools = await conn.fetchrow('''SELECT reg FROM pythonbot
                           WHERE user_id = $1''',
                           user_id)
    if bools and bools[0]:
        return True
        
    else:
        return False

async def admin_select(conn):
    select = await conn.fetchrow('''SELECT * FROM pythonbot''')
    return select
    

async def createuser(user_name, user_pass, conn):
    await conn.execute('''INSERT INTO reg_user(username, password_user)
                       VALUES($1, $2)''',
                       user_name,
                       user_pass) 


async def adminsql():
    async with Databaseconnect() as conn:
        await admin_create(conn)
        await reg_user(conn)