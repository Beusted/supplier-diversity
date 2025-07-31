# Small Business Supplier Diversity Dashboard

## Overview
The Small Business Supplier Diversity Dashboard is an innovative AI-powered analytics platform designed to help organizations achieve their small business procurement goals. It leverages machine learning algorithms and data analytics to analyze current procurement patterns, identify gaps, and provide actionable recommendations for transitioning purchase orders to small businesses. The dashboard specifically focuses on reaching the 25% small business procurement target through data-driven insights and strategic planning.

## Key Features
- **AI-Powered Supplier Matching**: Uses machine learning algorithms to identify optimal supplier transition opportunities based on similarity analysis.
- **Real-Time Analytics**: Comprehensive dashboard showing current procurement status (16.3% of POs to small businesses) versus the 25% target.
- **Strategic Planning Tools**: Provides phased implementation plans with confidence levels and timeline recommendations.
- **Interactive Visualization**: Dynamic charts, tables, and metrics that adapt to light/dark themes for optimal user experience.
- **Gap Analysis**: Calculates precise requirements (110 POs need transition) and provides actionable roadmaps.

## Technologies
- **Programming Language**: Python
- **Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn (TF-IDF, Cosine Similarity)
- **Visualization**: Plotly, Interactive Charts
- **Styling**: Custom CSS with Cal Poly branding

## Installation and Setup
1. Clone the repository to your local machine.
2. Install required dependencies:
   ```bash
   pip install streamlit plotly pandas numpy scikit-learn pathlib
   ```
3. Ensure all CSV data files are present in the `backend/` directory.
4. Run the dashboard:
   ```bash
   python run_po_dashboard.py
   ```
5. Access the dashboard via http://localhost:8503

## Usage
- Navigate through different sections using the top navigation bar (Dashboard, Settings, About).
- Toggle between light and dark themes using the Settings panel.
- Explore various analytics sections including current state analysis, transition scenarios, and implementation planning.
- Review detailed supplier matching recommendations and quick wins for immediate impact.
- Use the phased implementation plan to develop a strategic roadmap for achieving the 25% target.

## Customization
- The dashboard primarily targets a 25% small business procurement goal, but this can be modified in `po_quantity_analytics.py`.
- To adjust similarity thresholds or matching algorithms, modify the parameters in the supplier matching functions.
- Color themes and styling can be customized through the CSS variables in the dashboard file.
- Data sources can be updated by replacing CSV files in the `backend/` directory with your organization's procurement data.

## Contributing
- Contributions are welcome! Please make a pull request to propose changes or enhancements.
- Areas for contribution include: additional analytics features, improved visualization options, enhanced matching algorithms, or mobile responsiveness improvements.
- For questions or collaboration opportunities, reach out to [instructor-email@calpoly.edu].

## Support and Feedback
- The dashboard includes comprehensive error handling and troubleshooting guidance.
- For technical support, check the troubleshooting section or contact the development team.
- Feature requests and feedback can be submitted through the project repository or direct contact.
- Educational support for understanding AI concepts and procurement analytics is available through Cal Poly AI Summer Camp resources.

## Project Impact
This dashboard demonstrates practical applications of AI in procurement by:
- Automating supplier research and matching processes
- Providing data-driven insights for strategic decision making
- Supporting small business growth through improved procurement opportunities
- Showcasing how machine learning can solve real-world business challenges

---

🎓 **Cal Poly SLO AI Summer Camp Project**  
*Empowering Small Businesses Through Data-Driven Procurement Analytics*
