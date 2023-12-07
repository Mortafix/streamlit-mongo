import pandas as pd
import streamlit as st

st.set_page_config(page_title="MongoDB Connector", page_icon="🥑")


def main():
    st.title("🌐 MongoDB Connector Project")

    st.header("Overview")
    st.write(
        "This project is part of the [Streamlit Connections Hackathon]"
        "(https://discuss.streamlit.io/t/connections-hackathon)."
    )
    st.write(
        "The goal is to showcase a new _MongoDB_ connection using the "
        "recently released `st.connection` feature of **Streamlit**."
    )
    st.write("The application is divided into 3 main pages:")
    st.write(
        "1. **Connection demonstration** in [🔌 Connection](/Connection): This page "
        "will demonstrate how the connection to _MongoDB_ has been implemented, "
        "showing how data can be retrieved and manipulated."
    )
    st.write(
        "2. **Connection configuration** in [⚙️ Configuration](/Configuration): This "
        "page will demonstrate how the connection to _MongoDB_ has been implemented, "
        "showing how data can be retrieved and manipulated."
    )
    st.write(
        "3. **Demo application in [🦄 StreamY](/StreamY)**: The third page"
        " is a simple social network prototype, where users can post texts to a wall."
        " This showcase uses the _MongoDB_ connection to store and retrieve posts,"
        " demonstrating its practical application."
    )

    st.header("About me")
    st.write("Hello, I'm **Mortafix**! 👋🏻")
    st.write(
        "I've been working with _Streamlit_ since "
        "2022 and _MongoDB_ since 2019, giving me a strong background in both. 🧑🏻‍💻"
    )
    st.write(
        "In the course of my work, I've created "
        "[MagicLit](https://magiclit.streamlit.app), a framework developed "
        "to serve as the base for my company's management app. Through this project, "
        "I've gained substantial experience in designing and implementing software "
        "solutions to meet real-world needs."
    )
    st.write(
        "Participating in this hackathon is an opportunity for me to build an optimal "
        "component for connecting MongoDB to Streamlit. I believe that creating an "
        "effective, easy-to-use connection can make a significant difference in the "
        "experience of using Streamlit, by making it even more convenient and powerful."
    )
    st.write(
        "By sharing my work through this project, I hope to contribute to the "
        "Streamlit community and help other developers who might be facing similar "
        "challenges. 🪄"
    )

    st.header("Project details")
    st.write("The following **platforms** were used for this project")
    df = pd.DataFrame(
        {
            "name": ["Streamlit", "MongoDB", "Python3"],
            "version": ["1.29.0", "6.0", "3.10.13"],
            "url": [
                "https://streamlit.io",
                "https://mongodb.com",
                "https://python.org",
            ],
        }
    )
    st.dataframe(
        df,
        column_config={
            "name": "Platform",
            "version": "Version",
            "url": st.column_config.LinkColumn("App URL"),
        },
        hide_index=True,
    )
    st.write(
        "**Project repository:** [Mortafix/streamlit-mongo]"
        "(https://github.com/Mortafix/streamlit-mongo)"
    )


if __name__ == "__main__":
    main()
