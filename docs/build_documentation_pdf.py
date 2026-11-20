"""Build AID427 Phase 1 project documentation PDF with reportlab."""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak, HRFlowable, ListFlowable,
                                ListItem, KeepTogether)
from reportlab.lib.colors import HexColor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE is docs/ -> parent is project root when script lives in docs/
if os.path.basename(BASE) == "docs":
    ROOT = os.path.dirname(BASE)
else:
    ROOT = BASE
FIG = os.path.join(ROOT, "figures", "phase1")
OUT = os.path.join(ROOT, "docs", "AID427_Project_Documentation.pdf")

ACCENT = HexColor("#1B3A5C")
LIGHT_BG = HexColor("#EDF2F7")

styles = getSampleStyleSheet()
sTitle = ParagraphStyle("Title2", parent=styles["Title"], fontSize=22, leading=26,
                        textColor=ACCENT, alignment=TA_CENTER, spaceAfter=6)
sSubtitle = ParagraphStyle("Sub", parent=styles["Normal"], fontSize=12, leading=15,
                           alignment=TA_CENTER, textColor=colors.HexColor("#444444"))
sH1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15, leading=18,
                     textColor=ACCENT, spaceBefore=14, spaceAfter=6,
                     borderPadding=(0, 0, 4, 0))
sH2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, leading=15,
                     textColor=HexColor("#2C5282"), spaceBefore=10, spaceAfter=4)
sBody = ParagraphStyle("Body", parent=styles["Normal"], fontSize=9.5, leading=13.5,
                       alignment=TA_JUSTIFY, spaceAfter=5)
sBullet = ParagraphStyle("Bullet", parent=sBody, leftIndent=16, bulletIndent=6)
sCap = ParagraphStyle("Cap", parent=styles["Normal"], fontSize=8, leading=10.5,
                      alignment=TA_CENTER, textColor=colors.HexColor("#555555"),
                      spaceAfter=8)
sCell = ParagraphStyle("Cell", parent=styles["Normal"], fontSize=7.5, leading=9.5)
sCellH = ParagraphStyle("CellH", parent=sCell, textColor=colors.white,
                        fontName="Helvetica-Bold")
sCellSmall = ParagraphStyle("CellS", parent=styles["Normal"], fontSize=7, leading=8.5)

def P(t):
    return Paragraph(t, sBody)

def H(t):
    return Paragraph(t, sH1)

def H2(t):
    return Paragraph(t, sH2)

def tbl(headers, rows, widths=None, small=False):
    cs = sCellSmall if small else sCell
    data = [[Paragraph(f"<b>{h}</b>", sCellH) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), cs) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

def fig(name, width_cm=15, caption=""):
    p = os.path.join(FIG, name)
    elems = []
    if os.path.exists(p):
        elems.append(Image(p, width=width_cm * cm, height=width_cm * 0.55 * cm,
                           kind="proportional"))
        if caption:
            elems.append(Paragraph(caption, sCap))
    else:
        elems.append(Paragraph(f"[Figure missing: {name}]", sCap))
    return elems

story = []
# ---------- COVER ----------
story.append(Spacer(1, 2.2 * cm))
story.append(Paragraph("Feature Reduction, Feature Selection<br/>and Metaheuristic Optimisation<br/>for Sales-Level Classification", sTitle))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph("Noisy Walmart Retail Dataset — A Comparative Analysis", sSubtitle))
story.append(Spacer(1, 0.4 * cm))
story.append(HRFlowable(width="60%", thickness=1.2, color=ACCENT, spaceAfter=10, spaceBefore=6, hAlign="CENTER"))
story.append(Paragraph("AID427 — Math for Data Science · Project Phase 1<br/>Egypt-Japan University of Science and Technology (E-JUST)<br/>Artificial Intelligence and Data Science Program", sSubtitle))
story.append(Spacer(1, 0.6 * cm))
cover_info = [
    ["Dataset", "Walmart Recruiting — Store Sales Forecasting (421,570 dept-weeks, 45 stores, 81 depts)"],
    ["Task", "Balanced 3-class sales-level classification: Low / Medium / High (tertiles)"],
    ["Code", "Modeling.ipynb (Phase 1 section, self-contained, seed 42) + Extra_Analysis.ipynb"],
    ["Results", "results/phase1_results/ (JSON + 12 CSVs) · figures/phase1/ (30 figures)"],
    ["Paper", "paper/main.tex (IEEEtran) with full methods, results, comparison"],
    ["Date", "November 2026"],
]
story.append(tbl(["Item", "Detail"], cover_info, widths=[3.2 * cm, 13.3 * cm]))
story.append(Spacer(1, 0.5 * cm))
story.append(Paragraph("This document is generated from the repository contents (notebooks, paper sources and phase1_results.json). "
                       "It describes the data, preprocessing, methods, results and how to reproduce every table and figure.", sBody))
story.append(PageBreak())

# ---------- TOC (manual) ----------
story.append(H("Contents"))
toc = ["1. Objectives and Task Framing", "2. Dataset and Noise Audit", "3. Target Definition and Preprocessing",
       "4. Experimental Setup (Sampling, Splits, Reproducibility)", "5. Methods",
       "6. Results", "7. Comparison with Related Work", "8. Repository Structure",
       "9. How to Reproduce", "10. Limitations and Future Work", "References & Artefacts"]
for t in toc:
    story.append(Paragraph(t, sBullet))

