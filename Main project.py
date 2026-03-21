from nltk.corpus import wordnet as wn
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

def Input():
    while True:
        #sen=input("Enter full sentence:")
        #word=input("Enter word that needs to be replaced:")
        sen = 'i am drunk' #remember to remove these temp assignments
        word='drunk'
        if word not in sen:
            print("Word not in sentence. Please make sure the word is in the sentence.")
        else:
            break
    return [sen,word]

def FetchCandidates(word):
    L=[]
    for ss in wn.synsets(word):
        for word in ss.lemma_names():
            L.append(word)
    if len(L)>15:
        L[:]=L[:15]
    return L

def ComparisonSentence():
    inp=Input()
    sentence,word=inp[0],inp[1]
    Synsets=FetchCandidates(word)
    sentence_list=[]
    for i in Synsets:
        s=sentence.replace(word, i)
        sentence_list.append(s)
    return sentence_list,sentence,Synsets

def encoder():
    ComparisonSenten=ComparisonSentence()
    model=SentenceTransformer("all-MiniLM-L6-v2")
    batch,sentence,synsets=ComparisonSenten[0],ComparisonSenten[1],ComparisonSenten[2]
    encoded_vector=model.encode(batch)
    og=model.encode(sentence)
    og_reshaped=og.reshape(1,-1) 
    return og_reshaped,encoded_vector,synsets

def scoring():
    encodr=encoder()
    og_reshaped,candidate_batch,synsets=encodr[0],encodr[1],encodr[2]
    scores=cosine_similarity(og_reshaped,candidate_batch)
    scores=scores.flatten()
    pairs=list(zip(synsets,scores))
    return pairs
    
# TODO:
# priority 1 - fix repeated words in output
# priority 2 - clean up output
# cleanup 1 - remove print statement
# cleanup 2 - remove placeholder input
# task for later - edge cases such as short sentences or no synonyms


print(scoring())