from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData, CallbackQuery


class ListView(CallbackData, prefix='listview'):
    action: Optional[str] = None
    move: Optional[str] = None
    page_number: Optional[int] = None
    index: Optional[int] = None
    last_page: Optional[int] = None
    extra_act: Optional[str] = None
    extra_index: Optional[int] = None


class SimpleListView:

    def __init__(self, data_list, rows, columns, action, buttons=None, btns_per_row=1, extra_index=None):
        self.data_list = data_list
        self.rows = rows
        self.columns = columns
        self.action = action
        self.page_number = 1
        self.last_page = 0
        self.buttons = buttons
        self.btns_per_row = btns_per_row
        self.extra_index = extra_index


    async def start_lv(
            self, page_number=1
    ):
        self.page_number = page_number
        switch_builder = InlineKeyboardBuilder()
        builder = InlineKeyboardBuilder()
        buttons = InlineKeyboardBuilder()
        data_per_page = self.data_list[
                        (self.page_number-1)*self.rows*self.columns:
                        self.page_number*self.rows*self.columns
                        ]
        count = len(data_per_page)
        empty_btn = 0
        if len(self.data_list) % (self.rows*self.columns) == 0:
            self.last_page = len(self.data_list)//(self.rows*self.columns)

        else:
            self.last_page = len(self.data_list)//(self.rows*self.columns) + 1

        if count < self.rows*self.columns:
            for i in range(len(data_per_page)):
                builder.button(
                    text=f'{data_per_page[i]}', callback_data=ListView(
                        action=f'{self.action}',
                        page_number=self.page_number,
                        index=i+(self.page_number-1)*self.rows*self.columns,
                        extra_index=self.extra_index
                    ).pack()
                )

                empty_btn += 1

            for i in range(self.rows*self.columns-empty_btn):
                builder.button(
                    text=' ', callback_data=ListView(action='ignore').pack()
                )

        else:
            for i in range(len(data_per_page)):
                builder.button(
                    text=f'{data_per_page[i]}', callback_data=ListView(
                        action=f'{self.action}',
                        page_number=self.page_number,
                        index=i+(self.page_number-1)*self.rows*self.columns,
                        extra_index=self.extra_index
                    ).pack()
                )

        if self.page_number == 1 and self.page_number != self.last_page:
            switch_builder.button(
                text=' ', callback_data=ListView(
                    action=f'{self.action}',
                    move='ignore',
                ).pack()
            )
            switch_builder.button(
                text=f'{self.page_number}/{self.last_page}', callback_data=ListView(
                    action=f'{self.action}',
                    move='to_last_page',
                    extra_index=self.extra_index,
                    last_page=self.last_page
                ).pack()
            )
            switch_builder.button(
                text='>>', callback_data=ListView(
                    action=f'{self.action}',
                    move='forward',
                    page_number=self.page_number+1,
                    extra_index=self.extra_index
                ).pack()
            )

        if self.page_number == 1 and self.page_number == self.last_page:
            switch_builder.button(
                text=' ', callback_data=ListView(
                    move='ignore'
                ).pack()
            )
            switch_builder.button(
                text=f'{self.page_number}/{self.last_page}', callback_data=ListView(
                    move='ignore'
                ).pack()
            )
            switch_builder.button(
                text=' ', callback_data=ListView(
                    move='ignore'
                ).pack()
            )

        if self.page_number != 1 and self.page_number != self.last_page:
            switch_builder.button(
                text='<<', callback_data=ListView(
                    action=f'{self.action}',
                    move='backward',
                    page_number=self.page_number-1,
                    extra_index=self.extra_index
                ).pack()
            )
            switch_builder.button(
                text=f'{self.page_number}/{self.last_page}', callback_data=ListView(
                    action=f'{self.action}',
                    move='to_last_page',
                    extra_index=self.extra_index,
                    last_page=self.last_page
                ).pack()
            )
            switch_builder.button(
                text='>>', callback_data=ListView(
                    action=f'{self.action}',
                    move='forward',
                    page_number=self.page_number+1,
                    extra_index=self.extra_index
                ).pack()
            )
            
        if self.page_number != 1 and self.page_number == self.last_page:
            switch_builder.button(
                text='<<', callback_data=ListView(
                    action=f'{self.action}',
                    move='backward',
                    page_number=self.page_number-1,
                    extra_index=self.extra_index
                ).pack()
            )
            switch_builder.button(
                text=f'{self.page_number}/{self.last_page}', callback_data=ListView(
                    action=f'{self.action}',
                    move='to_first_page',
                    extra_index=self.extra_index
                ).pack()
            )
            switch_builder.button(
                text=' ', callback_data=ListView(
                    move='ignore'
                ).pack()
            )

        builder.adjust(self.columns)
        switch_builder.adjust(3)
        builder.attach(switch_builder)

        # Add extra buttons
        if self.buttons is not None:    
            for i in self.buttons.items():
                buttons.button(
                    text=f'{i[0]}', callback_data=ListView(
                        action=f'{self.action}',
                        extra_act=f'{i[1]}',
                        extra_index=self.extra_index
                    ).pack()
                )
            buttons.adjust(self.btns_per_row)
            builder.attach(buttons)

        return builder.as_markup(resize_keyboard=True)

    async def process_selection(
            self,
            callback: CallbackQuery,
            callback_data: ListView,
    ):
        index = callback_data.index
        # for buttons with no data
        if callback_data.move == 'ignore':
            await callback.answer(cache_time=60)
        # navigate to next page -> editing buttons
        if callback_data.move == 'forward':
            await callback.message.edit_reply_markup(reply_markup=await self.start_lv(callback_data.page_number))
        # navigate to previous page -> editing buttons
        if callback_data.move == 'backward':
            await callback.message.edit_reply_markup(reply_markup=await self.start_lv(callback_data.page_number))
        # navigate to last page -> editing buttons
        if callback_data.move == 'to_last_page':
            await callback.message.edit_reply_markup(reply_markup=await self.start_lv(callback_data.last_page))
        # navigate to first page -> editing buttons
        if callback_data.move == 'to_first_page':
            await callback.message.edit_reply_markup(reply_markup=await self.start_lv(1))

        return index