# ---------- 1 ----------
story.append(H("1. Objectives and Task Framing"))
story.append(P("Weekly department-level retail sales are heavy-tailed, partly missing and influenced by many weak covariates. "
               "Instead of point regression of weekly sales, this project re-formulates the Walmart <i>Store Sales Forecasting</i> data as a "
               "<b>balanced three-class sales-level problem (Low / Medium / High)</b> defined by the tertiles of the training distribution. "
               "Operational decisions (staffing template, replenishment tier) are categorical, so the formulation matches practice while giving "
               "a demanding benchmark for feature engineering."))
story.append(P("The study compares <b>10 feature-reduction methods</b> (PCA, LDA, SVD, Kernel PCA, SNE implemented from scratch, t-SNE, UMAP, "
               "metric/non-metric MDS, Isomap, LLE), <b>4 feature-selection families</b> (filter, wrapper, embedded, metaheuristic: GA / Binary PSO / "
               "Simulated Annealing), K-Means clustering before/after reduction, and <b>9 classifiers</b> evaluated with hold-out, stratified 5-fold CV, "
               "confusion matrices, ROC analysis and learning/validation curves."))

# ---------- 2 ----------
story.append(H("2. Dataset and Noise Audit"))
story.append(P("Source: Kaggle <i>Walmart Recruiting — Store Sales Forecasting</i>: <b>train</b> (421,570 department-week rows: Store, Dept, Date, "
               "Weekly_Sales, IsHoliday; 5 Feb 2010 – 26 Oct 2012), <b>features</b> (store-week context: Temperature, Fuel_Price, MarkDown1–5, CPI, "
               "Unemployment) and <b>stores</b> (Type A/B/C, Size). Joined on (Store, Date) and Store. Four Walmart holiday weeks (Super Bowl, Labor Day, "
               "Thanksgiving, Christmas) are flagged; the competition weights them 5x."))
story.append(tbl(["Issue", "Count", "% rows"],
    [["Negative weekly sales (returns)", "1,285", "0.30"],
     ["Sales outliers (1.5x IQR)", "35,521", "8.43"],
     ["MarkDown1 missing", "270,889", "64.26"],
     ["MarkDown2 missing", "310,322", "73.61"],
     ["MarkDown3 missing", "284,479", "67.48"],
     ["MarkDown4 missing", "286,603", "67.98"],
     ["MarkDown5 missing", "270,138", "64.08"],
     ["Negative MarkDown values (entry errors)", "1,568", "0.37"],
     ["Holiday-week rows", "29,661", "7.04"],
     ["Skewness of Weekly_Sales", "3.26 (mean $15,981 vs median $7,612; max $693,099)", "—"]],
    widths=[8.5 * cm, 3.5 * cm, 3.5 * cm]))
story.append(Paragraph("Table 1 — Noise and quality issues (421,570 rows). MarkDowns missing mostly before Nov 2011; context variables are identical "
                       "for ~74 departments of a store-week, hence weak/redundant for the dept-level target.", sCap))
story += fig("01_eda_overview.png", 15.5,
    "Figure 1 — EDA before reduction: signed log-sales with class thresholds; chain-wide weekly sales (Thanksgiving spike ~$66M, pre-Christmas ~$81M); "
    "size by type/class; MarkDown missingness.")
story += fig("02_correlation.png", 11,
    "Figure 2 — Spearman correlation. Strongest monotone signal: Size (rho=0.26), Type dummies (|rho|=0.10–0.19); all others |rho|&lt;0.08. "
    "Dept has rho=-0.03 yet is the most informative variable (non-monotone identifier effect).")

# ---------- 3 ----------
story.append(H("3. Target Definition and Preprocessing"))
story.append(P("Three ordered classes by the 33.3rd / 66.7th percentiles of Weekly_Sales: <b>Low (&le; $3,521.78), Medium ($3,521.78–$14,599.76), "
               "High (&gt; $14,599.76)</b> — balanced 140,524 / 140,523 / 140,523 rows, chance level 33.3%. Negative sales (returns) are kept as genuine "
               "events in Low."))
story.append(H2("3.1 Preprocessing pipeline (fit on training data only)"))
for b in ["<b>Missing promotions → 0</b> (no promotion that week) + binary <b>MarkDown_Available</b> flag preserving missingness info.",
          "<b>Promotion noise:</b> negative MarkDowns clipped to 0; each MarkDown winsorised at 99.5th percentile.",
          "<b>Calendar features from Date:</b> Year, Month, ISO Week, Day, signed days to Thanksgiving / Christmas, Super Bowl and Labor Day indicators.",
          "<b>Encoding:</b> store Type one-hot (Type_A/B/C); IsHoliday cast to int.",
          "<b>Result: 25 features, no missing values.</b> Groups — Identity: Store, Dept; Store: Size, Type_A/B/C; Economy: Temperature, Fuel_Price, CPI, "
          "Unemployment; Promotion: MarkDown1–5, MarkDown_Available; Calendar: IsHoliday, Year, Month, Week, Day, Days_to_Thanksgiving, Days_to_Christmas, SuperBowl, LaborDay."]:
    story.append(Paragraph(b, sBullet, bulletText="•"))

