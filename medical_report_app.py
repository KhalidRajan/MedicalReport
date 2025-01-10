import streamlit as st
from medical_report import process_user_query, super_graph
from langchain_core.messages import HumanMessage

def extract_content(message_dict):
    """Extract readable content from the message dictionary."""
    if 'messages' in message_dict:
        for message in message_dict['messages']:
            if isinstance(message, HumanMessage):
                return message.content
    return None

def main():
    st.title("Medical Report Generator")
    
    st.write("""
    This tool generates comprehensive medical reports based on your query.
    It uses a combination of web searches and medical literature to provide accurate information.
    """)
    
    user_query = st.text_area(
        "Enter your medical query:",
        height=100,
        placeholder="Example: Write a report on the health benefits of Mediterranean diet..."
    )
    
    if st.button("Generate Report"):
        if user_query:
            st.write("Generating report... This may take a few minutes.")
            
            # Create containers for different types of output
            research_container = st.container()
            report_container = st.container()
            
            with st.spinner('Processing...'):
                try:
                    for s in super_graph.stream(
                        process_user_query(user_query),
                        {'recursion_limit': 30}
                    ):
                        if "__end__" not in s:
                            # Extract the key and content
                            for key, value in s.items():
                                if key == "Medical Research Team":
                                    content = extract_content(value)
                                    if content:
                                        with research_container:
                                            st.markdown(content)
                                elif key == "Medical Report Team":
                                    content = extract_content(value)
                                    if content:
                                        with report_container:
                                            st.markdown(content)
                    
                    st.success("Report generated successfully!")
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a query first.")

if __name__ == "__main__":
    main() 