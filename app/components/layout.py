import reflex as rx
from app.components.navbar import navbar


def app_shell(*content: rx.Component) -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                *content,
                class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10",
            ),
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
    )
