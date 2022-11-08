import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import torch
import subprocess


def load_tokenizer_and_model(model_name_or_path):
    return GPT2Tokenizer.from_pretrained(model_name_or_path), GPT2LMHeadModel.from_pretrained(model_name_or_path)


def generate(
        model, tok, text, do_sample=True, max_length=50, repetition_penalty=5.0,
        top_k=5, top_p=0.95, temperature=1, num_beams=None, no_repeat_ngram_size=3
):
    input_ids = tok.encode(text, return_tensors="pt")
    out = model.generate(
        input_ids,
        max_length=max_length,
        repetition_penalty=repetition_penalty,
        do_sample=do_sample,
        top_k=top_k, top_p=top_p, temperature=temperature,
        num_beams=num_beams, no_repeat_ngram_size=no_repeat_ngram_size
    )
    return list(map(tok.decode, out))


if __name__ == '__main__':
    CUDA = \
        torch_version_suffix = "+cu110"
    np.random.seed(42)
    torch.manual_seed(42)
    tok, model = load_tokenizer_and_model("sberbank-ai/rugpt3large_based_on_gpt2")
    st.markdown("# Text generation")
    theme = st.text_area('start sentences')
    if st.button('continue text'):
        generated = generate(model, tok, theme, num_beams=10, max_length=250)
        st.write(generated[0])