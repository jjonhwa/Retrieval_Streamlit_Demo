import streamlit as st
import yaml
import torch
import pickle

from transformers import AutoTokenizer
from encoder import BertEncoder_For_BiEncoder, RoBertaEncoder_For_CrossEncoder


@st.cache(allow_output_mutation=True)
def load_q_encoder():
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    BertEncoder = BertEncoder_For_BiEncoder
    q_encoder = torch.load(config["q_encoder_path"], map_location=device)
    return q_encoder


@st.cache(allow_output_mutation=True)
def load_c_encoder():
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    RoBertaEncoder = RoBertaEncoder_For_CrossEncoder
    c_encoder = torch.load(config["c_encoder_path"], map_location=device)
    return c_encoder


@st.cache
def load_p_embedding():
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    with open(config["passage_embedding_path"], "rb") as file:
        p_embs = pickle.load(file)
    return p_embs


def get_tokenizer():
    model_checkpoint = "klue/bert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    return tokenizer
