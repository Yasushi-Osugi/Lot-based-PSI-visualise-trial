
#このコードでは、y軸のラベルを設定するために、
#y_axisという辞書を定義しています。
#tickvalsにはy軸の値のリストを、
#ticktextにはそれぞれの値に対応するラベルのリストを指定しています。
#
#その後、go.Figureを使って3D散布図を作成し、
#update_layoutを使ってレイアウトを設定しています。
#yaxis_titleには、先ほど定義したy_axisの設定を使って
#y軸のラベルを指定しています。最後に、fig.show()でグラフを表示しています。


import plotly.graph_objs as go

#input_list
node_I_psi = [[[], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], [], [], [], [], [], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], [], [], [], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], [], []], [[], [], [], [], [], [], [], [], [], [], [], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232', 'HAM_N2025220'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242', 'HAM_N2025230', 'HAM_N2025231', 'HAM_N2025232'], ['HAM_N2025240', 'HAM_N2025241', 'HAM_N2025242'], ['HAM_N2025250', 'HAM_N2025251', 'HAM_N2025252'], ['HAM_N2025260', 'HAM_N2025261', 'HAM_N2025262'], ['HAM_N2025270'], [], [], []]]

node_name=['JPN' , 'HAM', 'HAM-N']


#データの定義
x, y, z = [], [], []

for i in range(len(node_I_psi)):

    for j in range(len(node_I_psi[i])):

        #node_idx = node_name.index('JPN')

        node_label = node_name[i] # 修正


#        if i == node_idx:
#
#            node_label = node_name[node_idx]
#
#        else:
#
#            node_label = node_name[node_idx+1]



        for k in range(len(node_I_psi[i][j])):
            x.append(j)
            y.append(node_label)
            z.append(k)

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
fig = go.Figure(data=[go.Scatter3d(
    x=x,
    y=y,
    z=z,
    mode='markers',
    text=text,
    marker=dict(
        size=5,
        color=z,
        colorscale='Viridis',
        opacity=0.8
    )
)])

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
    )
)

#グラフの表示
fig.show()

