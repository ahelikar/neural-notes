import fitz
import spacy

def get_triples(pdf_file):
    # The model is now pre-installed by requirements.txt
    nlp = spacy.load("en_core_web_md")
        
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = " ".join([page.get_text() for page in doc])
    
    # Analyze text (limiting to 15k chars for speed)
    doc_nlp = nlp(text[:15000]) 
    triples = []
    for sent in doc_nlp.sents:
        entities = [t.text.strip() for t in sent if t.pos_ in ["NOUN", "PROPN"] and len(t.text) > 2]
        if len(entities) >= 2:
            triples.append((entities[0], "connects to", entities[1]))
    return list(set(triples))