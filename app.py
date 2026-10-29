
import streamlit as st

from src.rag_pipeline import answer_question
from src.vector_store import build_vector_store
from src.specialist_tool import search_specialists


# Configure the browser page.
st.set_page_config(
    page_title="MediGuide AI",
    page_icon="🩺",
    layout="centered",
)

# Display the application heading.
st.title("🩺 MediGuide AI")
st.caption("AI-powered healthcare information assistant")

st.warning(
    "Educational prototype only. Not a diagnostic tool. "
    "For emergencies, seek immediate medical assistance."
)


# Build the knowledge base once per Streamlit session resource cache.
@st.cache_resource
def load_knowledge_base():
    return build_vector_store()


# Prepare the vector database and embedding model.
try:
    collection, embedding_model = load_knowledge_base()
    st.success("Medical reference search is ready.")
except Exception as error:
    st.error(
        "The knowledge base could not be loaded. "
        "Check your terminal for the error details."
    )
    st.stop()


# Let the user ask a question.
st.subheader("Ask a health-information question")

question = st.text_area(
    "Enter your question",
    placeholder="For example: What are the signs of dehydration?",
    height=100,
)

if st.button("Get guidance", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Preparing your response..."):
            try:
                result = answer_question(
                    question,
                    collection,
                    embedding_model,
                )

                if result.get("emergency_detected", False):
                    st.error(result["answer"])
                else:
                    st.subheader("MediGuide AI response")
                    st.write(result["answer"])

                sources = result.get("sources", [])

                if sources:
                    st.subheader("Reference sources")
                    for source in sources:
                        st.write(f"- {source}")

                elif not result.get("emergency_detected", False):
                    st.info(
                        "No reference filenames were returned. "
                        "The response may not be sufficiently grounded."
                    )

            except Exception:
                st.error(
                    "The response could not be generated. "
                    "Check that Ollama is running and Mistral is available."
                )


# Specialist-search form.
st.divider()
st.subheader("Specialist search")
st.caption(
    "Request preparation only. A live provider directory is "
    "not connected yet."
)

with st.form("specialist_search_form"):
    specialty_question = st.text_input(
        "Which specialist do you need?",
        placeholder="For example: Find a dermatologist",
    )

    location = st.text_input(
        "City or area",
        placeholder="For example: Pune",
    )

    submitted = st.form_submit_button("Prepare search request")

if submitted:
    result = search_specialists(specialty_question, location)

    if result["status"] == "ready_for_provider_lookup":
        st.info(
            f"Specialty: {result['specialty']}\n\n"
            f"Location: {result['location']}\n\n"
            f"{result['message']}"
        )
    else:
        st.warning(result["message"])
