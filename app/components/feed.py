import reflex as rx
from app.states.auth_state import AuthState
from app.states.feed_state import FeedState, Post, Comment, SuggestedUser


def _category_pill(category: rx.Var) -> rx.Component:
    is_active = FeedState.active_category == category
    return rx.el.button(
        category,
        on_click=lambda: FeedState.set_category(category),
        class_name=rx.cond(
            is_active,
            "px-3.5 py-1.5 rounded-full text-xs font-semibold bg-indigo-600 text-white transition-colors shrink-0",
            "px-3.5 py-1.5 rounded-full text-xs font-semibold bg-white border border-gray-200 text-gray-700 hover:border-indigo-300 hover:text-indigo-600 transition-colors shrink-0",
        ),
    )


def _composer() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.current_user['avatar_seed']}",
                class_name="h-10 w-10 rounded-full bg-gray-100 shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    AuthState.current_user["display_name"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Share something with your community",
                    class_name="text-xs text-gray-500",
                ),
            ),
            class_name="flex items-center gap-3 mb-4",
        ),
        rx.cond(
            FeedState.compose_error != "",
            rx.el.div(
                rx.icon(
                    "circle-alert", class_name="h-4 w-4 text-red-500 shrink-0"
                ),
                rx.el.p(
                    FeedState.compose_error, class_name="text-sm text-red-700"
                ),
                class_name="flex items-center gap-2 p-2.5 mb-3 bg-red-50 border border-red-100 rounded-lg",
            ),
            rx.fragment(),
        ),
        rx.el.form(
            rx.el.textarea(
                name="content",
                placeholder="What's on your mind?",
                rows="3",
                class_name="w-full px-3.5 py-2.5 bg-gray-50 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "tag",
                            class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none",
                        ),
                        rx.el.select(
                            rx.el.option("Design", value="Design"),
                            rx.el.option("Tech", value="Tech"),
                            rx.el.option("Life", value="Life"),
                            rx.el.option("Travel", value="Travel"),
                            rx.el.option("Food", value="Food"),
                            name="category",
                            default_value="Life",
                            class_name="pl-9 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 appearance-none cursor-pointer focus:outline-none focus:ring-2 focus:ring-indigo-500",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="h-4 w-4 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                    rx.el.button(
                        rx.icon("image", class_name="h-4 w-4"),
                        rx.el.span("Photo", class_name="hidden sm:inline"),
                        type="button",
                        class_name="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("smile", class_name="h-4 w-4"),
                        rx.el.span("Emoji", class_name="hidden sm:inline"),
                        type="button",
                        class_name="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
                    ),
                    class_name="flex items-center gap-2 flex-wrap",
                ),
                rx.el.button(
                    rx.cond(
                        FeedState.is_posting,
                        rx.icon(
                            "loader-circle", class_name="h-4 w-4 animate-spin"
                        ),
                        rx.icon("send", class_name="h-4 w-4"),
                    ),
                    rx.el.span(
                        rx.cond(FeedState.is_posting, "Posting...", "Post")
                    ),
                    type="submit",
                    disabled=FeedState.is_posting,
                    class_name="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white text-sm font-semibold rounded-lg transition-colors shadow-sm",
                ),
                class_name="flex items-center justify-between mt-3 gap-2",
            ),
            on_submit=FeedState.create_post,
            reset_on_submit=True,
        ),
        class_name="bg-white border border-gray-200 rounded-2xl p-5",
    )


def _category_filter() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(FeedState.categories, _category_pill),
            class_name="flex items-center gap-2 overflow-x-auto pb-1",
        ),
        class_name="mt-4",
    )


