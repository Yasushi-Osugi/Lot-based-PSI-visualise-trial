# visualise_test230507_060_lot_trace.py

import plotly.graph_objs as go

#input_list
node_I_psi = [[[], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242'], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], []]]

node_name=['JPN' , 'HAM', 'HAM-N']

# カラーコードの定義
color_codes = {'JPN': 'rgb(255, 0, 0)', 'HAM': 'rgb(0, 255, 0)', 'HAM-N': 'rgb(0, 0, 255)'}

#データの定義
x, y, z, color = [], [], [], []

for i in range(len(node_I_psi)):

    for j in range(len(node_I_psi[i])):

        node_label = node_name[i] # 修正

        for k in range(len(node_I_psi[i][j])):
            lot_id = node_I_psi[i][j][k]
            x.append(j)
            y.append(node_label)
            z.append(k)
            color.append(color_codes[node_label])

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

# ロットIDに基づいて、node_nameごとに色分けする
colors = ['rgb(255, 0, 0)', 'rgb(0, 128, 0)', 'rgb(0, 0, 255)']
color_dict = dict(zip(node_name, colors))

trace_dict = {}

for i in range(len(node_I_psi)):
    for j in range(len(node_I_psi[i])):
        node_label = node_name[i]

        for k in range(len(node_I_psi[i][j])):
            lot_id = node_label + "YYYYWW" + str(k)

            if node_label not in trace_dict:
                trace_dict[node_label] = {
                    'x': [j], 'y': [node_label], 'z': [k], 'text': [node_I_psi[i][j][k]],
                    'marker': {'color': color_dict[node_label], 'size': 5}, 'name': node_label
                }
            else:
                trace_dict[node_label]['x'].append(j)
                trace_dict[node_label]['y'].append(node_label)
                trace_dict[node_label]['z'].append(k)
                trace_dict[node_label]['text'].append(node_I_psi[i][j][k])

# Traceの作成
trace_list = [go.Scatter3d(trace_dict[label]) for label in trace_dict]

# 3D散布図の作成
fig = go.Figure(data=trace_list)

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
    )
)

# グラフの表示
fig.show()

