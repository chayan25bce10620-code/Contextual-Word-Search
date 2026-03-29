import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"

from nltk.corpus import wordnet as wn
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def FetchCandidates(word):
    L=set()
    for ss in wn.synsets(word):
        for w in ss.lemma_names():
            if w != word:
                L.add(w)
    Li=list(L)
    if len(Li)>15:
        Li[:]=Li[:15]
    return Li

def ComparisonSentence(sentence,word):
    Synsets=FetchCandidates(word)
    sentence_list=[]
    for i in Synsets:
        s=sentence.replace(word, i)
        sentence_list.append(s)
    return sentence_list,Synsets

def encoder(sentence,word):
    ComparisonSenten=ComparisonSentence(sentence,word)
    model=SentenceTransformer("all-MiniLM-L6-v2")
    batch,synsets=ComparisonSenten[0],ComparisonSenten[1]
    encoded_vector=model.encode(batch)
    og=model.encode(sentence)
    og_reshaped=og.reshape(1,-1) 
    return og_reshaped,encoded_vector,synsets

def scoring(sentence,word):
    encodr=encoder(sentence,word)
    og_reshaped,candidate_batch,synsets=encodr[0],encodr[1],encodr[2]
    scores=cosine_similarity(og_reshaped,candidate_batch)
    scores=scores.flatten()
    pairs=list(zip(synsets,scores))
    return pairs
    
def ranking(sentence,word):
    score=scoring(sentence,word)
    ranked=sorted(score,key=lambda x:x[1],reverse=True)
    return ranked

    
# TODO:
# priority 1 - Fix work ranking. Ranking is inaccurate as of now. 

