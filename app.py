
# F1 DATA STORY


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64, os

st.set_page_config(layout="wide", page_title="F1 Elite Analytics", page_icon="🏎️")

@st.dialog("🏎️ Before You Start...")
def theme_popup():
    st.markdown("""
    <div style="text-align:center; padding: 8px 0 18px 0;">
        <div style="font-size: 2.8rem; margin-bottom: 6px;">🌑</div>
        <div style="font-size: 1.25rem; font-weight: 700; color: #fff; letter-spacing: 1px; margin-bottom: 10px;">
            Dark Theme Recommended
        </div>
        <div style="color: #bbb; font-size: 0.97rem; line-height: 1.7; margin-bottom: 18px;">
            This dashboard is designed for <b style="color:#E10600;">Dark Mode</b>.<br>
            Light theme will wash out the charts and backgrounds.
        </div>
        <div style="background: rgba(225,6,0,0.10); border: 1px solid rgba(225,6,0,0.35);
                    border-radius: 8px; padding: 12px 16px; font-size: 0.9rem; color: #ccc;
                    text-align: left; margin-bottom: 6px;">
            ⋮ &nbsp;<b>Top-right menu</b> → &nbsp;⚙️ <b>Settings</b> → <b>Theme</b> → select <b>Dark</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("✅  Got it!", use_container_width=True, type="primary"):
        st.session_state.theme_popup_shown = True
        st.rerun()

if "theme_popup_shown" not in st.session_state:
    theme_popup()
F1_COLORS = {
    'Ferrari': '#DC0000', 'Mercedes': '#00D2BE', 'Red Bull': '#0600EF',
    'McLaren': '#FF8700', 'Williams': '#005AFF', 'Aston Martin': '#006F62',
    'Alpine': '#0090FF', 'Alfa Romeo': '#900000', 'AlphaTauri': '#2B4562',
    'Haas': '#FFFFFF', 'Lotus F1': '#FFB800', 'Benetton': '#008860',
    'Renault': '#FFF500', 'Brabham': '#002A5C', 'Tyrrell': '#001A4C'
}
TOP_TEAMS = ['Ferrari', 'Mercedes', 'Red Bull', 'McLaren', 'Williams',
             'Lotus F1', 'Renault', 'Benetton', 'Tyrrell', 'Brabham']
ERA_DICT = {
    "1950s (The Birth of F1)":       {"start": 1950, "end": 1959, "img": "assets/era_1950.jpeg"},
    "1960s (The Garagistas)":        {"start": 1960, "end": 1969, "img": "assets/era_1960.jpg"},
    "1970s (Aero Revolution)":       {"start": 1970, "end": 1979, "img": "assets/era_1970.jpeg"},
    "1980s (Turbo Terrors)":         {"start": 1980, "end": 1989, "img": "assets/era_1980.jpeg"},
    "1990s (Electronic Aids)":       {"start": 1990, "end": 1999, "img": "assets/era_1990.jpg"},
    "2000s (The V10 Screamers)":     {"start": 2000, "end": 2009, "img": "assets/era_2000.jpeg"},
    "2010s (Hybrid Dawn)":           {"start": 2010, "end": 2019, "img": "assets/era_2010.jpeg"},
    "2020s (Ground Effect Returns)": {"start": 2020, "end": 2025, "img": "assets/era_2020.jpeg"},
    "2026+ (The Future Regs)":       {"start": 2026, "end": 2030, "img": "assets/car_2026.jpeg"},
}
LEGENDS = {
    "Lewis Hamilton":     {"color": "#00D2BE", "img": "assets/hamilton.jpeg",   "logo": "assets/mercedes_logo.jpeg"},
    "Michael Schumacher": {"color": "#DC0000", "img": "assets/schumacher.jpeg", "logo": "assets/ferrari_logo.jpeg"},
    "Max Verstappen":     {"color": "#0600EF", "img": "assets/verstappen.jpeg", "logo": "assets/redbull_logo.jpeg"},
}
CHART_BASE = dict(
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font_color="white", margin=dict(l=0, r=0, t=45, b=0)
)
GRID = dict(gridcolor="rgba(255,255,255,0.08)")

def set_bg(path: str):
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        enc = base64.b64encode(f.read()).decode()
    st.markdown(f"""<style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Barlow+Condensed:wght@400;700;900&display=swap');
    .stApp {{
        background-image: linear-gradient(rgba(0,0,0,0.87),rgba(14,0,0,0.93)),
                          url("data:image/jpeg;base64,{enc}");
        background-size:cover; background-attachment:fixed; background-position:center;
    }}
    html,body,[class*="css"] {{ font-family:'Rajdhani',sans-serif; }}
    h1,h2,h3 {{ font-family:'Barlow Condensed',sans-serif!important; font-weight:900!important;
               letter-spacing:2px!important; text-transform:uppercase!important; color:white!important; }}
    section.main>div {{ animation:fadeSlide .8s cubic-bezier(.16,1,.3,1) both; }}
    @keyframes fadeSlide {{ from{{opacity:0;transform:translateY(22px)}} to{{opacity:1;transform:translateY(0)}} }}
    .story-box {{ background:linear-gradient(135deg,rgba(30,0,0,.5),rgba(20,20,20,.5));
                  border-left:4px solid #E10600; padding:18px 22px; border-radius:0 8px 8px 0;
                  margin-bottom:22px; color:#D0D0D0; font-size:1.05rem; line-height:1.6;
                  backdrop-filter:blur(6px); }}
    hr {{ border-color:rgba(225,6,0,.2)!important; margin:36px 0!important; }}
    [data-testid="stMetric"] {{ background:rgba(255,255,255,.04); border:1px solid rgba(225,6,0,.3);
                                 border-radius:8px; padding:12px 16px; }}
    [data-testid="stMetricValue"] {{ font-family:'Barlow Condensed',sans-serif; font-size:2rem!important; font-weight:700; }}
    ::-webkit-scrollbar {{ width:5px; }} ::-webkit-scrollbar-track {{ background:#111; }}
    ::-webkit-scrollbar-thumb {{ background:#E10600; border-radius:3px; }}
    </style>""", unsafe_allow_html=True)

set_bg("assets/background_2.jpeg")

# ─── DATA ----------
@st.cache_data(show_spinner="Loading race data…")
def load_data():
    base = "data/"
    return (
        pd.read_csv(base + "results.csv",          low_memory=False),
        pd.read_csv(base + "races.csv",             low_memory=False),
        pd.read_csv(base + "drivers.csv",           low_memory=False),
        pd.read_csv(base + "driver_standings.csv",  low_memory=False),
        pd.read_csv(base + "constructors.csv",      low_memory=False),
    )

results, races, drivers, standings, constructors = load_data()

@st.cache_data(show_spinner="Crunching 75 years of data…")
def prepare_data(results, races, drivers, standings, constructors):
    drivers = drivers.copy()
    drivers["driverName"] = (
        (drivers["givenName"].fillna("") + " " + drivers["familyName"].fillna("")).str.strip()
        if "givenName" in drivers.columns else drivers.iloc[:, 1]
    )
    driver_map = drivers.set_index("driverId")["driverName"].to_dict()

    results = results.merge(races[["raceId", "year"]], on="raceId", how="left")
    results["position_num"] = pd.to_numeric(results["position"], errors="coerce")
    results["dnf"]          = results["position_num"].isna()

    season_races = results.groupby("year")["raceId"].nunique().reset_index(name="total_races")
    wpd = (
        results[results["position"] == "1"]
        .groupby(["year", "driverId"]).size().reset_index(name="wins")
        .merge(season_races, on="year")
        .assign(win_pct=lambda d: d["wins"] / d["total_races"])
    )
    top_driver = wpd.loc[wpd.groupby("year")["win_pct"].idxmax()].reset_index(drop=True)

    std = (
        standings.merge(races[["raceId", "year"]], on="raceId", how="left")
        .sort_values(["year", "driverId", "raceId"])
    )
    final_points = std.groupby(["year", "driverId"]).last().reset_index()
    champions = (
        final_points[final_points["position"] == 1][["year", "driverId", "points"]]
        .rename(columns={"driverId": "championId", "points": "champion_points"})
    )

    comparison = (
        top_driver.merge(champions, on="year", how="left")
        .assign(
            top_name      = lambda d: d["driverId"].map(driver_map),
            champion_name = lambda d: d["championId"].map(driver_map),
            fastest_won   = lambda d: d["driverId"] == d["championId"],
        )
    )

    dnf_year = results.groupby("year")["dnf"].mean().reset_index()

    c_col = "name" if "name" in constructors.columns else constructors.columns[1]
    const_wins = (
        results.merge(constructors, on="constructorId", how="left")
        .query(f"position == '1' and {c_col} in @TOP_TEAMS")
        .groupby(["year", c_col]).size().reset_index(name="wins")
    )

    tm = (
        results.merge(results, on=["raceId", "constructorId"], suffixes=("_a", "_b"))
        .query("driverId_a != driverId_b")
        .assign(
            pos_a=lambda d: pd.to_numeric(d["position_a"], errors="coerce"),
            pos_b=lambda d: pd.to_numeric(d["position_b"], errors="coerce"),
        )
        .dropna(subset=["pos_a", "pos_b"])
    )
    tm = tm.copy()
    tm["delta"] = tm["pos_b"] - tm["pos_a"]
    tsi = (
        tm.groupby("driverId_a").agg(delta=("delta", "mean"), races=("raceId", "count")).reset_index()
        .query("races > 30")
        .assign(driver=lambda d: d["driverId_a"].map(driver_map))
        .sort_values("delta", ascending=False).head(15)
    )

    return driver_map, comparison, dnf_year, const_wins, c_col, tsi, final_points, champions

(driver_map, comparison, dnf_year, const_wins,
 c_col, tsi, final_points, champions) = prepare_data(results, races, drivers, standings, constructors)

def apply_chart_style(fig, **extra):
    fig.update_layout(**{**CHART_BASE, **extra})
    fig.update_xaxes(**GRID)
    fig.update_yaxes(**GRID)
    return fig

def render_image(path: str, max_h: int, caption: str = ""):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            enc = base64.b64encode(f.read()).decode()
        ext = "jpeg" if path.lower().endswith((".jpg", ".jpeg")) else "png"
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;margin-bottom:10px;">
          <img src="data:image/{ext};base64,{enc}"
               style="max-height:{max_h}px;max-width:100%;width:auto;
                      border-radius:8px;box-shadow:0 4px 18px rgba(0,0,0,.6);">
          <span style="color:#888;font-size:.82rem;margin-top:7px;font-style:italic;">{caption}</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.warning(f"Image not found: {path}")

# ─── HERO ─────────────────────────────────────────────────────
col_logo, col_title = st.columns([1, 6])
with col_logo:
    if os.path.exists("assets/f1_logo.jpeg"):
        st.image("assets/f1_logo.jpeg", width=100)
with col_title:
    st.title("Does The Fastest Car Really Win Championships?")
    st.markdown(
        "<p style='color:#777;font-family:Barlow Condensed,sans-serif;"
        "font-size:1.15rem;letter-spacing:3px;text-transform:uppercase;'>"
        "75 Years of Data &nbsp;·&nbsp; Pure Analysis</p>",
        unsafe_allow_html=True
    )

st.markdown("""
<div class="story-box">
<b>The Premise:</b> In Formula 1, speed is everything. But does having the fastest car guarantee a World Championship?
I analysed 75 years of race data to find the truth. Roughly <b>1 in 5 times</b>, the fastest driver on the grid <i>loses</i> the championship.
Let's break down the system.
</div>""", unsafe_allow_html=True)

pct = comparison["fastest_won"].mean() * 100
c1, c2, c3 = st.columns(3)
c1.metric("Fastest Driver Won Title", f"{pct:.1f}%")
c2.metric("Seasons Analysed", comparison["year"].nunique())
c3.metric("Total Races", f"{results['raceId'].nunique():,}")
st.markdown("---")

# ─── 1. TRUE / FALSE SCATTER ──────────────────────────────────
st.header("🏎️ 1. The Speed Myth: True / False Reality Check")

st.markdown("""
<div class="story-box">
<b>The Reality Check:</b> If we plot the Win Percentage of the grid's fastest driver every year, we can see exactly when raw speed translated to a title (<span style='color:#00D2BE; font-weight:bold;'>Teal / True</span>) and when the fastest driver was upset by an underdog (<span style='color:#DC0000; font-weight:bold;'>Red / False</span>). 
<br><br><i>Hover over the dots to see the driver names!</i>
</div>
""", unsafe_allow_html=True)
fig_tf = px.scatter(
    comparison, x="year", y="win_pct",
    color="fastest_won",
    color_discrete_map={True: "#00D2BE", False: "#DC0000"},
    labels={"fastest_won": "Won the Title?", "win_pct": "Season Win %", "year": "Year"},
    title="Championship Outcome vs. Season Win % (True / False)",
    hover_data={"top_name": True, "champion_name": True, "win_pct": ":.0%"},
)
fig_tf.add_hline(
    y=0.45, line_dash="dot", line_color="rgba(255,255,255,0.4)",
    annotation_text="45% threshold — near-certain title", annotation_position="bottom right",
    annotation_font=dict(color="white", size=11)
)
fig_tf.update_traces(marker=dict(size=13, line=dict(width=1, color="rgba(255,255,255,0.7)")))
fig_tf.update_yaxes(tickformat=".0%")
apply_chart_style(fig_tf, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig_tf, use_container_width=True)
st.markdown("---")

# ─── 2. RELIABILITY ───────────────────────────────────────────
st.header("⚙️ 2. The Machine: The Reliability Revolution")
st.markdown("""
<div class="story-box">
<b>The "Aha!" Moment:</b> Almost every red dot above lands before 2000. Why?
Because their cars exploded. The DNF collapse below is the single biggest structural shift in 75 years of F1.
</div>""", unsafe_allow_html=True)

fig_dnf = px.area(
    dnf_year, x="year", y="dnf",
    title="DNF Rate — From Attrition to Bulletproof Reliability",
    color_discrete_sequence=["#E10600"]
)
fig_dnf.update_traces(fillcolor="rgba(225,6,0,0.12)", line_width=2)
for ann in [
    dict(x=1980, y=0.55, text="<b>Killer Era</b><br>Half the grid retired", ax=20, ay=-50),
    dict(x=2018, y=0.12, text="<b>Bulletproof Era</b>", ax=-55, ay=-35),
]:
    fig_dnf.add_annotation(showarrow=True, arrowhead=2, arrowcolor="#E10600",
                            font=dict(color="white", size=11), **ann)
fig_dnf.update_yaxes(tickformat=".0%")
apply_chart_style(fig_dnf)
st.plotly_chart(fig_dnf, use_container_width=True)

fig_const = px.bar(
    const_wins, x="year", y="wins", color=c_col,
    title="Constructor Dynasties — Race Wins by Year",
    color_discrete_map=F1_COLORS
)
apply_chart_style(fig_const, barmode="stack", legend_title_text="")
st.plotly_chart(fig_const, use_container_width=True)

# ─── 3. TEAMMATE SUPPRESSION INDEX ───────────────────────────
st.markdown("---")
st.header("3. The Human Element: Teammate Suppression Index")
st.markdown("""
<div class="story-box">
<b>Isolating Driver Skill:</b> When cars are unequal, how do we measure true talent?
Compare every driver to their teammate — the only other person on earth in the same machine.
<br><br>
<b>Delta</b> = Average finishing positions ahead of their teammate.
+4.0 means finishing 4 spots ahead every race. Legends <i>obliterate</i> teammates.
</div>""", unsafe_allow_html=True)

fig_tsi = px.bar(
    tsi, x="delta", y="driver", orientation="h",
    title="Teammate Suppression Index (Min. 30 Races Finished Together)",
    color="delta", color_continuous_scale=["#FF6666", "#E10600", "#7B0000"],
    text=tsi["delta"].round(2)
)
fig_tsi.update_traces(texttemplate="%{text}x", textposition="outside", textfont_color="white")
apply_chart_style(fig_tsi, yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)
fig_tsi.update_xaxes(title="Delta")
fig_tsi.update_yaxes(title="")
st.plotly_chart(fig_tsi, use_container_width=True)

# ─── 4. ERA EVOLUTION ────────────────────────────────────────
st.markdown("---")
st.header("4. Era Evolution: The Decades of Speed")
st.markdown("""
<div class="story-box">
<b>The Shifting Meta:</b> F1 has evolved dramatically. From the perilous 1950s to the high-tech 2020s,
championship requirements have completely transformed. Select a decade to see how the Speed Myth holds up.
</div>""", unsafe_allow_html=True)

era_option = st.selectbox("Select a Decade to Analyse:", list(ERA_DICT.keys()))
sel        = ERA_DICT[era_option]
era_df     = comparison[(comparison["year"] >= sel["start"]) & (comparison["year"] <= sel["end"])]

col_img, _, col_met = st.columns([1, 0.08, 1.4])
with col_img:
    render_image(sel["img"], max_h=400, caption=f"Machinery of the {era_option.split(' ')[0]}")

with col_met:
    st.markdown(
        f"<h3 style='color:#00D2BE;margin-top:0;'>{era_option.split(' ')[0]} Era Profile</h3>",
        unsafe_allow_html=True
    )
    if not era_df.empty:
        at_win  = comparison["win_pct"].mean() * 100
        at_fast = comparison["fastest_won"].mean() * 100
        e_win   = era_df["win_pct"].mean() * 100
        e_fast  = era_df["fastest_won"].mean() * 100
        e_pts   = era_df["champion_points"].mean()

        st.metric("👑 Fastest Driver Won Title",  f"{e_fast:.1f}%",
                  delta=f"{e_fast - at_fast:+.1f}% vs all-time")
        st.metric("⚡ Avg Win % of Fastest Car",  f"{e_win:.1f}%",
                  delta=f"{e_win - at_win:+.1f}% vs all-time")
        st.metric("🏆 Avg Champion Points",        f"{e_pts:.0f}",
                  help="Points system changed in 2010 — causes score inflation.")

        insight = ("highly predictable era — engineering dominance ruled"
                   if e_fast > 80 else
                   "chaotic era — breakdowns rewarded consistency over pure pace")
        st.markdown(f"""
        <div style="background:rgba(225,6,0,.12);border-left:4px solid #E10600;
                    padding:14px;border-radius:5px;margin-top:18px;font-size:.94rem;">
            <b>Era Insight:</b> Pure speed resulted in a title <b>{e_fast:.1f}%</b> of the time.
            This was a <i>{insight}</i>.
        </div>""", unsafe_allow_html=True)
    elif "2026" in era_option:
        st.info("2026 data not yet written. Will pure speed dominate or will new regs reset reliability?")
    else:
        st.warning("No data for this range.")

st.markdown("---")

# ─── 5. LEGEND SPOTLIGHT ─────────────────────────────────────
st.header("5. Legend Spotlight")
st.markdown("""
<div class="story-box">
<b>The Greats:</b> Some drivers transcend their machinery.
Let's examine the three defining champions of the modern sport.
</div>""", unsafe_allow_html=True)

legend_choice = st.selectbox("Select an F1 Legend:", list(LEGENDS.keys()))
leg      = LEGENDS[legend_choice]
last     = legend_choice.split()[-1]
l_stats  = comparison[comparison["top_name"].str.contains(last, case=False, na=False)]
l_points = final_points[final_points["driverId"].map(driver_map).str.contains(last, case=False, na=False)]

col_li, col_lm, col_lc = st.columns([0.8, 1, 1.5])

with col_li:
    if os.path.exists(leg["logo"]):
        st.image(leg["logo"], width=58)
    render_image(leg["img"], max_h=350)

with col_lm:
    st.markdown(f"#### {last}'s Numbers")
    if not l_stats.empty:
        titles_total   = champions[champions["championId"].map(driver_map)
                                   .str.contains(last, case=False, na=False)].shape[0]
        titles_fastest = int(l_stats["fastest_won"].sum())
        st.metric("Seasons as Fastest Car",  l_stats.shape[0])
        st.metric("Titles When Fastest",      titles_fastest)
        st.metric("Titles as Underdog",       titles_total - titles_fastest,
                  delta="Overperforming machinery", delta_color="normal")
    else:
        st.warning("Awaiting data…")

with col_lc:
    if not l_points.empty:
        fig_leg = px.area(
            l_points, x="year", y="points",
            title=f"{last} — Career Championship Points",
            color_discrete_sequence=[leg["color"]]
        )
        hex_c = leg["color"].lstrip("#")
        r, g, b = int(hex_c[0:2], 16), int(hex_c[2:4], 16), int(hex_c[4:6], 16)
        fig_leg.update_traces(fillcolor=f"rgba({r},{g},{b},0.12)", line_width=2.5)
        apply_chart_style(fig_leg, height=310)
        st.plotly_chart(fig_leg, use_container_width=True)

# ─── VERDICT ─────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="padding:36px 40px;border-radius:12px;
            background:linear-gradient(145deg,#1a0000,#0d0d0d);
            border:1px solid rgba(225,6,0,.35);text-align:center;
            box-shadow:0 8px 32px rgba(225,6,0,.15);margin-bottom:60px;">
  <h1 style="font-size:2rem;color:#fff;margin-bottom:8px;
             letter-spacing:4px;font-family:'Barlow Condensed',sans-serif;">🏁 The Final Verdict</h1>
  <p style="font-size:1.1rem;color:#888;margin-bottom:32px;">
    Speed wins races. Reliability protects championships. Consistency secures legacies.
  </p>
  <div style="text-align:left;max-width:780px;margin:0 auto;color:#ddd;font-size:1rem;line-height:1.9;">
    <p>My analysis of 75 years of Formula 1 data reveals three critical truths:</p>
    <ul style="list-style:none;padding:0;">
      <li style="margin-bottom:18px;">🏎️ <b>The 80% Rule:</b> The fastest car wins the title ~80% of the time. The other 20% is where history is written.</li>
      <li style="margin-bottom:18px;">🏎️ <b>The "Aha" Moment:</b> The defining shift was not speed — it was <span style="color:#E10600;font-weight:700;">reliability</span>. The DNF collapse post-2000 turned F1 from a survival lottery into an engineering dynasty.</li>
      <li style="margin-bottom:18px;">🏎️ <b>The Human Factor:</b> When machinery is equal, legends do not just beat their teammates — they statistically obliterate them.</li>
    </ul>
  </div>
  <hr style="border-color:rgba(225,6,0,.2);margin:28px 0;">
  <h2 style="font-size:1.5rem;color:#fff;font-family:'Barlow Condensed',sans-serif;letter-spacing:2px;">
    "The fastest car usually wins.<br>
    But the most complete package <span style="color:#E10600;">always</span> wins championships."
  </h2>
</div>
<div style="text-align:center;color:#444;font-size:11px;letter-spacing:1px;margin-top:40px;">
  DATA SOURCE: KAGGLE — 75 YEARS OF F1 &nbsp;|&nbsp; BUILT WITH STREAMLIT & PLOTLY &nbsp;|&nbsp; 🏎️ F1 ELITE ANALYTICS
</div>""", unsafe_allow_html=True)
