# visualise_test230507_070_lot_trace.py

import plotly.graph_objs as go
import random

# input_list
node_I_psi = [
    [[], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], [], [], [], [], [], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], []],
    [[], [], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242'], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], []]
]

node_name = ['JPN', 'HAM', 'HAM-N']

# lot_idを"node_name"+"YYYY"+"WW"別に抽出し、各node_nameで色を指定
colors = {}
for i in range(len(node_I_psi)):
    node_label = node_name[i]
    lot_ids = []
    for j in range(len(node_I_psi[i])):
        for k in range(len(node_I_psi[i][j])):
            lot_id = node_I_psi[i][j][k]
            if lot_id:
                lot_ids.append(lot_id[:7])
    colors[node_label] = {}
    for lot_id in set(lot_ids):
        colors[node_label][lot_id] = random.randint(0, 255**3)  # 色の指定



# データの定義
x, y, z, color = [], [], [], []

for i in range(len(node_I_psi)):
    node_label = node_name[i]
    for j in range(len(node_I_psi[i])):
        for k in range(len(node_I_psi[i][j])):
            lot_id = node_I_psi[i][j][k]
            if lot_id:


                node_name_length = len(node_label)
                #node_name_length = len(node_name)
                year = lot_id[node_name_length:node_name_length+4]
                week = lot_id[node_name_length+4:node_name_length+6]

                #year, week, _ = lot_id.split('_')[-1].split('-')


                color_rgb = colors[node_label].get(node_label + year + week, None)
                if color_rgb:
                    x.append(j)
                    y.append(k)
                    z.append(i)
                    color.append(color_rgb)


#データの定義
x, y, z = [], [], []

for i in range(len(node_I_psi)):
    for j in range(len(node_I_psi[i])):
        node_label = node_name[i]
        for k in range(len(node_I_psi[i][j])):
            lot_id = node_I_psi[i][j][k]
            x.append(j)


            node_name_length = len(node_label)
            #node_name_length = len(node_name)
            year = lot_id[node_name_length:node_name_length+4]
            week = lot_id[node_name_length+4:node_name_length+6]


            y.append(node_label + year + week) # "node_name"+"YYYY"+"WW"
            #y.append(node_label + '-' + lot_id[4:8]) # "node_name"+"YYYY"+"WW"

            z.append(k)




# 3D散布図のプロット
fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(color=color, size=5))])

# レイアウトの設定
fig.update_layout(scene=dict(xaxis=dict(title='X axis'), yaxis=dict(title='Y axis'), zaxis=dict(title='Z axis')), width=800, height=800)

# 表示
fig.show()

