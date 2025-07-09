import streamlit as st
import requests

st.set_page_config(page_title="Bioinformatics Paper Search", layout="wide")

st.title("🔬 Future Omics Bioinformatics Research Paper Search🤖")
st.write("Search scientific papers using keywords (e.g., CRISPR, genomics, RNA-seq, etc.)")

# Input section
query = st.text_input("Enter keywords", placeholder="e.g., bioinformatics, gene expression, sequencing")

# API query function
def search_papers(keyword, rows=10):
    url = "https://api.crossref.org/works"
    params = {
        "query": keyword,
        "filter": "type:journal-article",
        "rows": rows,
        "sort": "relevance"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data["message"]["items"]
    except Exception as e:
        st.error(f"Failed to fetch papers: {e}")
        return []

# Search and display results
if st.button("🔍 Search") and query:
    with st.spinner("Searching papers..."):
        results = search_papers(query)

    if results:
        st.success(f"Found {len(results)} results")
        for idx, item in enumerate(results, 1):
            title = item.get("title", ["No title"])[0]
            authors = item.get("author", [])
            authors_str = ", ".join(f"{a.get('given', '')} {a.get('family', '')}" for a in authors) if authors else "Unknown authors"
            journal = item.get("container-title", [""])[0]
            year = item.get("published-print", {}).get("date-parts", [[None]])[0][0] or item.get("issued", {}).get("date-parts", [[None]])[0][0]
            doi = item.get("DOI", "")
            link = f"https://doi.org/{doi}" if doi else "#"

            with st.expander(f"{idx}. {title}"):
                st.markdown(f"**Authors**: {authors_str}")
                st.markdown(f"**Journal**: {journal or 'N/A'} ({year or 'N/A'})")
                st.markdown(f"[View Paper ↗️]({link})", unsafe_allow_html=True)
    else:
        st.warning("No results found. Try refining your keywords.")

# Footer
st.markdown("---")
st.caption("Powered by CrossRef API · By Future Omics · 🤖Bioinformatics made easy ❤️ using Streamlit")
