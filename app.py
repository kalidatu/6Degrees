
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

from database import connect, initialize_database
from main import get_network, find_connection
from seed_demo import seed_demo

st.set_page_config(
    page_title="6Degrees",
    page_icon="🌐",
    layout="wide"
)

initialize_database()
seed_demo()


def search_people(search_text, limit=10):
    """Search contacts by partial name."""

    search_text = search_text.strip()

    if not search_text:
        return []

    with connect() as db:
        return db.execute(
            """
            SELECT id, name
            FROM people
            WHERE name LIKE ? COLLATE NOCASE
            ORDER BY
                CASE
                    WHEN name = ? COLLATE NOCASE THEN 0
                    WHEN name LIKE ? COLLATE NOCASE THEN 1
                    ELSE 2
                END,
                name
            LIMIT ?
            """,
            (
                f"%{search_text}%",
                search_text,
                f"{search_text}%",
                limit
            )
        ).fetchall()


def person_search(label, key):
    """Search for a person and select a matching result."""

    search_text = st.text_input(
        label,
        key=f"{key}_search",
        placeholder="Type a person's name..."
    )

    matches = search_people(search_text)

    if not search_text.strip():
        st.caption("Start typing to search.")
        return None

    if not matches:
        st.warning("No matching people found.")
        return None

    options = {
        f"{name} (ID: {person_id})": person_id
        for person_id, name in matches
    }

    selected = st.selectbox(
        "Matching people",
        options=list(options.keys()),
        key=f"{key}_selected"
    )

    return options[selected]


def draw_network(path):
    """Draw the shortest connection path."""

    net = Network(
        height="480px",
        width="100%",
        bgcolor="#101827",
        font_color="white",
        directed=False
    )

    net.barnes_hut()

    with connect() as db:
        names = dict(
            db.execute("SELECT id, name FROM people")
        )

    for index, person_id in enumerate(path):
        name = names[person_id]

        net.add_node(
            person_id,
            label=name,
            title=name,
            size=35 if index in (0, len(path)-1) else 25,
            color="#38bdf8" if index in (0, len(path)-1)
                  else "#64748b"
        )

    for first, second in zip(path, path[1:]):
        net.add_edge(
            first,
            second,
            color="#38bdf8",
            width=4
        )

    return net.generate_html(notebook=False)


st.title("🌐 6Degrees")
st.caption("Discover who connects you.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    start_id = person_search("Who are you?", "start")

with col2:
    target_id = person_search(
        "Who do you want to connect with?",
        "target"
    )

st.write("")

if st.button(
    "Find Connection",
    type="primary",
    disabled=start_id is None or target_id is None
):

    network = get_network()
    path = find_connection(start_id, target_id, network)

    if path is None:
        st.error("No connection found in our database.")

    else:
        with connect() as db:
            names = dict(
                db.execute("SELECT id, name FROM people")
            )

        st.success("Connection found!")

        st.metric(
            "Degrees of Separation",
            len(path) - 1
        )

        st.write(
            " → ".join(names[person_id] for person_id in path)
        )

        html = draw_network(path)

        components.html(
            html,
            height=500,
            scrolling=False
        )

st.divider()

st.caption(
    "6Degrees v0.6 — Local demonstration network. "
    "Relationships are not independently verified."
)
