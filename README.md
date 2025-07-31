# Cal Poly AI Summer Camp: Small Business Supplier Diversity Dashboard

Welcome to our AI Summer Camp project! This dashboard uses artificial intelligence and data analytics to help organizations achieve their small business procurement goals. Don't worry if you're new to these technologies!

## Contact Information

**Instructor**: [Your Instructor Name] - [email@calpoly.edu]

Feel free to reach out if you have questions about:
- Setting up the dashboard environment
- Understanding the supplier matching algorithms
- Interpreting the analytics results
- Troubleshooting dashboard errors
- Ideas for extending this project
- General questions about AI in procurement

## Video Tutorial

- For a complete walkthrough of this project and how to set it up: [Coming Soon]
- For understanding the supplier matching algorithm: [Coming Soon]
- For interpreting the dashboard analytics: [Coming Soon]

## What You'll Learn

- **AI-Powered Supplier Matching**: How machine learning algorithms can identify similar suppliers
- **Data Analytics**: Processing and analyzing procurement data for insights
- **Interactive Dashboards**: Building professional web applications with Streamlit
- **Procurement Strategy**: Understanding small business diversity goals and implementation
- **Python Data Science**: Using pandas, scikit-learn, and visualization libraries

## What This Dashboard Does

This project demonstrates how AI can solve real-world procurement challenges by:

1. **Analyzing Current State**: Shows exactly where your organization stands (16.3% of POs go to small businesses)
2. **Identifying the Gap**: Calculates precisely what's needed to reach the 25% target (110 more POs)
3. **AI-Powered Matching**: Uses machine learning to find the best supplier transition opportunities
4. **Strategic Planning**: Provides phased implementation plans with confidence levels
5. **Interactive Visualization**: Presents complex data through charts, tables, and metrics

## Prerequisites

Before you start, you'll need:

### 1. Python Installation
- Python 3.8 or higher installed on your computer
- You can download it from [python.org](https://www.python.org/downloads/)

### 2. Required Python Packages
Install the necessary packages by running this command in your terminal:
```bash
pip install streamlit plotly pandas numpy scikit-learn pathlib
```

### 3. Project Files
- Download or clone this repository to your computer
- Ensure all CSV data files are in the `backend/` directory

## Understanding the Project

### Key Components

**Streamlit**: A Python framework that turns data scripts into interactive web applications. Think of it as a way to create professional dashboards without complex web development.

**Machine Learning**: The project uses similarity algorithms to match current suppliers with potential small business alternatives based on their services and characteristics.

**Data Analytics**: Processes procurement data to identify patterns, calculate gaps, and recommend optimal transition strategies.

**Interactive Visualization**: Uses Plotly charts and tables to make complex procurement data easy to understand and actionable.

### The Main Features Explained

#### 1. **Current State Analysis**
Shows exactly where your organization stands:
- Current percentage of POs going to small businesses (16.3%)
- Total PO counts and breakdowns
- Visual comparison with the 25% target

#### 2. **AI-Powered Gap Analysis**
Calculates precisely what's needed:
- Exact number of POs to transition (110)
- Identifies which current suppliers have the most transition opportunities
- Provides confidence levels for different scenarios

#### 3. **Smart Supplier Matching**
Uses machine learning to find the best matches:
- Analyzes supplier descriptions and services
- Calculates similarity scores between current and small business suppliers
- Ranks opportunities by feasibility and impact

#### 4. **Strategic Implementation Planning**
Provides actionable roadmaps:
- Phased approach with different confidence thresholds
- Quick wins for immediate impact
- Long-term strategy for sustainable growth

## How to Run the Dashboard

1. **Navigate to your project folder**:
   ```bash
   cd path/to/supplier-diversity
   ```

2. **Run the dashboard**:
   ```bash
   python run_po_dashboard.py
   ```

3. **Open your browser** to: http://localhost:8503

4. **Explore the dashboard**:
   - Use the navigation buttons (Dashboard, Settings, About)
   - Toggle between light and dark themes
   - Scroll through different analytics sections

## Customizing the Dashboard

### Try Different Scenarios
You can modify the target percentage or explore different matching thresholds:
```python
# In po_quantity_analytics.py, change the target:
self.target_percentage = 30.0  # Try 30% instead of 25%
```

### Understanding the Algorithms
The project uses several AI techniques:
- **TF-IDF Vectorization**: Converts supplier descriptions into numerical data
- **Cosine Similarity**: Measures how similar two suppliers are
- **Optimization Algorithms**: Finds the best combination of transitions

### Adding New Data
To analyze your own procurement data:
1. Format your data to match the expected CSV structure
2. Place files in the `backend/` directory
3. Update file paths in the analytics modules

## Dashboard Navigation

### Main Sections

#### **📊 Purchase Order Analysis**
- Big number metrics showing current state
- Visual comparison of current vs. target percentages
- Detailed PO breakdowns and statistics

#### **🎯 Transition Scenarios**
- High confidence matches (≥40% similarity)
- Medium confidence matches (≥20% similarity)
- All available matches for maximum potential

#### **📈 Implementation Planning**
- Phased rollout strategy
- Timeline and milestone tracking
- Progress visualization

#### **⚡ Quick Wins**
- Top individual PO transition opportunities
- Detailed supplier matching recommendations
- Impact scores and similarity ratings

#### **🔄 Supplier Analysis**
- Current suppliers with most transition potential
- Aggregate statistics and insights
- Strategic focus recommendations

## Common Issues and Solutions

### "Module not found" errors
Install missing packages:
```bash
pip install [package-name]
```

### "File not found" errors
Ensure all CSV files are in the correct `backend/` directory structure.

### Dashboard won't load
Check that port 8503 isn't already in use:
```bash
pkill -f streamlit
python run_po_dashboard.py
```

### Data doesn't display
Verify your CSV files have the expected column names and data format.

## Important Notes

- **Data Privacy**: All analysis is performed locally on your machine
- **Scalability**: The dashboard can handle datasets with thousands of suppliers and POs
- **Customization**: Colors, themes, and layouts can be modified in the CSS sections
- **Performance**: Large datasets may take a few moments to process initially

## Understanding the Results

### Similarity Scores
- **0.4+ (High Confidence)**: Very similar suppliers, low risk transitions
- **0.2-0.4 (Medium Confidence)**: Moderately similar, may need evaluation
- **<0.2 (Low Confidence)**: Different suppliers, higher risk transitions

### Implementation Strategy
- Start with high confidence matches for quick wins
- Gradually expand to medium confidence matches
- Use the phased approach to minimize disruption

## Getting Help

If you run into issues:
1. Check the error message in the terminal
2. Verify all required files are present
3. Ask our camp staff for assistance
4. Check the troubleshooting section above
5. Don't hesitate to experiment - the dashboard is designed to be robust!

## Resources for Further Learning

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Data Analysis](https://pandas.pydata.org/docs/)
- [Scikit-learn Machine Learning](https://scikit-learn.org/stable/)
- [Plotly Visualization](https://plotly.com/python/)
- [Small Business Administration](https://www.sba.gov/)

## Project Impact

This dashboard demonstrates how AI can create real-world value by:
- **Increasing Efficiency**: Automates manual supplier research
- **Improving Accuracy**: Uses data-driven matching instead of guesswork
- **Enabling Strategy**: Provides clear roadmaps for achieving diversity goals
- **Supporting Small Business**: Helps identify opportunities for underrepresented suppliers

---

**Remember**: The goal isn't just to build a dashboard, but to understand how AI can solve complex business problems. Every feature demonstrates a different aspect of data science and machine learning in action.

Happy analyzing! 🚀

---

🎓 **Cal Poly SLO AI Summer Camp Project**  
*Empowering Small Businesses Through Data-Driven Procurement*