# ---------- 4 ----------
story.append(H("4. Experimental Setup"))
story.append(P("<b>Sampling (compute budget: 2-core / 8-GB machine):</b> stratified sample of <b>100,000 rows</b> (23.7%) split <b>80/20 stratified</b> "
               "(80k train / 20k test). Selection uses a 20,000-row subsample of the <i>training</i> split only — test rows never influence selection. "
               "Manifold methods use a 3,000-point training subsample (1,500 for from-scratch SNE, 1,000 for MDS). "
               "<b>Seed 42</b> everywhere; stack: scikit-learn, LightGBM, XGBoost, umap-learn. "
               "The Phase-1 notebook section reloads raw data so it runs standalone (Kernel → Restart from the Phase-1 header)."))

# ---------- 5 ----------
story.append(H("5. Methods"))
story.append(H2("5.1 Linear reduction"))
story.append(P("PCA: eigen-decomposition of covariance, keep top-k (16 comps = 95% variance). LDA: generalised eigenproblem on between/within scatter "
               "(C=3 classes → max 2 axes; supervised). Truncated SVD on standardised (= centred) data as PCA sanity check."))
story.append(H2("5.2 Non-linear reduction"))
story.append(P("Kernel PCA (RBF, gamma from {0.005, 0.02, 0.05, 0.1} by kNN accuracy — best 0.005, near-linear). "
               "SNE from scratch (perplexity 30, momentum 0.5→0.8, lr 0.1, 600 iters, gradient clipping). t-SNE (perplexity 30, PCA init, Student-t kernel). "
               "UMAP (15 neighbours, min_dist 0.1). Metric MDS (raw stress, SMACOF) vs non-metric MDS (isotonic mapping). Isomap (10-NN geodesics). "
               "LLE (12 neighbours, local-weight preservation)."))
story.append(H2("5.3 Embedding quality criteria"))
story.append(P("(i) 5-fold accuracy of 5-NN <i>in</i> the embedding (class information retained); (ii) trustworthiness "
               "T(k), k=10 (fraction of embedding neighbours that are true neighbours); (iii) silhouette of true classes. "
               "Clustering: K-Means k=3 — silhouette of found clusters + ARI / NMI vs true classes."))
story.append(H2("5.4 Feature selection (all on 20k training rows)"))
for b in ["<b>Filter (K=10 by rank fusion):</b> min-max variance, |Spearman| vs ordinal class, ANOVA-F, chi2 (min-max), mutual information "
          "(discrete handling &lt;60 uniques). Fast (&lt;1 s) but redundancy-blind.",
          "<b>Wrapper (K=10, fast LightGBM-60-trees, 3-fold macro-F1):</b> SFS-forward (99 s), SFS-backward (201 s), RFE with 60-tree RF (14 s).",
          "<b>Embedded:</b> multinomial logistic (C=0.05) under L1 / L2 / Elastic-Net (alpha=1/0/0.5); keep non-zero coefficient-norm features "
          "(L1:19, EN:21, L2: top-10 norms). Plus LightGBM total-gain reference (Dept 67.0%, Size 14.5%, Store 4.8%).",
          "<b>Metaheuristics — bit-mask b in {0,1}^25, fitness f(b)= mean 3-fold macro-F1 − 0.02·|b|/25</b> (size-penalised, cached): "
          "GA (pop 24, 20 gens, pc=0.9, pm=1/25, tournament k=3, elitism 2; 331 evals, 193 s); BPSO (20 particles, 20 iters, w=0.7, c1=c2=1.5, vmax ±4, "
          "sigmoid transfer; 400 evals, 242 s); SA (300 single-bit moves, T0=0.02, alpha=0.985, Metropolis; 248 evals, 151 s)."]:
    story.append(Paragraph(b, sBullet, bulletText="•"))
story.append(H2("5.5 Classifiers and evaluation"))
story.append(P("Nine models: Logistic Regression, Gaussian NB, k-NN (k=15), unpruned Decision Tree, Random Forest (150 trees, min-leaf 2), "
               "Extra Trees (same), MLP (128–64 ReLU, early stopping), XGBoost (400 trees, depth 8, lr 0.1, subsample 0.9), "
               "LightGBM (500 trees, 127 leaves, lr 0.05). Scale-sensitive models in StandardScaler pipelines fit on train folds only."))
story.append(P("Metrics on 20% test: confusion matrix, accuracy, error rate, macro precision/recall/F1, macro one-vs-rest ROC-AUC. "
               "Stratified 5-fold CV on full 100k (mean ± std). Diagnosis: gap (train−test) &gt; 5 pts → over-fitting; test &lt; 70% with small gap → "
               "under-fitting. Plus LightGBM learning curve and tree-depth validation curve."))

# ---------- 6 ----------
story.append(H("6. Results"))
story.append(H2("6.1 Linear reduction"))
story.append(P("PC1 (17.5%) + PC2 (14.9%); <b>16/25 components for 95% variance</b> — flat noisy spectrum. Last 4 comps ~0 variance "
               "(Type_A+B+C=1; Week/Days_to_Thanksgiving/Days_to_Christmas collinear). PC1 = seasonality (Week/Month/days-to-holiday, loading 0.43 each); "
               "PC2 = promotion era (MarkDown_Available 0.41, MarkDown5 0.37, MarkDown1 0.36, Year 0.34) — orthogonal to Dept/Size, so classes mix. "
               "LDA disc-1 explains 84.3%; only supervised map shows Low/High regions (2-D kNN 46.3%) but as classifier only 44.1% → boundaries non-linear. "
               "SVD reproduces PCA (17.4%/15.0%, kNN 37.1%, trust 0.889; singulars 591.7/545.4/447.6/392.6/375.9)."))
