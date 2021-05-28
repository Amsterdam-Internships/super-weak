import spacy
from spacy.tokens import DocBin
nlp = spacy.load("nl_core_news_md")

def to_spacy(path: str) -> list:
	"""
	returns list of spacy docs from file at path
	"""
	docbin = DocBin().from_disk(path)
	return list(docbin.get_docs(nlp.vocab))

def relabel(ent_list: list) -> list:
    """
    returns a relabeled list of tuples (text, label) with new labels complying with ConLL labels 
    """
    mappings = {"PERSON":"PER", "COMPANY":"ORG", "GPE":"LOC", 'EVENT':"MISC", 'FAC':"MISC", 'LANGUAGE':"MISC", 
                      'LAW':"MISC", 'NORP':"MISC", 'PRODUCT':"MISC",'WORK_OF_ART':"MISC", "MISC":"MISC", "PER":"PER", "ORG":"ORG", "LOC":"LOC"}
    
    exclude = {"CARDINAL", "ORDINAL", "DATE", "PERCENT", "QUANTITY", "TIME", "MONEY"}
    return [(ent[0], mappings[ent[1]]) for ent in ent_list if ent[1] not in exclude]

def ent_tup(ent) -> tuple:
    """
    returns a tuple containing (text, label) for specified ent
    """
    return (ent.text, ent.label_)

def ent_list(doc) -> list:
    """
    returns list of tuples (text, label) of all entities in doc
    """
    ent_list = [ent_tup(ent) for ent in doc.ents]
    return relabel(ent_list)

def get_spacy_ents(docs: list) -> list: 
    """
    returns docs with entities as provided by spacy's default NER pipeline
    """
    return [nlp(doc.text) for doc in docs]

def score(docs: list, truth: list) -> dict:
    """
    returns scores {precision, recall, f1} of docs using truth as ground truth. 
    """
    tp = []
    fp = []
    fn = []
    
    for i, doc in enumerate(docs):
        pred = ent_list(doc)
        true = ent_list(truth[i])
        for ent in pred:
            pred_label = ent[1]
            pred_text = ent[0]
            for true_ent in true: 
                text = true_ent[0]
                label = true_ent[1]
                if pred_text in text or text in pred_text:
                    if pred_label == label:        
                        tp.append(ent)
                        break
                    else:
                        fp.append(ent)
                        break

        doc_fn = [ent for ent in true if ent not in tp + fp]
        fn.extend(doc_fn)
    
    precision = len(tp) / (len(tp) + len(fp))
    recall = len(tp) / (len(tp) + len(fn))
    f1 = 2 * (recall * precision) / (recall + precision)
    return {"precision" : precision, "recall" : recall, "f1" : f1}

def spacy_benchmark(path: str) -> dict:
    """
    returns benchmarks {precision, recall, f1} of spacy file at path using 
    spacy default NER pipeline
    """
    true = to_spacy(path)
    pred = get_spacy_ents(true)

    return score(true, pred)