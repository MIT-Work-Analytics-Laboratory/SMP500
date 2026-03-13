import pandas as pd

df_e = pd.read_csv('Eloundou_New/full_labelset_new.tsv', sep='\t')
df_p = pd.read_csv('Anthropic/task_penetration.csv')

df_used = df_p[df_p['penetration'] != 0].copy()
df_beta = df_e[['Task','beta']].drop_duplicates(subset=['Task']).rename(columns={'Task':'task'})
df_used['task'] = df_used['task'].str.strip()
df_beta['task'] = df_beta['task'].str.strip()

df_m = df_used.merge(df_beta, on='task', how='left').dropna(subset=['beta']).copy()
df_m['bb'] = df_m['beta'].round(1)

c = df_m.groupby('bb').size().reindex([0.0, 0.5, 1.0], fill_value=0)
cp = c / c.sum() * 100

p = df_m.groupby('bb')['penetration'].sum().reindex([0.0, 0.5, 1.0], fill_value=0)
pp = p / p.sum() * 100

print("Beta | Count% | Penetration-Weighted%")
for b in [0.0, 0.5, 1.0]:
    print(f"  {b:.1f} | {cp[b]:.1f}% | {pp[b]:.1f}%")
