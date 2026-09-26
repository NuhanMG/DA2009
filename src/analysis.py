#=========================================================================#
#  FILE   : src/analysis.py                                                #
#  PURPOSE: Makes the charts and works out the summary figures.            #
#  OWNER  : 25ada141                                                       #
#                                                                          #
#  Collecting data is only useful if somebody can see something in it. A   #
#  table of 291 rows tells you very little at a glance, but a sorted bar   #
#  chart shows straight away which companies moved.                        #
#                                                                          #
#  Green means the price went up and red means it went down, which is the  #
#  usual convention for share prices. Every bar is also labelled with the  #
#  word up or down and a plus or minus sign, so the direction is still     #
#  clear if the colours are hard to tell apart.                            #
#=========================================================================#

import pandas as pd
import plotly.graph_objects as go


#-------------------------------------------------------------------------#
#  COLOURS                                                                 #
#                                                                          #
#  Two sets, one for the dark theme and one for the light theme.           #
#-------------------------------------------------------------------------#

COLOURS = {
    "dark": {
        "up": "#34d399", "down": "#c02626", "bar": "#22d3ee",
        "text": "#e6edf3", "faint": "#8b949e", "grid": "#21262d",
        "panel": "#0d1117",
    },
    "light": {
        "up": "#047857", "down": "#dc2626", "bar": "#0891b2",
        "text": "#161b22", "faint": "#57606a", "grid": "#e5e7eb",
        "panel": "#ffffff",
    },
}


def colours(dark=True):
    return COLOURS["dark" if dark else "light"]


def style(figure, dark=True, height=420):
    """Apply the same plain styling to every chart."""
    c = colours(dark)

    figure.update_layout(
        height=height,
        # A see-through background so the chart matches whichever theme
        # the app is using.
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="system-ui, Segoe UI, sans-serif", size=12,
                  color=c["text"]),
        margin=dict(l=10, r=20, t=50, b=40),
        showlegend=False,
        title=dict(font=dict(size=15), x=0, xanchor="left"),
        hoverlabel=dict(bgcolor=c["panel"], bordercolor=c["faint"]),
    )

    # Keep the grid lines faint so the bars stand out.
    figure.update_xaxes(gridcolor=c["grid"], linecolor=c["grid"],
                        tickfont=dict(color=c["faint"], size=11))
    figure.update_yaxes(gridcolor=c["grid"], linecolor=c["grid"],
                        tickfont=dict(color=c["faint"], size=11))
    return figure


def empty_chart(message="No data yet", dark=True):
    """Shown instead of a broken empty chart."""
    c = colours(dark)
    figure = go.Figure()
    figure.add_annotation(text=message, showarrow=False,
                          font=dict(size=14, color=c["faint"]),
                          xref="paper", yref="paper", x=0.5, y=0.5)
    figure.update_xaxes(visible=False)
    figure.update_yaxes(visible=False)
    return style(figure, dark, height=280)


#-------------------------------------------------------------------------#
#  CHART 1 - BIGGEST RISERS AND FALLERS                                    #
#-------------------------------------------------------------------------#

def chart_movers(df, top=10, dark=True):
    """The companies whose share price moved the most today."""
    c = colours(dark)

    if df is None or df.empty or "percentageChange" not in df.columns:
        return empty_chart("Collect the market data first", dark)

    data = df[["symbol", "percentageChange"]].dropna()
    data = data[data["percentageChange"] != 0]
    if data.empty:
        return empty_chart("No prices moved today", dark)

    risers = data.nlargest(top, "percentageChange")
    fallers = data.nsmallest(top, "percentageChange")
    movers = pd.concat([fallers, risers]).sort_values("percentageChange")

    bar_colours = [c["up"] if v > 0 else c["down"]
                   for v in movers["percentageChange"]]

    # The word and the sign mean the direction is readable even without
    # the colours.
    labels = [f"{'up' if v > 0 else 'down'} {v:+.2f}%"
              for v in movers["percentageChange"]]

    figure = go.Figure(go.Bar(
        x=movers["percentageChange"],
        y=movers["symbol"],
        orientation="h",
        marker=dict(color=bar_colours,
                    line=dict(color=c["panel"], width=1)),
        text=labels,
        textposition="outside",
        textfont=dict(color=c["faint"], size=11),
        # Without this, a label at the edge of the chart gets cut off.
        cliponaxis=False,
        hovertemplate="%{y}<br>Change: %{x:+.2f}%<extra></extra>",
    ))

    figure.update_layout(title=f"Biggest movers today (top {top} each way)",
                         bargap=0.35)

    # Leave room on both sides so the labels fit.
    limit = movers["percentageChange"].abs().max() * 1.6
    figure.update_xaxes(title_text="Price change (%)", range=[-limit, limit],
                        zeroline=True)

    return style(figure, dark, height=520)


#-------------------------------------------------------------------------#
#  CHART 2 - WHERE THE MONEY WENT                                          #
#-------------------------------------------------------------------------#