story += fig("04_pca_scree_loadings.png", 15.5, "Figure 3 — PCA scree (16 comps to 95%) and loadings of first three PCs.")
story += fig("05_linear_embeddings.png", 15.5, "Figure 4 — Linear 2-D maps (PCA, SVD identical up to sign; LDA shows partial separation).")
story.append(H2("6.2 Non-linear reduction (all ten embeddings)"))
story.append(tbl(["Method", "kNN acc.", "Trustw.", "Class sil.", "Time (s)"],
    [["PCA", "0.371", "0.889", "-0.016", "0.002"],
     ["LDA (supervised)", "0.463", "0.699", "-0.020", "0.14"],
     ["SVD", "0.371", "0.889", "-0.016", "0.005"],
     ["Kernel PCA (g=0.005)", "0.364", "0.889", "-0.014", "2.1"],
     ["SNE (from scratch, 1500 pts)", "0.373", "0.958", "-0.019", "44.8"],
     ["t-SNE", "0.395", "0.996", "-0.024", "7.9"],
     ["UMAP", "0.388", "0.990", "-0.030", "10.8"],
     ["Metric MDS (1000 pts)", "0.374", "0.899", "-0.023", "4.0"],
     ["Non-metric MDS (1000 pts)", "0.370", "0.900", "-0.029", "55.2"],
     ["Isomap", "0.374", "0.910", "-0.043", "1.9"],
     ["LLE", "0.351", "0.841", "-0.079", "2.3"]],
    widths=[6.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm]))
story.append(Paragraph("Table 2 — 2-D embedding quality (3,000-pt sample; raw 25-D 5-NN reference 0.412). t-SNE/UMAP best neighbourhood fidelity; "
                       "LDA best class signal (supervised); LLE worst (collapses on duplicate store-week contexts).", sCap))
story.append(P("Islands = store context, not sales segments: 5-NN in t-SNE/UMAP recovers store type (99.4%/98.8%), year (97.8%/96.3%), promotion era "
               "(99.5%/99.3%) but sales class only 39.5%/38.8%. SNE shows classic crowding (uniform cloud vs t-SNE). Non-metric MDS costs 14x metric for "
               "no gain. Isomap → calendar filaments; LLE → degenerate line (exact-duplicate neighbourhoods). All class silhouettes negative (−0.08…−0.01)."))
story += fig("06_all_embeddings.png", 15.5, "Figure 5 — All ten 2-D embeddings coloured by true class (kNN accuracy in brackets).")
story.append(H2("6.3 Clustering before and after reduction"))
story.append(tbl(["Space", "Silhouette", "ARI", "NMI"],
    [["Original (25-D)", "0.131", "0.000", "0.001"],
     ["PCA (16-D, 95% var)", "0.136", "0.000", "0.001"],
     ["PCA (2-D)", "0.437", "0.001", "0.001"],
     ["LDA (2-D)", "0.453", "0.018", "0.024"],
     ["t-SNE (2-D)", "0.473", "0.008", "0.008"],
     ["UMAP (2-D)", "0.570", "0.009", "0.009"]],
    widths=[6 * cm, 3.5 * cm, 3.5 * cm, 3.5 * cm]))
story.append(Paragraph("Table 3 — K-Means (k=3). Silhouette rises sharply in 2-D (UMAP 0.57) but ARI/NMI ≈ 0: crisp clusters are seasons/promo-eras/store tiers, "
                       "not sales levels. A good-looking UMAP ≠ three sales segments.", sCap))
story += fig("07_clustering_before_after.png", 15.5, "Figure 6 — K-Means clusters before (shown on PCA plane) and after reduction.")
story.append(H2("6.4 Filter selection"))
story.append(P("Rank fusion top-10: Size (2.00), Type_A (3.00), Type_C (3.75), Dept (4.75), Store (4.75), Type_B (6.50), MarkDown1 (7.50), MarkDown4 (8.25), "
               "MarkDown5 (9.25), CPI (10.50). Only variance flags MarkDown3 as near-constant. Key disagreement: linear stats rank Size/Type top and Dept "
               "low (|rho|=0.027); mutual information ranks Dept first by far (MI 0.418 nats, ~7x Store 0.063). Filters are fast but keep redundant dummies + "
               "MarkDowns → weakest subset later (91.04%)."))
story += fig("08_filter_scores.png", 15.5, "Figure 7 — Filter scores: MI alone recognises Dept; ANOVA-F/Spearman favour Size and store type.")
story.append(H2("6.5 Wrapper and embedded selection"))
story.append(P("<b>Wrappers</b> (all keep Store/Dept/Size + Week; CV-F1 0.871/0.867/0.866): forward adds cheap categorical context (Type block, holiday flags); "
               "backward keeps MarkDowns + CPI/Unemployment; RFE keeps 4 economic + 2 calendar vars. Cost: RFE 14 s, forward 99 s, backward 201 s. "
               "<b>Embedded:</b> L1 keeps 19/25, EN 21/25 (train acc ~44.1% — linear under-fit; penalty selects among features of an inadequate model); "
               "L2 keeps all (top-10 norms reported). All agree on Size/Type_C/Dept/Type_B/CPI top. LightGBM gain (non-linear reference): Dept 67.0% alone."))
