import fitz  # PyMuPDF
import spacy

def load_nlp_model():
    try:
        return spacy.load("en_core_web_md")
    except Exception:
        import spacy.cli
        spacy.cli.download("en_core_web_md")
        return spacy.load("en_core_web_md")

def extract_neurons(pdf_file):
    nlp = load_nlp_model()
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = " ".join([page.get_text() for page in doc])
    
    doc_nlp = nlp(text[:10000]) 
    triples = []
    for sent in doc_nlp.sents:
        entities = [token.text.strip() for token in sent if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2]
        actions = [token.lemma_ for token in sent if token.pos_ == "VERB"]
        if len(entities) >= 2:
            rel = actions[0] if actions else "relates to"
            triples.append((entities[0], rel, entities[1]))
    return list(set(triples))