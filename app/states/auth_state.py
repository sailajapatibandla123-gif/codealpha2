import reflex as rx
from typing import TypedDict


class UserProfile(TypedDict):
    username: str
    email: str
    password: str
    display_name: str
    bio: str
    location: str
    website: str
    interests: list[str]
    avatar_seed: str
    joined: str
    followers: int
    following: int
    posts: int


DEFAULT_USER: UserProfile = {
    "username": "alexdoe",
    "email": "alex@example.com",
    "password": "password123",
    "display_name": "Alex Doe",
    "bio": "Product designer & coffee enthusiast. Building delightful experiences on the web.",
    "location": "San Francisco, CA",
    "website": "https://alex.design",
    "interests": ["Design", "Coffee", "Photography", "Travel"],
    "avatar_seed": "alexdoe",
    "joined": "January 2024",
    "followers": 1284,
    "following": 342,
    "posts": 87,
}


class AuthState(rx.State):
    users: list[UserProfile] = [DEFAULT_USER]
    current_username: str = ""
    login_error: str = ""
    register_error: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_username != ""

    @rx.var
    def current_user(self) -> UserProfile:
        for u in self.users:
            if u["username"] == self.current_username:
                return u
        return {
            "username": "",
            "email": "",
            "password": "",
            "display_name": "Guest",
            "bio": "",
            "location": "",
            "website": "",
            "interests": [],
            "avatar_seed": "guest",
            "joined": "",
            "followers": 0,
            "following": 0,
            "posts": 0,
        }

    @rx.event
    def login(self, form_data: dict):
        self.login_error = ""
        username = (form_data.get("username") or "").strip().lower()
        password = form_data.get("password") or ""
        if not username or not password:
            self.login_error = "Please enter both username and password."
            return
        for u in self.users:
            if u["username"] == username and u["password"] == password:
                self.current_username = username
                return rx.redirect("/")
        self.login_error = "Invalid username or password."

    @rx.event
    def register(self, form_data: dict):
        self.register_error = ""
        username = (form_data.get("username") or "").strip().lower()
        email = (form_data.get("email") or "").strip()
        display_name = (form_data.get("display_name") or "").strip()
        password = form_data.get("password") or ""
        confirm = form_data.get("confirm_password") or ""

        if not username or not email or not display_name or not password:
            self.register_error = "All fields are required."
            return
        if len(username) < 3:
            self.register_error = "Username must be at least 3 characters."
            return
        if "@" not in email or "." not in email:
            self.register_error = "Please enter a valid email address."
            return
        if len(password) < 6:
            self.register_error = "Password must be at least 6 characters."
            return
        if password != confirm:
            self.register_error = "Passwords do not match."
            return
        for u in self.users:
            if u["username"] == username:
                self.register_error = "That username is already taken."
                return
            if u["email"] == email:
                self.register_error = "That email is already registered."
                return

        new_user: UserProfile = {
            "username": username,
            "email": email,
            "password": password,
            "display_name": display_name,
            "bio": "New to the community! Say hi 👋",
            "location": "",
            "website": "",
            "interests": [],
            "avatar_seed": username,
            "joined": "Today",
            "followers": 0,
            "following": 0,
            "posts": 0,
        }
        self.users.append(new_user)
        self.current_username = username
        return rx.redirect("/")

    @rx.event
    def logout(self):
        self.current_username = ""
        return rx.redirect("/login")

    @rx.event
    def require_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    def redirect_if_authed(self):
        if self.is_authenticated:
            return rx.redirect("/")

    def _update_current(self, **fields):
        for i, u in enumerate(self.users):
            if u["username"] == self.current_username:
                updated = {**u, **fields}
                self.users[i] = updated
                return

    @rx.event
    def update_profile(self, form_data: dict):
        self._update_current(
            display_name=(form_data.get("display_name") or "").strip()
            or self.current_user["display_name"],
            bio=(form_data.get("bio") or "").strip(),
            location=(form_data.get("location") or "").strip(),
            website=(form_data.get("website") or "").strip(),
            email=(form_data.get("email") or "").strip()
            or self.current_user["email"],
        )
        yield rx.toast("Profile updated successfully.", duration=3000)

    @rx.event
    def add_interest(self, form_data: dict):
        val = (form_data.get("interest") or "").strip()
        if not val:
            return
        current = list(self.current_user["interests"])
        if val in current:
            yield rx.toast("Interest already added.", duration=2000)
            return
        current.append(val)
        self._update_current(interests=current)

    @rx.event
    def remove_interest(self, interest: str):
        current = [i for i in self.current_user["interests"] if i != interest]
        self._update_current(interests=current)

    @rx.event
    def regenerate_avatar(self):
        import random, string

        seed = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        self._update_current(avatar_seed=seed)
