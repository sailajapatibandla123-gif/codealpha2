import reflex as rx
from app.states.feed_state import FeedState, SuggestedUser


DISCOVER_USERS: list[dict[str, str]] = [
    {
        "username": "priyanair",
        "display": "Priya Nair",
        "seed": "priyanair",
        "bio": "Design systems & typography",
        "role": "Product Designer",
    },
    {
        "username": "tomwalker",
        "display": "Tom Walker",
        "seed": "tomwalker",
        "bio": "Travel writer · 32 countries",
        "role": "Traveler",
    },
    {
        "username": "sarahkim",
        "display": "Sarah Kim",
        "seed": "sarahkim",
        "bio": "Home cook, curious eater",
        "role": "Chef",
    },
    {
        "username": "devjordan",
        "display": "Jordan Rivera",
        "seed": "devjordan",
        "bio": "Backend engineer · Postgres fan",
        "role": "Engineer",
    },
    {
        "username": "mayachen",
        "display": "Maya Chen",
        "seed": "mayachen",
        "bio": "Nature lover, slow living advocate",
        "role": "Writer",
    },
    {
        "username": "leoharrison",
        "display": "Leo Harrison",
        "seed": "leoharrison",
        "bio": "Photographer capturing city moods",
        "role": "Photographer",
    },
    {
        "username": "aminafall",
        "display": "Amina Fall",
        "seed": "aminafall",
        "bio": "Frontend engineer & accessibility fan",
        "role": "Engineer",
    },
    {
        "username": "yukitanaka",
        "display": "Yuki Tanaka",
        "seed": "yukitanaka",
        "bio": "Illustrator · zines · risograph",
        "role": "Illustrator",
    },
]

TRENDING = [
    {
        "tag": "#DesignSystems",
        "posts": "2.4k posts",
        "desc": "Reusable UI at scale",
    },
    {
        "tag": "#SlowLiving",
        "posts": "1.8k posts",
        "desc": "A calmer daily rhythm",
    },
    {
        "tag": "#RemoteWork",
        "posts": "1.2k posts",
        "desc": "Async, remote, distributed",
    },
    {"tag": "#Ramen", "posts": "864 posts", "desc": "Bowls, broth, and beyond"},
    {
        "tag": "#Kyoto",
        "posts": "512 posts",
        "desc": "Autumn light and old temples",
    },
    {
        "tag": "#WebDev",
        "posts": "3.1k posts",
        "desc": "Craft on the modern web",
    },
]


def _discover_user(user: dict) -> rx.Component:
    is_following = FeedState.following_map[user["username"]].to(bool)
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={user['seed']}",
                class_name="h-14 w-14 rounded-full bg-gray-100 shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    user["display"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"@{user['username']}",
                    class_name="text-xs text-gray-500",
                ),
                rx.el.span(
                    user["role"],
                    class_name="inline-block mt-1.5 px-2 py-0.5 bg-indigo-50 text-indigo-700 text-[10px] font-semibold rounded-full w-fit",
                ),
                class_name="flex-1 min-w-0",
            ),
            class_name="flex items-start gap-3",
        ),
        rx.el.p(
            user["bio"],
            class_name="text-sm text-gray-600 mt-3 leading-relaxed",
        ),
        rx.el.button(
            rx.icon(
                rx.cond(is_following, "check", "plus"),
                class_name="h-4 w-4",
            ),
            rx.el.span(rx.cond(is_following, "Following", "Follow")),
            on_click=lambda: FeedState.toggle_follow(user["username"]),
            type="button",
            aria_label="Follow user",
            class_name=rx.cond(
                is_following,
                "mt-4 flex items-center justify-center gap-1.5 w-full py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold rounded-lg transition-colors",
                "mt-4 flex items-center justify-center gap-1.5 w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm",
            ),
        ),
        class_name="bg-white border border-gray-200 rounded-2xl p-5 hover:border-indigo-200 transition-colors",
    )


def _trending_card(topic: dict) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon("hash", class_name="h-4 w-4 text-indigo-600"),
            class_name="h-9 w-9 rounded-lg bg-indigo-50 flex items-center justify-center shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                topic["tag"],
                class_name="text-sm font-semibold text-gray-900",
            ),
            rx.el.p(
                topic["desc"],
                class_name="text-xs text-gray-500 mt-0.5",
            ),
            class_name="flex-1 min-w-0",
        ),
        rx.el.p(
            topic["posts"],
            class_name="text-xs font-semibold text-gray-500 shrink-0",
        ),
        href="#",
        class_name="flex items-center gap-3 p-3 bg-white border border-gray-200 rounded-xl hover:border-indigo-200 transition-colors",
    )


def discover_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "🌟 Discover",
                    class_name="text-sm font-medium text-indigo-600",
                ),
                rx.el.h1(
                    "Find your community",
                    class_name="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight mt-1",
                ),
                rx.el.p(
                    "New voices, trending topics, and creators to follow.",
                    class_name="text-sm text-gray-600 mt-1",
                ),
            ),
            class_name="mb-6",
        ),
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    "Trending topics",
                    class_name="text-lg font-semibold text-gray-900",
                ),
                rx.icon("trending-up", class_name="h-5 w-5 text-indigo-600"),
                class_name="flex items-center justify-between mb-3",
            ),
            rx.el.div(
                *[_trending_card(t) for t in TRENDING],
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3",
            ),
            class_name="mb-8",
        ),
        rx.el.section(
            rx.el.div(
                rx.el.h2(
                    "People to follow",
                    class_name="text-lg font-semibold text-gray-900",
                ),
                rx.icon("users", class_name="h-5 w-5 text-indigo-600"),
                class_name="flex items-center justify-between mb-3",
            ),
            rx.el.div(
                *[_discover_user(u) for u in DISCOVER_USERS],
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4",
            ),
        ),
        class_name="max-w-6xl mx-auto",
    )
