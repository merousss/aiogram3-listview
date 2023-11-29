# List view using Inline buttons aiogram3

## Preview

## Usage

``` python
import random
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackQuery
from aiogram.filters import Command
from aiogram3_listview import SimpleListView, LV_CallBack
import logging

API_TOKEN = 'TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

data_list1 = random.sample(range(200), 101)

# extra buttons
buttons = {                 # 'text' : 'action'
    'meow': 'send_meow',    # builder.button(text='meow', callback_data=ListView(extra_act='send_meow'))
    'back': 'send_back',
    'text': 'test'
}


lv_1 = SimpleListView(
    data_list=data_list1,
    rows=5,
    columns=5,
    action='first_lv',
    buttons=buttons,
    btns_per_row=3
)


@dp.message(Command(commands=['start']))    # start command
async def start(message: Message):
    await message.answer('Start message', reply_markup = await lv_1.start_lv())


@dp.callback_query(LV_CallBack.filter())    # listview callback
async def lv_callback(
        callback: CallbackQuery,
        callback_data: LV_CallBack
):
    if callback_data.action == 'first_lv':
        index = await lv_1.process_selection(callback, callback_data)

        if index is not None:
            await callback.message.answer(f'index: {index} | item: {data_list1[index]}')

        # handle extra buttons
        if callback_data.extra_act == 'send_meow':
            await callback.message.answer('meow')

        if callback_data.extra_act == 'test':
            await callback.message.answer('❤️')
    await callback.answer()

if __name__ == '__main__':
    try:
        dp.run_polling(bot)
    finally:
        bot.session.close()
        print('Bot stopped.')
```
