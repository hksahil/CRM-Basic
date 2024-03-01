import streamlit as st
import pandas as pd
# Page Settings
st.set_page_config(page_title='Kellogg Simulator',page_icon=':smile:')

# CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def merge_and_mark_status(early_users_file, enrolled_users_file):
    early_users = pd.read_excel(early_users_file)
    enrolled_users = pd.read_excel(enrolled_users_file)

    merged = early_users.merge(enrolled_users, on="Name", how="outer", suffixes=("_early", "_enrolled"))
    
    def mark_status(row):
        if pd.isnull(row["Course_early"]) and pd.isnull(row["Course_enrolled"]):
            return "Unknown"
        elif pd.notnull(row["Course_early"]) and pd.notnull(row["Course_enrolled"]):
            return "Early + Enrolled"
        elif pd.notnull(row["Course_early"]) and pd.isnull(row["Course_enrolled"]):
            return "Early User Not Enrolled"
        elif pd.isnull(row["Course_early"]) and pd.notnull(row["Course_enrolled"]):
            return "Enrolled"
    
    merged["Status"] = merged.apply(mark_status, axis=1)
    
    #merged.drop(["Course_early", "Course_enrolled"], axis=1, inplace=True)
    
    return merged

def main():
    st.sidebar.title("Upload Files")
    
    early_users_file = st.sidebar.file_uploader("Upload File1 (Excel)", type="xlsx")
    enrolled_users_file = st.sidebar.file_uploader("Upload File2 (Excel)", type="xlsx")

    if early_users_file is not None and enrolled_users_file is not None:
        merged_df = merge_and_mark_status(early_users_file, enrolled_users_file)
        merged_df['Phone'] = merged_df['Phone_early'].fillna(merged_df['Phone_enrolled'])
        merged_df['Email'] = merged_df['Email_early'].fillna(merged_df['Email_enrolled'])
        merged_df['Course'] = merged_df['Course_early'].fillna(merged_df['Course_enrolled'])
        # Drop the specified columns
        columns_to_drop = ['Email_early', 'Phone_early', 'Email_enrolled', 'Phone_enrolled','Course_early','Course_enrolled']
        merged_df.drop(columns=columns_to_drop, inplace=True)
        if not merged_df.empty:
            status_to_filter = st.selectbox("Select Status", ["All"] + merged_df["Status"].unique().tolist())
            
            if status_to_filter != "All":
                filtered_df = merged_df[merged_df["Status"] == status_to_filter]
            else:
                filtered_df = merged_df
            
            st.write(filtered_df)
        

if __name__ == "__main__":
    main()
