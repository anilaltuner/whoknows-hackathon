import json

import streamlit as st

from utilities.discovery import Discovery
from utilities.mistral import Mistral

product_discovery = Discovery()
mistral = Mistral()


def query_product(query):
    results, images, sources = product_discovery.query(query)
    print(results, images, sources)

    return {
        "results": results,
        "images": images,
        "sources": sources
    }


def main():
    st.title("WhoKnows - Product Discovery")

    # Custom CSS
    st.markdown("""
    <style>
    .css-1oe3uqb {
        justify-content: center;
    }
    .source-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .source-box {
        flex: 1;
        min-width: 200px;
        max-width: 300px;
        background-color: #333;
        color: #fff;
        padding: 15px;
        margin: 5px;
        border-radius: 10px;
        text-align: left;
    }
    .source-title {
        font-size: 1.2em;
        font-weight: bold;
    }
    .source-url a {
        text-decoration: none;
        color: #1E90FF;
    }
    .source-url a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
    query = st.text_input("Enter your query:", key="query_input")
    if st.button("Run Query"):
        data = query_product(query)
        images = data.get("images", [])
        sources = data.get("sources", [])
        results = data.get("results", [])
        if images == []:
            st.write("No results found.")
            return

        st.subheader("Images")
        image_html = ""
        for img in images:
            image_html += f"""
            <div style="display:inline-block; margin-right: 10px;">
                <img src="{img}" style="width:200px; height:auto; border-radius: 10px;">
            </div>
            """
        st.markdown(image_html, unsafe_allow_html=True)

        st.subheader("Sources")
        source_html = ""
        for source in sources:
            source_html += f"""
            <div class="source-box">
                <div class="source-url"><a href="{source['url']}" target="_blank">{source['title']}</a></div>
            </div>
            """
        st.markdown(f"{source_html}", unsafe_allow_html=True)

        st.subheader("Answer")

        st.write(mistral.chat(json.dumps(results)))


if __name__ == "__main__":
    main()
