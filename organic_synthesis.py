import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Organic Synthesis Database",
    page_icon="🧪",
    layout="wide"
)

# Title and description
st.title("🧪 Organic Synthesis Reaction Database")
st.markdown("Explore various organic synthesis reactions with detailed information.")

# Common names dictionary
COMMON_NAMES = {
    "diazomethane": "CH2N2", "silver oxide": "Ag2O", "diketone": "RCOCOR",
    "diol": "R(OH)R(OH)", "sulfonyl chloride": "RSO2Cl", "quaternary ammonium": "R4N+ OH-",
    "hydroxylamine": "NH2OH", "oxime": "RR'C=NOH", "nitroso compound": "RNO",
    "formaldehyde": "HCHO", "formic acid": "HCOOH", "sodium cyanide": "NaCN",
    "phenol": "C6H5OH", "quinoline": "C9H7N", "nitro compound": "RNO2",
    "carboxylic acid": "RCOOH", "haloform": "CHX3", "alkene": "R2C=CR2",
    "aldehyde": "RCHO", "ketone": "RCOR'", "alkane": "RH", "amine": "RNH2",
    "isocyanate": "RNCO", "isothiocyanate": "RNCS", "amide": "RCONH2",
    "alcohol": "ROH", "alkyl halide": "RX", "aryl halide": "ArX"
}

