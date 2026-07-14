import reflex as rx
from app.states.auth_state import AuthState
from app.states.messages_state import MessagesState


NAV_LINKS = [
    ("Home", "/", "house"),
    ("Discover", "/discover", "compass"),
    ("Messages", "/messages", "message-circle"),
    ("Profile", "/profile", "user"),
    ("Settings", "/settings", "settings"),
]


def _nav_link(label: str, href: str, icon: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label, class_name="hidden lg:inline"),
        href=href,
        class_name="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 transition-colors",
    )


def _mobile_link(label: str, href: str, icon: str) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-5 w-5"),
        rx.el.span(label),
        href=href,
        class_name="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-gray-700 hover:text-indigo-600 hover:bg-indigo-50 transition-colors",
    )


class NavState(rx.State):
    mobile_open: bool = False

    @rx.event
    def toggle_mobile(self):
        self.mobile_open = not self.mobile_open

    @rx.event
    def close_mobile(self):
        self.mobile_open = False


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("sparkles", class_name="h-5 w-5 text-white"),
                        class_name="h-9 w-9 rounded-xl bg-indigo-600 flex items-center justify-center shadow-sm",
                    ),
                    rx.el.span(
                        "Ripple",
                        class_name="text-lg font-bold text-gray-900 tracking-tight",
                    ),
                    href="/",
                    class_name="flex items-center gap-2",
                ),
                rx.el.div(
                    *[_nav_link(l, h, i) for l, h, i in NAV_LINKS],
                    class_name="hidden md:flex items-center gap-1",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "search",
                            class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                        ),
                        rx.el.input(
                            placeholder="Search...",
                            class_name="pl-9 pr-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm w-56 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-gray-700",
                        ),
                        class_name="relative hidden lg:block",
                    ),
                    rx.el.a(
                        rx.el.img(
                            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.current_user['avatar_seed']}",
                            class_name="h-9 w-9 rounded-full bg-gray-100",
                        ),
                        href="/profile",
                        class_name="hidden md:block",
                    ),
                    rx.el.button(
                        rx.icon("log-out", class_name="h-4 w-4"),
                        rx.el.span("Sign out", class_name="hidden lg:inline"),
                        on_click=AuthState.logout,
                        class_name="hidden md:flex items-center gap-2 px-3 py-2 text-sm font-medium text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                    ),
                    rx.el.button(
                        rx.icon(
                            rx.cond(NavState.mobile_open, "x", "menu"),
                            class_name="h-5 w-5",
                        ),
                        on_click=NavState.toggle_mobile,
                        class_name="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100",
                    ),
                    class_name="flex items-center gap-3",
                ),
                class_name="flex items-center justify-between h-16",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        rx.cond(
            NavState.mobile_open,
            rx.el.div(
                rx.el.div(
                    *[_mobile_link(l, h, i) for l, h, i in NAV_LINKS],
                    rx.el.button(
                        rx.icon("log-out", class_name="h-5 w-5"),
                        rx.el.span("Sign out"),
                        on_click=AuthState.logout,
                        class_name="flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 transition-colors w-full text-left",
                    ),
                    class_name="flex flex-col gap-1 p-4",
                ),
                class_name="md:hidden border-t border-gray-200 bg-white",
            ),
            rx.fragment(),
        ),
        class_name="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-gray-200",
    )