story += fig("09_embedded.png", 15.5, "Figure 8 — Embedded: logistic coefficient norms (zero = removed) + LightGBM gain share (Dept-dominated).")
story.append(H2("6.6 Metaheuristic selection"))
story.append(tbl(["Algorithm", "#feat", "F1", "Fitness", "Evals", "Time (s)"],
    [["GA: Store Dept Size Type_B CPI Week", "6", "0.872", "0.867", "331", "193"],
     ["BPSO (9 feats)", "9", "0.870", "0.863", "400", "242"],
     ["SA: Store Dept Size Type_B Days_to_Thanksgiving", "5", "0.873", "0.869", "248", "151"]],
    widths=[7.5 * cm, 1.5 * cm, 1.8 * cm, 1.8 * cm, 1.5 * cm, 2.4 * cm], small=True))
story.append(Paragraph("Table 4 — Metaheuristics (fitness = 3-fold macro-F1 − 0.02·k/25). Shared core {Store, Dept, Size, Type_B}; SA smallest, GA best trade-off. "
                       "BPSO adds IsHoliday/CPI/holiday distances. GA jumps early (crossover), BPSO steady contraction, SA slow climb with downhill moves.", sCap))
story += fig("10_metaheuristic_convergence.png", 11, "Figure 9 — Convergence of best fitness (x-axis normalised).")
story.append(P("<b>Consensus (11 selectors):</b> Store/Dept/Size 11/11, Type_B 10/11, CPI 9/11; Days_to_Christmas 0 (exact copy of Days_to_Thanksgiving), "
               "MarkDown3/MarkDown5 only 2 each. Identity + size of store-department first, macro-economy distant second, promotions/holiday flags marginal once identity known."))
story += fig("11_selection_frequency.png", 11, "Figure 10 — Selection frequency across the 11 methods.")
story.append(H2("6.7 Selection before reduction"))
story.append(tbl(["Method", "kNN all-25", "kNN GA-6", "Delta", "Trust (GA)"],
    [["PCA", "0.371", "0.505", "+0.134", "0.938"],
     ["LDA", "0.463", "0.461", "-0.002", "0.891"],
     ["t-SNE", "0.395", "0.515", "+0.120", "0.999"],
     ["UMAP", "0.388", "0.500", "+0.112", "0.998"]],
    widths=[3.5 * cm, 3 * cm, 3 * cm, 2.5 * cm, 3.5 * cm]))
story.append(Paragraph("Table 5 — Same 3,000 points embedded from all 25 vs 6 GA features. Unsupervised maps gain +11–13 pts; supervised LDA unchanged "
                       "(already down-weights noise). K-Means ARI still ≤0.03 — even clean maps cannot geometrise nominal Dept. Lesson: select before you reduce.", sCap))
story += fig("17_reduction_after_selection.png", 15.5, "Figure 11 — Top: all-25 embeddings; bottom: GA-6 embeddings (more class-coherent neighbourhoods).")
story.append(H2("6.8 Classification: hold-out"))
story.append(tbl(["Model", "Train", "Test", "F1", "AUC", "Gap", "Diagnosis"],
    [["LightGBM", "0.993", "0.934", "0.934", "0.991", "0.059", "Slight over-fit"],
     ["XGBoost", "0.987", "0.932", "0.932", "0.990", "0.056", "Slight over-fit"],
     ["Decision Tree", "1.000", "0.902", "0.902", "0.926", "0.098", "Over-fitting"],
     ["MLP", "0.726", "0.690", "0.687", "0.852", "0.036", "Under-fitting"],
     ["Random Forest", "0.925", "0.671", "0.670", "0.850", "0.254", "Over-fitting"],
     ["Extra Trees", "0.910", "0.601", "0.599", "0.788", "0.309", "Over-fitting"],
     ["KNN (k=15)", "0.592", "0.508", "0.506", "0.694", "0.084", "Over+under"],
     ["Gaussian NB", "0.456", "0.462", "0.460", "0.638", "-0.006", "Under-fitting"],
     ["LogReg", "0.441", "0.444", "0.443", "0.631", "-0.003", "Under-fitting"]],
    widths=[3.2*cm,1.7*cm,1.7*cm,1.7*cm,1.7*cm,1.5*cm,4.0*cm], small=True))
story.append(Paragraph("Table 6 — Hold-out (80k/20k, all 25 feats; macro P/R/F1, OvR AUC). Three tiers: boosting ≫ single tree ≫ everything that cannot exploit "
                       "Dept as nominal identifier (44–69%). LightGBM fit 9.2 s, XGBoost 7.7 s, MLP 61.7 s.", sCap))
story.append(tbl(["", "Accuracy", "Macro-F1", "ROC-AUC"],
    [["LightGBM", "0.9342 ± 0.0020", "0.9343 ± 0.0020", "0.9906"],
     ["XGBoost", "0.9306 ± 0.0013", "0.9307 ± 0.0013", "0.9898"],
     ["Decision Tree", "0.9042 ± 0.0014", "0.9042 ± 0.0013", "0.9282"],
     ["Random Forest", "0.6699 ± 0.0019", "0.6695 ± 0.0018", "0.8492"],
     ["MLP", "0.6645 ± 0.0235", "0.6606 ± 0.0228", "0.8361"],
     ["Extra Trees", "0.5953 ± 0.0050", "0.5936 ± 0.0049", "0.7855"],
     ["KNN (k=15)", "0.5091 ± 0.0029", "0.5070 ± 0.0029", "0.6915"],
     ["Gaussian NB", "0.4570 ± 0.0034", "0.4548 ± 0.0054", "0.6347"],
     ["LogReg", "0.4410 ± 0.0007", "0.4403 ± 0.0006", "0.6294"]],
    widths=[4.0*cm,4.2*cm,4.2*cm,4.1*cm], small=True))