# Comprehensive reaction database
SYNTHESIS_DB = {
    "Arndt-Eistert Reaction": {
        "reactants": "RCOOH + CH₂N₂",
        "products": "RCH₂COOH",
        "description": "Homologation of carboxylic acids via diazomethane and Wolff rearrangement",
        "mechanism": "Diazoketone formation, Wolff rearrangement",
        "year": 1935,
        "chemist": "Fritz Arndt and Bernd Eistert"
    },
    "Hofmann Degradation": {
        "reactants": "RCONH₂ + Br₂ + NaOH",
        "products": "RNH₂ + CO₂",
        "description": "Conversion of primary amides to primary amines with loss of one carbon atom",
        "mechanism": "Hypobromite intermediate, isocyanate formation",
        "year": 1881,
        "chemist": "August Wilhelm von Hofmann"
    },
    "Pinacol Reduction": {
        "reactants": "2 R₂C=O",
        "products": "R₂C(OH)C(OH)R₂",
        "description": "Reductive coupling of carbonyl compounds to form 1,2-diols",
        "mechanism": "Single electron transfer, radical coupling",
        "year": 1859,
        "chemist": "Rudolph Fittig"
    },
    "Pinacol-Pinacolone Rearrangement": {
        "reactants": "R₂C(OH)C(OH)R₂",
        "products": "R₂C(O)CR₂",
        "description": "Acid-catalyzed rearrangement of 1,2-diols to carbonyl compounds",
        "mechanism": "Carbocation rearrangement",
        "year": 1860,
        "chemist": "Rudolph Fittig"
    },
    "Pfitzer Reaction": {
        "reactants": "R₂C(OH)CH₂R'",
        "products": "R₂C=CR'",
        "description": "Dehydration of tertiary alcohols to alkenes",
        "mechanism": "E1 elimination",
        "year": 1892,
        "chemist": "Wilhelm Pfitzer"
    },
    "Paal-Knorr Synthesis": {
        "reactants": "1,4-dicarbonyl compound + NH₃ or amine",
        "products": "pyrrole or substituted pyrrole",
        "description": "Formation of pyrroles from 1,4-dicarbonyl compounds and ammonia or primary amines",
        "mechanism": "Condensation and cyclization",
        "year": 1885,
        "chemist": "Carl Paal and Ludwig Knorr"
    },
    "Oppenauer Oxidation": {
        "reactants": "RCH₂OH + (CH₃)₂C=O",
        "products": "RCHO + (CH₃)₂CHOH",
        "description": "Oxidation of secondary alcohols to ketones using aluminum isopropoxide",
        "mechanism": "Hydride transfer",
        "year": 1937,
        "chemist": "Rupert Viktor Oppenauer"
    },
    "Orton Rearrangement": {
        "reactants": "ArNClCOR",
        "products": "ClArNHCOR",
        "description": "Rearrangement of N-chloroacyl anilines to chloro anilides",
        "mechanism": "Ion pair dissociation/recombination",
        "year": 1899,
        "chemist": "Kennedy Joseph Orton"
    },
    "Meerwein-Ponndorf-Verley Reduction": {
        "reactants": "R₂C=O + (CH₃)₂CHOH",
        "products": "R₂CHOH + (CH₃)₂C=O",
        "description": "Reduction of ketones to secondary alcohols using aluminum isopropoxide",
        "mechanism": "Hydride transfer via aluminum alkoxide",
        "year": 1925,
        "chemist": "Hans Meerwein, Wolfgang Ponndorf, and Albert Verley"
    },
    "Meerwein Reaction": {
        "reactants": "ArN₂⁺ + CH₂=CHR",
        "products": "ArCH₂CH₂R",
        "description": "Arylation of alkenes using arenediazonium salts",
        "mechanism": "Radical addition",
        "year": 1939,
        "chemist": "Hans Meerwein"
    },
    "Lossen Rearrangement": {
        "reactants": "RCONHOH",
        "products": "RNCO",
        "description": "Conversion of hydroxamic acids to isocyanates",
        "mechanism": "O-acylation, rearrangement",
        "year": 1872,
        "chemist": "Wilhelm Lossen"
    },
    "Lobry de Bruyn-van Ekenstein Rearrangement": {
        "reactants": "aldose",
        "products": "ketose",
        "description": "Base-catalyzed isomerization of aldoses to ketoses",
        "mechanism": "Enolization",
        "year": 1895,
        "chemist": "Cornelis Adriaan Lobry van Troostenburg de Bruyn and Willem Alberda van Ekenstein"
    },
    "Leuckart Reaction": {
        "reactants": "R₂C=O + HCOONH₄",
        "products": "R₂CHNH₂",
        "description": "Reductive amination of carbonyl compounds using formamide or ammonium formate",
        "mechanism": "Iminium ion formation, reduction",
        "year": 1885,
        "chemist": "Rudolf Leuckart"
    },
    "Lederer-Manasse Reaction": {
        "reactants": "phenol + CH₂O",
        "products": "o-HOC₆H₄CH₂OH",
        "description": "Hydroxymethylation of phenols with formaldehyde",
        "mechanism": "Electrophilic aromatic substitution",
        "year": 1894,
        "chemist": "Lederer and Manasse"
    },
    "Kolbe-Schmitt Synthesis": {
        "reactants": "phenol + CO₂",
        "products": "salicylic acid",
        "description": "Carboxylation of phenols to hydroxybenzoic acids",
        "mechanism": "Electrophilic aromatic substitution",
        "year": 1860,
        "chemist": "Adolph Wilhelm Hermann Kolbe and Rudolf Schmitt"
    },
    "Kolbe Electrolytic Synthesis": {
        "reactants": "2 RCOO⁻",
        "products": "R-R + 2 CO₂",
        "description": "Electrochemical decarboxylative dimerization of carboxylates",
        "mechanism": "Radical formation and coupling",
        "year": 1849,
        "chemist": "Adolph Wilhelm Hermann Kolbe"
    },
    "Kiliani Reaction": {
        "reactants": "aldose + HCN",
        "products": "higher aldose",
        "description": "Chain elongation of aldoses via cyanohydrin formation and hydrolysis",
        "mechanism": "Cyanohydrin formation, hydrolysis, reduction",
        "year": 1886,
        "chemist": "Heinrich Kiliani"
    },
    "Hofmann Mustard Oil Reaction": {
        "reactants": "RNH₂ + CS₂",
        "products": "RNCS",
        "description": "Conversion of primary amines to isothiocyanates via dithiocarbamates",
        "mechanism": "Dithiocarbamate formation, decomposition",
        "year": 1868,
        "chemist": "August Wilhelm von Hofmann"
    },
    "Hofmann Exhaustive Methylation": {
        "reactants": "R₃N + CH₃I → R₄N⁺I⁻ → R₄N⁺OH⁻ → alkene",
        "products": "alkene + trimethylamine",
        "description": "Degradation of amines to alkenes via quaternary ammonium hydroxides",
        "mechanism": "Hofmann elimination",
        "year": 1851,
        "chemist": "August Wilhelm von Hofmann"
    },
    "Markovnikov's Rule": {
        "reactants": "asymmetric addition to alkenes",
        "products": "rich get richer",
        "description": "Prediction of regiochemistry in electrophilic additions to alkenes",
        "mechanism": "Carbocation stability",
        "year": 1870,
        "chemist": "Vladimir Markovnikov"
    },
    "Houben-Hoesch Synthesis": {
        "reactants": "ArH + RCN",
        "products": "ArC(O)R",
        "description": "Acylation of arenes with nitriles in the presence of Lewis acids",
        "mechanism": "Electrophilic aromatic substitution",
        "year": 1915,
        "chemist": "J. Houben, K. Hoesch"
    },
    "Hunsdieker Reaction": {
        "reactants": "RCOOAg + Br2",
        "products": "RBr + CO2 + AgBr",
        "description": "Decarboxylative bromination of silver carboxylates",
        "mechanism": "Radical decarboxylation",
        "year": 1942,
        "chemist": "Heinrich Hunsdieker"
    },
    "Hoffmann-Martius Rearrangement": {
        "reactants": "C6H5NHR",
        "products": "o/p-R-C6H4NH2",
        "description": "Acid-catalyzed rearrangement of N-alkyl anilines to alkyl anilines",
        "mechanism": "Intramolecular electrophilic substitution",
        "year": 1868,
        "chemist": "August Wilhelm von Hofmann, Carl Alexander Martius"
    }
}

