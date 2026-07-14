import reflex as rx
from typing import TypedDict
from datetime import datetime, timedelta
import uuid
import logging


class Comment(TypedDict):
    id: str
    post_id: str
    author_username: str
    author_display: str
    author_seed: str
    content: str
    created_at: str
    timestamp: float


class Post(TypedDict):
    id: str
    author_username: str
    author_display: str
    author_seed: str
    content: str
    category: str
    created_at: str
    timestamp: float
    image_seed: str


CATEGORIES: list[str] = ["All", "Design", "Tech", "Life", "Travel", "Food"]


def _fmt_time(dt: datetime) -> str:
    return dt.strftime("%b %d, %Y · %I:%M %p")


def _seed_posts() -> list[Post]:
    now = datetime.now()
    seed = [
        {
            "author_username": "alexdoe",
            "author_display": "Alex Doe",
            "author_seed": "alexdoe",
            "content": "Just shipped a redesign of our onboarding flow. Small details matter — a well-timed tooltip made conversion jump 12%. ✨",
            "category": "Design",
            "delta": timedelta(minutes=12),
            "image_seed": "design-onboarding",
        },
        {
            "author_username": "mayachen",
            "author_display": "Maya Chen",
            "author_seed": "mayachen",
            "content": "Weekend hike through the redwoods was exactly the reset I needed. Nature > notifications, always.",
            "category": "Life",
            "delta": timedelta(hours=2, minutes=30),
            "image_seed": "redwoods-hike",
        },
        {
            "author_username": "devjordan",
            "author_display": "Jordan Rivera",
            "author_seed": "devjordan",
            "content": "Hot take: the best programming skill isn't syntax — it's writing self-documenting code so future-you doesn't cry at 2am. 🧠",
            "category": "Tech",
            "delta": timedelta(hours=5),
            "image_seed": "code-editor",
        },
        {
            "author_username": "sarahkim",
            "author_display": "Sarah Kim",
            "author_seed": "sarahkim",
            "content": "Made handmade ramen from scratch tonight. Twelve hours for the broth, four minutes to devour it. Worth every second.",
            "category": "Food",
            "delta": timedelta(hours=8),
            "image_seed": "ramen-bowl",
        },
        {
            "author_username": "tomwalker",
            "author_display": "Tom Walker",
            "author_seed": "tomwalker",
            "content": "Kyoto in the fall is unreal. The light through the maples at Tofuku-ji felt like walking through a painting. 🍁",
            "category": "Travel",
            "delta": timedelta(hours=14),
            "image_seed": "kyoto-autumn",
        },
        {
            "author_username": "priyanair",
            "author_display": "Priya Nair",
            "author_seed": "priyanair",
            "content": "Finally cracked a design system that scales across three product lines. Component tokens > component sprawl. Sharing my write-up soon.",
            "category": "Design",
            "delta": timedelta(days=1, hours=1),
            "image_seed": "design-system",
        },
        {
            "author_username": "devjordan",
            "author_display": "Jordan Rivera",
            "author_seed": "devjordan",
            "content": "TIL: Postgres full-text search gets you 90% of the way to a search feature without adding Elasticsearch. Sometimes boring is beautiful.",
            "category": "Tech",
            "delta": timedelta(days=1, hours=6),
            "image_seed": "postgres-tech",
        },
        {
            "author_username": "mayachen",
            "author_display": "Maya Chen",
            "author_seed": "mayachen",
            "content": "Reminder: rest is not a reward for finishing your work. It's part of the work. 🌱",
            "category": "Life",
            "delta": timedelta(days=2),
            "image_seed": "peaceful-morning",
        },
    ]
    posts: list[Post] = []
    for s in seed:
        dt = now - s["delta"]
        posts.append(
            Post(
                id=str(uuid.uuid4()),
                author_username=s["author_username"],
                author_display=s["author_display"],
                author_seed=s["author_seed"],
                content=s["content"],
                category=s["category"],
                created_at=_fmt_time(dt),
                timestamp=dt.timestamp(),
                image_seed=s["image_seed"],
            )
        )
    return posts


