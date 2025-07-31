# 🌐 Deploy Your Supplier Diversity Dashboard

**Make your Cal Poly AI Summer Camp project accessible to anyone on the web!**

## 🚀 **Option 1: Streamlit Community Cloud** (Recommended - FREE)

Perfect for academic projects, portfolios, and sharing with classmates/professors.

### **Step 1: Prepare Your Code**

1. **Make sure your project works locally first:**
   ```bash
   python run_po_dashboard.py
   ```

2. **Check that all files are in your project:**
   ```
   supplier-diversity/
   ├── frontend/po_quantity_dashboard.py  ✅ Main app
   ├── backend/*.csv                      ✅ Data files
   ├── requirements.txt                   ✅ Dependencies
   └── run_po_dashboard.py               ✅ Local runner
   ```

### **Step 2: Push to GitHub**

1. **Initialize Git (if not already done):**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Supplier Diversity Dashboard"
   ```

2. **Create a GitHub repository:**
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it: `supplier-diversity-dashboard`
   - Make it **Public** (required for free Streamlit hosting)
   - Don't initialize with README (you already have one)

3. **Push your code:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/supplier-diversity-dashboard.git
   git branch -M main
   git push -u origin main
   ```

### **Step 3: Deploy on Streamlit Cloud**

1. **Go to Streamlit Cloud:**
   - Visit: [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign up" and use your GitHub account

2. **Create New App:**
   - Click "New app"
   - **Repository:** Select `YOUR_USERNAME/supplier-diversity-dashboard`
   - **Branch:** `main`
   - **Main file path:** `frontend/po_quantity_dashboard.py`
   - **App URL:** Choose a custom name like `cal-poly-supplier-diversity`

3. **Deploy:**
   - Click "Deploy!"
   - Wait 2-3 minutes for deployment
   - Your app will be live at: `https://YOUR_APP_NAME.streamlit.app`

### **Step 4: Share Your Dashboard**

🎉 **Your dashboard is now live!** Share the URL with:
- Classmates and professors
- Potential employers (great for portfolios!)
- Anyone interested in supplier diversity analysis

---

## 🔧 **Troubleshooting**

### **Common Issues:**

**❌ "File not found" error:**
- Make sure the main file path is exactly: `frontend/po_quantity_dashboard.py`

**❌ "Module not found" error:**
- Check that `requirements.txt` includes all dependencies:
  ```
  streamlit>=1.40.0
  plotly>=5.0.0
  pandas>=2.0.0
  numpy>=1.20.0
  scikit-learn>=1.0.0
  ```

**❌ "Data files not found" error:**
- Ensure all CSV files in `backend/` are committed to Git
- Check file paths in your Python code

### **Need to Update Your App?**
Just push changes to GitHub:
```bash
git add .
git commit -m "Update dashboard"
git push
```
Streamlit will automatically redeploy!

---

## 🌟 **Alternative Deployment Options**

### **Option 2: Heroku** (Simple but $5-7/month)
- More control over environment
- Good for production applications
- Requires credit card for hosting

### **Option 3: AWS/Google Cloud** (Advanced)
- Professional deployment
- Requires cloud knowledge
- Good for enterprise use

### **Option 4: GitHub Pages + Streamlit** (Hybrid)
- Host project documentation on GitHub Pages
- Link to Streamlit app for the dashboard

---

## 📋 **Pre-Deployment Checklist**

- [ ] Dashboard runs locally without errors
- [ ] All data files are included in the repository
- [ ] `requirements.txt` is complete and accurate
- [ ] Repository is public on GitHub
- [ ] Main file path is correct: `frontend/po_quantity_dashboard.py`
- [ ] No sensitive data (API keys, passwords) in the code

---

## 🎓 **For Your Cal Poly Project**

**Perfect for:**
- ✅ Class presentations
- ✅ Portfolio demonstrations
- ✅ Sharing with professors
- ✅ Job interviews
- ✅ Academic conferences

**Your deployed dashboard shows:**
- Professional data analysis skills
- Modern web development knowledge
- Real-world problem-solving ability
- Clean, accessible data visualization

---

**🚀 Ready to deploy? Start with Step 1 above!**

*Questions? Check the [Streamlit Community Cloud docs](https://docs.streamlit.io/streamlit-community-cloud) or ask for help!*