story.append(Paragraph("Table 7 — Stratified 5-fold CV on 100k (mean ± std). CV agrees with hold-out ≤0.2 pts except MLP (unstable 63.2–69.4%, early-stopping variance). "
                       "LightGBM worst fold (93.12%) still beats XGBoost mean.", sCap))
story += fig("12_cv_boxplot.png", 11, "Figure 12 — Fold-wise 5-fold accuracy (only MLP spreads).")
story.append(H2("6.9 Confusion matrices and ROC"))
story.append(P("LightGBM recalls: Low 95.3%, Medium 90.1%, High 94.9% — Medium borders both sides. Of 1,312 errors the top cell is Medium→Low (383); "
               "only 7 (0.5%) are far Low↔High — near-threshold, low-cost errors. Same pattern for XGBoost (9 far) and tree (23). "
               "Linear models invert this: LogReg 11,122 errors, 3,094 far (27.8%), top cell Medium→High (2,698), Medium recall 37.2% — no usable notion of sales ordering."))
story += fig("13_confusion_matrices.png", 15.5, "Figure 13 — Row-normalised test confusion matrices (top: 3 best; bottom: tree + 2 under-fitting models).")
story.append(P("Per-class LightGBM AUC: Low 0.995, Medium 0.982, High 0.996 (micro-average figure). RF/MLP rank far better than they decide "
               "(AUC 0.850/0.852 vs acc 67–69%) — errors concentrate near thresholds."))
story += fig("14_roc_curves.png", 15.5, "Figure 14 — ROC: LightGBM per-class (left) + micro-average of all nine models (right).")
story.append(H2("6.10 Over- / under-fitting"))
story.append(P("Train–test gaps: LogReg/NB equal + low (pure under-fit); tree 100% train / 9.8-pt gap; RF/ET 25.4/30.9-pt gaps (memorise store-week context); "
               "k=15-NN both problems (50.8% + 8.4-pt gap); LightGBM/XGBoost 5.9/5.6-pt gaps — benign for boosted ensembles at best accuracy. "
               "LightGBM learning curve: train 100% (99.8% full), val 77.2% → 85.5% → 89.1% → 91.5% → 92.6% with 2.7k→53k rows, no plateau — variance gap, "
               "more store-dept-weeks would add ~1 pt. Depth curve: under-fit at depth 2 (46.9%/46.9%), joint rise to depth 8 (76.6/76.0), val peak at depth 16 "
               "(89.5%), over-fit beyond (train→100%, val→89.2%)."))
story += fig("15_over_under_fitting.png", 15.5, "Figure 15 — Train vs test bars; LightGBM learning curve; tree-depth validation curve (optimum 16).")
story.append(H2("6.11 Ablation: why default forests fail"))
story.append(tbl(["Model", "max_feat", "Train", "Test", "F1", "AUC"],
    [["Random Forest", "sqrt (5)", "0.925", "0.671", "0.670", "0.850"],
     ["Random Forest", "0.5 (12)", "0.990", "0.914", "0.914", "0.981"],
     ["Random Forest", "1.0 (25)", "0.989", "0.930", "0.930", "0.988"],
     ["Extra Trees", "sqrt (5)", "0.910", "0.601", "0.599", "0.788"],
     ["Extra Trees", "0.5 (12)", "0.998", "0.905", "0.905", "0.977"],
     ["Extra Trees", "1.0 (25)", "0.997", "0.933", "0.933", "0.990"]],
    widths=[3.5*cm,2.5*cm,2.2*cm,2.2*cm,2.2*cm,2.2*cm], small=True))
story.append(Paragraph("Table 8 — max_features ablation (150 trees). Dept carries 67% of gain but is offered at only ~20% of splits under sqrt(25)=5; "
                       "trees split on near-unique context vars and memorise. Full-subspace bagging reaches 93.0/93.3% (gaps 3–6 pts). Lesson: random-subspace "
                       "hurts when one nominal feature dominates.", sCap))
story.append(H2("6.12 Effect of reduction / selection on the best model"))
story.append(tbl(["Input", "Dims", "Test acc", "F1", "AUC", "Fit (s)"],
    [["GA (6)", "6", "0.9370", "0.9369", "0.9915", "5.5"],
     ["BPSO (9)", "9", "0.9364", "0.9364", "0.9915", "5.7"],
     ["RFE (10)", "10", "0.9354", "0.9354", "0.9910", "6.2"],
     ["LGBM-gain (10)", "10", "0.9346", "0.9346", "0.9911", "6.6"],
     ["All (25)", "25", "0.9344", "0.9344", "0.9906", "9.5"],
     ["SFS-back (10)", "10", "0.9342", "0.9342", "0.9909", "7.2"],
     ["SFS-for (10)", "10", "0.9332", "0.9332", "0.9907", "5.1"],
     ["SA (5)", "5", "0.9322", "0.9322", "0.9907", "5.0"],
     ["L2 (10)", "10", "0.9146", "0.9146", "0.9859", "5.3"],
     ["Filter (10)", "10", "0.9104", "0.9103", "0.9841", "6.2"],
     ["PCA-16", "16", "0.6968", "0.6960", "0.8761", "9.5"],
     ["LDA-2", "2", "0.5108", "0.5104", "0.6984", "4.5"]],
    widths=[3.6*cm,1.4*cm,1.9*cm,1.9*cm,1.9*cm,1.8*cm], small=True))
