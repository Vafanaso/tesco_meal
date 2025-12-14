from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)




def general_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Start"),
                KeyboardButton(text="New menu"),
            ],
            [
                KeyboardButton(text="Menu"),
                KeyboardButton(text="List of products"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Choose an action…",
    )


# def drinks_keyboard(drinks: list[Drink]) -> InlineKeyboardMarkup:
#     rows = [
#         [InlineKeyboardButton(text=d.name, callback_data=f"drink:view:{d.id}")]
#         for d in drinks
#     ]
#
#     if drinks:
#         actions = [
#             InlineKeyboardButton(text="✏️ Rename", callback_data="drink:rename"),
#             InlineKeyboardButton(text="🗑️ Delete", callback_data="drink:delete"),
#         ]
#         rows.append(actions)
#
#     return InlineKeyboardMarkup(inline_keyboard=rows)
#
#
# def drink_action_keyboard(action: str, drinks: list[Drink]) -> InlineKeyboardMarkup:
#     rows = [
#         [InlineKeyboardButton(text=d.name, callback_data=f"drink:{action}:{d.id}")]
#         for d in drinks
#     ]
#     rows.append([InlineKeyboardButton(text="↩️ Back", callback_data="drink:back")])
#     return InlineKeyboardMarkup(inline_keyboard=rows)
#
#
# def drink_manage_keyboard(drink_id: int) -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text="+1", callback_data=f"drink:adjust:{drink_id}:add:1"
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     text="-1", callback_data=f"drink:adjust:{drink_id}:take:1"
#                 ),
#             ],
#             [
#                 InlineKeyboardButton(
#                     text="📜 History", callback_data=f"drink:history:{drink_id}"
#                 )
#             ],
#             [
#                 InlineKeyboardButton(
#                     text="🔄 Refresh", callback_data=f"drink:refresh:{drink_id}"
#                 ),
#                 InlineKeyboardButton(text="↩️ Back", callback_data="drink:back"),
#             ],
#         ]
#     )
#
#
# def delete_confirm_keyboard(drink_id: int) -> InlineKeyboardMarkup:
#     return InlineKeyboardMarkup(
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(
#                     text="✅ Yes, delete",
#                     callback_data=f"drink:delete:confirm:{drink_id}",
#                 )
#             ],
#             [InlineKeyboardButton(text="↩️ Cancel", callback_data="drink:cancel")],
#         ]
#     )