# Sidebar for navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", ["Reaction Search", "Common Names", "All Reactions"])

# Reaction Search Section
if section == "Reaction Search":
    st.header("🔍 Search Organic Reactions")
    
    # Search options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("Search by reaction name:", placeholder="e.g., Hofmann, Kolbe, etc.")
    
    with col2:
        search_by = st.selectbox("Search by:", ["Reaction Name", "Chemist", "Reactants"])
    
    # Filter reactions based on search
    filtered_reactions = {}
    
    if search_term:
        search_term_lower = search_term.lower()
        for name, data in SYNTHESIS_DB.items():
            if search_by == "Reaction Name" and search_term_lower in name.lower():
                filtered_reactions[name] = data
            elif search_by == "Chemist" and search_term_lower in data["chemist"].lower():
                filtered_reactions[name] = data
            elif search_by == "Reactants" and search_term_lower in data["reactants"].lower():
                filtered_reactions[name] = data
    else:
        filtered_reactions = SYNTHESIS_DB
    
    # Display results
    if filtered_reactions:
        st.subheader(f"Found {len(filtered_reactions)} reaction(s)")
        
        for reaction_name, data in filtered_reactions.items():
            with st.expander(f"{reaction_name}** ({data['year']})"):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.write(f"*Reactants:* {data['reactants']}")
                    st.write(f"*Products:* {data['products']}")
                    st.write(f"*Chemist(s):* {data['chemist']}")
                
                with col2:
                    st.write(f"*Year:* {data['year']}")
                    st.write(f"*Mechanism:* {data['mechanism']}")
                
                st.write(f"*Description:* {data['description']}")
    else:
        st.warning("No reactions found matching your search criteria.")

# Common Names Section
elif section == "Common Names":
    st.header("📚 Common Chemical Names")
    
    # Convert to DataFrame for better display
    common_names_df = pd.DataFrame(list(COMMON_NAMES.items()), columns=["Common Name", "Formula"])
    
    # Search in common names
    search_common = st.text_input("Search common names:", placeholder="e.g., phenol, aldehyde, etc.")
    
    if search_common:
        filtered_common = common_names_df[common_names_df["Common Name"].str.contains(search_common, case=False)]
        st.dataframe(filtered_common, use_container_width=True)
    else:
        st.dataframe(common_names_df, use_container_width=True)

# All Reactions Section
elif section == "All Reactions":
    st.header("📖 All Organic Reactions")
    
    # Convert to DataFrame for better display
    reactions_data = []
    for name, data in SYNTHESIS_DB.items():
        reactions_data.append({
            "Reaction Name": name,
            "Reactants": data["reactants"],
            "Products": data["products"],
            "Chemist": data["chemist"],
            "Year": data["year"]
        })
    
    reactions_df = pd.DataFrame(reactions_data)
    st.dataframe(reactions_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("### 🧪 Organic Synthesis Database")
st.markdown("A comprehensive collection of organic chemical reactions and their properties.")

# Add some statistics
if section == "Reaction Search" and not search_term:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Database Statistics")
    st.sidebar.write(f"*Total Reactions:* {len(SYNTHESIS_DB)}")
    
    # Count reactions by century
    centuries = {}
    for data in SYNTHESIS_DB.values():
        century = (data['year'] // 100) * 100
        centuries[century] = centuries.get(century, 0) + 1
    
    st.sidebar.write("*Reactions by Century:*")
    for century, count in sorted(centuries.items()):
        st.sidebar.write(f"- {century}s: {count} reactions")