def _comment_card(comment: Comment) -> rx.Component:
    return rx.el.div(
        rx.el.img(
            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={comment['author_seed']}",
            class_name="h-8 w-8 rounded-full bg-gray-100 shrink-0",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        comment["author_display"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        f"@{comment['author_username']}",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="flex items-center gap-2 flex-wrap",
                ),
                rx.el.p(
                    comment["content"],
                    class_name="text-sm text-gray-800 mt-1 leading-relaxed whitespace-pre-wrap",
                ),
                class_name="bg-gray-50 border border-gray-100 rounded-2xl px-3.5 py-2.5",
            ),
            rx.el.div(
                rx.icon("clock", class_name="h-3 w-3"),
                rx.el.span(comment["created_at"]),
                class_name="flex items-center gap-1 text-xs text-gray-500 mt-1 ml-1",
            ),
            class_name="flex-1 min-w-0",
        ),
        class_name="flex gap-2.5 items-start",
    )


def _comments_section(post: Post) -> rx.Component:
    post_id = post["id"]
    is_open = FeedState.open_comments[post_id].to(bool)
    post_comments = FeedState.comments_by_post[post_id]
    err = FeedState.comment_errors[post_id].to(str)
    return rx.cond(
        is_open,
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src=f"https://api.dicebear.com/9.x/notionists/svg?seed={AuthState.current_user['avatar_seed']}",
                    class_name="h-8 w-8 rounded-full bg-gray-100 shrink-0",
                ),
                rx.el.form(
                    rx.el.input(type="hidden", name="post_id", value=post_id),
                    rx.el.div(
                        rx.el.input(
                            name="content",
                            placeholder="Write a thoughtful comment...",
                            class_name="flex-1 px-3.5 py-2 bg-gray-50 border border-gray-200 rounded-full text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent",
                        ),
                        rx.el.button(
                            rx.icon("send", class_name="h-4 w-4"),
                            type="submit",
                            class_name="p-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full transition-colors shrink-0",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.cond(
                        err != "",
                        rx.el.p(
                            err,
                            class_name="text-xs text-red-600 mt-1.5 ml-1",
                        ),
                        rx.fragment(),
                    ),
                    on_submit=FeedState.add_comment,
                    reset_on_submit=True,
                    class_name="flex-1",
                ),
                class_name="flex gap-2.5 items-start",
            ),
            rx.cond(
                post_comments.length() > 0,
                rx.el.div(
                    rx.foreach(post_comments, _comment_card),
                    class_name="flex flex-col gap-3 mt-4 pl-4 border-l-2 border-gray-100",
                ),
                rx.el.div(
                    rx.icon(
                        "message-square",
                        class_name="h-5 w-5 text-gray-300 mx-auto",
                    ),
                    rx.el.p(
                        "Be the first to comment.",
                        class_name="text-xs text-gray-500 text-center mt-1.5",
                    ),
                    class_name="mt-4 py-4",
                ),
            ),
            class_name="mt-4 pt-4 border-t border-gray-100",
        ),
        rx.fragment(),
    )


