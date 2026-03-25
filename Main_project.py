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


import streamlit as st
st.title("Contextual Word Search")
sentence=st.text_input("Please enter your Sentence")
word= st.text_input("Word to replace")
button=st.button("suggest")
if button:
    if word not in sentence:
        st.error("Word not in sentence. Please make sure the word is in the sentence.")
    else:
        results=ranking(sentence,word)
        st.subheader("Suggestions:")
        for i,(w,score) in enumerate(results,1):
            st.write(f"{i}.{w}-score:{round(score,2)}")

    
# TODO:
# priority 1 - Fix work ranking. Ranking is inaccurate as of now. 
# priority 2 - Need to fix UI. 
# cleanup 1 - remove print statement
# cleanup 2 - remove placeholder input
# task for later - edge cases such as short sentences or no synonyms


if __name__ == "__main__":
    import subprocess
    subprocess.run(["streamlit", "run", __file__])


# Issue is with Ranking() function. maybe not compatible with the UI? or im running the UI wrong. Worked when using playground.