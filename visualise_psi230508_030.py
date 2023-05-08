# visualise_psi230508_010.py

import plotly.graph_objs as go

#input_list
node_I_psi = [[[], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242'], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], []]]

node_name = ['JPN', 'HAM', 'HAM-N']


# データの定義
x, y, z, color, lot_coordinates, lot_colors = [], [], [], [], {}, {}

for i in range(len(node_I_psi)):
    for j in range(len(node_I_psi[i])):
        node_label = node_name[i]
        for k in range(len(node_I_psi[i][j])):
            lot_id = node_I_psi[i][j][k]
            x.append(j)
            y.append(node_label)
            z.append(k)
            color.append(i)  # ロットIDのカラーマップを作成するために、node_nameのインデックスをcolorに追加する
            if lot_id not in lot_coordinates:
                lot_coordinates[lot_id] = [(j, node_label, k)]
                lot_colors[lot_id] = i  # ロットIDごとの色を保存する
            else:
                lot_coordinates[lot_id].append((j, node_label, k))

# y軸のラベルを設定
y_axis = dict(
    tickvals=node_name,
    ticktext=node_name
)

# 3D散布図の作成
fig = go.Figure()

for lot_id, coordinates in lot_coordinates.items():
    x = [coordinate[0] for coordinate in coordinates]
    y = [coordinate[1] for coordinate in coordinates]
    z = [coordinate[2] for coordinate in coordinates]
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines+markers',
        name=lot_id,
        marker=dict(
            size=5,
            color=z,  # ロットIDごとに色分けするためにzを指定する
            colorscale='Viridis',
            opacity=0.8
        ),
        line=dict(
            color=lot_colors[lot_id],  # ロットIDごとの色を適用する
            width=3
        ),
        text=[lot_id],
        hoverinfo='text'
    ))

# レイアウトの設定
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

# グラフの表示
fig.show()