def _post_card(post: Post) -> rx.Component:
    post_id = post["id"]
    comment_count = FeedState.comment_count_by_post[post_id].to(int)
    like_count = FeedState.like_count_by_post[post_id].to(int)
    is_liked = FeedState.liked_by_me[post_id].to(bool)
    is_own = AuthState.current_user["username"] == post["author_username"]
    is_following = FeedState.following_map[post["author_username"]].to(bool)
    return rx.el.article(
        rx.el.div(
            rx.el.img(
                src=f"https://api.dicebear.com/9.x/notionists/svg?seed={post['author_seed']}",
                class_name="h-11 w-11 rounded-full bg-gray-100 shrink-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        post["author_display"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.span(
                        f"@{post['author_username']}",
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="flex items-center gap-2 flex-wrap",
                ),
                rx.el.div(
                    rx.icon("clock", class_name="h-3 w-3"),
                    rx.el.span(post["created_at"]),
                    class_name="flex items-center gap-1 text-xs text-gray-500 mt-0.5",
                ),
                class_name="flex-1 min-w-0",
            ),
            rx.el.span(
                post["category"],
                class_name="px-2.5 py-1 bg-indigo-50 text-indigo-700 text-xs font-semibold rounded-full w-fit shrink-0",
            ),
            rx.cond(
                is_own,
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: FeedState.delete_post(post_id),
                    type="button",
                    aria_label="Delete post",
                    class_name="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors shrink-0",
                ),
                rx.el.button(
                    rx.cond(
                        is_following,
                        rx.el.span(
                            "Following", class_name="text-xs font-semibold"
                        ),
                        rx.el.span(
                            "Follow", class_name="text-xs font-semibold"
                        ),
                    ),
                    on_click=lambda: FeedState.toggle_follow(
                        post["author_username"]
                    ),
                    type="button",
                    aria_label="Follow user",
                    class_name=rx.cond(
                        is_following,
                        "px-3 py-1.5 rounded-full bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors shrink-0",
                        "px-3 py-1.5 rounded-full bg-indigo-600 text-white hover:bg-indigo-700 transition-colors shrink-0",
                    ),
                ),
            ),
            class_name="flex items-start gap-3",
        ),
        rx.el.p(
            post["content"],
            class_name="text-[15px] text-gray-800 mt-4 leading-relaxed whitespace-pre-wrap",
        ),
        rx.el.div(
            rx.el.img(
                src=f"https://picsum.photos/seed/{post['image_seed']}/800/450",
                class_name="w-full h-56 sm:h-72 object-cover",
            ),
            class_name="mt-4 rounded-xl overflow-hidden border border-gray-100 bg-gray-50",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(
                    "heart",
                    class_name=rx.cond(
                        is_liked,
                        "h-4 w-4 fill-red-500 text-red-500",
                        "h-4 w-4",
                    ),
                ),
                rx.el.span(
                    like_count.to_string(),
                    class_name="text-xs font-semibold",
                ),
                rx.el.span(
                    "Likes",
                    class_name="text-xs font-semibold hidden sm:inline",
                ),
                on_click=lambda: FeedState.toggle_like(post_id),
                type="button",
                aria_label="Like post",
                class_name=rx.cond(
                    is_liked,
                    "flex items-center gap-1.5 px-3 py-1.5 text-red-600 bg-red-50 rounded-lg transition-colors",
                    "flex items-center gap-1.5 px-3 py-1.5 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                ),
            ),
            rx.el.button(
                rx.icon("message-circle", class_name="h-4 w-4"),
                rx.el.span(
                    rx.cond(comment_count > 0, comment_count.to_string(), "0"),
                    class_name="text-xs font-semibold",
                ),
                rx.el.span(
                    "Comments",
                    class_name="text-xs font-semibold hidden sm:inline",
                ),
                on_click=lambda: FeedState.toggle_comments(post_id),
                type="button",
                aria_label="Show comments",
                class_name="flex items-center gap-1.5 px-3 py-1.5 text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
            ),
            rx.el.button(
                rx.icon("share-2", class_name="h-4 w-4"),
                rx.el.span(
                    "Share", class_name="text-xs font-semibold hidden sm:inline"
                ),
                type="button",
                class_name="flex items-center gap-1.5 px-3 py-1.5 text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
            ),
            rx.el.button(
                rx.icon("bookmark", class_name="h-4 w-4"),
                rx.el.span(
                    "Save", class_name="text-xs font-semibold hidden sm:inline"
                ),
                type="button",
                class_name="flex items-center gap-1.5 px-3 py-1.5 text-gray-600 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors ml-auto",
            ),
            class_name="flex items-center gap-1 mt-4 pt-3 border-t border-gray-100",
        ),
        _comments_section(post),
        class_name="bg-white border border-gray-200 rounded-2xl p-5 sm:p-6",
    )


def _empty_feed() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("inbox", class_name="h-6 w-6 text-indigo-600"),
            class_name="h-14 w-14 rounded-2xl bg-indigo-50 flex items-center justify-center mx-auto",
        ),
        rx.el.h3(
            "No posts here yet",
            class_name="text-base font-semibold text-gray-900 text-center mt-4",
        ),
        rx.el.p(
            "Try a different category, or be the first to share something.",
            class_name="text-sm text-gray-600 text-center mt-1",
        ),
        class_name="bg-white border border-gray-200 rounded-2xl p-10",
    )


