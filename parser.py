import fitz
import spacy

def get_triples(pdf_file):
    # Standard English model for node extraction
    try:
        nlp = spacy.load("en_core_web_md")
    except Exception:
        import spacy.cli
        spacy.cli.download("en_core_web_md")
        nlp = spacy.load("en_core_web_md")
        
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = " ".join([page.get_text() for page in doc])
    
    # Process text for connections (neurons)
    doc_nlp = nlp(text[:10000]) 
    triples = []
    for sent in doc_nlp.sents:
        entities = [t.text.strip() for t in sent if t.pos_ in ["NOUN", "PROPN"] and len(t.text) > 2]
        if len(entities) >= 2:
            triples.append((entities[0], "relates to", entities[1]))
    return list(set(triples))