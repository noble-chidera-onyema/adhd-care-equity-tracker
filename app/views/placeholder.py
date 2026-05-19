"""
app/views/placeholder.py — generic in-development stub for views not yet built.

Used by the four non-Overview views (Waiting Times, Demographics, Trends,
Methodology) until each has its own module.

Copyright (c) 2026 Noble Chidera Onyema. All Rights Reserved.
"""

import streamlit as st


VIEW_TITLES = {
    "waiting_times": "Waiting Times",
    "demographics":  "Demographics",
    "trends":        "Trends",
    "methodology":   "Methodology",
}


def render(view_key: str):
    """Render a clean in-development stub for the given view key."""
    title = VIEW_TITLES.get(view_key, view_key.replace("_", " ").title())

    st.markdown(
        f'<div class="ace-section-title">{title}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="ace-section-intro">'
        f'This view is in development. The {title.lower()} analysis attaches here in a future commit. '
        f'For now, see the Overview tab for the project\'s headline finding.'
        f'</div>',
        unsafe_allow_html=True,
    )
