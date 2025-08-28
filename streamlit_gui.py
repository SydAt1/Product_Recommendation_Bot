import streamlit as st
from util.langchain_helper import get_product_recommendation

# Configure the Streamlit page
st.set_page_config(page_title = "Product Recommendation Bot", page_icon = "🛍️")

# Title of the application and description
st.title("Product Recommendation Bot©")
st.write("Upload a description file or Enter your product description to get a recommendation")

# Input Options for the description
# Either upload a file with the description 
# Or input the description on the text area in the Page

# For Uploading a Txt File
upload_file = st.file_uploader("Upload a description text file", type = ["txt"])

# Manual Text input
user_input = st.text_area("Enter the product Description: ", height = 100)
submit_button = st.button("Submit")

if submit_button:
    if user_input:
        st.write(f"Submission Successful!")
    else:
        st.warning("Please enter text before submitting")

# Read the description
description = None
if upload_file is not None:
    description = upload_file.read().decode("utf-8").strip()
elif user_input:
    description = user_input.strip()

# Showing the description
if description:
    st.subheader("Your Description: ")
    st.info(description)

    # Using this description to run the LangChain Model
    if st.button("Get Recommendation"):
        with st.spinner("Analyzing product... Please Wait"):
            try:
                output = get_product_recommendation(description)

                # Show success message
                st.success("Recommendation Generated", icon="✅")

                # Display the results
                st.subheader("Results")
                st.write(f"**Category:** {output['category']}")
                st.write(f"**Product Name:** {output['product_name']}")
                st.write(f"**Specification:** {output['spec_sheet']}")
        
            except Exception as e:
                # Show the error
                st.error(f"Error: {e}")



