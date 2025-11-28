import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, AllChem
from rdkit.Chem.Draw import MolDraw2DCairo
import pandas as pd
import re
import io
from PIL import Image

# Compound Database
def get_compound_database():
    return {
        # Alcohols
        'benzyl alcohol': 'c1ccccc1CO',
        'ethanol': 'CCO',
        'methanol': 'CO',
        'cyclohexanol': 'OC1CCCCC1',
        'isopropanol': 'CC(C)O',
        
        # Aldehydes
        'benzaldehyde': 'c1ccccc1C=O',
        'acetaldehyde': 'CC=O',
        'formaldehyde': 'C=O',
        'propionaldehyde': 'CCC=O',
        
        # Carboxylic acids
        'benzoic acid': 'c1ccccc1C(=O)O',
        'acetic acid': 'CC(=O)O',
        'formic acid': 'OC=O',
        'propionic acid': 'CCC(=O)O',
        
        # Ketones
        'acetophenone': 'CC(=O)c1ccccc1',
        'acetone': 'CC(=O)C',
        'cyclohexanone': 'O=C1CCCCC1',
        'butanone': 'CCC(=O)C',
        
        # Aromatic compounds
        'toluene': 'Cc1ccccc1',
        'benzene': 'c1ccccc1',
        'phenol': 'Oc1ccccc1',
        'aniline': 'Nc1ccccc1',
        'nitrobenzene': 'O=[N+]([O-])c1ccccc1',
        'bromobenzene': 'Brc1ccccc1',
        'chlorobenzene': 'Clc1ccccc1',
        'iodobenzene': 'Ic1ccccc1',
        'anisole': 'COc1ccccc1',
        
        # Esters and derivatives
        'methyl benzoate': 'COC(=O)c1ccccc1',
        'ethyl acetate': 'CCOC(=O)C',
        'acetanilide': 'CC(=O)Nc1ccccc1',
        'acetyl chloride': 'CC(=O)Cl',
        'acetic anhydride': 'CC(=O)OC(=O)C',
        
        # Amines and amides
        'methylamine': 'CN',
        'dimethylamine': 'CNC',
        'trimethylamine': 'CN(C)C',
        'acetamide': 'CC(=O)N',
        
        # Alkenes and alkanes
        'ethylene': 'C=C',
        'acetylene': 'C#C',
        'cyclohexane': 'C1CCCCC1',
        'hexane': 'CCCCCC'
    }