def _seed_comments(posts: list[Post]) -> list[Comment]:
    now = datetime.now()
    if not posts:
        return []
    templates = [
        (
            "mayachen",
            "Maya Chen",
            "mayachen",
            "This is beautiful — thanks for sharing!",
            timedelta(minutes=5),
        ),
        (
            "devjordan",
            "Jordan Rivera",
            "devjordan",
            "Totally agree. Small details compound.",
            timedelta(minutes=20),
        ),
        (
            "sarahkim",
            "Sarah Kim",
            "sarahkim",
            "Adding this to my weekend list 😍",
            timedelta(hours=1),
        ),
        (
            "alexdoe",
            "Alex Doe",
            "alexdoe",
            "Love the perspective here. Bookmarking.",
            timedelta(hours=3),
        ),
    ]
    comments: list[Comment] = []
    for i, post in enumerate(posts[:4]):
        for j, (u, dn, sd, txt, td) in enumerate(templates[: (i % 3) + 1]):
            dt = now - td - timedelta(minutes=j * 3)
            comments.append(
                Comment(
                    id=str(uuid.uuid4()),
                    post_id=post["id"],
                    author_username=u,
                    author_display=dn,
                    author_seed=sd,
                    content=txt,
                    created_at=_fmt_time(dt),
                    timestamp=dt.timestamp(),
                )
            )
    return comments


_INITIAL_POSTS = _seed_posts()
_INITIAL_COMMENTS = _seed_comments(_INITIAL_POSTS)


class SuggestedUser(TypedDict):
    username: str
    display: str
    seed: str
    bio: str


SUGGESTED_USERS: list[SuggestedUser] = [
    {
        "username": "priyanair",
        "display": "Priya Nair",
        "seed": "priyanair",
        "bio": "Design systems & typography",
    },
    {
        "username": "tomwalker",
        "display": "Tom Walker",
        "seed": "tomwalker",
        "bio": "Travel writer · 32 countries",
    },
    {
        "username": "sarahkim",
        "display": "Sarah Kim",
        "seed": "sarahkim",
        "bio": "Home cook, curious eater",
    },
    {
        "username": "devjordan",
        "display": "Jordan Rivera",
        "seed": "devjordan",
        "bio": "Backend engineer @ Postgres fan",
    },
]

TRENDING_TOPICS: list[dict[str, str]] = [
    {"tag": "#DesignSystems", "posts": "2.4k posts"},
    {"tag": "#SlowLiving", "posts": "1.8k posts"},
    {"tag": "#RemoteWork", "posts": "1.2k posts"},
    {"tag": "#Ramen", "posts": "864 posts"},
    {"tag": "#Kyoto", "posts": "512 posts"},
]


_INITIAL_LIKES: dict[str, list[str]] = {
    _INITIAL_POSTS[i]["id"]: [
        u
        for u in [
            "mayachen",
            "devjordan",
            "sarahkim",
            "tomwalker",
            "priyanair",
        ][: (i % 4) + 1]
    ]
    for i in range(len(_INITIAL_POSTS))
}

_INITIAL_FOLLOWING: list[str] = ["mayachen", "devjordan"]


