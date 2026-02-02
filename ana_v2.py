import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Tableau de Bord Investissements - NSIA VIE",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Couleurs NSIA
NSIA_BLUE = "#002654"
NSIA_GOLD = "#FFB81C"
SUCCESS_COLOR = "#28a745"
WARNING_COLOR = "#ffc107"
DANGER_COLOR = "#dc3545"

# CSS personnalisé
st.markdown(f"""
<style>
    .main {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }}
    
    .header-container {{
        background: linear-gradient(135deg, {NSIA_BLUE} 0%, #003d82 100%);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    
    .header-container::before {{
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,184,28,0.15) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.1); }}
    }}
    
    .header-title {{
        color: white;
        font-size: 2.8rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        position: relative;
        z-index: 1;
    }}
    
    .header-subtitle {{
        color: {NSIA_GOLD};
        font-size: 1.3rem;
        margin-top: 0.5rem;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }}
    
    .date-filter-container {{
        background: rgba(255, 255, 255, 0.15);
        padding: 1rem 2rem;
        border-radius: 15px;
        margin-top: 1.5rem;
        position: relative;
        z-index: 1;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 184, 28, 0.3);
    }}
    
    .section-card {{
        background: white;
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        margin: 1.5rem 0;
    }}
    
    .section-title {{
        color: {NSIA_BLUE};
        font-size: 1.8rem;
        font-weight: 800;
        margin-bottom: 1.5rem;
        border-bottom: 4px solid {NSIA_GOLD};
        padding-bottom: 0.8rem;
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, {NSIA_BLUE} 0%, #003d82 100%);
        color: white;
        padding: 1.8rem;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
    }}
    
    .metric-label {{
        font-size: 1rem;
        opacity: 0.9;
        margin-bottom: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    
    .metric-value {{
        font-size: 2.2rem;
        font-weight: 900;
        color: {NSIA_GOLD};
        margin: 0.5rem 0;
    }}
    
    .metric-detail {{
        font-size: 0.95rem;
        margin-top: 0.8rem;
        opacity: 0.9;
        line-height: 1.8;
    }}
    
    .kpi-card {{
        background: white;
        border-radius: 18px;
        padding: 1.8rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.12);
        border-left: 6px solid {NSIA_GOLD};
        transition: all 0.4s ease;
    }}
    
    .kpi-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.18);
    }}
    
    .kpi-title {{
        color: {NSIA_BLUE};
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
    }}
    
    .kpi-value {{
        color: {NSIA_BLUE};
        font-size: 2.2rem;
        font-weight: 900;
        margin: 0.8rem 0;
    }}
    
    .kpi-subtitle {{
        color: #666;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }}
    
    .progress-container {{
        width: 100%;
        height: 28px;
        background: linear-gradient(to right, #e9ecef, #f8f9fa);
        border-radius: 14px;
        overflow: hidden;
        position: relative;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }}
    
    .progress-bar {{
        height: 100%;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 0.85rem;
        transition: width 0.8s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }}
    
    .progress-success {{
        background: linear-gradient(90deg, {SUCCESS_COLOR} 0%, #34c759 100%);
    }}
    
    .progress-warning {{
        background: linear-gradient(90deg, {WARNING_COLOR} 0%, #ffdb4d 100%);
    }}
    
    .progress-danger {{
        background: linear-gradient(90deg, {DANGER_COLOR} 0%, #f56565 100%);
    }}
    
    .kpi-delta {{
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-top: 0.8rem;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    }}
    
    .delta-positive {{
        background: linear-gradient(135deg, {SUCCESS_COLOR} 0%, #34c759 100%);
        color: white;
    }}
    
    .delta-negative {{
        background: linear-gradient(135deg, {DANGER_COLOR} 0%, #f56565 100%);
        color: white;
    }}
    
    .status-badge {{
        display: inline-block;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }}
    
    .badge-success {{
        background: linear-gradient(135deg, {SUCCESS_COLOR} 0%, #34c759 100%);
        color: white;
    }}
    
    .badge-warning {{
        background: linear-gradient(135deg, {WARNING_COLOR} 0%, #ffdb4d 100%);
        color: {NSIA_BLUE};
    }}
    
    .badge-danger {{
        background: linear-gradient(135deg, {DANGER_COLOR} 0%, #f56565 100%);
        color: white;
    }}
    
    .input-section {{
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid {NSIA_GOLD};
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin-bottom: 2rem;
    }}
    
    .stNumberInput > label {{
        color: {NSIA_BLUE};
        font-weight: 600;
        font-size: 0.9rem;
    }}
</style>
""", unsafe_allow_html=True)

