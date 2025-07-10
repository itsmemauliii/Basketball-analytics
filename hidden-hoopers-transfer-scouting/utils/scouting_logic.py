import pandas as pd

def filter_undervalued_teams(df):
    df = df[df['Ret Mins'].str.contains('%')]
    df['Ret Mins'] = df['Ret Mins'].str.replace('%', '').astype(float)
    df['RPMs'] = df['RPMs'].str.replace('%', '').astype(float)

    undervalued = df[
        (df['Trans.'] >= 5) &
        (df['Ret Mins'] < 40) &
        ((df['AdjOE'].rank(ascending=False) <= 50) | (df['AdjDE'].rank() <= 50))
    ]
    undervalued['Scouting Report'] = undervalued.apply(generate_scouting_report, axis=1)
    return undervalued

def generate_scouting_report(row):
    return f"{row['Team']} added {int(row['Trans.'])} new transfers with only {row['Ret Mins']}% minutes returning. They’re projected with {row['AdjOE']} AdjOE and {row['AdjDE']} AdjDE — a sleeper team to watch."