class FeedState(rx.State):
    posts: list[Post] = _INITIAL_POSTS
    comments: list[Comment] = _INITIAL_COMMENTS
    active_category: str = "All"
    compose_error: str = ""
    comment_errors: dict[str, str] = {}
    open_comments: dict[str, bool] = {}
    likes_by_post: dict[str, list[str]] = _INITIAL_LIKES
    following: list[str] = _INITIAL_FOLLOWING
    is_posting: bool = False

    @rx.var
    def categories(self) -> list[str]:
        return CATEGORIES

    @rx.var
    def filtered_posts(self) -> list[Post]:
        if self.active_category == "All":
            return sorted(
                self.posts, key=lambda p: p["timestamp"], reverse=True
            )
        return sorted(
            [p for p in self.posts if p["category"] == self.active_category],
            key=lambda p: p["timestamp"],
            reverse=True,
        )

    @rx.var
    def total_posts(self) -> int:
        return len(self.posts)

    @rx.var
    def total_comments(self) -> int:
        return len(self.comments)

    @rx.var
    def comments_by_post(self) -> dict[str, list[Comment]]:
        result: dict[str, list[Comment]] = {}
        for c in sorted(self.comments, key=lambda x: x["timestamp"]):
            result.setdefault(c["post_id"], []).append(c)
        return result

    @rx.var
    def comment_count_by_post(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for c in self.comments:
            counts[c["post_id"]] = counts.get(c["post_id"], 0) + 1
        return counts

    @rx.var
    def suggested_users(self) -> list[SuggestedUser]:
        return SUGGESTED_USERS

    @rx.var
    def trending_topics(self) -> list[dict[str, str]]:
        return TRENDING_TOPICS

    @rx.var
    def like_count_by_post(self) -> dict[str, int]:
        return {pid: len(users) for pid, users in self.likes_by_post.items()}

    @rx.var
    async def liked_by_me(self) -> dict[str, bool]:
        user = await self._resolve_current_user()
        me = user.get("username", "")
        return {pid: (me in users) for pid, users in self.likes_by_post.items()}

    @rx.var
    async def following_map(self) -> dict[str, bool]:
        return {u: True for u in self.following}

    @rx.var
    def total_likes(self) -> int:
        return sum(len(v) for v in self.likes_by_post.values())

    @rx.event
    def set_category(self, category: str):
        self.active_category = category

    @rx.event
    async def toggle_like(self, post_id: str):
        user = await self._resolve_current_user()
        me = user.get("username", "")
        if not me:
            return
        current = list(self.likes_by_post.get(post_id, []))
        if me in current:
            current.remove(me)
        else:
            current.append(me)
        new_map = dict(self.likes_by_post)
        new_map[post_id] = current
        self.likes_by_post = new_map

    @rx.event
    def toggle_follow(self, username: str):
        if not username:
            return
        if username in self.following:
            self.following = [u for u in self.following if u != username]
            yield rx.toast(f"Unfollowed @{username}", duration=2000)
        else:
            self.following = self.following + [username]
            yield rx.toast(f"Now following @{username}", duration=2000)

    @rx.event
    def toggle_comments(self, post_id: str):
        self.open_comments[post_id] = not self.open_comments.get(post_id, False)

    async def _resolve_current_user(self) -> dict:
        from app.states.auth_state import AuthState, DEFAULT_USER

        try:
            auth = await self.get_state(AuthState)
            user = auth.current_user
            if user and user.get("username"):
                return dict(user)
            username = getattr(auth, "current_username", "") or ""
            if username:
                for u in auth.users:
                    if u["username"] == username:
                        return dict(u)
            if auth.users:
                return dict(auth.users[0])
        except Exception:
            logging.exception("Unexpected error")
        return dict(DEFAULT_USER)

    @rx.event
    async def create_post(self, form_data: dict):
        self.compose_error = ""
        content = (form_data.get("content") or "").strip()
        category = (form_data.get("category") or "Life").strip()
        if not content:
            self.compose_error = "Say something before posting."
            return
        if len(content) > 500:
            self.compose_error = "Posts must be 500 characters or less."
            return
        if category not in CATEGORIES or category == "All":
            category = "Life"

        user = await self._resolve_current_user()
        if not user.get("username"):
            self.compose_error = "You must be signed in to post."
            return
        self.is_posting = True
        yield
        now = datetime.now()
        new_post = Post(
            id=str(uuid.uuid4()),
            author_username=user["username"],
            author_display=user.get("display_name") or user["username"],
            author_seed=user.get("avatar_seed") or user["username"],
            content=content,
            category=category,
            created_at=_fmt_time(now),
            timestamp=now.timestamp(),
            image_seed=f"post-{uuid.uuid4().hex[:8]}",
        )
        self.posts.append(new_post)
        new_likes = dict(self.likes_by_post)
        new_likes[new_post["id"]] = []
        self.likes_by_post = new_likes
        self.is_posting = False
        yield rx.toast("Post published!", duration=2500)

    @rx.event
    async def add_comment(self, form_data: dict):
        post_id = (form_data.get("post_id") or "").strip()
        content = (form_data.get("content") or "").strip()
        errs = dict(self.comment_errors)
        if not post_id:
            return
        if not content:
            errs[post_id] = "Comment cannot be empty."
            self.comment_errors = errs
            return
        if len(content) > 300:
            errs[post_id] = "Comments must be 300 characters or less."
            self.comment_errors = errs
            return
        errs.pop(post_id, None)
        self.comment_errors = errs

        user = await self._resolve_current_user()
        if not user.get("username"):
            return
        now = datetime.now()
        self.comments.append(
            Comment(
                id=str(uuid.uuid4()),
                post_id=post_id,
                author_username=user["username"],
                author_display=user.get("display_name") or user["username"],
                author_seed=user.get("avatar_seed") or user["username"],
                content=content,
                created_at=_fmt_time(now),
                timestamp=now.timestamp(),
            )
        )
        opens = dict(self.open_comments)
        opens[post_id] = True
        self.open_comments = opens

    @rx.event
    def delete_post(self, post_id: str):
        self.posts = [p for p in self.posts if p["id"] != post_id]
        self.comments = [c for c in self.comments if c["post_id"] != post_id]
        new_likes = {
            k: v for k, v in self.likes_by_post.items() if k != post_id
        }
        self.likes_by_post = new_likes