# Fonctions utilitaires
def format_montant(value):
    if pd.isna(value) or value == 0:
        return "-"
    return f"{value:,.0f}".replace(",", " ")

def calculer_taux(realise, budget):
    if pd.isna(budget) or budget == 0:
        return 0
    return (realise / budget) * 100

def get_progress_class(rate):
    if rate >= 100:
        return "progress-success"
    elif rate >= 80:
        return "progress-warning"
    else:
        return "progress-danger"

# Initialiser session_state pour stocker les données avec dates
if 'data_historique' not in st.session_state:
    st.session_state.data_historique = {}

# Définir les classes d'actifs
actifs_list = [
    'Obligations d\'États',
    'Obligation des sociétés commerciales',
    'Actions des Sociétés Commerciales',
    'Droits immobiliers',
    'Prêts',
    'Dépôts à terme',
    'Autres investissements',
    'Investissements d\'exploitation (DRI)'
]

# Données par défaut
def get_default_data():
    return {
        'Obligations d\'États': {'budget_initial': 6676, 'budget_ajuste': 3575, 'budget_semaine': 106, 'real_semaine': 120, 'budget_cumule': 500, 'real_cumule': 450},
        'Obligation des sociétés commerciales': {'budget_initial': 1931, 'budget_ajuste': 1734, 'budget_semaine': 0, 'real_semaine': 0, 'budget_cumule': 0, 'real_cumule': 0},
        'Actions des Sociétés Commerciales': {'budget_initial': 1000, 'budget_ajuste': 1000, 'budget_semaine': 0, 'real_semaine': 0, 'budget_cumule': 0, 'real_cumule': 0},
        'Droits immobiliers': {'budget_initial': 2500, 'budget_ajuste': 2500, 'budget_semaine': 0, 'real_semaine': 0, 'budget_cumule': 0, 'real_cumule': 0},
        'Prêts': {'budget_initial': 1500, 'budget_ajuste': 0, 'budget_semaine': 2000, 'real_semaine': 1800, 'budget_cumule': 4000, 'real_cumule': 3500},
        'Dépôts à terme': {'budget_initial': 7710, 'budget_ajuste': 5700, 'budget_semaine': 3005, 'real_semaine': 2800, 'budget_cumule': 2605, 'real_cumule': 2100},
        'Autres investissements': {'budget_initial': 0, 'budget_ajuste': 0, 'budget_semaine': 0, 'real_semaine': 0, 'budget_cumule': 0, 'real_cumule': 0},
        'Investissements d\'exploitation (DRI)': {'budget_initial': 450, 'budget_ajuste': 450, 'budget_semaine': 0, 'real_semaine': 0, 'budget_cumule': 0, 'real_cumule': 0}
    }

# ===========================
# EN-TÊTE AVEC FILTRE DE DATE
# ===========================
st.markdown(f"""
<div class="header-container">
    <h1 class="header-title">📊 TABLEAU DE BORD INVESTISSEMENTS HEBDOMADAIRE</h1>
    <p class="header-subtitle">NSIA VIE ASSURANCES - Suivi des Placements</p>
</div>
""", unsafe_allow_html=True)

# Section de filtre par date (en-dessous de l'en-tête principal)
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown(f'<h2 style="color: {NSIA_BLUE}; font-weight: 800; margin-bottom: 1.5rem;">📅 Sélection de la Période</h2>', unsafe_allow_html=True)

col_date1, col_date2, col_date3 = st.columns([2, 2, 1])

with col_date1:
    # Date de début de semaine (lundi par défaut)
    date_debut = st.date_input(
        "📅 Date de début de semaine",
        value=datetime.now().date() - timedelta(days=datetime.now().weekday()),
        key='date_debut'
    )