def chart_turnover(df, top=15, dark=True):
    """
    The companies with the highest turnover today.

    This chart has no up or down, only size, so it uses one colour.
    """
    c = colours(dark)

    if df is None or df.empty or "turnover" not in df.columns:
        return empty_chart("Collect the market data first", dark)

    data = df[["symbol", "turnover"]].dropna()
    data = data[data["turnover"] > 0].nlargest(top, "turnover")
    if data.empty:
        return empty_chart("No turnover recorded today", dark)

    data = data.sort_values("turnover")

    # Turnover runs into the billions, which is hard to read on an axis,
    # so we show it in millions.
    millions = data["turnover"] / 1_000_000

    figure = go.Figure(go.Bar(
        x=millions,
        y=data["symbol"],
        orientation="h",
        marker=dict(color=c["bar"], line=dict(color=c["panel"], width=1)),
        text=[f"{v:,.1f}M" for v in millions],
        textposition="outside",
        textfont=dict(color=c["faint"], size=11),
        cliponaxis=False,
        hovertemplate="%{y}<br>Turnover: Rs %{x:,.1f} million<extra></extra>",
    ))

    figure.update_layout(title=f"Highest turnover today (top {top})",
                         bargap=0.35)
    figure.update_xaxes(title_text="Turnover (Rs millions)",
                        range=[0, millions.max() * 1.25])

    return style(figure, dark, height=480)


#-------------------------------------------------------------------------#
#  CHART 3 - HOW THE SECTORS MOVED                                         #
#-------------------------------------------------------------------------#

def chart_sectors(df, dark=True):
    """Which parts of the market went up and down today."""
    c = colours(dark)

    if df is None or df.empty:
        return empty_chart("Collect the market data first", dark)

    name_column = "name" if "name" in df.columns else "indexName"
    if name_column not in df.columns or "changePercentage" not in df.columns:
        return empty_chart("The sector data is missing some columns", dark)

    data = df[[name_column, "changePercentage"]].dropna()
    data = data.sort_values("changePercentage")
    if data.empty:
        return empty_chart("No sector movements to show", dark)

    bar_colours = [c["up"] if v > 0 else c["down"] if v < 0 else c["faint"]
                   for v in data["changePercentage"]]
    labels = [f"{v:+.2f}%" for v in data["changePercentage"]]

    figure = go.Figure(go.Bar(
        x=data["changePercentage"],
        y=data[name_column],
        orientation="h",
        marker=dict(color=bar_colours,
                    line=dict(color=c["panel"], width=1)),
        text=labels,
        textposition="outside",
        textfont=dict(color=c["faint"], size=10),
        cliponaxis=False,
        hovertemplate="%{y}<br>Change: %{x:+.2f}%<extra></extra>",
    ))

    figure.update_layout(title="How each sector moved today", bargap=0.3)

    limit = data["changePercentage"].abs().max() * 1.45
    figure.update_xaxes(title_text="Change (%)", range=[-limit, limit],
                        zeroline=True)

    return style(figure, dark, height=max(400, 26 * len(data) + 110))


#-------------------------------------------------------------------------#
#  SUMMARY FIGURES                                                         #
#-------------------------------------------------------------------------#

def market_figures(df):
    """The headline numbers shown at the top of the app."""
    if df is None or df.empty:
        return {}

    figures = {"Companies": len(df)}

    if "percentageChange" in df.columns:
        changes = df["percentageChange"].dropna()
        figures["Rose"] = int((changes > 0).sum())
        figures["Fell"] = int((changes < 0).sum())
        figures["No change"] = int((changes == 0).sum())

    if "turnover" in df.columns:
        total = df["turnover"].dropna().sum()
        figures["Turnover"] = f"Rs {total / 1_000_000_000:,.2f} bn"

    return figures


def summary(df, index_data=None):
    """A short written description of what the numbers show."""
    if df is None or df.empty:
        return "No data collected yet."

    figures = market_figures(df)
    sentences = []

    if index_data:
        value = index_data.get("value", 0)
        change = index_data.get("change", 0)
        direction = ("rose" if change > 0
                     else "fell" if change < 0 else "did not move")
        sentences.append(
            f"The All Share Price Index {direction} to {value:,.2f} "
            f"({change:+.2f} points)."
        )

    rose = figures.get("Rose", 0)
    fell = figures.get("Fell", 0)

    if rose or fell:
        mood = ("more companies rose than fell" if rose > fell
                else "more companies fell than rose" if fell > rose
                else "risers and fallers were evenly matched")
        sentences.append(
            f"Out of {figures.get('Companies', 0)} companies traded, "
            f"{rose} rose, {fell} fell and {figures.get('No change', 0)} "
            f"finished unchanged, so {mood}."
        )

    if "Turnover" in figures:
        sentences.append(f"Total turnover was {figures['Turnover']}.")

    sentences.append(
        "This is one trading day, collected for a university assignment. "
        "It is not investment advice."
    )

    return " ".join(sentences)


#-------------------------------------------------------------------------#
#  Run this file on its own:  python -m src.analysis                       #
#-------------------------------------------------------------------------#

if __name__ == "__main__":
    from src.api_client import CSEApi
    from src.cleaner import clean

    api = CSEApi()
    raw = api.trade_summary()

    if raw.empty:
        print("No data - check your internet connection.")
    else:
        tidy, _ = clean(raw)

        print("Summary figures")
        print("-" * 55)
        for name, value in market_figures(tidy).items():
            print(f"  {name:12} {value}")

        print()
        print(summary(tidy, api.aspi()))

        print()
        print("Building the charts")
        print("-" * 55)
        for name, figure in [("movers", chart_movers(tidy)),
                             ("turnover", chart_turnover(tidy)),
                             ("sectors", chart_sectors(api.sectors()))]:
            print(f"  {name:10} built")