story.append(Paragraph("Table 9 — LightGBM retrained per input (same 80/20). Metaheuristic subsets best: GA-6 tops full model (+0.26 pts, 76% fewer feats, "
                       "42% faster, gap 4.5 pts). Wrappers/embedded-gain match full with 10 feats. Linear/univariate subsets lose 2–2.4 pts. "
                       "Projections destroy tree signal: PCA −24 pts, LDA −42 pts — rotation mixes nominal Dept with noise, killing axis-aligned splits. "
                       "For tree ensembles on mixed tabular data: select, don't project.", sCap))
story += fig("16_subset_comparison.png", 11, "Figure 16 — Test macro-F1 per input (dims annotated; metaheuristics in green).")

# ---------- 7 ----------
story.append(H("7. Comparison with Related Work"))
story.append(P("All prior Walmart studies are regression (R2/MAE/RMSE/SMAPE) at store or dept level — not directly comparable to classification accuracy/F1/AUC — "
               "and two use store-level aggregates (errors in $100ks). Agreement on four points: (i) boosted trees strongest conventional learners "
               "(XGBoost best in Chenwi et al. 2024, Akande et al. 2022; only TFT in Punati et al. 2025 beats it); (ii) linear models fail at dept level "
               "(reasonable at store level where Dept is summed out); (iii) over-fitting is the main risk (polynomial RMSE explosion ↔ tree/forest gaps, depth curve); "
               "(iv) identity/size dominate (Type/Size in Chen 2022 ↔ Store/Dept/Size unanimous here). "
               "This work's addition: 10-method reduction comparison with quality criteria, clustering negative result, 4-family selection incl. GA/BPSO/SA, "
               "and selection-before-reduction (+10 pts) plus 6-feat GA beating the full model."))
story.append(tbl(["Study", "Task", "Best result"],
    [["Chen (2022)", "Regression, store", "MLR R2=0.933; ENR 0.814; poly over-fits"],
     ["Akande et al. (2022)", "Regression", "XGBoost effective"],
     ["Yao (2023)", "Regression, dept", "RF R2=0.937, MAE=1937.8"],
     ["Chenwi et al. (2024)", "Regression", "XGBoost MAE=1226.5"],
     ["Punati et al. (2025)", "Forecast, store", "TFT R2=0.9875, SMAPE 4.51%"],
     ["This work", "3-class level, dept", "LightGBM 93.44%/0.934/0.991; GA-6 93.70%/0.992"]],
    widths=[3.8*cm, 4.2*cm, 8.5*cm], small=True))

# ---------- 8 ----------
story.append(H("8. Repository Structure"))
story.append(P("Root contains the two notebooks, plus four tracked folders (raw Datasets/ is git-ignored and must be downloaded from Kaggle — see §9):"))
struct = [["Modeling.ipynb", "Main experiments. Cells 0–34: Kaggle regression baseline (RF/ET + submissions). From cell 35 (Phase 1 header): self-contained Phase-1 pipeline — load → noise audit → 25 feats → 100k/20k/3k samples → 10 reductions → K-Means → filter/wrapper/embedded/GA-BPSO-SA → 9 classifiers → CV/CM/ROC/curves → ablation → subset retrain → JSON + figures."],
    ["Extra_Analysis.ipynb", "Supplementary deep-dives (calendar windows, promotions, exogenous relationships, sales anatomy, missingness, cartography, error analysis, overlap, F1-vs-dims, elbows, dominance, temporal structure, preprocessing effects)."],
    ["results/phase1_results/", "phase1_results.json (all numbers) + 12 CSVs: 01 holdout, 02 CV-5fold, 03 embedding quality, 04 clustering, 05 reduction-after-selection, 06 filter scores, 07 subsets, 08 metaheuristics, 09 best-model-per-subset, 10 forest ablation, 11 confusion interpretation, 12 related work."],
    ["figures/phase1/", "30 PNGs 01–30 (EDA → correlation → PCA/loadings → embeddings → clustering → filters → embedded → convergence → frequency → CV/CM/ROC/fit → subsets → reduction-after-selection → preprocessing/temporal/dominance/quality/composition/elbow/dims/overlap/error/cartography/missingness/anatomy/exogenous/promotions/windows)."],
    ["paper/", "IEEE conference paper (main.tex + sec_*.tex, refs.bib, IEEEtran.cls/bst): pipeline figure, all tables/figures; paper/figures/ = curated copies of key PNGs."],
    ["docs/ + archive/", "This PDF + cover-sheet PDF live in docs/; archive/ holds phase1_results.zip, phase1_figures.zip, LaTeX-source zip."]]
story.append(tbl(["Path", "Contents"], struct, widths=[4.2 * cm, 12.3 * cm], small=True))