with col_date2:
    # Date de fin de semaine (dimanche par défaut)
    date_fin = st.date_input(
        "📅 Date de fin de semaine",
        value=datetime.now().date() - timedelta(days=datetime.now().weekday()) + timedelta(days=6),
        key='date_fin'
    )

with col_date3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📆 Semaine actuelle", use_container_width=True):
        today = datetime.now().date()
        monday = today - timedelta(days=today.weekday())
        st.session_state.date_debut = monday
        st.session_state.date_fin = monday + timedelta(days=6)
        st.rerun()

# Afficher la période sélectionnée
periode_str = f"{date_debut.strftime('%d/%m/%Y')} - {date_fin.strftime('%d/%m/%Y')}"
date_key = f"{date_debut.strftime('%Y-%m-%d')}"

st.markdown(f"""
<div style="background: linear-gradient(135deg, {NSIA_BLUE} 0%, #003d82 100%); 
            padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;">
    <p style="color: white; font-size: 1.2rem; font-weight: 700; margin: 0;">
        📊 Période analysée : <span style="color: {NSIA_GOLD};">{periode_str}</span>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# SECTION DE SAISIE DES DONNÉES
# ===========================
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown(f'<h2 style="color: {NSIA_BLUE}; font-weight: 800; margin-bottom: 1.5rem;">📝 Saisie des Données Hebdomadaires</h2>', unsafe_allow_html=True)

# Charger les données pour la date sélectionnée ou utiliser les données par défaut
if date_key not in st.session_state.data_historique:
    st.session_state.data_historique[date_key] = get_default_data()

data_saisie = st.session_state.data_historique[date_key]

# Sélectionner l'actif à modifier
actif_selectionne = st.selectbox(
    "🎯 Sélectionnez la classe d'actifs à modifier",
    actifs_list,
    key='actif_select'
)

# Formulaire de saisie
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💰 Budgets")
    budget_initial = st.number_input(
        "Budget Initial 2026",
        value=float(data_saisie[actif_selectionne]['budget_initial']),
        step=100.0,
        key='budget_initial'
    )
    
    budget_ajuste = st.number_input(
        "Budget Ajusté",
        value=float(data_saisie[actif_selectionne]['budget_ajuste']),
        step=100.0,
        key='budget_ajuste'
    )

with col2:
    st.markdown("### 📅 Cette Semaine")
    budget_semaine = st.number_input(
        "Budget Semaine",
        value=float(data_saisie[actif_selectionne]['budget_semaine']),
        step=100.0,
        key='budget_semaine'
    )
    
    real_semaine = st.number_input(
        "Réalisation Semaine",
        value=float(data_saisie[actif_selectionne]['real_semaine']),
        step=100.0,
        key='real_semaine'
    )

with col3:
    st.markdown("### 📊 Cumulé")
    budget_cumule = st.number_input(
        "Budget Cumulé",
        value=float(data_saisie[actif_selectionne]['budget_cumule']),
        step=100.0,
        key='budget_cumule'
    )
    
    real_cumule = st.number_input(
        "Réalisation Cumulée",
        value=float(data_saisie[actif_selectionne]['real_cumule']),
        step=100.0,
        key='real_cumule'
    )

# Bouton de mise à jour
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    if st.button("✅ Enregistrer les données", use_container_width=True, type="primary"):
        st.session_state.data_historique[date_key][actif_selectionne] = {
            'budget_initial': budget_initial,
            'budget_ajuste': budget_ajuste,
            'budget_semaine': budget_semaine,
            'real_semaine': real_semaine,
            'budget_cumule': budget_cumule,
            'real_cumule': real_cumule
        }
        st.success(f"✅ Données enregistrées pour {actif_selectionne} - Semaine du {date_debut.strftime('%d/%m/%Y')}")
        st.rerun()

# Afficher le nombre de semaines enregistrées
nb_semaines = len(st.session_state.data_historique)
st.info(f"📊 {nb_semaines} semaine(s) enregistrée(s) dans l'historique")

st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# CONSTRUCTION DU DATAFRAME
# ===========================
def construire_dataframe(data):
    data_rows = []
    
    # Actifs principaux (Niveau 1)
    for actif in actifs_list[:7]:  # Sans le DRI
        d = data[actif]
        data_rows.append({
            'Classe d\'Actifs': actif,
            'Niveau': 1,
            'Budget_Initial_2026': d['budget_initial'],
            'Budget_Ajuste': d['budget_ajuste'],
            'Budget_Semaine': d['budget_semaine'],
            'Realisation_Semaine': d['real_semaine'],
            'Budget_Cumule': d['budget_cumule'],
            'Realisation_Cumulee': d['real_cumule']
        })
    
    # Sous-total Actions et obligations (Niveau 2)
    sous_total_actions = {
        'Classe d\'Actifs': 'S/Total Actions et obligations des stes sociales',
        'Niveau': 2,
        'Budget_Initial_2026': sum([data[a]['budget_initial'] for a in actifs_list[1:3]]),
        'Budget_Ajuste': sum([data[a]['budget_ajuste'] for a in actifs_list[1:3]]),
        'Budget_Semaine': sum([data[a]['budget_semaine'] for a in actifs_list[1:3]]),
        'Realisation_Semaine': sum([data[a]['real_semaine'] for a in actifs_list[1:3]]),
        'Budget_Cumule': sum([data[a]['budget_cumule'] for a in actifs_list[1:3]]),
        'Realisation_Cumulee': sum([data[a]['real_cumule'] for a in actifs_list[1:3]])
    }
    data_rows.append(sous_total_actions)
    
    # TOTAL (sans DRI) (Niveau 2)
    total_sans_dri = {
        'Classe d\'Actifs': 'TOTAL',
        'Niveau': 2,
        'Budget_Initial_2026': sum([data[a]['budget_initial'] for a in actifs_list[:7]]),
        'Budget_Ajuste': sum([data[a]['budget_ajuste'] for a in actifs_list[:7]]),
        'Budget_Semaine': sum([data[a]['budget_semaine'] for a in actifs_list[:7]]),
        'Realisation_Semaine': sum([data[a]['real_semaine'] for a in actifs_list[:7]]),
        'Budget_Cumule': sum([data[a]['budget_cumule'] for a in actifs_list[:7]]),
        'Realisation_Cumulee': sum([data[a]['real_cumule'] for a in actifs_list[:7]])
    }
    data_rows.append(total_sans_dri)
    
    # DRI (Niveau 1)
    data_dri = data['Investissements d\'exploitation (DRI)']
    data_rows.append({
        'Classe d\'Actifs': 'Investissements d\'exploitation (DRI)',
        'Niveau': 1,
        'Budget_Initial_2026': data_dri['budget_initial'],
        'Budget_Ajuste': data_dri['budget_ajuste'],
        'Budget_Semaine': data_dri['budget_semaine'],
        'Realisation_Semaine': data_dri['real_semaine'],
        'Budget_Cumule': data_dri['budget_cumule'],
        'Realisation_Cumulee': data_dri['real_cumule']
    })
    
    # TOTAL GENERAL (Niveau 3)
    total_general = {
        'Classe d\'Actifs': 'TOTAL GENERAL',
        'Niveau': 3,
        'Budget_Initial_2026': sum([data[a]['budget_initial'] for a in actifs_list]),
        'Budget_Ajuste': sum([data[a]['budget_ajuste'] for a in actifs_list]),
        'Budget_Semaine': sum([data[a]['budget_semaine'] for a in actifs_list]),
        'Realisation_Semaine': sum([data[a]['real_semaine'] for a in actifs_list]),
        'Budget_Cumule': sum([data[a]['budget_cumule'] for a in actifs_list]),
        'Realisation_Cumulee': sum([data[a]['real_cumule'] for a in actifs_list])
    }
    data_rows.append(total_general)
    
    df = pd.DataFrame(data_rows)
    
    # Calculs automatiques
    df['Ecart_Semaine'] = df['Realisation_Semaine'] - df['Budget_Semaine']
    df['Taux_Realisation_Hebdo'] = df.apply(
        lambda row: calculer_taux(row['Realisation_Semaine'], row['Budget_Semaine']), axis=1
    )
    
    df['Ecart_Cumule'] = df['Realisation_Cumulee'] - df['Budget_Cumule']
    df['Taux_Realisation_Cumule'] = df.apply(
        lambda row: calculer_taux(row['Realisation_Cumulee'], row['Budget_Cumule']), axis=1
    )
    
    return df

# Construire le dataframe pour la période sélectionnée
df = construire_dataframe(data_saisie)

# Calcul des KPI globaux
total_real_hebdo = df[df['Niveau'] == 3]['Realisation_Semaine'].iloc[0]
total_budget_hebdo = df[df['Niveau'] == 3]['Budget_Semaine'].iloc[0]
taux_hebdo = calculer_taux(total_real_hebdo, total_budget_hebdo)
delta_hebdo = total_real_hebdo - total_budget_hebdo

total_real_cumul = df[df['Niveau'] == 3]['Realisation_Cumulee'].iloc[0]
total_budget_cumul = df[df['Niveau'] == 3]['Budget_Cumule'].iloc[0]
taux_cumul = calculer_taux(total_real_cumul, total_budget_cumul)
delta_cumul = total_real_cumul - total_budget_cumul

total_budget_annuel = df[df['Niveau'] == 3]['Budget_Ajuste'].iloc[0]
taux_vs_annuel = calculer_taux(total_real_cumul, total_budget_annuel)
restant = total_budget_annuel - total_real_cumul

# ===========================
# RÉSUMÉ EXÉCUTIF (EN PREMIER)
# ===========================
st.markdown("---")
st.markdown("## 📝 Résumé Exécutif pour le Briefing Hebdomadaire")

st.markdown('<div class="section-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    ecart_sign = "+" if delta_hebdo >= 0 else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 CETTE SEMAINE</div>
        <div class="metric-value">{format_montant(total_real_hebdo)}</div>
        <div class="metric-detail">
            • Budget prévu: {format_montant(total_budget_hebdo)}<br>
            • Taux: <strong>{taux_hebdo:.1f}%</strong><br>
            • Écart: <strong>{ecart_sign}{format_montant(abs(delta_hebdo))}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    ecart_sign = "+" if delta_cumul >= 0 else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📈 CUMULÉ À DATE</div>
        <div class="metric-value">{format_montant(total_real_cumul)}</div>
        <div class="metric-detail">
            • Budget cumulé: {format_montant(total_budget_cumul)}<br>
            • Taux: <strong>{taux_cumul:.1f}%</strong><br>
            • Écart: <strong>{ecart_sign}{format_montant(abs(delta_cumul))}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🎯 PROGRESSION ANNUELLE</div>
        <div class="metric-value">{taux_vs_annuel:.1f}%</div>
        <div class="metric-detail">
            • Budget annuel: {format_montant(total_budget_annuel)}<br>
            • Réalisé: <strong>{format_montant(total_real_cumul)}</strong><br>
            • Restant: <strong>{format_montant(restant)}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# INDICATEURS CLÉS DE PERFORMANCE
# ===========================
st.markdown("---")
st.markdown("## 📈 Indicateurs Clés de Performance")

col1, col2, col3, col4 = st.columns(4)

# KPI 1
with col1:
    progress_class = get_progress_class(taux_hebdo)
    delta_class = "delta-positive" if delta_hebdo >= 0 else "delta-negative"
    delta_icon = "▲" if delta_hebdo >= 0 else "▼"
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">💰 Réalisation Hebdomadaire</div>
        <div class="kpi-value">{format_montant(total_real_hebdo)}</div>
        <div class="kpi-subtitle">Budget: {format_montant(total_budget_hebdo)}</div>
        <div class="progress-container">
            <div class="progress-bar {progress_class}" style="width: {min(taux_hebdo, 100)}%;">
                {taux_hebdo:.0f}%
            </div>
        </div>
        <div class="kpi-delta {delta_class}">
            {delta_icon} {format_montant(abs(delta_hebdo))} ({taux_hebdo:.1f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)

# KPI 2
with col2:
    progress_class = get_progress_class(taux_cumul)
    delta_class = "delta-positive" if delta_cumul >= 0 else "delta-negative"
    delta_icon = "▲" if delta_cumul >= 0 else "▼"
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">📊 Réalisation Cumulée</div>
        <div class="kpi-value">{format_montant(total_real_cumul)}</div>
        <div class="kpi-subtitle">Budget: {format_montant(total_budget_cumul)}</div>
        <div class="progress-container">
            <div class="progress-bar {progress_class}" style="width: {min(taux_cumul, 100)}%;">
                {taux_cumul:.0f}%
            </div>
        </div>
        <div class="kpi-delta {delta_class}">
            {delta_icon} {format_montant(abs(delta_cumul))} ({taux_cumul:.1f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)

# KPI 3
with col3:
    progress_class = get_progress_class(taux_vs_annuel)
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🎯 Budget Annuel Ajusté</div>
        <div class="kpi-value">{format_montant(total_budget_annuel)}</div>
        <div class="kpi-subtitle">Réalisé: {taux_vs_annuel:.1f}%</div>
        <div class="progress-container">
            <div class="progress-bar {progress_class}" style="width: {min(taux_vs_annuel, 100)}%;">
                {taux_vs_annuel:.0f}%
            </div>
        </div>
        <div class="kpi-subtitle" style="margin-top: 0.8rem; font-weight: 600;">
            Restant: {format_montant(restant)}
        </div>
    </div>
    """, unsafe_allow_html=True)