def _suggested_user_card(user: SuggestedUser) -> rx.Component:
    is_following = FeedState.following_map[user["username"]].to(bool)
    return rx.el.div(
        rx.el.img(
            src=f"https://api.dicebear.com/9.x/notionists/svg?seed={user['seed']}",
            class_name="h-10 w-10 rounded-full bg-gray-100 shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                user["display"],
                class_name="text-sm font-semibold text-gray-900 truncate",
            ),
            rx.el.p(user["bio"], class_name="text-xs text-gray-500 truncate"),
            class_name="flex-1 min-w-0",
        ),
        rx.el.button(
            rx.cond(is_following, "Following", "Follow"),
            on_click=lambda: FeedState.toggle_follow(user["username"]),
            type="button",
            aria_label="Follow user",
            class_name=rx.cond(
                is_following,
                "px-3 py-1.5 text-xs font-semibold text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors shrink-0",
                "px-3 py-1.5 text-xs font-semibold text-indigo-600 border border-indigo-200 hover:bg-indigo-50 rounded-lg transition-colors shrink-0",
            ),
        ),
        class_name="flex items-center gap-3",
    )


def _trending_row(topic: dict) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.p(
                topic["tag"], class_name="text-sm font-semibold text-gray-900"
            ),
            rx.el.p(topic["posts"], class_name="text-xs text-gray-500 mt-0.5"),
        ),
        rx.icon("arrow-up-right", class_name="h-4 w-4 text-gray-400"),
        href="#",
        class_name="flex items-center justify-between py-2 px-2 -mx-2 hover:bg-gray-50 rounded-lg transition-colors",
    )


def _right_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Your activity",
                    class_name="text-sm font-bold text-gray-900",
                ),
                rx.icon("activity", class_name="h-4 w-4 text-indigo-600"),
                class_name="flex items-center justify-between mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        FeedState.total_posts.to_string(),
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Posts", class_name="text-xs text-gray-500 font-medium"
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.p(
                        FeedState.total_comments.to_string(),
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Comments",
                        class_name="text-xs text-gray-500 font-medium",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.current_user["followers"].to_string(),
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Followers",
                        class_name="text-xs text-gray-500 font-medium",
                    ),
                    class_name="flex-1",
                ),
                class_name="flex gap-2",
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-5",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Who to follow",
                    class_name="text-sm font-bold text-gray-900",
                ),
                rx.icon("user-plus", class_name="h-4 w-4 text-indigo-600"),
                class_name="flex items-center justify-between mb-4",
            ),
            rx.el.div(
                rx.foreach(FeedState.suggested_users, _suggested_user_card),
                class_name="flex flex-col gap-4",
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-5 mt-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Trending", class_name="text-sm font-bold text-gray-900"
                ),
                rx.icon("trending-up", class_name="h-4 w-4 text-indigo-600"),
                class_name="flex items-center justify-between mb-2",
            ),
            rx.el.div(
                rx.foreach(FeedState.trending_topics, _trending_row),
                class_name="flex flex-col",
            ),
            class_name="bg-white border border-gray-200 rounded-2xl p-5 mt-4",
        ),
        rx.el.p(
            "© Ripple · Built with care",
            class_name="text-xs text-gray-400 text-center mt-4",
        ),
        class_name="hidden lg:block w-80 shrink-0",
    )


def feed_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "👋 Welcome back",
                    class_name="text-sm font-medium text-indigo-600",
                ),
                rx.el.h1(
                    f"Hey, {AuthState.current_user['display_name']}",
                    class_name="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight mt-1",
                ),
                rx.el.p(
                    "Here's what your community is sharing today.",
                    class_name="text-sm text-gray-600 mt-1",
                ),
                class_name="mb-5",
            ),
            _composer(),
            _category_filter(),
            rx.cond(
                FeedState.filtered_posts.length() > 0,
                rx.el.div(
                    rx.foreach(FeedState.filtered_posts, _post_card),
                    class_name="flex flex-col gap-4 mt-4",
                ),
                rx.el.div(_empty_feed(), class_name="mt-4"),
            ),
            class_name="flex-1 min-w-0 max-w-2xl",
        ),
        _right_sidebar(),
        class_name="flex gap-6 items-start",
    )
