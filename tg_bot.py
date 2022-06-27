import environs
import telegram

env = environs.Env()
env.read_env()
token = env.str('TG_TOKEN')

chat_id = '@nasa_spacex_images_channel'

bot = telegram.Bot(token=token)
bot.send_message(chat_id=chat_id, text='hello im bot')