# KPI 4
with col4:
    nb_objectifs_atteints = len(df[(df['Taux_Realisation_Hebdo'] >= 100) & (df['Niveau'] == 1)])
    nb_total_actifs = len(df[df['Niveau'] == 1])
    taux_success = (nb_objectifs_atteints / nb_total_actifs) * 100 if nb_total_actifs > 0 else 0
    
    progress_class = get_progress_class(taux_success)
    
    if taux_success >= 100:
        badge_class = "badge-success"
        badge_text = "✓ Objectif atteint"
    elif taux_success >= 80:
        badge_class = "badge-warning"
        badge_text = "⚠ En cours"
    else:
        badge_class = "badge-danger"
        badge_text = "✗ En retard"
    
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">🏆 Performance Globale</div>
        <div class="kpi-value">{nb_objectifs_atteints}/{nb_total_actifs}</div>
        <div class="kpi-subtitle">Objectifs atteints</div>
        <div class="progress-container">
            <div class="progress-bar {progress_class}" style="width: {min(taux_success, 100)}%;">
                {taux_success:.0f}%
            </div>
        </div>
        <span class="status-badge {badge_class}">{badge_text}</span>
    </div>
    """, unsafe_allow_html=True)

# ===========================
# TABLEAU DÉTAILLÉ
# ===========================
st.markdown("---")
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">📋 Tableau Détaillé par Classe d\'Actifs</h2>', unsafe_allow_html=True)

df_table = pd.DataFrame({
    'Classe d\'Actifs': df['Classe d\'Actifs'],
    'Budget Initial 2026': df['Budget_Initial_2026'].apply(format_montant),
    'Budget Ajusté': df['Budget_Ajuste'].apply(format_montant),
    'Budget Semaine': df['Budget_Semaine'].apply(format_montant),
    'Réalisation Semaine': df['Realisation_Semaine'].apply(format_montant),
    'Taux Hebdo (%)': df['Taux_Realisation_Hebdo'].apply(lambda x: f"{x:.0f}%" if x > 0 else "-"),
    'Budget Cumulé': df['Budget_Cumule'].apply(format_montant),
    'Réalisation Cumulée': df['Realisation_Cumulee'].apply(format_montant),
    'Taux Cumulé (%)': df['Taux_Realisation_Cumule'].apply(lambda x: f"{x:.0f}%" if x > 0 else "-"),
    'Écart Cumulé': df['Ecart_Cumule'].apply(lambda x: f"{x:+,.0f}".replace(",", " ") if x != 0 else "-"),
})

st.dataframe(df_table, use_container_width=True, height=500, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# ===========================
# GRAPHIQUES
# ===========================
st.markdown("---")
st.markdown("## 📊 Visualisations")

col1, col2 = st.columns(2)

# Graphique 1
with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Budget vs Réalisation Hebdomadaire")
    
    df_hebdo = df[df['Niveau'] == 1].copy()
    
    fig_hebdo = go.Figure()
    
    fig_hebdo.add_trace(go.Bar(
        name='Budget Semaine',
        x=df_hebdo['Classe d\'Actifs'],
        y=df_hebdo['Budget_Semaine'],
        marker=dict(color=NSIA_BLUE, line=dict(color=NSIA_BLUE, width=2)),
        text=[format_montant(x) for x in df_hebdo['Budget_Semaine']],
        textposition='outside'
    ))
    
    fig_hebdo.add_trace(go.Bar(
        name='Réalisation Semaine',
        x=df_hebdo['Classe d\'Actifs'],
        y=df_hebdo['Realisation_Semaine'],
        marker=dict(color=NSIA_GOLD, line=dict(color=NSIA_GOLD, width=2)),
        text=[format_montant(x) for x in df_hebdo['Realisation_Semaine']],
        textposition='outside'
    ))
    
    fig_hebdo.update_layout(
        barmode='group',
        height=450,
        xaxis_title="",
        yaxis_title="Montant",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(250,250,250,0.5)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig_hebdo.update_xaxes(tickangle=-45)
    
    st.plotly_chart(fig_hebdo, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Graphique 2
with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📈 Taux de Réalisation par Actif")
    
    df_taux = df[df['Niveau'] == 1].copy()
    colors = df_taux['Taux_Realisation_Hebdo'].apply(lambda x: SUCCESS_COLOR if x >= 100 else (WARNING_COLOR if x >= 80 else DANGER_COLOR))
    
    fig_taux = go.Figure(go.Bar(
        x=df_taux['Classe d\'Actifs'],
        y=df_taux['Taux_Realisation_Hebdo'],
        marker=dict(color=colors),
        text=[f"{x:.0f}%" for x in df_taux['Taux_Realisation_Hebdo']],
        textposition='outside'
    ))
    
    fig_taux.add_hline(y=100, line_dash="dash", line_color=SUCCESS_COLOR, line_width=3)
    
    fig_taux.update_layout(
        height=450,
        xaxis_title="",
        yaxis_title="Taux de Réalisation (%)",
        plot_bgcolor='rgba(250,250,250,0.5)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    fig_taux.update_xaxes(tickangle=-45)
    
    st.plotly_chart(fig_taux, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Graphique 3
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown("### 📈 Réalisation Cumulée vs Budget")

df_cumul = df[df['Niveau'] == 1].copy()

fig_cumul = go.Figure()

fig_cumul.add_trace(go.Scatter(
    name='Budget Cumulé',
    x=df_cumul['Classe d\'Actifs'],
    y=df_cumul['Budget_Cumule'],
    mode='lines+markers',
    line=dict(color=NSIA_BLUE, width=4),
    marker=dict(size=12)
))

fig_cumul.add_trace(go.Scatter(
    name='Réalisation Cumulée',
    x=df_cumul['Classe d\'Actifs'],
    y=df_cumul['Realisation_Cumulee'],
    mode='lines+markers',
    line=dict(color=NSIA_GOLD, width=4),
    marker=dict(size=12)
))

fig_cumul.update_layout(
    height=450,
    xaxis_title="",
    yaxis_title="Montant Cumulé",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(250,250,250,0.5)',
    paper_bgcolor='rgba(0,0,0,0)'
)

fig_cumul.update_xaxes(tickangle=-45)

st.plotly_chart(fig_cumul, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 2.5rem; background: white; border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
    <p style="margin: 0; font-weight: 800; font-size: 1.3rem; color: {NSIA_BLUE};">NSIA VIE ASSURANCES</p>
    <p style="margin: 0.8rem 0 0 0; font-size: 1rem; color: {NSIA_GOLD}; font-weight: 700;">Direction des Investissements</p>
    <p style="margin: 1rem 0 0 0; font-size: 0.9rem; color: #666;">
        📅 Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
    </p>
</div>
""", unsafe_allow_html=True)