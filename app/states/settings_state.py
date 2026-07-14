import reflex as rx


class SettingsState(rx.State):
    email_notifications: bool = True
    push_notifications: bool = False
    mentions_notifications: bool = True
    weekly_digest: bool = True
    private_account: bool = False
    show_online: bool = True
    allow_messages_from_anyone: bool = False
    theme_mode: str = "Light"
    language: str = "English"
    accent_color: str = "Indigo"

    @rx.event
    def toggle(self, field: str):
        current = getattr(self, field, False)
        setattr(self, field, not current)

    @rx.event
    def set_theme(self, mode: str):
        self.theme_mode = mode

    @rx.event
    def set_language(self, lang: str):
        self.language = lang

    @rx.event
    def set_accent(self, color: str):
        self.accent_color = color

    @rx.event
    def save(self, form_data: dict):
        yield rx.toast("Settings saved.", duration=2000)
