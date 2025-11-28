markdown
# Organic Synthesis Applications

This repository contains comprehensive organic chemistry applications built with Streamlit for students, researchers, and educators.

## 📁 Applications

### 1. 🧪 Organic Synthesis Reaction Database (Basic)
**File:** `organic_synthesis.py`

A comprehensive database of organic chemical reactions with search and filtering capabilities.

#### Features:
- Search reactions by name, chemist, or reactants
- Common chemical names dictionary
- Complete reaction database browsing
- Reaction mechanisms and historical information
- User-friendly interface with sidebar navigation

#### Usage:
bash
streamlit run organic_synthesis.py


---

2. 🔬 Comprehensive Organic Synthesis Analyzer

File: streamlit_org_synthesis_comprehensive.py

An advanced version with additional features for in-depth reaction analysis and study.

Enhanced Features:

· Advanced search and filtering options
· Reaction mechanism visualizations
· Study mode with quizzes and flashcards
· Reaction pathway planning
· Export capabilities
· More detailed reaction information

Usage:

bash
streamlit run streamlit_org_synthesis_comprehensive.py


---

🚀 Quick Start

Installation

bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
pip install -r requirements.txt


Running Applications

bash
# Run Basic Version
streamlit run organic_synthesis.py

# Run Comprehensive Version  
streamlit run streamlit_org_synthesis_comprehensive.py


📋 File Structure


repository/
├── organic_synthesis.py                    # Basic organic synthesis database
├── streamlit_org_synthesis_comprehensive.py # Advanced comprehensive version
├── requirements.txt                        # Python dependencies
└── README.md                              # This file


📦 Dependencies

requirements.txt:

txt
streamlit>=1.28.0
pandas>=1.5.0
matplotlib>=3.5.0
plotly>=5.15.0
seaborn>=0.12.0


Install all dependencies:

bash
pip install -r requirements.txt


🎯 Application Comparison

Feature Basic Version Comprehensive Version
Reaction Search ✅ ✅
Common Names Dictionary ✅ ✅
Mechanism Details ✅ ✅
Advanced Filtering ❌ ✅
Study Mode ❌ ✅
Reaction Pathways ❌ ✅
Data Export ❌ ✅
Visualizations Basic Advanced

📊 Database Content

Both applications include information on 23+ organic reactions:

Key Reactions Included:

· Arndt-Eistert Reaction - Carboxylic acid homologation
· Hofmann Degradation - Amide to amine conversion
· Pinacol Reduction & Rearrangement - Diol chemistry
· Paal-Knorr Synthesis - Pyrrole formation
· Kolbe-Schmitt Synthesis - Salicylic acid production
· Markovnikov's Rule - Addition reaction regiochemistry
· Meerwein-Ponndorf-Verley Reduction - Ketone reduction
· And 15+ more classical reactions...

Each Reaction Includes:

· Reactants and products with proper chemical notation
· Detailed mechanistic descriptions
· Historical context (year, chemist)
· Step-by-step reaction mechanisms
· Educational descriptions

🔧 For Educators

Classroom Use:

· Basic Version: Ideal for introductory organic chemistry
· Comprehensive Version: Suitable for advanced courses and research

Customization:

Both applications can be easily extended by modifying the SYNTHESIS_DB dictionary:

python
"New Reaction Name": {
    "reactants": "Reactant formulas",
    "products": "Product formulas",
    "description": "Educational description",
    "mechanism": "Step-by-step mechanism",
    "year": 2024,
    "chemist": "Discoverer Name",
    "conditions": "Reaction conditions",
    "applications": "Practical uses"
}


🎮 Usage Guide

Basic Version (organic_synthesis.py)

1. Reaction Search: Use the search bar to find specific reactions
2. Common Names: Look up chemical compound names and formulas
3. Browse All: View complete database in table format
4. Details: Click on reactions to expand and see full information

Comprehensive Version (streamlit_org_synthesis_comprehensive.py)

1. Advanced Search: Filter by multiple criteria simultaneously
2. Study Mode: Test knowledge with interactive quizzes
3. Pathway Planning: Design multi-step syntheses
4. Data Export: Download reaction information for offline use
5. Visualizations: View reaction mechanisms graphically

🤝 Contributing

Adding New Reactions

Edit the SYNTHESIS_DB dictionary in either application:

python
"Reaction Name": {
    "reactants": "RCOOH + CH₂N₂",
    "products": "RCH₂COOH", 
    "description": "Homologation of carboxylic acids...",
    "mechanism": "Diazoketone formation, Wolff rearrangement...",
    "year": 1935,
    "chemist": "Fritz Arndt and Bernd Eistert",
    "conditions": "Diazomethane, heat",
    "applications": "Chain elongation in synthesis"
}


🆘 Troubleshooting

Common Issues

Module Not Found Errors:

bash
pip install --upgrade streamlit pandas matplotlib plotly seaborn


Application Won't Start:

· Ensure Python 3.7+ is installed
· Check all dependencies are installed
· Verify file paths are correct

Display Issues:

· Clear browser cache
· Check console for error messages
· Ensure compatible browser version

📚 Educational Value

For Students:

· Quick reference for reaction mechanisms
· Understanding historical development of reactions
· Study aid for organic chemistry exams
· Visual learning of complex mechanisms

For Researchers:

· Quick lookup of reaction conditions
· Historical context for literature research
· Teaching resource preparation
· Reaction pathway inspiration

📄 License

Educational Use - Open for academic and research purposes.

---

🔗 Related Resources

· Organic Chemistry Portal
· Reaction Flashcard Apps
· Streamlit Documentation

💡 Tips

· Use the comprehensive version for research and advanced study
· Use the basic version for quick reference and teaching
· Both apps work on mobile devices for on-the-go access
· Bookmark frequently used reactions for quick access

---

Perfect for organic chemistry courses, research labs, and self-study!



And here's the corresponding requirements.txt:

txt
# Requirements for Organic Synthesis Applications
streamlit>=1.28.0
pandas>=1.5.0
matplotlib>=3.5.0
plotly>=5.15.0
seaborn>=0.12.0


This README.md now:

1. Focuses exclusively on the two organic synthesis applications
2. Compares both versions clearly (basic vs comprehensive)
3. Provides specific usage instructions for each application
4. Highlights educational value for different user types
5. Includes proper installation and troubleshooting guidance
6. Shows how to extend the reaction database
7. Clear file structure showing only the relevant Python files

The repository structure would be:


your-repo/
├── organic_synthesis.py
├── streamlit_org_synthesis_comprehensive.py
├── requirements.txt
└── README.md


Users can now easily understand they have two versions of the same organic synthesis application and choose which one to run based on their needs!
