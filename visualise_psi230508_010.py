# visualise_psi230508_010.py

import plotly.graph_objs as go

#input_list
node_I_psi = [[[], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242'], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], []]]

node_name = ['JPN', 'HAM', 'HAM-N']

# データの定義
x, y, z, color = [], [], [], []

for i in range(len(node_I_psi)):
    for j in range(len(node_I_psi[i])):
        node_label = node_name[i]
        for k in range(len(node_I_psi[i][j])):
            x.append(j)
            y.append(node_label)
            z.append(k)
            color.append(i)  # ロットIDのカラーマップを作成するために、node_nameのインデックスをcolorに追加する

text = []
for i in range(len(node_I_psi)):
    for j in range(len(node_I_psi[i])):
        for k in range(len(node_I_psi[i][j])):
            text.append(node_I_psi[i][j][k])

# y軸のラベルを設定
y_axis = dict(
    tickvals=node_name,
    ticktext=node_name
)



#3D散布図の作成
fig = go.Figure()

for i in range(len(node_I_psi)):
    for j in range(len(node_I_psi[i])):
        node_label = node_name[i]
        for k in range(len(node_I_psi[i][j])):
            lot_id = node_I_psi[i][j][k]
            x = j
            y = node_label
            z = k
            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers',
                name=lot_id,
                marker=dict(
                    size=5,
                    color=k,
                    colorscale='Viridis',
                    opacity=0.8
                ),
                text=[lot_id],
                hoverinfo='text'
            ))

#レイアウトの設定
fig.update_layout(
    title="Node Connections",
    scene=dict(
        xaxis_title="Week",
        yaxis_title="Location",
        zaxis_title="Lot ID"
    ),
    width=800,
    height=800,
    margin=dict(
        l=65,
        r=50,
        b=65,
        t=90
    ),
    legend=dict(
        title='Lot ID',
        yanchor='top',
        y=0.99,
        xanchor='left',
        x=0.01
    )
)

#グラフの表示
fig.show()