# Enhanced Reaction Pathways
def get_reaction_pathways():
    return {
        'oxidation': [
            {
                'name': 'Primary Alcohol Oxidation',
                'A': 'c1ccccc1CO',      # Benzyl alcohol
                'B': 'c1ccccc1C=O',     # Benzaldehyde
                'C': 'c1ccccc1C(=O)O',  # Benzoic acid
                'description': 'Primary alcohol → Aldehyde → Carboxylic acid',
                'reagents': ['KMnO₄', 'K₂Cr₂O₇/H₂SO₄', 'Jones reagent'],
                'mechanism': 'Stepwise oxidation via chromate ester intermediate'
            },
            {
                'name': 'Toluene Oxidation',
                'A': 'Cc1ccccc1',       # Toluene
                'B': 'c1ccccc1C=O',     # Benzaldehyde
                'C': 'c1ccccc1C(=O)O',  # Benzoic acid
                'description': 'Alkyl benzene → Aldehyde → Carboxylic acid',
                'reagents': ['KMnO₄', 'Heat', 'Co/Mn catalysts'],
                'mechanism': 'Radical mechanism with benzylic hydrogen abstraction'
            },
            {
                'name': 'Alkene Oxidation',
                'A': 'C=CC',           # Propene
                'B': 'CC(=O)C',        # Acetone
                'description': 'Alkene → Ketone (Ozonolysis)',
                'reagents': ['O₃, then Zn/H₂O'],
                'mechanism': 'Ozonolysis followed by reductive workup'
            }
        ],
        'reduction': [
            {
                'name': 'Nitro Reduction',
                'A': 'c1ccccc1',           # Benzene
                'B': 'O=[N+]([O-])c1ccccc1', # Nitrobenzene
                'C': 'Nc1ccccc1',          # Aniline
                'description': 'Benzene → Nitrobenzene → Aniline',
                'reagents': ['HNO₃/H₂SO₄', 'Sn/HCl', 'Fe/HCl', 'H₂/Pd'],
                'mechanism': 'Electrophilic aromatic substitution followed by nitro reduction'
            },
            {
                'name': 'Carbonyl Reduction',
                'A': 'CC(=O)c1ccccc1',     # Acetophenone
                'B': 'CC(O)c1ccccc1',      # 1-Phenylethanol
                'description': 'Ketone → Secondary alcohol',
                'reagents': ['NaBH₄', 'LiAlH₄'],
                'mechanism': 'Nucleophilic addition of hydride ion'
            },
            {
                'name': 'Carboxylic Acid Reduction',
                'A': 'c1ccccc1C(=O)O',     # Benzoic acid
                'B': 'c1ccccc1CO',         # Benzyl alcohol
                'description': 'Carboxylic acid → Primary alcohol',
                'reagents': ['LiAlH₄', 'BH₃'],
                'mechanism': 'Nucleophilic acyl substitution followed by reduction'
            }
        ],
        'esterification': [
            {
                'name': 'Fischer Esterification',
                'A': 'c1ccccc1C(=O)O',     # Benzoic acid
                'B': 'COC(=O)c1ccccc1',    # Methyl benzoate
                'description': 'Carboxylic acid → Ester',
                'reagents': ['CH₃OH/H₂SO₄', 'Heat', 'Acid catalyst'],
                'mechanism': 'Nucleophilic acyl substitution with acid catalysis'
            },
            {
                'name': 'Acyl Chloride Route',
                'A': 'c1ccccc1C(=O)O',     # Benzoic acid
                'B': 'CC(=O)Cl',           # Acetyl chloride (intermediate)
                'C': 'COC(=O)c1ccccc1',    # Methyl benzoate
                'description': 'Acid → Acyl chloride → Ester',
                'reagents': ['SOCl₂', 'CH₃OH'],
                'mechanism': 'Conversion to acyl chloride followed by alcoholysis'
            }
        ],
        'hydrolysis': [
            {
                'name': 'Ester Hydrolysis',
                'A': 'COC(=O)c1ccccc1',    # Methyl benzoate
                'B': 'c1ccccc1C(=O)O',     # Benzoic acid
                'description': 'Ester → Carboxylic acid',
                'reagents': ['NaOH/H₂O', 'H₃O⁺'],
                'mechanism': 'Nucleophilic acyl substitution (basic or acidic)'
            },
            {
                'name': 'Amide Hydrolysis',
                'A': 'CC(=O)Nc1ccccc1',    # Acetanilide
                'B': 'Nc1ccccc1',          # Aniline
                'C': 'CC(=O)O',            # Acetic acid
                'description': 'Amide → Amine + Carboxylic acid',
                'reagents': ['NaOH/H₂O', 'H₃O⁺', 'Heat'],
                'mechanism': 'Nucleophilic acyl substitution under vigorous conditions'
            }
        ],
        'acetylation': [
            {
                'name': 'Amine Acetylation',
                'A': 'Nc1ccccc1',          # Aniline
                'B': 'CC(=O)Nc1ccccc1',    # Acetanilide
                'description': 'Amine → Amide',
                'reagents': ['Acetic anhydride', 'Pyridine', 'Acetyl chloride'],
                'mechanism': 'Nucleophilic acyl substitution'
            },
            {
                'name': 'Alcohol Acetylation',
                'A': 'c1ccccc1CO',         # Benzyl alcohol
                'B': 'COC(=O)c1ccccc1',    # Benzyl acetate
                'description': 'Alcohol → Ester',
                'reagents': ['Acetic anhydride', 'Acetyl chloride', 'Pyridine'],
                'mechanism': 'Nucleophilic acyl substitution'
            }
        ],
        'halogenation': [
            {
                'name': 'Aromatic Bromination',
                'A': 'c1ccccc1',           # Benzene
                'B': 'Brc1ccccc1',         # Bromobenzene
                'description': 'Benzene → Bromobenzene',
                'reagents': ['Br₂/FeBr₃'],
                'mechanism': 'Electrophilic aromatic substitution'
            },
            {
                'name': 'Alkene Bromination',
                'A': 'C=CC',               # Propene
                'B': 'CC(Br)CBr',          # 1,2-dibromopropane
                'description': 'Alkene → Dibromide',
                'reagents': ['Br₂/CCl₄'],
                'mechanism': 'Electrophilic addition via bromonium ion'
            },
            {
                'name': 'Free Radical Bromination',
                'A': 'CCCC',               # Butane
                'B': 'CCC(C)Br',           # 2-bromobutane
                'description': 'Alkane → Alkyl bromide',
                'reagents': ['Br₂/hv'],
                'mechanism': 'Free radical chain reaction'
            }
        ],
        'nitration': [
            {
                'name': 'Aromatic Nitration',
                'A': 'c1ccccc1',           # Benzene
                'B': 'O=[N+]([O-])c1ccccc1', # Nitrobenzene
                'description': 'Benzene → Nitrobenzene',
                'reagents': ['HNO₃/H₂SO₄'],
                'mechanism': 'Electrophilic aromatic substitution via nitronium ion'
            }
        ],
        'alkylation': [
            {
                'name': 'Friedel-Crafts Alkylation',
                'A': 'c1ccccc1',           # Benzene
                'B': 'CCc1ccccc1',         # Ethylbenzene
                'description': 'Benzene → Alkylbenzene',
                'reagents': ['CH₃CH₂Cl/AlCl₃'],
                'mechanism': 'Electrophilic aromatic substitution via carbocation'
            }
        ],
        'acylation': [
            {
                'name': 'Friedel-Crafts Acylation',
                'A': 'c1ccccc1',           # Benzene
                'B': 'CC(=O)c1ccccc1',     # Acetophenone
                'description': 'Benzene → Ketone',
                'reagents': ['CH₃COCl/AlCl₃'],
                'mechanism': 'Electrophilic aromatic substitution via acylium ion'
            }
        ],
        'grignard': [
            {
                'name': 'Grignard with Carbonyl',
                'A': 'Brc1ccccc1',         # Bromobenzene
                'B': 'C=O',                # Formaldehyde
                'C': 'COc1ccccc1',         # Benzyl alcohol
                'description': 'Aryl halide → Grignard → Alcohol',
                'reagents': ['Mg/ether', 'HCHO', 'H₃O⁺'],
                'mechanism': 'Formation of Grignard reagent followed by nucleophilic addition'
            }
        ]
    }

