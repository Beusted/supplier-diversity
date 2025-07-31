# Diversity in Procurement Dashboard

A comprehensive web application for analyzing and visualizing supplier diversity in procurement data, built with Streamlit and featuring Cal Poly's brand aesthetic.

## Features

### Core Functionality
- **Data Upload**: Upload Excel spreadsheets containing procurement data
- **Report Generation**: Generate comprehensive diversity reports with key metrics
- **Data Visualization**: Create pie charts and comparison charts for original and optimized data
- **Data Optimization**: Backend integration for data optimization (placeholder functionality)

### User Interface
- **Top Navigation Bar**: Clean navigation with Home, Dashboard, and Reports
- **Responsive Design**: Optimized for desktop and mobile viewing
- **Cal Poly Branding**: Consistent use of Cal Poly green (#154734) and gold (#ffc72c)
- **Modern Styling**: Glass-morphism effects and smooth animations

### Interactive Features
- **Sticky Chatbot**: AI assistant positioned at bottom-right corner
- **Real-time Updates**: Dynamic content updates based on user actions
- **Data Preview**: Interactive data tables with original and optimized views

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd supplier-diversity
   ```

2. Run the application:
   ```bash
   python run_app.py
   ```
   This will automatically install dependencies and launch the Streamlit app.

### Manual Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

3. Open your browser to `http://localhost:8501`

## Usage

### 1. Upload Data
- Click on the file uploader in the "Data Upload" section
- Select an Excel file (.xlsx or .xls) containing your procurement data
- Preview the uploaded data to ensure it loaded correctly

### 2. Generate Reports
- Click "Generate Report" to create a comprehensive analysis
- View key metrics including total suppliers, diversity percentages, and spending analysis
- Review insights and recommendations

### 3. Create Visualizations
- Click "Generate Charts" to create pie charts and comparison visualizations
- Compare original data distribution with optimized scenarios
- Analyze diversity improvements across different supplier categories

### 4. Optimize Data
- Click "Optimize Data" to run backend optimization algorithms
- Compare original vs. optimized data in the data overview section
- View improvement metrics in the comparison charts

### 5. Use the Chatbot
- Click the chat icon (?) in the bottom-right corner
- Ask questions about your data, reports, or how to use the application
- Get real-time assistance with procurement diversity analysis

## File Structure

```
supplier-diversity/
├── streamlit_app.py      # Main Streamlit application
├── run_app.py           # Launch script with dependency management
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── FrontEnd.py         # Legacy Streamlit component
├── index.html          # Legacy HTML PDF viewer
├── script.js           # Legacy JavaScript functionality
└── styles.css          # Legacy CSS styling
```

## Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualizations
- **OpenPyXL**: Excel file reading/writing
- **NumPy**: Numerical computing

### Styling
- Custom CSS with Cal Poly brand colors
- Glass-morphism design elements
- Responsive layout with CSS Grid and Flexbox
- Google Fonts (Inter) for typography

### Data Processing
- Excel file upload and validation
- Data preview and summary statistics
- Mock optimization algorithms (placeholder for backend integration)
- Interactive data tables with filtering capabilities

## Development

### Adding New Features
1. Modify `streamlit_app.py` for new functionality
2. Update CSS styling in the custom CSS section
3. Add new dependencies to `requirements.txt`
4. Update this README with new feature documentation

### Customization
- **Colors**: Modify the CSS color variables to change the theme
- **Layout**: Adjust the Streamlit columns and containers
- **Charts**: Customize Plotly chart configurations
- **Branding**: Update logos and text in the navigation bar

## Future Enhancements

- [ ] Backend API integration for real data optimization
- [ ] User authentication and session management
- [ ] Advanced filtering and search capabilities
- [ ] Export functionality for reports and charts
- [ ] Real-time data updates and notifications
- [ ] Multi-language support
- [ ] Advanced analytics and machine learning insights

## Support

For questions, issues, or feature requests, please contact the development team or create an issue in the repository.

---

**Built with love using Streamlit and Cal Poly pride**