import streamlit as st
from db_utils import get_all_queries, get_open_queries, close_query

def support_dashboard():
    st.header("🛠 Support Dashboard")

    # === Query Filter Section ===
    st.subheader("View Queries")
    try:
        all_df = get_all_queries()
        open_df = all_df[all_df['status'] == 'Open']
        closed_df = all_df[all_df['status'] == 'Closed']

        # show counts
        st.write(f"🟢 Open: {len(open_df)} | 🔵 Closed: {len(closed_df)} | ⚪ All: {len(all_df)}")

        # Filter option (dropdown)
        filter_choice = st.selectbox("Select Query Type to View", ["All", "Open", "Closed"])

        # Display based on filter
        if filter_choice == "All":
            st.dataframe(all_df, use_container_width=True)
        elif filter_choice == "Open":
            st.dataframe(open_df, use_container_width=True)
        else:
            st.dataframe(closed_df, use_container_width=True)
    except Exception as e:
        st.error("Unable to load queries: " + str(e))
        return

    # === Close Open Queries Section ===
    st.subheader("Close an Open Query")
    try:
        open_df = get_open_queries()
        if open_df.empty:
            st.info("No open queries.")
        else:
            query_id = st.selectbox("Select a Query to Close", [int(x) for x in open_df['query_id'].tolist()])
            if st.button("Close Selected Query"):
                try:
                    close_query(query_id)
                    st.success(f" Query {query_id} closed successfully!")
                except Exception as e:
                    st.error("Failed to close query: " + str(e))
    except Exception as e:
        st.error("Unable to load open queries: " + str(e))

    # === Logout Button ===
    if st.button("Logout"):
        for k in ("username", "role", "logged_in"):
            if k in st.session_state:
                del st.session_state[k]
        st.experimental_rerun = None