# Advanced Functions
def validate_smiles(smiles):
    try:
        mol = Chem.MolFromSmiles(smiles)
        return mol is not None
    except:
        return False

def get_compound_name(smiles):
    database = get_compound_database()
    for name, smi in database.items():
        if smi == smiles:
            return name.title()
    return "Unknown compound"

def draw_molecule(smiles, size=(300, 300)):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            return Draw.MolToImage(mol, size=size)
    except:
        return None
    return None

def calculate_molecular_properties(smiles):
    """Calculate molecular properties using RDKit"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            return {
                'Molecular Weight': f"{Descriptors.MolWt(mol):.2f} g/mol",
                'Formula': Chem.rdMolDescriptors.CalcMolFormula(mol),
                'Heavy Atoms': mol.GetNumHeavyAtoms(),
                'Rotatable Bonds': Descriptors.NumRotatableBonds(mol),
                'H-Bond Donors': Descriptors.NumHDonors(mol),
                'H-Bond Acceptors': Descriptors.NumHAcceptors(mol),
                'LogP': f"{Descriptors.MolLogP(mol):.2f}",
                'TPSA': f"{Descriptors.TPSA(mol):.2f} Å²"
            }
    except:
        return {}
    return {}

def parse_problem(problem_text):
    """Enhanced problem parsing with better pattern matching"""
    problem_lower = problem_text.lower()
    
    # Identify compounds mentioned
    compounds_found = {}
    database = get_compound_database()
    
    # Look for compound names
    for name, smiles in database.items():
        if name in problem_lower:
            compounds_found[name] = smiles
    
    # Look for compound patterns (A, B, C)
    compound_pattern = r'compound\s+([A-Z])'
    matches = re.finditer(compound_pattern, problem_lower)
    for match in matches:
        compounds_found[match.group(1)] = None
    
    # Identify reaction types with better matching
    reactions_found = []
    reaction_keywords = {
        'oxidation': ['oxid'],
        'reduction': ['reduc'],
        'esterification': ['esterif'],
        'hydrolysis': ['hydrolys'],
        'acetylation': ['acetylat'],
        'halogenation': ['halogenat', 'bromin', 'chlorin'],
        'nitration': ['nitrat'],
        'alkylation': ['alkylat'],
        'acylation': ['acylat'],
        'grignard': ['grignard']
    }
    
    for reaction_type, keywords in reaction_keywords.items():
        for keyword in keywords:
            if keyword in problem_lower:
                reactions_found.append(reaction_type)
                break
    
    return compounds_found, reactions_found

def solve_chemistry_problem(problem_text, selected_reactions=None):
    """Enhanced problem solving with better matching"""
    if selected_reactions is None:
        selected_reactions = ['oxidation']
    
    all_pathways = get_reaction_pathways()
    relevant_pathways = []
    
    # Get pathways for selected reaction types
    for reaction_type in selected_reactions:
        if reaction_type in all_pathways:
            relevant_pathways.extend(all_pathways[reaction_type])
    
    return relevant_pathways

def create_reaction_flow_diagram(pathway):
    """Create a visual reaction flow diagram"""
    compounds = []
    labels = []
    
    for comp in ['A', 'B', 'C']:
        if comp in pathway:
            compounds.append(pathway[comp])
            labels.append(f"Compound {comp}\n{get_compound_name(pathway[comp])}")
    
    if len(compounds) >= 2:
        try:
            # Create a grid of molecules
            mols = [Chem.MolFromSmiles(smiles) for smiles in compounds]
            img = Draw.MolsToGridImage(
                mols, 
                molsPerRow=len(compounds),
                subImgSize=(300, 300),
                legends=labels,
                returnPNG=False
            )
            return img
        except:
            return None
    return None

def main():
    st.set_page_config(page_title="Advanced Chemistry Solver", layout="wide")
    
    st.title("🧪 Advanced Organic Chemistry Problem Solver")
    st.markdown("""
    *Solve complex organic chemistry problems with advanced analysis and visualization*
    """)
    
    # Initialize data
    compound_database = get_compound_database()
    reaction_pathways = get_reaction_pathways()
    
    # Enhanced example problems
    example_problems = {
        "Oxidation Example": "Compound A on oxidation gives Compound B which on further oxidation gives compound C, benzoic acid.",
        "Reduction Example": "Benzene on nitration gives Compound A which on reduction gives Compound B, aniline.",
        "Esterification Example": "Benzoic acid undergoes esterification with methanol to give Compound A.",
        "Acetylation Example": "Aniline undergoes acetylation to give Compound A.",
        "Multi-step Synthesis": "Benzene is first acylated to Compound A, which is then reduced to Compound B.",
        "Grignard Reaction": "Bromobenzene reacts with formaldehyde via Grignard reaction to give Compound A."
    }
    
    # Sidebar with enhanced features
    with st.sidebar:
        st.header("⚙ Advanced Configuration")
        
        # Reaction type selection
        st.subheader("🧪 Reaction Types")
        all_reactions = list(reaction_pathways.keys())
        selected_reactions = st.multiselect(
            "Select reactions to consider:",
            all_reactions,
            default=['oxidation', 'reduction', 'esterification']
        )
        
        # Analysis options
        st.subheader("🔬 Analysis Options")
        show_properties = st.checkbox("Show Molecular Properties", value=True)
        show_mechanism = st.checkbox("Show Reaction Mechanisms", value=True)
        show_flow_diagram = st.checkbox("Show Reaction Flow Diagram", value=True)
        
        st.markdown("---")
        st.subheader("🔍 Advanced Tools")
        
        # SMILES validator with properties
        test_smiles = st.text_input("Analyze SMILES:", "c1ccccc1C(=O)O")
        if test_smiles:
            if validate_smiles(test_smiles):
                st.success("✅ Valid SMILES")
                img = draw_molecule(test_smiles, (200, 200))
                if img:
                    st.image(img, caption=get_compound_name(test_smiles))
                
                if show_properties:
                    properties = calculate_molecular_properties(test_smiles)
                    if properties:
                        st.write("*Molecular Properties:*")
                        for prop, value in properties.items():
                            st.write(f"- {prop}: {value}")
            else:
                st.error("❌ Invalid SMILES")
        
        # Quick compound lookup
        st.markdown("---")
        st.subheader("📋 Quick Compound Lookup")
        compound_query = st.selectbox("Select compound:", list(compound_database.keys()))
        if compound_query:
            smiles = compound_database[compound_query]
            st.write(f"*SMILES:* {smiles}")
            img = draw_molecule(smiles, (150, 150))
            if img:
                st.image(img, caption=compound_query.title())
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Problem input with enhanced options
        selected_example = st.selectbox("Choose an example problem:", list(example_problems.keys()))
        problem_text = st.text_area(
            "Enter your chemistry problem:",
            value=example_problems[selected_example],
            height=120,
            help="Describe the reaction sequence with compounds and reaction types"
        )
        
        # Advanced problem analysis
        if st.button("🔬 Advanced Analysis", type="primary"):
            with st.spinner("Performing comprehensive analysis..."):
                # Parse and analyze problem
                compounds_found, reactions_found = parse_problem(problem_text)
                
                # Enhanced analysis display
                st.subheader("🔍 Detailed Problem Analysis")
                
                analysis_col1, analysis_col2, analysis_col3 = st.columns(3)
                
                with analysis_col1:
                    st.markdown("📦 Compounds Identified:")
                    if compounds_found:
                        for name, smiles in compounds_found.items():
                            if smiles:
                                st.write(f"- *{name.title()}*: {smiles}")
                                if show_properties:
                                    props = calculate_molecular_properties(smiles)
                                    if props:
                                        st.write(f"  - MW: {props['Molecular Weight']}, Formula: {props['Formula']}")
                            else:
                                st.write(f"- *Compound {name}*: Structure unknown")
                    else:
                        st.write("- No specific compounds identified")
                
                with analysis_col2:
                    st.markdown("⚗ Reactions Identified:")
                    if reactions_found:
                        for reaction in reactions_found:
                            st.write(f"- {reaction.title()}")
                            # Show number of available pathways
                            pathway_count = len(reaction_pathways.get(reaction, []))
                            st.write(f"  - {pathway_count} pathway(s) available")
                    else:
                        st.write("- No specific reactions identified")
                
                with analysis_col3:
                    st.markdown("🎯 Problem Type:")
                    if 'benzoic acid' in problem_text.lower():
                        st.write("- Carboxylic acid synthesis")
                    if 'aniline' in problem_text.lower():
                        st.write("- Amine synthesis")
                    if len(reactions_found) > 1:
                        st.write("- Multi-step synthesis")
                    else:
                        st.write("- Single-step transformation")
                
                # Solve problem with enhanced display
                pathways = solve_chemistry_problem(problem_text, selected_reactions)
                
                st.subheader("🎯 Comprehensive Pathway Solutions")
                
                if not pathways:
                    st.warning("No pathways found. Try adjusting the reaction types or problem description.")
                else:
                    for i, pathway in enumerate(pathways):
                        with st.expander(f"Pathway {i+1}: {pathway['name']} ({len([c for c in ['A','B','C'] if c in pathway])} steps)", expanded=True):
                            
                            # Enhanced compound table
                            results_data = []
                            for compound in ['A', 'B', 'C']:
                                if compound in pathway:
                                    smiles = pathway[compound]
                                    results_data.append({
                                        'Compound': compound,
                                        'SMILES': smiles,
                                        'Name': get_compound_name(smiles),
                                        'Valid': '✅' if validate_smiles(smiles) else '❌'
                                    })
                            
                            # Display enhanced table
                            if results_data:
                                df = pd.DataFrame(results_data)
                                st.table(df)
                                
                                # Reaction flow diagram
                                if show_flow_diagram:
                                    st.write("*Reaction Flow:*")
                                    flow_img = create_reaction_flow_diagram(pathway)
                                    if flow_img:
                                        st.image(flow_img, use_column_width=True)
                                
                                # Molecular structures with properties
                                st.write("*Molecular Analysis:*")
                                compounds_to_draw = [c for c in ['A', 'B', 'C'] if c in pathway]
                                cols = st.columns(len(compounds_to_draw))
                                
                                for idx, compound in enumerate(compounds_to_draw):
                                    smiles = pathway[compound]
                                    with cols[idx]:
                                        st.write(f"*Compound {compound}*")
                                        img = draw_molecule(smiles, (200, 200))
                                        if img:
                                            st.image(img, caption=get_compound_name(smiles))
                                        
                                        if show_properties:
                                            props = calculate_molecular_properties(smiles)
                                            if props:
                                                st.write(f"*MW:* {props['Molecular Weight']}")
                                                st.write(f"*Formula:* {props['Formula']}")
                            
                            # Enhanced pathway details
                            st.info(f"*Description:* {pathway['description']}")
                            
                            if 'reagents' in pathway:
                                st.write("🧪 Typical Reagents:")
                                for reagent in pathway['reagents']:
                                    st.write(f"- {reagent}")
                            
                            if show_mechanism and 'mechanism' in pathway:
                                st.write("🔬 Reaction Mechanism:")
                                st.write(pathway['mechanism'])
    
    with col2:
        st.markdown("### 🎓 Learning Resources")
        
        # Quick reaction guide
        with st.expander("📚 Quick Reaction Guide", expanded=True):
            st.write("*Common Transformations:*")
            st.write("- Alcohol → Aldehyde: PCC, Swern")
            st.write("- Aldehyde → Acid: KMnO₄, K₂Cr₂O₇")
            st.write("- Nitro → Amino: Sn/HCl, H₂/Pd")
            st.write("- Acid → Ester: ROH/H⁺")
            st.write("- Alkene → Alkane: H₂/Pd")
        
        # Functional group interconversions
        with st.expander("🔄 Functional Group Map"):
            st.write("""
            *Common Pathways:*
            - R-CH₂OH → R-CHO → R-COOH
            - R-NO₂ → R-NH₂ → R-NHCOR
            - R-COOH → R-COCl → R-CONR₂
            - Ar-H → Ar-NO₂ → Ar-NH₂
            """)
        
        # Study tips
        with st.expander("💡 Study Tips"):
            st.write("""
            *Problem Solving Strategy:*
            1. Identify functional groups
            2. Determine reaction type
            3. Work backwards from product
            4. Consider multi-step sequences
            5. Verify SMILES structures
            """)
    
    # Advanced Features Section
    st.markdown("---")
    st.subheader("🔬 Advanced Chemistry Tools")
    
    adv_col1, adv_col2 = st.columns(2)
    
    with adv_col1:
        st.markdown("### 📊 Molecular Property Calculator")
        prop_smiles = st.text_input("Enter SMILES for property calculation:", "CCO")
        if prop_smiles and validate_smiles(prop_smiles):
            properties = calculate_molecular_properties(prop_smiles)
            if properties:
                st.write("*Calculated Properties:*")
                for prop, value in properties.items():
                    st.write(f"- *{prop}:* {value}")
                img = draw_molecule(prop_smiles, (200, 200))
                if img:
                    st.image(img, caption=get_compound_name(prop_smiles))
    
    with adv_col2:
        st.markdown("### 🧪 Reaction Mechanism Library")
        selected_mechanism = st.selectbox("Select reaction type:", list(reaction_pathways.keys()))
        if selected_mechanism:
            pathways = reaction_pathways[selected_mechanism]
            st.write(f"{len(pathways)} pathway(s) available:")
            for pathway in pathways:
                with st.expander(pathway['name']):
                    st.write(f"*Description:* {pathway['description']}")
                    if 'mechanism' in pathway:
                        st.write(f"*Mechanism:* {pathway['mechanism']}")
                    st.write("*Reagents:* " + ", ".join(pathway.get('reagents', [])))

if __name__ == "__main__":
    main()
