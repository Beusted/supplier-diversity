import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Implementation Guide - Supplier Diversity",
    page_icon="📋",
    layout="wide"
)

st.title("Implementation Guide")
st.markdown("**Strategic roadmap to achieve 25% small business PO target**")

# Implementation overview
st.markdown("""
This guide provides a phased approach to transitioning Purchase Orders from current suppliers 
to small businesses, with specific timelines and success metrics.
""")

# Current status
st.subheader("Current Status")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current PO %", "16.3%", "-8.7% from target")
with col2:
    st.metric("POs to Transition", "110", "Gap to close")
with col3:
    st.metric("Available Matches", "200", "Potential transitions")

# Implementation phases
st.subheader("Phase 1: High Confidence Transitions")
st.markdown("""
**Objective**: Transition highest similarity matches first  
**Timeline**: 30-60 days  
**Target**: 20 PO transitions  

**Criteria**:
- Similarity Score ≥ 0.4
- Business category alignment
- Capacity verification completed
""")

with st.expander("Phase 1 Action Items"):
    phase1_items = [
        "Review and validate top 20 high-confidence matches",
        "Contact recommended small businesses for capacity assessment", 
        "Negotiate contract terms and transition timeline",
        "Obtain necessary certifications and documentation",
        "Execute pilot transitions with 5 suppliers"
    ]
    
    for i, item in enumerate(phase1_items, 1):
        st.checkbox(f"{i}. {item}", key=f"phase1_{i}")

st.subheader("Phase 2: Medium Confidence Expansion")
st.markdown("""
**Objective**: Expand to medium confidence matches  
**Timeline**: 60-120 days  
**Target**: 50 additional PO transitions  

**Criteria**:
- Similarity Score 0.2-0.4
- Successful Phase 1 completion
- Enhanced due diligence process
""")

with st.expander("Phase 2 Action Items"):
    phase2_items = [
        "Analyze Phase 1 results and lessons learned",
        "Expand outreach to medium-confidence matches",
        "Develop supplier development programs",
        "Implement performance monitoring systems",
        "Scale successful transition processes"
    ]
    
    for i, item in enumerate(phase2_items, 1):
        st.checkbox(f"{i}. {item}", key=f"phase2_{i}")

st.subheader("Phase 3: Strategic Gap Filling")
st.markdown("""
**Objective**: Address remaining gaps through strategic partnerships  
**Timeline**: 120+ days  
**Target**: 40 PO transitions to reach 25%  

**Approach**:
- Identify underserved categories
- Develop new small business partnerships
- Create supplier development initiatives
""")

# Progress tracking
st.subheader("Progress Tracking Dashboard")

# Sample progress data
progress_data = pd.DataFrame({
    'Phase': ['Phase 1', 'Phase 2', 'Phase 3'],
    'Target POs': [20, 50, 40],
    'Completed': [5, 0, 0],
    'In Progress': [8, 0, 0],
    'Not Started': [7, 50, 40],
    'Success Rate': ['25%', '0%', '0%']
})

st.dataframe(progress_data, use_container_width=True, hide_index=True)

# Success metrics
st.subheader("Key Success Metrics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Quantitative Metrics**:
    - Small business PO percentage
    - Number of successful transitions
    - Cost savings achieved
    - Supplier diversity index
    """)

with col2:
    st.markdown("""
    **Qualitative Metrics**:
    - Supplier satisfaction scores
    - Service quality maintenance
    - Relationship strength
    - Community impact assessment
    """)
