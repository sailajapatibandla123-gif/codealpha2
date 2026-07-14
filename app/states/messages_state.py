import reflex as rx
from typing import TypedDict
from datetime import datetime, timedelta
import uuid


class Message(TypedDict):
    id: str
    sender: str
    content: str
    time: str
    timestamp: float


class Conversation(TypedDict):
    id: str
    username: str
    display: str
    seed: str
    last_message: str
    last_time: str
    unread: int


def _fmt(dt: datetime) -> str:
    return dt.strftime("%I:%M %p")


def _seed_conversations() -> list[Conversation]:
    now = datetime.now()
    data = [
        (
            "mayachen",
            "Maya Chen",
            "mayachen",
            "Loved your onboarding post ✨",
            5,
            2,
        ),
        (
            "devjordan",
            "Jordan Rivera",
            "devjordan",
            "Sending you the repo link soon.",
            25,
            0,
        ),
        (
            "sarahkim",
            "Sarah Kim",
            "sarahkim",
            "That ramen looked incredible!",
            60,
            1,
        ),
        (
            "tomwalker",
            "Tom Walker",
            "tomwalker",
            "Kyoto tips coming your way.",
            180,
            0,
        ),
        (
            "priyanair",
            "Priya Nair",
            "priyanair",
            "Design system draft attached 🧩",
            720,
            0,
        ),
    ]
    result: list[Conversation] = []
    for uname, disp, seed, last, mins, unread in data:
        dt = now - timedelta(minutes=mins)
        result.append(
            Conversation(
                id=uname,
                username=uname,
                display=disp,
                seed=seed,
                last_message=last,
                last_time=_fmt(dt),
                unread=unread,
            )
        )
    return result


def _seed_messages() -> dict[str, list[Message]]:
    now = datetime.now()
    threads: dict[str, list[Message]] = {
        "mayachen": [
            ("mayachen", "Hey! Just saw your onboarding redesign post.", 30),
            (
                "mayachen",
                "That 12% bump is huge — details really do matter.",
                28,
            ),
            ("me", "Thanks Maya! Took a lot of iteration to get right.", 22),
            ("mayachen", "Loved your onboarding post ✨", 5),
        ],
        "devjordan": [
            ("devjordan", "Do you have that FastAPI boilerplate handy?", 60),
            ("me", "Yeah, cleaning it up now.", 40),
            ("devjordan", "Sending you the repo link soon.", 25),
        ],
        "sarahkim": [
            ("sarahkim", "That ramen looked incredible!", 60),
        ],
        "tomwalker": [
            ("tomwalker", "Planning a trip to Japan?", 200),
            ("me", "Yeah, thinking November.", 190),
            ("tomwalker", "Kyoto tips coming your way.", 180),
        ],
        "priyanair": [
            ("priyanair", "Design system draft attached 🧩", 720),
        ],
    }
    result: dict[str, list[Message]] = {}
    for k, msgs in threads.items():
        result[k] = []
        for sender, content, mins in msgs:
            dt = now - timedelta(minutes=mins)
            result[k].append(
                Message(
                    id=str(uuid.uuid4()),
                    sender=sender,
                    content=content,
                    time=_fmt(dt),
                    timestamp=dt.timestamp(),
                )
            )
    return result


class MessagesState(rx.State):
    conversations: list[Conversation] = _seed_conversations()
    threads: dict[str, list[Message]] = _seed_messages()
    active_id: str = "mayachen"
    search: str = ""
    send_error: str = ""

    @rx.var
    def filtered_conversations(self) -> list[Conversation]:
        q = self.search.strip().lower()
        if not q:
            return self.conversations
        return [
            c
            for c in self.conversations
            if q in c["display"].lower() or q in c["username"].lower()
        ]

    @rx.var
    def active_conversation(self) -> Conversation:
        for c in self.conversations:
            if c["id"] == self.active_id:
                return c
        if self.conversations:
            return self.conversations[0]
        return Conversation(
            id="",
            username="",
            display="",
            seed="",
            last_message="",
            last_time="",
            unread=0,
        )

    @rx.var
    def active_messages(self) -> list[Message]:
        return self.threads.get(self.active_id, [])

    @rx.var
    def total_unread(self) -> int:
        return sum(c["unread"] for c in self.conversations)

    @rx.event
    def select(self, conv_id: str):
        self.active_id = conv_id
        self.send_error = ""
        new_convs: list[Conversation] = []
        for c in self.conversations:
            if c["id"] == conv_id:
                new_convs.append({**c, "unread": 0})
            else:
                new_convs.append(c)
        self.conversations = new_convs

    @rx.event
    def set_search(self, val: str):
        self.search = val

    @rx.event
    def send(self, form_data: dict):
        content = (form_data.get("content") or "").strip()
        if not content:
            self.send_error = "Message cannot be empty."
            return
        if len(content) > 500:
            self.send_error = "Message must be 500 characters or less."
            return
        self.send_error = ""
        now = datetime.now()
        msg = Message(
            id=str(uuid.uuid4()),
            sender="me",
            content=content,
            time=_fmt(now),
            timestamp=now.timestamp(),
        )
        new_threads = dict(self.threads)
        new_threads[self.active_id] = new_threads.get(self.active_id, []) + [
            msg
        ]
        self.threads = new_threads
        new_convs: list[Conversation] = []
        for c in self.conversations:
            if c["id"] == self.active_id:
                new_convs.append(
                    {**c, "last_message": content, "last_time": _fmt(now)}
                )
            else:
                new_convs.append(c)
        self.conversations = new_convs
