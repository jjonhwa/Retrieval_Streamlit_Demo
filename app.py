import streamlit as st
import yaml
import torch

from loading import load_q_encoder, load_c_encoder, load_p_embedding, get_tokenizer
from encoder import BertEncoder_For_BiEncoder, RoBertaEncoder_For_CrossEncoder
from utils import Passage_Embedding
from rerank import get_relavant_doc, rerank
from confirm_button_hack import cache_on_button_press

st.set_page_config(layout="wide")

BertEncoder = BertEncoder_For_BiEncoder
RoBertaEncoder = RoBertaEncoder_For_CrossEncoder

if "q_encoder" not in st.session_state:
    with st.spinner("Uploading.."):
        with open("config.yaml") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        st.session_state.p_embs = load_p_embedding()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        st.session_state.q_encoder = load_q_encoder()

        st.session_state.corpus = Passage_Embedding(
            config["wikipedia_path"], p_encoder=None
        ).get_corpus()
        st.session_state.tokenizer = get_tokenizer()

        st.session_state.c_encoder = load_c_encoder()


def main():
    p_embs = st.session_state.p_embs
    q_encoder = st.session_state.q_encoder
    c_encoder = st.session_state.c_encoder
    tokenizer = st.session_state.tokenizer
    corpus = st.session_state.corpus

    text_input = st.text_input("질문을 입력해주세요.")
    st.write(text_input)
    # query = "나폴레옹이 죽은 날짜는?"
    query = [text_input]

    k = 5
    if st.button("자세히 찾기"):
        st.write("약 1분 정도 소요됩니다.")
        with st.spinner("Please wait.."):
            k_plus = k * 10
            doc_scores, doc_indices = get_relavant_doc(
                q_encoder, tokenizer, query, p_embs, k=k_plus
            )

            result_scores, result_indices = rerank(
                query, c_encoder, doc_indices, corpus, tokenizer
            )

            # get final Top-k Passages: Here, I just get 50 passage
            final_indices = []
            for i in range(len(doc_indices)):
                t_list = [doc_indices[i][result_indices[i][j]] for j in range(k)]
                final_indices.append(t_list)

        st.write("-------------------------------------")
        for i in range(k):
            st.write(corpus[final_indices[0][i]])
            st.write("-------------------------------------")

    if st.button("빠르게 찾기"):
        with st.spinner("Please wait.."):
            doc_scores, doc_indices = get_relavant_doc(
                q_encoder, tokenizer, query, p_embs, k=k
            )

        # st.write(corpus[doc_indices[0][0]])
        st.write("-------------------------------------")
        for i in range(k):
            st.write(corpus[doc_indices[0][i]])
            st.write("-------------------------------------")


root_password = "qustjddbs"
password = st.text_input(
    "AI BoostCamp 2기! Product Serving Master는 누구인가요?", type="password"
)


@cache_on_button_press("Authenticate")
def authenticate(password) -> bool:
    return password == root_password


if authenticate(password):
    st.success("성공!")
    st.title("Retrieve Document about Question")
    main()
else:
    st.error("부스트캠프 AI Tech 2기 멤버가 아닌가요?")
