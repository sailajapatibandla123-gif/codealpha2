import reflex as rx
from app.states.auth_state import AuthState


def _brand_header(title: str, subtitle: str) -> rx.Component:
    return rx.el.div(
        rx.el.a(
            rx.el.div(
                rx.icon("sparkles", class_name="h-6 w-6 text-white"),
                class_name="h-12 w-12 rounded-2xl bg-indigo-600 flex items-center justify-center shadow-sm mx-auto",
            ),
            href="/",
        ),
        rx.el.h1(
            title,
            class_name="mt-6 text-2xl font-bold text-gray-900 text-center tracking-tight",
        ),
        rx.el.p(subtitle, class_name="mt-2 text-sm text-gray-600 text-center"),
        class_name="mb-8",
    )


def _labeled_input(
    label: str, name: str, type_: str = "text", placeholder: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label, class_name="block text-sm font-semibold text-gray-700 mb-1.5"
        ),
        rx.el.input(
            name=name,
            type=type_,
            placeholder=placeholder,
            class_name="w-full px-3.5 py-2.5 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all",
        ),
        class_name="mb-4",
    )


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            _brand_header("Welcome back", "Sign in to continue to Ripple"),
            rx.cond(
                AuthState.login_error != "",
                rx.el.div(
                    rx.icon(
                        "circle-alert",
                        class_name="h-4 w-4 text-red-500 shrink-0",
                    ),
                    rx.el.p(
                        AuthState.login_error, class_name="text-sm text-red-700"
                    ),
                    class_name="flex items-center gap-2 p-3 mb-4 bg-red-50 border border-red-100 rounded-lg",
                ),
                rx.fragment(),
            ),
            rx.el.form(
                _labeled_input("Username", "username", "text", "your_username"),
                _labeled_input("Password", "password", "password", "••••••••"),
                rx.el.button(
                    "Sign in",
                    type="submit",
                    class_name="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm",
                ),
                on_submit=AuthState.login,
                reset_on_submit=False,
            ),
            rx.el.div(
                rx.el.div(class_name="flex-1 h-px bg-gray-200"),
                rx.el.span("or", class_name="text-xs text-gray-500 px-3"),
                rx.el.div(class_name="flex-1 h-px bg-gray-200"),
                class_name="flex items-center my-6",
            ),
            rx.el.p(
                "Don't have an account? ",
                rx.el.a(
                    "Create one",
                    href="/register",
                    class_name="text-indigo-600 hover:text-indigo-700 font-semibold",
                ),
                class_name="text-sm text-gray-600 text-center",
            ),
            rx.el.div(
                rx.el.p(
                    "Try demo:",
                    class_name="text-xs font-semibold text-gray-500 mb-1",
                ),
                rx.el.p(
                    "Username: alexdoe",
                    class_name="text-xs text-gray-600 font-mono",
                ),
                rx.el.p(
                    "Password: password123",
                    class_name="text-xs text-gray-600 font-mono",
                ),
                class_name="mt-6 p-3 bg-gray-50 border border-gray-200 rounded-lg",
            ),
            class_name="w-full max-w-md bg-white border border-gray-200 rounded-2xl p-8 shadow-sm",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-50 p-4",
    )


def register_form() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            _brand_header(
                "Create your account", "Join Ripple and start connecting"
            ),
            rx.cond(
                AuthState.register_error != "",
                rx.el.div(
                    rx.icon(
                        "circle-alert",
                        class_name="h-4 w-4 text-red-500 shrink-0",
                    ),
                    rx.el.p(
                        AuthState.register_error,
                        class_name="text-sm text-red-700",
                    ),
                    class_name="flex items-center gap-2 p-3 mb-4 bg-red-50 border border-red-100 rounded-lg",
                ),
                rx.fragment(),
            ),
            rx.el.form(
                _labeled_input(
                    "Display name", "display_name", "text", "Alex Doe"
                ),
                _labeled_input("Username", "username", "text", "alexdoe"),
                _labeled_input("Email", "email", "email", "you@example.com"),
                _labeled_input(
                    "Password", "password", "password", "At least 6 characters"
                ),
                _labeled_input(
                    "Confirm password",
                    "confirm_password",
                    "password",
                    "••••••••",
                ),
                rx.el.button(
                    "Create account",
                    type="submit",
                    class_name="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm",
                ),
                on_submit=AuthState.register,
                reset_on_submit=False,
            ),
            rx.el.p(
                "Already have an account? ",
                rx.el.a(
                    "Sign in",
                    href="/login",
                    class_name="text-indigo-600 hover:text-indigo-700 font-semibold",
                ),
                class_name="text-sm text-gray-600 text-center mt-6",
            ),
            class_name="w-full max-w-md bg-white border border-gray-200 rounded-2xl p-8 shadow-sm",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-50 p-4 py-10",
    )
