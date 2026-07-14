import reflex as rx
from app.states.auth_state import AuthState


def _card(icon: str, title: str, desc: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-5 w-5 text-indigo-600"),
            class_name="h-10 w-10 rounded-xl bg-indigo-50 flex items-center justify-center mb-4",
        ),
        rx.el.h3(title, class_name="text-base font-semibold text-gray-900"),
        rx.el.p(desc, class_name="text-sm text-gray-600 mt-1 leading-relaxed"),
        class_name="bg-white border border-gray-200 rounded-2xl p-6 hover:border-indigo-200 transition-colors",
    )


def home_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "👋 Welcome back",
                    class_name="text-sm font-medium text-indigo-600",
                ),
                rx.el.h1(
                    f"Hey, {AuthState.current_user['display_name']}",
                    class_name="text-3xl sm:text-4xl font-bold text-gray-900 tracking-tight mt-1",
                ),
                rx.el.p(
                    "Your feed is warming up. Phase 2 will bring posts, comments, and likes.",
                    class_name="text-sm text-gray-600 mt-2 max-w-xl",
                ),
                class_name="",
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8",
        ),
        rx.el.div(
            _card(
                "pencil",
                "Compose posts",
                "Share updates, thoughts, and moments with your followers.",
            ),
            _card(
                "heart",
                "Like & react",
                "Show love for content that resonates with you.",
            ),
            _card(
                "users",
                "Follow people",
                "Curate a personalized feed by following creators you enjoy.",
            ),
            _card(
                "compass",
                "Discover",
                "Explore trending topics and meet new people in the community.",
            ),
            _card(
                "message-circle",
                "Message",
                "Have private conversations with your connections.",
            ),
            _card(
                "bell",
                "Stay notified",
                "Never miss a mention, comment, or new follower.",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6",
        ),
        class_name="",
    )


def simple_placeholder(title: str, description: str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-indigo-600"),
            class_name="h-14 w-14 rounded-2xl bg-indigo-50 flex items-center justify-center mx-auto",
        ),
        rx.el.h1(
            title,
            class_name="text-2xl font-bold text-gray-900 tracking-tight text-center mt-4",
        ),
        rx.el.p(
            description,
            class_name="text-sm text-gray-600 text-center mt-2 max-w-md mx-auto",
        ),
        class_name="bg-white border border-gray-200 rounded-2xl p-10 sm:p-16 max-w-2xl mx-auto",
    )
