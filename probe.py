import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    return (pl,)


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


if __name__ == "__main__":
    app.run()
