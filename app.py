import suggester as sg
import streamlit as st


st.title("Contextual Word Search")
sentence=st.text_input("Please enter your Sentence")
word= st.text_input("Word to replace")
button=st.button("suggest")
if button:
    if word not in sentence:
        st.error("Word not in sentence. Please make sure the word is in the sentence.")
    else:
        results=sg.ranking(sentence,word)
        st.subheader("Suggestions:")
        for i,(w,score) in enumerate(results,1):
            st.write(f"{i}.{w}-score:{round(score,2)}")