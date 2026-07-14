import reflex as rx
from app.states.auth_state import AuthState
from app.components.auth_forms import login_form, register_form
from app.components.layout import app_shell
from app.components.profile_page import profile_view
from app.components.feed import feed_view
from app.components.discover import discover_view
from app.components.messages import messages_view
from app.components.settings import settings_view


def index() -> rx.Component:
    return app_shell(feed_view())


def login_page() -> rx.Component:
    return login_form()


def register_page() -> rx.Component:
    return register_form()


def profile_page() -> rx.Component:
    return app_shell(profile_view())


def discover_page() -> rx.Component:
    return app_shell(discover_view())


def messages_page() -> rx.Component:
    return app_shell(messages_view())


def settings_page() -> rx.Component:
    return app_shell(settings_view())


app = rx.App(
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
    theme=rx.theme(appearance="light"),
)
app.add_page(index, route="/", on_load=AuthState.require_auth)
app.add_page(login_page, route="/login", on_load=AuthState.redirect_if_authed)
app.add_page(
    register_page, route="/register", on_load=AuthState.redirect_if_authed
)
app.add_page(profile_page, route="/profile", on_load=AuthState.require_auth)
app.add_page(discover_page, route="/discover", on_load=AuthState.require_auth)
app.add_page(messages_page, route="/messages", on_load=AuthState.require_auth)
app.add_page(settings_page, route="/settings", on_load=AuthState.require_auth)
