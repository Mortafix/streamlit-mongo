import streamlit as st


def app():
    st.title("⚙️ MongoDB Configuration")
    st.write(
        "_MongoDB_ configuration can be specified in the `secrets.toml` file or "
        "directly in the `st.connection` call."
    )

    st.subheader("Using `secrets.toml`")
    st.write(
        "Specify your MongoDB connection parameters in the `secrets.toml` file. "
        "The `kwargs` section corresponds to the MongoDB **connection string options**,"
        " read [MongoDB docs](https://www.mongodb.com/docs/manual/reference/"
        "connection-string/#std-label-connections-connection-options) about those."
    )
    st.code(
        """
        [connections.mongodb]
        url="mongodb+srv://<username>:<password>@<cluster-name>.<cluster-id>.mongodb.net"
        database="streamlit"
        collection="connection"

        [connections.mongodb.kwargs]
        retryWrites=true
        w="majority"
        maxIdleTimeMS=180000
        serverSelectionTimeoutMS=2000
        """
    )

    st.subheader("Using `st.connection`")
    st.write(
        "Alternatively, you can specify the database, collection and connection options"
        " directly in the `st.connection` call."
    )
    st.code(
        """
        conn = st.connection(
            "mongodb",
            url="mongodb+srv://<username>:<password>@<cluster-name>.<cluster-id>.mongodb.net",
            database="streamlit",
            collection="connection",
            kwargs={
                "retryWrites": true,
                "w": "majority",
                "maxIdleTimeMS": 180000,
                "serverSelectionTimeoutMS": 2000
            }
        )
        """
    )

    st.write(
        "The connection details you provide will determine how Streamlit connects to "
        "your _MongoDB_ database."
    )


if __name__ == "__main__":
    app()
