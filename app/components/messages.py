import reflex as rx
from app.states.messages_state import MessagesState, Conversation, Message


def _conv_row(conv: Conversation) -> rx.Component:
    is_active = MessagesState.active_id == conv["id"]
    return rx.el.button(
        rx.el.img(
            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={conv['seed']}",
            class_name="h-11 w-11 rounded-full bg-gray-100 shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    conv["display"],
                    class_name="text-sm font-semibold text-gray-900 truncate",
                ),
                rx.el.p(
                    conv["last_time"],
                    class_name="text-[10px] text-gray-500 shrink-0 ml-2",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.p(
                conv["last_message"],
                class_name="text-xs text-gray-500 truncate mt-0.5",
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.cond(
            conv["unread"] > 0,
            rx.el.span(
                conv["unread"].to_string(),
                class_name="h-5 w-5 rounded-full bg-indigo-600 text-white text-[10px] font-bold flex items-center justify-center shrink-0",
            ),
            rx.fragment(),
        ),
        on_click=lambda: MessagesState.select(conv["id"]),
        type="button",
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 p-3 bg-indigo-50 border border-indigo-100 rounded-xl w-full text-left transition-colors",
            "flex items-center gap-3 p-3 hover:bg-gray-50 border border-transparent rounded-xl w-full text-left transition-colors",
        ),
    )


def _message_bubble(msg: Message) -> rx.Component:
    is_me = msg["sender"] == "me"
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                msg["content"],
                class_name="text-sm leading-relaxed whitespace-pre-wrap",
            ),
            rx.el.p(
                msg["time"],
                class_name=rx.cond(
                    is_me,
                    "text-[10px] text-indigo-100 mt-1 text-right",
                    "text-[10px] text-gray-400 mt-1",
                ),
            ),
            class_name=rx.cond(
                is_me,
                "max-w-[75%] px-3.5 py-2.5 bg-indigo-600 text-white rounded-2xl rounded-br-sm",
                "max-w-[75%] px-3.5 py-2.5 bg-gray-100 text-gray-900 rounded-2xl rounded-bl-sm",
            ),
        ),
        class_name=rx.cond(
            is_me,
            "flex justify-end",
            "flex justify-start",
        ),
    )


def _empty_thread() -> rx.Component:
    return rx.el.div(
        rx.icon("message-square", class_name="h-6 w-6 text-gray-300"),
        rx.el.p(
            "No messages yet",
            class_name="text-sm font-semibold text-gray-700 mt-2",
        ),
        rx.el.p(
            "Start the conversation below.",
            class_name="text-xs text-gray-500 mt-1",
        ),
        class_name="flex flex-col items-center justify-center py-16",
    )


def messages_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Messages",
                    class_name="text-2xl font-bold text-gray-900 tracking-tight",
                ),
                rx.cond(
                    MessagesState.total_unread > 0,
                    rx.el.span(
                        MessagesState.total_unread.to_string(),
                        class_name="px-2 py-0.5 bg-indigo-600 text-white text-xs font-bold rounded-full",
                    ),
                    rx.fragment(),
                ),
                class_name="flex items-center gap-2 p-4 border-b border-gray-100",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search conversations...",
                    default_value=MessagesState.search,
                    on_change=MessagesState.set_search.debounce(200),
                    aria_label="Search conversations",
                    class_name="pl-9 pr-3 py-2 w-full bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                ),
                class_name="relative p-3 border-b border-gray-100",
            ),
            rx.el.div(
                rx.cond(
                    MessagesState.filtered_conversations.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            MessagesState.filtered_conversations, _conv_row
                        ),
                        class_name="flex flex-col gap-1 p-2",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "No conversations found.",
                            class_name="text-sm text-gray-500 text-center py-8",
                        ),
                    ),
                ),
                class_name="overflow-y-auto flex-1",
            ),
            class_name="w-full md:w-80 shrink-0 bg-white border border-gray-200 rounded-2xl flex flex-col md:h-[70vh]",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={MessagesState.active_conversation['seed']}",
                    class_name="h-10 w-10 rounded-full bg-gray-100 shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        MessagesState.active_conversation["display"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.div(
                        rx.el.span(
                            class_name="h-1.5 w-1.5 rounded-full bg-green-500"
                        ),
                        rx.el.span(
                            "Active now",
                            class_name="text-xs text-gray-500",
                        ),
                        class_name="flex items-center gap-1.5 mt-0.5",
                    ),
                    class_name="flex-1 min-w-0",
                ),
                rx.el.button(
                    rx.icon("phone", class_name="h-4 w-4"),
                    type="button",
                    aria_label="Call",
                    class_name="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.icon("video", class_name="h-4 w-4"),
                    type="button",
                    aria_label="Video call",
                    class_name="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
                ),
                rx.el.button(
                    rx.icon("info", class_name="h-4 w-4"),
                    type="button",
                    aria_label="Info",
                    class_name="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
                ),
                class_name="flex items-center gap-2 p-4 border-b border-gray-100",
            ),
            rx.el.div(
                rx.cond(
                    MessagesState.active_messages.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            MessagesState.active_messages, _message_bubble
                        ),
                        class_name="flex flex-col gap-2",
                    ),
                    _empty_thread(),
                ),
                class_name="flex-1 overflow-y-auto p-4 bg-gray-50/50",
            ),
            rx.el.form(
                rx.cond(
                    MessagesState.send_error != "",
                    rx.el.p(
                        MessagesState.send_error,
                        class_name="text-xs text-red-600 mb-2",
                    ),
                    rx.fragment(),
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("paperclip", class_name="h-4 w-4"),
                        type="button",
                        aria_label="Attach",
                        class_name="p-2 text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors shrink-0",
                    ),
                    rx.el.input(
                        name="content",
                        placeholder="Type a message...",
                        aria_label="Message content",
                        class_name="flex-1 px-3.5 py-2 bg-gray-50 border border-gray-200 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                    ),
                    rx.el.button(
                        rx.icon("send", class_name="h-4 w-4"),
                        type="submit",
                        aria_label="Send message",
                        class_name="p-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full transition-colors shrink-0 shadow-sm",
                    ),
                    class_name="flex items-center gap-2",
                ),
                on_submit=MessagesState.send,
                reset_on_submit=True,
                class_name="p-4 border-t border-gray-100",
            ),
            class_name="flex-1 min-w-0 bg-white border border-gray-200 rounded-2xl flex flex-col md:h-[70vh]",
        ),
        class_name="flex flex-col md:flex-row gap-4 max-w-6xl mx-auto",
    )