# ---------- 9 ----------
story.append(H("9. How to Reproduce"))
for i, b in enumerate([
    "<b>Data:</b> download Kaggle <i>Walmart Recruiting — Store Sales Forecasting</i> (train.csv, features.csv, stores.csv, test.csv) into <b>Datasets/</b> at repo root (the notebooks expect paths Datasets/train.csv, ...).",
    "<b>Environment:</b> Python 3.10+ with scikit-learn, LightGBM, XGBoost, umap-learn, seaborn, matplotlib, pandas, numpy (uncomment the %pip line at the top of the Phase-1 section if needed).",
    "<b>Run:</b> open Modeling.ipynb → Kernel → Restart → run from the cell headed 'Phase 1 — Feature Reduction, Feature Selection & Classification (AID427)' (cell ~35). Everything reloads raw data; seed 42 controls sampling, splits, CV, embeddings and metaheuristics.",
    "<b>Outputs:</b> all reported numbers are written to results/phase1_results/phase1_results.json (plus the 12 CSVs) and every paper figure to figures/phase1/. Re-running regenerates Tables 1–9 and Figures 1–16 of this document.",
    "<b>Paper:</b> compile paper/main.tex with pdflatex + bibtex (IEEEtran) — figures are referenced from paper/figures/.",
    "<b>Timings (reference 2-core/8-GB):</b> filters &lt;1 s; RFE 14 s; SFS 99/201 s; GA 193 s; BPSO 242 s; SA 151 s; LightGBM fit ~9 s (GA-6 ~5.5 s); SNE 44.8 s; non-metric MDS 55.2 s."]):
    story.append(Paragraph(f"{i+1}. {b}", sBullet, bulletText="•"))

# ---------- 10 ----------
story.append(H("10. Limitations and Future Work"))
for b in ["<b>Random (not temporal) split</b> — required by the brief; each store-dept appears in train and test weeks, so typical levels are partly memorised. A forward-chaining time split (deployed-forecaster protocol) would score lower.",
          "<b>Sampling:</b> 100k modelling / 20k selection / 1–3k manifold points. Learning curve suggests ~+1 pt from full data.",
          "<b>Tertile thresholds</b> are statistical, not business-defined; most errors hug them. Store-specific cuts would shift absolute numbers, likely not rankings.",
          "<b>Defaults, not full search:</b> one hyper-parameter (max_features) moves forests 60→93%; nested (possibly metaheuristic) tuning is next.",
          "<b>Single-seed metaheuristics;</b> repeats would quantify variance.",
          "<b>Future:</b> (i) temporal-split evaluation; (ii) target/embedding encodings of Store/Dept so linear/distance/unsupervised methods can use them; "
          "(iii) multi-objective NSGA-II over accuracy × size × time; (iv) cost-sensitive/ordinal losses penalising Low↔High errors."]:
    story.append(Paragraph(b, sBullet, bulletText="•"))
story.append(H("Key takeaways"))
for b in ["LightGBM best: 93.44% / F1 0.934 / AUC 0.991 (CV 93.42±0.20%); errors near-adjacent (0.5% far).",
          "Linear/distance models under-fit (44–51%); default forests over-fit (gaps 25–31 pts) — ablation fixes via max_features.",
          "No unsupervised embedding/clustering recovers sales levels (ARI≈0) despite silhouettes up to 0.57.",
          "Select-before-reduce: +11–13 pts kNN in PCA/t-SNE/UMAP maps.",
          "GA-6 (Store, Dept, Size, Type_B, CPI, Week) beats full-25 (93.70% vs 93.44%, −42% time); BPSO-9/SA-5 comparable.",
          "For tree ensembles on mixed tabular data: selection preserves accuracy, projection destroys it."]:
    story.append(Paragraph(b, sBullet, bulletText="•"))

story.append(H("References & Artefacts"))
story.append(P("Full bibliography in paper/refs.bib. Core citations: Kaggle Walmart Store Sales Forecasting; Chen (2022); Akande et al. (2022); "
               "Yao (2023); Chenwi et al. (2024); Punati et al. (2025); Pearson (1901) PCA; Fisher (1936) LDA; Golub & Van Loan SVD; Schölkopf Kernel PCA; "
               "Hinton & Roweis (2002) SNE; van der Maaten & Hinton (2008) t-SNE; McInnes et al. (2018) UMAP; Torgerson MDS; Kruskal non-metric MDS; "
               "Tenenbaum et al. (2000) Isomap; Roweis & Saul (2000) LLE; Venna & Kaski (2006) trustworthiness; Rousseeuw silhouette; Lloyd K-Means; "
               "Hubert & Arabie ARI; Guyon & Elisseeff (2003); Kohavi & John wrappers; Guyon et al. RFE; Tibshirani Lasso; Hoerl & Kennard Ridge; "
               "Zou & Hastie Elastic-Net; Holland/Goldberg GA; Kennedy & Eberhart PSO; Kirkpatrick SA; Xue et al. (2016) survey; Pedregosa et al. scikit-learn; "
               "Ke et al. LightGBM; Chen & Guestrin XGBoost; Breiman RF; Geurts et al. Extra Trees; Fawcett ROC; Kohavi CV; Wolpert & Macready no-free-lunch."))
story.append(P("Artefacts: paper/main.tex (+ sec_data/methods/results/ablation/subsets/end), results/phase1_results/phase1_results.json + 12 CSVs, "
               "figures/phase1/01–30 PNGs, archive/*.zip, docs cover-sheet PDF. Notebook Modeling.ipynb is the single source of truth — every number and "
               "figure in this PDF traces to a cell whose outputs are cached in the JSON."))

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(2 * cm, 1.2 * cm, "AID427 Phase 1 — Walmart Sales-Level Classification · E-JUST · Nov 2026")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                        topMargin=1.8 * cm, bottomMargin=1.8 * cm, title="AID427 Project Documentation")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("Wrote", OUT)
