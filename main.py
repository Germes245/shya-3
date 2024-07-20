from aiogram import Bot,Dispatcher,executor,types
from configparser import ConfigParser
from text import COMMANDS
from datetime import datetime
import requests
config=ConfigParser()
config.read(r'C:\python_projects\Aleksey\token.ini')
token=config['Telegram']['shya_3']
wtoken=config['Weather']['api_token']
bot=Bot(token)
dp=Dispatcher(bot)

async def shya(_):
    print('MAIN')
@dp.message_handler(commands=('start'))
async def start(message:types.Message):
    print(message)
    await message.answer(text=f'hello {message.from_user.first_name}\nyour id is {message.from_user.id}')
@dp.message_handler(content_types=["photo"])
async def get_photo(message:types.Message):
    print(message)
    await message.answer(text='this is photo')
    filename=f'photos/{message.photo[-1].file_id}.jpg'
    await message.photo[-1].download(f'photos\\{message.photo[-1].file_id}.jpg')
@dp.message_handler(commands=('help'))
async def help(message:types.Message):
    print(message)
    await message.answer(text=COMMANDS,parse_mode='Markdown')#"_italic_ \*text"

@dp.message_handler(commands=('image'))
async def help(message:types.Message):
    print(message)
    f=open('image.jpeg','rb')
    await message.answer_photo(f)
@dp.message_handler()
async def send_weather(message:types.Message):
    print(message)
    text=message.text.split()
    if text[0]=='/weather':
        city=' '.join(text[1:])
        print(city)
        try:
            dictinary=dict(requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={wtoken}&units=metric').json())
            print(dictinary)
            if int(dictinary['cod'])>=400:
                await message.answer(text=f"{dictinary['cod']} ERROR")
            else:
                worker=dictinary["main"]
                #wind=dictinary['wind']
                weather=dictinary['weather'][0]
                sys=dictinary['sys']
                print(weather['icon'])
                await bot.send_photo(chat_id=message.from_user.id,photo=f'https://openweathermap.org/img/wn/{weather['icon']}@2x.png')
                await message.answer(text=f"it's {weather["main"]}\ndescription - {weather['description']}\n\ntemperature - {worker["temp"]} °C\npressure - {worker["pressure"]} Pa\nthe speed of wind - {dictinary['wind']["speed"]} m/s\n\nsunrise - {datetime.fromtimestamp(sys['sunrise'])}\nsunset - {datetime.fromtimestamp(sys['sunset'])}\nlength of the day - {datetime.fromtimestamp(sys['sunset'])-datetime.fromtimestamp(sys['sunrise'])}")
        except Exception as e:
            print('error-',e)
if __name__=='__main__':
    executor.start_polling(dp,on_startup=shya)