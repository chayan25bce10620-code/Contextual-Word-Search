from nltk.corpus import wordnet as wn
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


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
    return sentence_list,sentence

def encoder():
    model=SentenceTransformer("all-MiniLM-L6-v2")
    batch,sentence=ComparisonSentence()[0],ComparisonSentence()[1]
    encoded_vector=model.encode(batch)
    og=model.encode(sentence)
    og_reshaped=og.reshape(1,-1) 
    return og_reshaped,encoded_vector

def scoring():
    og_reshaped,candidate_batch=encoder()[0],encoder()[1]
    scores=cosine_similarity(og_reshaped,candidate_batch)
    scores=scores.flatten()
    pairs=list(zip(candidate_batch,scores))
    return pairs
    
    


print(scoring())