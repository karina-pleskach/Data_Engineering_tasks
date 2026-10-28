from io import BytesIO
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from src.dashboard.analysis import calculate_general_statistics
from src.dashboard.anomalies.iqr import calculate_iqr_anomalies
from src.dashboard.anomalies.z_score import calculate_z_score_anomalies
from src.dashboard.anomalies.moving_average import calculate_moving_average_anomalies
from src.dashboard.anomalies.grubbs import calculate_grubbs_anomalies
from src.dashboard.charts import get_anomalies

def get_params(name):
    return (st.session_state.get(f"iqr_param_{name}", 1.5), 
            st.session_state.get(f"z_score_param_{name}", 3.0), 
            st.session_state.get(f"moving_average_window_{name}", 7), 
            st.session_state.get(f"moving_average_param_{name}", 50.0), 
            st.session_state.get(f"grubbs_alpha_{name}", 0.05))

def get_results(series, name):
    stats = calculate_general_statistics(series)
    iqr, z, window, distance, alpha = get_params(name)
    return stats, {"Anomalies detected by IQR rule:": (calculate_iqr_anomalies(series, iqr, stats), f"parameter: {iqr}"), 
                   "Anomalies detected by z-score:": (calculate_z_score_anomalies(series, stats, z), f"parameter: {z}"), 
                   "Anomalies detected by distance (percent) from moving average:": (calculate_moving_average_anomalies(series, window, distance), f"window (days): {window}, parameter: {distance}"), 
                   "Anomalies detected by Grubbs test:": (calculate_grubbs_anomalies(series, alpha), f"alpha: {alpha}")}

def add_table(story, rows):
    table = Table(rows, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)]))
    story.extend([table])

def add_statistics(story, series, name, styles):
    stats, results = get_results(series, name)
    story.append(Paragraph(name, styles["Heading1"]))
    add_table(story, [["Statistic", "Value"]] + [[key, f"{stats[key]:.2f}"] for key in ["mean daily output", "standard deviation", "median", "interquartile range"]])
    for method, (anomalies, param) in results.items():
        story.append(Paragraph(f"{method} ({param})", styles["Heading4"]))
        rows = [["Day"] + list(anomalies.columns)] if isinstance(anomalies, pd.DataFrame) else [["Day", "value"]]
        if isinstance(anomalies, pd.DataFrame):
            for index, row in anomalies.iterrows():
                rows.append([str(index)] + [round(v, 3) for v in row])
        else:
            for index, value in anomalies.items():
                rows.append([str(index), round(value, 3)])
        add_table(story, rows if len(rows) > 1 else [["Day", "Result"], ["—", "No anomalies found"]])
    story.append(PageBreak())

def add_bars(ax, series, dates):
    bottom = np.zeros(len(series))
    for mine in series.columns:
        ax.bar(dates, series[mine], bottom=bottom, label=mine)
        bottom += series[mine].to_numpy()
    return series.sum(axis=1).to_numpy()

def add_trend(ax, x, dates, y, degree):
    trend = np.polyval(np.polyfit(x, y, degree), x)
    ax.plot(dates, trend, color="green", label=f"Trend (degree {degree})")

def save_chart(fig):
    image = BytesIO()
    fig.savefig(image, format="png", dpi=140)
    plt.close(fig)
    image.seek(0)
    return Image(image, width=17 * cm, height=7.5 * cm)

def make_chart(series, title, kind, degree, anomalies):
    fig, ax = plt.subplots(figsize=(9, 4))
    dates = series.index
    x = np.arange(len(series))
    if kind == "Stacked bar":
        y = add_bars(ax, series, dates)
    elif kind == "Line":
        y = series.to_numpy()
        ax.plot(dates, y, label="Output")
    else:
        y = series.to_numpy()
        ax.bar(dates, y, label="Output")
    add_trend(ax, x, dates, y, degree)
    ax.scatter(anomalies.index, anomalies.values, color="red", label="IQR anomalies", zorder=3)
    ax.set(title=title, xlabel="Day", ylabel="Output")
    ax.tick_params(axis="x", rotation=45)
    ax.legend()
    fig.tight_layout()
    return save_chart(fig)

def add_charts(story, df, styles, degree):
    story.append(Paragraph("Charts", styles["Title"]))
    for mine in df.columns:
        series = df[mine]
        anomalies = get_anomalies(series)
        for kind in ["Line", "Bar"]:
            story.append(make_chart(series, f"{mine} ({kind})", kind, degree, anomalies))
    total = df.sum(axis=1)
    anomalies = get_anomalies(total)
    story.append(make_chart(df, "All mines (Stacked bar)", "Stacked bar", degree, anomalies))

def generate_report(df):
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    story = [Paragraph("Mining ops simulator", styles["Title"])]
    add_statistics(story, df.sum(axis=1).rename("Total output"), "All mines", styles)
    for mine in df.columns:
        add_statistics(story, df[mine], mine, styles)
    degree = st.session_state.get("polynomial_degree", 1)
    add_charts(story, df, styles, degree)
    SimpleDocTemplate(buffer, pagesize=A4).build(story)
    return buffer.getvalue()
