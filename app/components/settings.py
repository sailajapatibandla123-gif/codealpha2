import reflex as rx
from app.states.settings_state import SettingsState
from app.states.auth_state import AuthState


def _toggle_row(
    label: str, description: str, field: str, value
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-semibold text-gray-900"),
            rx.el.p(
                description,
                class_name="text-xs text-gray-500 mt-0.5",
            ),
            class_name="flex-1 min-w-0 pr-4",
        ),
        rx.el.button(
            rx.el.span(
                class_name=rx.cond(
                    value,
                    "block h-5 w-5 bg-white rounded-full shadow-sm transform translate-x-5 transition-transform",
                    "block h-5 w-5 bg-white rounded-full shadow-sm transform translate-x-0.5 transition-transform",
                )
            ),
            on_click=lambda: SettingsState.toggle(field),
            type="button",
            aria_label=label,
            class_name=rx.cond(
                value,
                "relative w-11 h-6 bg-indigo-600 rounded-full transition-colors shrink-0",
                "relative w-11 h-6 bg-gray-300 rounded-full transition-colors shrink-0",
            ),
        ),
        class_name="flex items-center justify-between py-3",
    )


def _section(title: str, icon: str, *children) -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4 text-indigo-600"),
                class_name="h-9 w-9 rounded-lg bg-indigo-50 flex items-center justify-center",
            ),
            rx.el.h2(
                title,
                class_name="text-base font-semibold text-gray-900",
            ),
            class_name="flex items-center gap-3 mb-2",
        ),
        rx.el.div(
            *children,
            class_name="divide-y divide-gray-100",
        ),
        class_name="bg-white border border-gray-200 rounded-2xl p-5 sm:p-6",
    )


def _select_row(
    label: str, description: str, options: list[str], value, on_change
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-semibold text-gray-900"),
            rx.el.p(
                description,
                class_name="text-xs text-gray-500 mt-0.5",
            ),
            class_name="flex-1 min-w-0 pr-4",
        ),
        rx.el.div(
            rx.el.select(
                *[rx.el.option(o, value=o) for o in options],
                value=value,
                on_change=on_change,
                aria_label=label,
                class_name="pr-8 pl-3 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500",
            ),
            rx.icon(
                "chevron-down",
                class_name="h-4 w-4 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
            ),
            class_name="relative",
        ),
        class_name="flex items-center justify-between py-3",
    )


def settings_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "⚙ Settings",
                    class_name="text-sm font-medium text-indigo-600",
                ),
                rx.el.h1(
                    "Preferences",
                    class_name="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight mt-1",
                ),
                rx.el.p(
                    "Manage notifications, privacy, and appearance.",
                    class_name="text-sm text-gray-600 mt-1",
                ),
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.current_user['avatar_seed']}",
                    class_name="h-14 w-14 rounded-full bg-gray-100 shrink-0",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.current_user["display_name"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        AuthState.current_user["email"],
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="flex-1 min-w-0",
                ),
                rx.el.a(
                    "Edit profile",
                    href="/profile",
                    class_name="px-3 py-1.5 text-xs font-semibold text-indigo-600 border border-indigo-200 hover:bg-indigo-50 rounded-lg transition-colors",
                ),
                class_name="flex items-center gap-3 bg-white border border-gray-200 rounded-2xl p-5 mb-4",
            ),
            _section(
                "Notifications",
                "bell",
                _toggle_row(
                    "Email notifications",
                    "Get updates via email",
                    "email_notifications",
                    SettingsState.email_notifications,
                ),
                _toggle_row(
                    "Push notifications",
                    "Receive push alerts on this device",
                    "push_notifications",
                    SettingsState.push_notifications,
                ),
                _toggle_row(
                    "Mentions",
                    "Notify me when someone @mentions me",
                    "mentions_notifications",
                    SettingsState.mentions_notifications,
                ),
                _toggle_row(
                    "Weekly digest",
                    "A summary of activity every Monday",
                    "weekly_digest",
                    SettingsState.weekly_digest,
                ),
            ),
            rx.el.div(class_name="h-4"),
            _section(
                "Privacy",
                "shield",
                _toggle_row(
                    "Private account",
                    "Only followers can see your posts",
                    "private_account",
                    SettingsState.private_account,
                ),
                _toggle_row(
                    "Show online status",
                    "Let others know when you're active",
                    "show_online",
                    SettingsState.show_online,
                ),
                _toggle_row(
                    "Messages from anyone",
                    "Allow non-followers to message you",
                    "allow_messages_from_anyone",
                    SettingsState.allow_messages_from_anyone,
                ),
            ),
            rx.el.div(class_name="h-4"),
            _section(
                "Appearance",
                "palette",
                _select_row(
                    "Theme",
                    "Choose light, dark, or system default",
                    ["Light", "Dark", "System"],
                    SettingsState.theme_mode,
                    SettingsState.set_theme,
                ),
                _select_row(
                    "Accent color",
                    "Highlight color for interactive elements",
                    ["Indigo", "Purple", "Emerald", "Rose"],
                    SettingsState.accent_color,
                    SettingsState.set_accent,
                ),
                _select_row(
                    "Language",
                    "Preferred display language",
                    ["English", "Español", "Français", "日本語"],
                    SettingsState.language,
                    SettingsState.set_language,
                ),
            ),
            rx.el.div(class_name="h-4"),
            _section(
                "Danger zone",
                "triangle-alert",
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Sign out",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "You'll need to sign in again next time.",
                            class_name="text-xs text-gray-500 mt-0.5",
                        ),
                        class_name="flex-1",
                    ),
                    rx.el.button(
                        "Sign out",
                        on_click=AuthState.logout,
                        type="button",
                        class_name="px-3 py-1.5 text-xs font-semibold text-red-600 border border-red-200 hover:bg-red-50 rounded-lg transition-colors",
                    ),
                    class_name="flex items-center justify-between py-3",
                ),
            ),
            class_name="max-w-3xl mx-auto",
        ),
        class_name="",
    )
