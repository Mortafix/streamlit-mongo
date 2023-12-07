import streamlit as st
from connection.mongo import MongoDBConnection


def app():
    st.title("🔌 MongoDB Connection")
    st.info(
        "This component use the last **pymongo** version available (_December 2023_)",
        icon="ℹ️",
    )
    st.write(
        "**First step**: create a _connection_ using `st.connection` "
        "and `MongoDBConnection` component"
    )
    connection = st.connection("mongodb", type=MongoDBConnection)
    st.code("""connection = st.connection("mongodb", type=MongoDBConnection)""")

    tabs = st.tabs(
        ["Connection 🔌", "Find 🔎", "Insert ✅", "Update ⚡️", "Delete ❌", "Extra 🪄"]
    )

    # ---- introduction
    tabs[0].write("This below is the _MongoDB_ collection instance 👇🏻")
    tabs[0].write(connection._instance)
    tabs[0].write("and the `st.help()` output")
    tabs[0].help(connection)

    # ---- find
    tabs[1].subheader("Functions")
    tabs[1].write("These functions represent `find` and `find_one` of **pymongo**")
    tabs[1].code(
        """
        # Find documents in the MongoDB collection that match the provided filters.
        # If 'one' is True, only the first match will be returned.
        # If 'mongo_id' is False, the Mongo ID will be excluded from the results.
        connection.find(filters, one=False, mongo_id=False, ttl=3600, **kwargs)

        # Find a single document in the MongoDB collection that matches the filters.
        # If 'mongo_id' is False, the Mongo ID will be excluded from the results.
        connection.find_one(filters, mongo_id=False, ttl=3600, **kwargs)
        """
    )
    tabs[1].subheader("Examples")
    # find
    tabs[1].code("""connection.find({"a": {"$gt": 0}})""")
    if tabs[1].button("**Try** it 🎈", key="find-1"):
        tabs[1].json(connection.find({"a": {"$gt": 0}}, sort=[("a", -1)]))
        st.toast("Operation `find` succesful!", icon="✅")
    # find with args
    tabs[1].code("""connection.find(sort=[("b", -1)], limit=3, ttl=0)""")
    if tabs[1].button("**Try** it 🎈", key="find-2"):
        tabs[1].json(connection.find(sort=[("b", -1)], limit=3, ttl=0))
        st.toast("Operation `find` succesful!", icon="✅")
    # find one
    tabs[1].code(
        """
        connection.find_one({"z": 8}, mongo_id=True)
        connection.find({"z": 8}, one=True, mongo_id=True) # same operation
        """
    )
    if tabs[1].button("**Try** it 🎈", key="find-3"):
        tabs[1].json(connection.find_one({"z": 8}, mongo_id=True))
        st.toast("Operation `find_one` succesful!", icon="✅")

    # ---- insert
    tabs[2].subheader("Functions")
    tabs[2].write(
        "These functions represent `insert_one` and `insert_many` of **pymongo**"
    )
    tabs[2].code(
        """
        # Insert the provided data into the MongoDB collection.
        # The data can be a single document (dict) or multiple documents (list).
        connection.insert(data, ttl=0, **kwargs)
        """
    )
    tabs[2].subheader("Examples")
    # insert many
    tabs[2].code("""connection.insert({"a": 55, "b": 6}""")
    if tabs[2].button("**Try** it 🎈", key="insert-1"):
        tabs[2].json(connection.insert({"a": 55, "b": 6}))
        st.toast("Operation `insert` succesful!", icon="✅")
    # insert one
    tabs[2].code("""connection.insert([{"a": 77, "b": 100}, {"d": 4}, {"a": 0}])""")
    if tabs[2].button("**Try** it 🎈", key="insert-2"):
        tabs[2].json(connection.insert([{"a": 77, "b": 100}, {"d": 4}, {"a": 0}]))
        st.toast("Operation `insert` succesful!", icon="✅")

    # ---- update
    tabs[3].subheader("Functions")
    tabs[3].write(
        "These functions represent `update_one` and `update_many` of **pymongo**"
    )
    tabs[3].code(
        """
        # Update the documents in the MongoDB collection that match the provided
        # filters with the provided data
        # If 'one' is True, only the first matching document will be updated
        connection.update(filters, data, one=False, ttl=0, **kwargs)

        # Update a single document in the MongoDB collection that matches the provided
        # filters with the provided data
        connection.update_one(filters, data, ttl=0, **kwargs)
        """
    )
    tabs[3].subheader("Examples")
    # update many
    tabs[3].code("""connection.update({"a": {"$gte": 2}}, {"$set": {"u": 1}})""")
    if tabs[3].button("**Try** it 🎈", key="update-1"):
        tabs[3].json(connection.update({"a": {"$gte": 2}}, {"$set": {"u": 1}}))
        st.toast("Operation `update` succesful!", icon="✅")
    # insert one
    tabs[3].code("""connection.update({"h": 2}, {"$push": {"l": 7}}, upsert=True)""")
    if tabs[3].button("**Try** it 🎈", key="update-2"):
        tabs[3].json(connection.update({"h": 2}, {"$push": {"l": 7}}, upsert=True))
        st.toast("Operation `update` succesful!", icon="✅")
    tabs[3].code(
        """
        connection.update_one({"a": {"$lt": 100}}, {"$set": {"s": 5}})
        connection.update({"a": {"$lt": 100}}, {"$set": {"s": 5}}, one=True) # same
        """
    )
    if tabs[3].button("**Try** it 🎈", key="update-3"):
        tabs[3].json(connection.update_one({"a": {"$lt": 100}}, {"$set": {"s": 5}}))
        st.toast("Operation `update_one` succesful!", icon="✅")

    # ---- delete
    tabs[4].subheader("Functions")
    tabs[4].write(
        "These functions represent `delete_one` and `delete_many` of **pymongo**"
    )
    tabs[4].code(
        """
        # Delete documents in the MongoDB collection that match the provided filters.
        # If 'one' is True, only the first matching document will be deleted
        connection.delete(filters, one=False, ttl=0, **kwargs)

        # Delete a single document in the MongoDB collection that matches the
        # provided filters
        connection.delete_one(filters, ttl=0, **kwargs)
        """
    )
    tabs[4].subheader("Examples")
    # delete many
    tabs[4].code("""connection.delete({"d": 4})""")
    if tabs[4].button("**Try** it 🎈", key="delete-1"):
        tabs[4].json(connection.delete({"d": 4}))
        st.toast("Operation `delete` succesful!", icon="✅")
    # delete one
    tabs[4].code(
        """
        connection.delete_one({"a": 77})
        connection.delete({"a": 77}, one=True) # same operation
        """
    )
    if tabs[4].button("**Try** it 🎈", key="delete-2"):
        tabs[4].json(connection.delete_one({"a": 77}))
        st.toast("Operation `delete_one` succesful!", icon="✅")

    # ---- extra
    tabs[5].subheader("Functions")
    tabs[5].write(
        "These functions represent `replace`, `aggregate`, `distinct` and "
        "`count_documents` of **pymongo**"
    )
    tabs[5].code(
        """
        # Replace a single document in the MongoDB collection that matches the
        # provided filters with the provided replacement
        connection.replace(filters, replacement, ttl=0, **kwargs)

        # Aggregate the data in the MongoDB collection using the provided
        # aggregation pipeline
        connection.aggregate(pipeline, ttl=3600, **kwargs)

        # Count the number of documents in the MongoDB collection that match the
        # provided filters
        connection.count(filters, ttl=3600, **kwargs)

        # Find the distinct values for a specified field across a single collection
        # and returns the results in an array
        connection.distinct(field, filters, ttl=3600, **kwargs)
        """
    )
    tabs[5].subheader("Examples")
    # replace
    tabs[5].code("""connection.replace({"a": 77}, {"n": 6})""")
    if tabs[5].button("**Try** it 🎈", key="replace"):
        tabs[5].json(connection.replace({"a": 77}, {"n": 6}))
        st.toast("Operation `replace` succesful!", icon="✅")
    # aggregate
    tabs[5].code(
        """
        connection.aggregate(
            [
                {"$match": {"b": {"$ne": None}}},
                {"$project": {"mul": {"$multiply": [10, "$b"]}}},
                {"$limit": 2},
            ]
        )
        """
    )
    if tabs[5].button("**Try** it 🎈", key="aggregate"):
        tabs[5].json(
            connection.aggregate(
                [
                    {"$match": {"b": {"$ne": None}}},
                    {"$project": {"mul": {"$multiply": [10, "$b"]}}},
                    {"$limit": 2},
                ]
            )
        )
        st.toast("Operation `aggregate` succesful!", icon="✅")
    # count
    tabs[5].code("""connection.count({"a": {$ne: 3}})""")
    if tabs[5].button("**Try** it 🎈", key="count"):
        tabs[5].json({"documents": connection.count({"a": {"$ne": 3}})})
        st.toast("Operation `count` succesful!", icon="✅")
    # distinct
    tabs[5].code("""connection.distinct("b")""")
    if tabs[5].button("**Try** it 🎈", key="distinct"):
        tabs[5].json(connection.distinct("b"))
        st.toast("Operation `distinct` succesful!", icon="✅")


if __name__ == "__main__":
    app()
