import streamlit as st

def tooltip(text: str, icon: str = "🛈", width: int = 200):
    tooltip_html = f"""
    <style>
    .tooltip {{
      position: relative;
      display: inline-block;
      cursor: pointer;
    }}
    .tooltip .tooltiptext {{
      visibility: hidden;
      width: {width}px;
      background-color: #555;
      color: #fff;
      text-align: left;
      border-radius: 6px;
      padding: 8px;
      position: absolute;
      z-index: 1;
      bottom: 125%;
      left: 50%;
      transform: translateX(-50%);
      opacity: 0;
      transition: opacity 0.3s;
      font-size: 0.9em;
    }}
    .tooltip:hover .tooltiptext {{
      visibility: visible;
      opacity: 1;
    }}
    </style>
    <div class="tooltip">{icon}
      <span class="tooltiptext">{text}</span>
    </div>
    """
    st.markdown(tooltip_html, unsafe_allow_html=True)
