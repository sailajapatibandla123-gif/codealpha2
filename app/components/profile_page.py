import reflex as rx
from app.states.auth_state import AuthState
from app.states.feed_state import FeedState


def _stat(label: str, value) -> rx.Component:
    return rx.el.div(
        rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        rx.el.p(
            label,
            class_name="text-xs font-medium text-gray-500 uppercase tracking-wide",
        ),
        class_name="text-center",
    )


def _interest_chip(interest: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.span(interest, class_name="text-sm font-medium text-indigo-700"),
        rx.el.button(
            rx.icon("x", class_name="h-3.5 w-3.5"),
            on_click=lambda: AuthState.remove_interest(interest),
            type="button",
            class_name="text-indigo-500 hover:text-indigo-700",
        ),
        class_name="inline-flex items-center gap-1.5 px-3 py-1 bg-indigo-50 border border-indigo-100 rounded-full w-fit",
    )


def profile_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="h-32 sm:h-48 bg-gradient-to-r from-indigo-500 via-indigo-400 to-purple-500 rounded-t-2xl"
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.img(
                        src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.current_user['avatar_seed']}",
                        class_name="h-24 w-24 sm:h-32 sm:w-32 rounded-full bg-white ring-4 ring-white -mt-16 sm:-mt-20",
                    ),
                    rx.el.button(
                        rx.icon("refresh-cw", class_name="h-3.5 w-3.5"),
                        rx.el.span("New avatar"),
                        on_click=AuthState.regenerate_avatar,
                        class_name="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
                    ),
                    class_name="flex items-end justify-between",
                ),
                rx.el.div(
                    rx.el.h1(
                        AuthState.current_user["display_name"],
                        class_name="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight",
                    ),
                    rx.el.p(
                        f"@{AuthState.current_user['username']}",
                        class_name="text-sm text-gray-500 mt-0.5",
                    ),
                    class_name="mt-4",
                ),
                rx.el.p(
                    AuthState.current_user["bio"],
                    class_name="text-sm text-gray-700 mt-3 leading-relaxed",
                ),
                rx.el.div(
                    rx.cond(
                        AuthState.current_user["location"] != "",
                        rx.el.div(
                            rx.icon("map-pin", class_name="h-4 w-4"),
                            rx.el.span(AuthState.current_user["location"]),
                            class_name="flex items-center gap-1.5 text-sm text-gray-600",
                        ),
                        rx.fragment(),
                    ),
                    rx.cond(
                        AuthState.current_user["website"] != "",
                        rx.el.a(
                            rx.icon("link", class_name="h-4 w-4"),
                            rx.el.span(AuthState.current_user["website"]),
                            href=AuthState.current_user["website"],
                            target="_blank",
                            class_name="flex items-center gap-1.5 text-sm text-indigo-600 hover:text-indigo-700",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.div(
                        rx.icon("calendar", class_name="h-4 w-4"),
                        rx.el.span(
                            f"Joined {AuthState.current_user['joined']}"
                        ),
                        class_name="flex items-center gap-1.5 text-sm text-gray-600",
                    ),
                    class_name="flex flex-wrap items-center gap-x-5 gap-y-2 mt-4",
                ),
                rx.el.div(
                    _stat("Posts", AuthState.current_user["posts"]),
                    _stat("Followers", AuthState.current_user["followers"]),
                    _stat("Following", AuthState.current_user["following"]),
                    class_name="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-gray-100",
                ),
                class_name="p-6 sm:p-8",
            ),
            class_name="bg-white border border-gray-200 rounded-2xl overflow-hidden",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Edit profile",
                    class_name="text-lg font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Update your public information.",
                    class_name="text-sm text-gray-500 mt-0.5",
                ),
                class_name="mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Display name",
                            class_name="block text-sm font-semibold text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="display_name",
                            default_value=AuthState.current_user[
                                "display_name"
                            ],
                            key=AuthState.current_user["display_name"],
                            class_name="w-full px-3.5 py-2.5 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Email",
                            class_name="block text-sm font-semibold text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="email",
                            type="email",
                            default_value=AuthState.current_user["email"],
                            key=AuthState.current_user["email"],
                            class_name="w-full px-3.5 py-2.5 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                        ),
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Bio",
                        class_name="block text-sm font-semibold text-gray-700 mb-1.5",
                    ),
                    rx.el.textarea(
                        name="bio",
                        default_value=AuthState.current_user["bio"],
                        key=AuthState.current_user["bio"],
                        rows="3",
                        class_name="w-full px-3.5 py-2.5 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none",
                    ),
                    class_name="mt-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Location",
                            class_name="block text-sm font-semibold text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="location",
                            default_value=AuthState.current_user["location"],
                            key=AuthState.current_user["location"],
                            placeholder="City, Country",
                            class_name="w-full px-3.5 py-2.5 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Website",
                            class_name="block text-sm font-semibold text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="website",
                            default_value=AuthState.current_user["website"],
                            key=AuthState.current_user["website"],
                            placeholder="https://example.com",
                            class_name="w-full px-3.5 py-2.5 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                        ),
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("check", class_name="h-4 w-4"),
                        rx.el.span("Save changes"),
                        type="submit",
                        class_name="flex items-center gap-2 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm",
                    ),
                    class_name="mt-6 flex justify-end",
                ),
                on_submit=AuthState.update_profile,
                reset_on_submit=False,
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 mt-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Following",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        FeedState.following.length().to_string(),
                        class_name="px-2 py-0.5 bg-indigo-50 text-indigo-700 text-xs font-semibold rounded-full",
                    ),
                    class_name="flex items-center gap-2 mb-3",
                ),
                rx.cond(
                    FeedState.following.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            FeedState.following,
                            lambda u: rx.el.div(
                                rx.el.img(
                                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={u}",
                                    class_name="h-8 w-8 rounded-full bg-gray-100",
                                ),
                                rx.el.span(
                                    f"@{u}",
                                    class_name="text-sm font-medium text-gray-700",
                                ),
                                rx.el.button(
                                    "Unfollow",
                                    on_click=lambda: FeedState.toggle_follow(u),
                                    type="button",
                                    class_name="ml-auto px-2.5 py-1 text-xs font-semibold text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                                ),
                                class_name="flex items-center gap-2 py-1.5",
                            ),
                        ),
                        class_name="flex flex-col divide-y divide-gray-100",
                    ),
                    rx.el.p(
                        "You're not following anyone yet.",
                        class_name="text-sm text-gray-500 italic",
                    ),
                ),
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 mt-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Interests",
                    class_name="text-lg font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Add topics you love. They help others discover you.",
                    class_name="text-sm text-gray-500 mt-0.5",
                ),
                class_name="mb-4",
            ),
            rx.cond(
                AuthState.current_user["interests"].length() > 0,
                rx.el.div(
                    rx.foreach(
                        AuthState.current_user["interests"], _interest_chip
                    ),
                    class_name="flex flex-wrap gap-2 mb-4",
                ),
                rx.el.p(
                    "No interests added yet.",
                    class_name="text-sm text-gray-500 italic mb-4",
                ),
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.input(
                        name="interest",
                        placeholder="e.g. Photography",
                        class_name="flex-1 px-3.5 py-2.5 bg-white border border-gray-200 rounded-lg text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                    ),
                    rx.el.button(
                        rx.icon("plus", class_name="h-4 w-4"),
                        rx.el.span("Add"),
                        type="submit",
                        class_name="flex items-center gap-1.5 px-4 py-2.5 bg-gray-900 hover:bg-gray-800 text-white text-sm font-semibold rounded-lg transition-colors",
                    ),
                    class_name="flex gap-2",
                ),
                on_submit=AuthState.add_interest,
                reset_on_submit=True,
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 mt-6",
        ),
        class_name="max-w-3xl mx-auto",
    )
