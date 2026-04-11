# Dashboard Réunion de Rédaction — Journal du Geek

Dashboard Streamlit interne pour les réunions de rédaction hebdomadaires et mensuelles.  
Analyse de la production éditoriale, performances GSC, stats par auteur et recommandations SEO.

---

## Fonctionnalités

### 📊 Vue d'ensemble
- KPIs globaux : vues totales, articles publiés, rédacteurs actifs, vues moyennes
- Timeline de publication sur la période
- Top 10 articles de la semaine / du mois avec liens directs
- Répartition par format éditorial (article, test, dossier, bon plan, critique)
- Historique des semaines et mois archivés (graphiques de tendance)

### 👥 Stats par auteur
- Top 5 et flops par rédacteur (sans chevauchement)
- Volume et vues moyennes par auteur
- Liens directs vers les articles

### 📈 Tendances & Catégories
- Vues totales par catégorie éditoriale
- Scatter **efficacité vs volume** : identifie les catégories pépites, piliers, à rationaliser
- Insights automatiques : catégorie sous-exploitée, format le plus rentable, meilleur jour de publication
- Expander des articles non catégorisés pour affiner les règles

**Catégories détectées automatiquement par mots-clés dans les titres :**
- 🎬 Pop Culture · 🎮 Jeux Vidéo · 💻 Nouvelles Tech · 🛒 Conso & Produits
- 🔬 Sciences · 📱 Réseaux Sociaux · ₿ Crypto & Web3 · 🔒 Cybersécurité
- 🚗 Auto & Mobilité · 🌍 Société & Numérique

### 🔍 Optimisation éditoriale (GSC)
- Connexion directe à **Google Search Console** via OAuth2 sur la période exacte du CSV
- Top et Flop articles SEO recoupés avec les articles du CSV
- Diagnostic automatique par article : CTR faible, position trop basse, impressions insuffisantes, etc.
- **Recommandations SEO générées par Claude (Anthropic)** pour chaque article en flop

---

## Installation locale

### Prérequis
- Python 3.10+
- Accès au projet `seo-monitor` (même dossier parent) pour les credentials GSC

### Setup

```bash
git clone https://github.com/lapuj77/jdg-redac-dashboard.git
cd jdg-redac-dashboard
pip install -r requirements.txt
```

### Configuration

Créer `.streamlit/secrets.toml` :

```toml
app_password   = "votre_mot_de_passe"
anthropic_key  = "sk-ant-..."
```

Ou renseigner `config.json` à la racine :

```json
{
  "app_password": "votre_mot_de_passe",
  "anthropic_key": "sk-ant-..."
}
```

### Credentials Google Search Console

Le dashboard réutilise le token OAuth2 du projet `seo-monitor` :

```
../seo-monitor/credentials/gsc_token.json
```

Ce fichier est généré automatiquement lors de la première authentification dans `seo-monitor`.

### Lancement

```bash
python -m streamlit run dashboard.py
# ou double-clic sur lancer_dashboard.bat
```

---

## Format des fichiers CSV

Le CSV doit contenir les colonnes suivantes (export interne) :

| Colonne    | Description                          |
|------------|--------------------------------------|
| `Titre`    | Titre de l'article                   |
| `Rédacteur`| Prénom Nom de l'auteur               |
| `Date`     | Date de publication (JJ/MM/AAAA)     |
| `Vues`     | Nombre de vues                       |
| `Mots`     | Nombre de mots                       |
| `Type`     | Type : `post`, `test`, `dossier`, `bonplan`, `critique` |

**Nommage attendu :**
- Hebdomadaire : `Auteur_Tous_2026-03-16_2026-03-22.csv`
- Mensuel : tout fichier dont la plage de dates dépasse 20 jours

---

## Déploiement Streamlit Cloud

L'app est déployée sur [Streamlit Community Cloud](https://streamlit.io/cloud).  
Tout push sur `master` déclenche un redéploiement automatique.

Les secrets (`app_password`, `anthropic_key`) sont à renseigner dans les settings de l'app sur Streamlit Cloud — **ne jamais committer `.streamlit/secrets.toml`**.

---

## Structure du projet

```
reu-redac/
├── dashboard.py          # Application principale
├── requirements.txt      # Dépendances Python
├── config.json           # Config locale (non commité)
├── logo-jdg.jpg          # Logo sidebar/header
├── lancer_dashboard.bat  # Raccourci lancement Windows
├── archives/             # CSV archivés localement
└── .streamlit/
    └── secrets.toml      # Secrets locaux (non commité)
```
