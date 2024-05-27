import streamlit as st
import fast_ft as ft
from filters import *
import numpy as np
from io import BytesIO
import json


def img_to_bytes(img):
    buf = BytesIO()
    img.save(buf, format="png")
    return buf.getvalue()


def crop_to_even_shape(array):
    M, N = array.shape
    if M % 2 != 0:
        M -= 1
    if N % 2 != 0:
        N -= 1
    return array[:M, :N]


def apply_transform(_image, _shift):
    _ft = ft.fast_ft2(_image)
    if _shift:
        st.session_state["original_ft"] = ft.ft_shift(_ft)
    else:
        st.session_state["original_ft"] = _ft
    st.session_state["new"] = False
    return


def img_changed():
    st.session_state["new"] = True
    st.session_state["original_ft"] = None
    st.session_state["filtered_ft"] = None


def d_values(_ft):
    M, N = _ft.shape
    m, n = M//2, N//2
    _max = d(0,0,m,n)
    _average = _max*0.5
    _min = 0.0
    return (_min, _max, _average)


def apply_filter(_filter, _d0, _d1, _coef):
    if _filter == "Low pass":
        st.session_state["filtered_ft"] = lowpass_filter(st.session_state["original_ft"], _d0, _coef)
    if _filter == "High pass":
        st.session_state["filtered_ft"] = highpass_filter(st.session_state["original_ft"], _d0, _coef)
    if _filter == "Bond stop":
        st.session_state["filtered_ft"] = bondstop_filter(st.session_state["original_ft"], _d0, _d1, _coef)
    if _filter == "Bond pass":
        st.session_state["filtered_ft"] = bondpass_filter(st.session_state["original_ft"], _d0, _d1, _coef)


def show_examples():
    st.session_state["examples_shown"] = True
    

def hide_examples():
    st.session_state["examples_shown"] = False
    

with open("examples/examples.json", "r", encoding="UTF-8") as read_file:
    examples_dicts = json.load(read_file)


