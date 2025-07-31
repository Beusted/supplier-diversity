# 📋 Small Business PO Percentage Dashboard

**Cal Poly SLO AI Summer Camp - Supplier Diversity Analysis Project**

## 🎯 What This Does

Shows the **percentage of Purchase Orders (POs)** going to small businesses and how to reach the 25% target.

**Current Status**: 16.3% of POs go to small businesses (208 out of 1,274 POs)  
**Target**: 25% of POs should go to small businesses  
**Gap**: Need to transition 110 more POs to small businesses

## 🚀 How to Run

```bash
python run_po_dashboard.py
```

Opens at: http://localhost:8503

## 📊 What You'll See

- **Current vs Target**: 16.3% → 25% PO percentage
- **Gap Analysis**: Exactly 110 POs need to transition
- **Implementation Plan**: Phased approach to reach 25%
- **Quick Wins**: Top PO transition opportunities
- **Supplier Analysis**: Which suppliers have most POs to transition

## 📁 Project Structure

```
supplier-diversity/
├── backend/
│   ├── supplier_similarity_matcher.py    # Core matching algorithm
│   ├── *.csv                            # Analysis results data
│   └── *.md                             # Documentation
├── frontend/
│   ├── po_quantity_dashboard.py         # Main dashboard
│   └── po_quantity_analytics.py         # Data processing
├── run_po_dashboard.py                  # Easy run script
└── requirements.txt                     # Dependencies
```

## 🔧 Requirements

```bash
pip install streamlit plotly pandas numpy scikit-learn
```

## 💡 Key Insight

**Focus**: Percentage of POs (not dollar amounts) going to small businesses  
**Goal**: Each PO counts equally toward the 25% target  
**Strategy**: Transition 110 specific POs from current suppliers to small businesses

---

🎓 **Cal Poly SLO AI Summer Camp Project**  
*Small Business Procurement Target Analysis*
