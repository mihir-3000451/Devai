import streamlit as st
import google.generativeai as genai
import json

def annotate_text(text):
    # Define the prompt for annotation
    prompt = "As a text annotator with more than 10 years of experience, annotate the following text for Named Entity Recognition (NER):"
    # Send the text and prompt to Gemini Pro for annotation
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + " " + text)
    # Parse the response to extract entities or perform any necessary post-processing
    # For demonstration, let's assume the response contains the annotated entities
    entities = response.entities  # Update this based on the actual response structure
    annotated_entities = [{"text": ent.text, "start_char": ent.start_char, "end_char": ent.end_char, "label": ent.label_}
                          for ent in entities]
    return annotated_entities

def save_annotations_to_json(data, output_path):
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

st.set_page_config(page_title="Text Annotation Tool")
st.header("Text Annotation Tool")

uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

if uploaded_file is not None:
    file_contents = uploaded_file.getvalue().decode("utf-8")
    st.text_area("Text", file_contents, height=200)

    annotate_button = st.button("Annotate Text")

    if annotate_button:
        entities = annotate_text(file_contents)
        
        json_data = {"text": file_contents, "annotations": entities}
        st.write("Generated JSON data:")
        st.json(json_data)

        save_button = st.button("Download Annotations as JSON")
        if save_button:
            output_path = "annotations.json"
            save_annotations_to_json(json_data, output_path)
            st.success(f"Annotations saved to {output_path}")
