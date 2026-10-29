import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    return mo, pl


@app.cell
def _(pl):
    df = pl.read_parquet("data/verkehrszaehlungen_werte_fussgaenger_velo_alle_jahre.parquet")
    df = df.with_columns(pl.col("DATUM").str.slice(0, 4).cast(pl.Int64).alias("JAHR"))
    df.head()
    return (df,)


@app.cell
def _(df, pl):
    pro_jahr = (
        df.group_by("JAHR")
        .agg(pl.col("FK_STANDORT").n_unique().alias("zaehlstellen"))
        .sort("JAHR")
    )
    pro_jahr
    return (pro_jahr,)


@app.cell
def _(df, pl, pro_jahr):
    n_jahre = pro_jahr.height
    jahre_pro_stelle = df.group_by("FK_STANDORT").agg(pl.col("JAHR").n_unique().alias("jahre"))
    n_stellen = jahre_pro_stelle.height
    n_alle_jahre = jahre_pro_stelle.filter(pl.col("jahre") == n_jahre).height
    anteil = n_alle_jahre / n_stellen
    {"jahre": n_jahre, "zaehlstellen_gesamt": n_stellen, "in_allen_jahren": n_alle_jahre, "anteil": round(anteil, 3)}
    return (jahre_pro_stelle,)


@app.cell
def _(jahre_pro_stelle, pl):
    jahre_pro_stelle.group_by("jahre").agg(pl.len().alias("zaehlstellen")).sort("jahre")
    return


@app.cell
def _(df):
    {"spalten": df.columns, "zeilen": df.height}
    return


@app.cell
def _(df, pl):
    koordinaten_pro_id = (
        df.group_by("FK_STANDORT")
        .agg(pl.struct("OST", "NORD").n_unique().alias("koordinatenpaare"))
    )
    ids_pro_ort = df.group_by("OST", "NORD").agg(pl.col("FK_STANDORT").n_unique().alias("ids"))
    {
        "zaehlstellen_ids": koordinaten_pro_id.height,
        "ids_mit_mehr_als_einem_koordinatenpaar": koordinaten_pro_id.filter(pl.col("koordinatenpaare") > 1).height,
        "orte_ost_nord": ids_pro_ort.height,
        "orte_mit_mehreren_ids": ids_pro_ort.filter(pl.col("ids") > 1).height,
    }
    return


@app.cell
def _(df, pl):
    jahr_abdeckung = (
        df.group_by("JAHR")
        .agg(pl.col("DATUM").min().alias("erster"), pl.col("DATUM").max().alias("letzter"))
        .sort("JAHR")
        .with_columns(
            (pl.col("erster").str.slice(5, 5).eq("01-01") & pl.col("letzter").str.slice(5, 5).eq("12-31")).alias("vollstaendig")
        )
    )
    vollstaendige_jahre = jahr_abdeckung.filter(pl.col("vollstaendig"))["JAHR"].to_list()
    jahr_abdeckung
    return (vollstaendige_jahre,)


@app.cell
def _(df, mo, pl, vollstaendige_jahre):
    velo = df.filter(pl.col("VELO_IN").is_not_null() | pl.col("VELO_OUT").is_not_null())
    velo_pro_jahr = (
        velo.group_by("JAHR")
        .agg(pl.col("FK_STANDORT").n_unique().alias("velo_zaehlstellen"))
        .sort("JAHR")
    )
    velo_jahre_pro_stelle = (
        velo.filter(pl.col("JAHR").is_in(vollstaendige_jahre))
        .group_by("FK_STANDORT")
        .agg(pl.col("JAHR").n_unique().alias("jahre"))
    )
    n_velo_stellen = velo["FK_STANDORT"].n_unique()
    n_velo_in_jedem_jahr = velo_jahre_pro_stelle.filter(pl.col("jahre") == len(vollstaendige_jahre)).height
    mo.vstack([
        velo_pro_jahr,
        {
            "vollstaendige_jahre": len(vollstaendige_jahre),
            "velo_zaehlstellen_gesamt": n_velo_stellen,
            "in_jedem_vollstaendigen_jahr": n_velo_in_jedem_jahr,
            "anteil": round(n_velo_in_jedem_jahr / n_velo_stellen, 3),
        },
    ])
    return (velo,)


@app.cell
def _(pl, velo):
    velo_jahre_von_bis = (
        velo.group_by("FK_STANDORT", "OST", "NORD")
        .agg(
            pl.col("JAHR").min().alias("erstes_jahr"),
            pl.col("JAHR").max().alias("letztes_jahr"),
            pl.col("JAHR").n_unique().alias("jahre"),
        )
        .sort("OST", "NORD", "erstes_jahr")
    )
    velo_jahre_von_bis
    return


@app.cell
def _(pl, velo, vollstaendige_jahre):
    velo_orte_jahre = (
        velo.filter(pl.col("JAHR").is_in(vollstaendige_jahre))
        .group_by("OST", "NORD")
        .agg(pl.col("JAHR").n_unique().alias("jahre"))
    )
    n_velo_orte = velo.select("OST", "NORD").unique().height
    n_velo_orte_in_jedem_jahr = velo_orte_jahre.filter(pl.col("jahre") == len(vollstaendige_jahre)).height
    {
        "velo_orte": n_velo_orte,
        "vollstaendige_jahre": len(vollstaendige_jahre),
        "orte_in_jedem_vollstaendigen_jahr": n_velo_orte_in_jedem_jahr,
        "anteil": round(n_velo_orte_in_jedem_jahr / n_velo_orte, 3),
    }
    return


if __name__ == "__main__":
    app.run()
