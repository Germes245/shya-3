from aiogram import Bot,Dispatcher,executor,types
from configparser import ConfigParser
config=ConfigParser()
config.read(r'C:\python_projects\Aleksey\token.ini')
token=config['Telegram']['shya_3']
bot=Bot(token)
dp=Dispatcher(bot)
async def shya(_):
    print('main')
@dp.message_handler(commands=('start'))
async def start(message:types.Message):
    print(message)
    await message.answer(text=f'hello {message.from_user.first_name}\nyour id is {message.from_user.id}')

if __name__=='__main__':
    executor.start_polling(dp,on_startup=shya)