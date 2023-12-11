from datetime import datetime
from random import choice, randint
from re import sub

import streamlit as st
from connection.mongo import MongoDBConnection

DB = st.connection("streamy", type=MongoDBConnection)

# ---- utils


def create_username():
    adj = ["Handsome", "Curious", "Peaceful", "Dumb", "Ugly", "Hysterical", "Funny"]
    names = ["Dolphin", "Ninja", "Dragon", "Robot", "Ghost", "Clown", "Moon", "Pizza"]
    return f"{choice(adj).title()}{choice(names).title()}{randint(10, 99)}"


def send_post(post):
    data = {
        "user": st.session_state.username,
        "post": post,
        "timestamp": datetime.utcnow(),
    }
    if DB.insert(data):
        st.toast("New **post** created!", icon="🦄")


def retrieve_post(ttl):
    return DB.find(sort=[("timestamp", -1)], limit=500, ttl=ttl)


# ---- app


def app():
    st.title("🦄 StreamY")

    # ---- wall refresh
    side_section = st.sidebar.container()
    ttl = side_section.slider(
        "Wall",
        min_value=0,
        max_value=60,
        step=5,
        value=10,
        label_visibility="collapsed",
    )
    side_section.info(
        f"Wall is updated every **{ttl}** seconds (after a _Streamlit_ refresh)",
        icon="ℹ️",
    )
    side_section.button("Refresh 🔄", use_container_width=True)
    side_section.divider()
    # stats
    total_chars = DB.aggregate(
        [
            {"$addFields": {"length": {"$strLenCP": "$post"}}},
            {"$group": {"_id": None, "total": {"$sum": "$length"}}},
        ],
        ttl=ttl,
    )
    side_section.title("📊 Wall stats")
    side_section.write(f"* **Post** count: `{DB.count(ttl=ttl)}`")
    side_section.write(f"* Unique **users**: `{len(DB.distinct('user', ttl=ttl))}`")
    side_section.write(f"* Total **chars**: `{total_chars[0].get('total')}`")

    # ---- user
    if not (username := st.session_state.get("username")):
        username = create_username()
        st.session_state.username = username
    st.info(f"You're logged in as **{username}**", icon="👤")
    # new post
    with st.form("new-post", clear_on_submit=True):
        post = st.text_area(
            "Post",
            placeholder="What are you thinking about?",
            max_chars=140,
            label_visibility="collapsed",
        )
        if st.form_submit_button("Post 🌐", use_container_width=True):
            send_post(post)
    st.divider()

    # ---- wall
    emojis = {
        "Do": "🐬",
        "Ni": "🥷",
        "Dr": "🐲",
        "Ro": "🤖",
        "Gh": "👻",
        "Cl": "🤡",
        "Mo": "🌝",
        "Pi": "🍕",
    }
    for entry in retrieve_post(ttl):
        user = entry.get("user")
        chat_name = "user" if user != st.session_state.username else "assistant"
        avatar = emojis.get(sub(r"[A-Z][a-z]+([A-Z][a-z])[a-z]+\d{2}", r"\g<1>", user))
        # posts
        with st.chat_message(chat_name, avatar=avatar):
            with st.container():
                st.write(f"`{user}` _{entry.get('timestamp'):%d.%m.%Y %H:%M}_")
                st.subheader(entry.get("post"))


if __name__ == "__main__":
    app()
