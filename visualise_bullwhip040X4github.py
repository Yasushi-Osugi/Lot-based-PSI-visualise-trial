# visualise_bullwhip030X4github.py

# 処理内容
# 入力ファイル: 拠点node別、複数年別、1月-12月の需要数
#               node_listを生成しておく

# 処理        : iso_year+iso_weekをkeyにして、需要数を月間から週間に変換する

#               前処理で、各月の日数と月間販売数から、月毎の日平均値を求める
#               年月日からISO weekを判定し、
#               月間販売数の日平均値をISO weekの変数に加算、週間販売数を計算

#               ***** pointは「年月日からiso_year+iso_weekへの変換処理」 *****
#               dt = datetime.date(year, month, day) 
#               iso_year, iso_week, _ = dt.isocalendar()

#               for nodeのループ下で、
#               YM_key_list.append(key)  ## keyをappendして
#               pos = len( YW_key_list ) ## YM_key_listの長さを位置にして
#               YW_value_list( pos ) += average_daily_value ## 値を+=加算

# 出力リスト  : node別 複数年のweekの需要 S_week
#               縦持ちwrite    : sql処理用
#               横持ちwrite    : python psi処理用
#               年別横持ちwrite: excel用


import pandas as pd
import csv


import math
import numpy as np

import datetime
import calendar

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

import plotly.graph_objs as go


# ***********************************
# def
# ***********************************
def visualise_psi_label(node_I_psi, node_name):
    
    #データの定義
    x, y, z = [], [], []
    
    for i in range(len(node_I_psi)):
    
        for j in range(len(node_I_psi[i])):
    
            #node_idx = node_name.index('JPN')
    
            node_label = node_name[i] # 修正
    
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



# 前処理として、年月の月間販売数の一日当たりの平均値を計算する
def calc_average_sales(monthly_sales, year):

    month_daily_average = [0]*12

    for i, month_qty in enumerate(monthly_sales):

        month = i + 1

        days_in_month = calendar.monthrange(year, month)[1]

        month_daily_average[i] = monthly_sales[i] / days_in_month

    return month_daily_average




# ある年の月次販売数量を年月から年ISO週に変換する
def calc_weekly_sales(node, monthly_sales, year,year_month_daily_average, sales_by_iso_year, yyyyww_value, yyyyww_key):

    weekly_sales = [0] * 53    

 
    for i, month_qty in enumerate( monthly_sales ):

        # 開始月とリストの要素番号を整合
        month = i + 1

        # 月の日数を調べる
        days_in_month = calendar.monthrange(year, month )[1]

        # 月次販売の日平均
        avg_daily_sales = year_month_daily_average[year][ i ] # i=month-1

        # 月の日毎の処理
        for day in range(1, days_in_month + 1):
        # その年の"年月日"を発生

            ## iso_week_noの確認 年月日でcheck その日がiso weekで第何週か
            #iso_week = datetime.date(year,month, day).isocalendar()[1]

            # ****************************
            # year month dayからiso_year, iso_weekに変換
            # ****************************
            dt = datetime.date(year, month, day)

            iso_year, iso_week, _ = dt.isocalendar()


            # 辞書に入れる場合 
            sales_by_iso_year[iso_year][iso_week-1] += avg_daily_sales


            # リストに入れる場合
            node_year_week_str = f"{node}{iso_year}{iso_week:02d}"


            if node_year_week_str not in yyyyww_key:

                yyyyww_key.append(node_year_week_str)

            pos = len(yyyyww_key) - 1

            yyyyww_value[pos]  += avg_daily_sales

    return sales_by_iso_year[year]




# *********************************
# start of code
# *********************************

# *******************************************************
# trans S from monthly to weekly
# *******************************************************

def trans_month2week(input_file, outputfile):


# IN:      'S_month_data.csv'
# PROCESS: nodeとyearを読み取る yearはstart-1年に"0"セットしてLT_shiftに備える
# OUT:     'S_iso_week_data.csv'

# *********************************
# read monthly S
# *********************************

####
    # csvファイルの読み込み
    df = pd.read_csv( input_file ) # IN:      'S_month_data.csv'
    
    # リストに変換
    month_data_list = df.values.tolist()
    
    
    
    # node_nameをユニークなキーとしたリストを作成する
    node_list = df['node_name'].unique().tolist()
    
    
    # *********************************
    # write csv file header [prod-A,node_name,year.w0,w1,w2,w3,,,w51,w52,w53]
    # *********************************
    
    file_name_out = outputfile # OUT:     'S_iso_week_data.csv'
    
    with open(file_name_out, mode='w', newline='') as f:
    
        writer = csv.writer(f)
    
        writer.writerow(['product_name', 'node_name', 'year', 
    'w1' ,'w2' ,'w3' ,'w4' ,'w5' ,'w6' ,'w7' ,'w8' ,'w9' ,'w10','w11','w12','w13    ',
    'w14','w15','w16','w17','w18','w19','w20','w21','w22','w23','w24','w25','w26    ',
    'w27','w28','w29','w30','w31','w32','w33','w34','w35','w36','w37','w38','w39    ',
    'w40','w41','w42','w43','w44','w45','w46','w47','w48','w49','w50','w51','w52    ',
    'w53'])
    
    
# *********************************
# plan initial setting
# *********************************

# node別に、中期計画の3ヵ年、5ヵ年をiso_year+iso_week連番で並べたもの
# node_lined_iso_week = { node-A+year+week: [iso_year+iso_week1,2,3,,,,,],   } 
# 例えば、2024W00, 2024W01, 2024W02,,, ,,,2028W51,2028W52,2028W53という5年間分
    
    node_lined_iso_week = {} 
    
    node_yyyyww_value = []
    node_yyyyww_key   = []
    
    
    
    
    for node in node_list:
    
        #print('node',node)
    
        df_node = df[df['node_name'] == node]
    
        #print('df_node',df_node)
    
        # リストに変換
        node_data_list = df_node.values.tolist()
    
        #
        # getting start_year and end_year
        #
        start_year = node_data_min = df_node['year'].min()
        end_year   = node_data_max = df_node['year'].max()
    
        #print('max min',node_data_max, node_data_min)
    
    
        # S_month辞書の初期セット
        monthly_sales_data    = {}
    
    
    # *********************************
    # plan initial setting
    # *********************************
    
        plan_year_st = start_year                  # 2024  # plan開始年
    
        plan_range = end_year - start_year + 1     # 5     # 5ヵ年計画分のS計画
    
        plan_year_end = plan_year_st + plan_range
    
    
    # *********************************
    # by node    node_yyyyww = [ node-a, yyyy01, yyyy02,,,, ]
    # *********************************
    
        yyyyww_value = [0]*53*plan_range  # 5ヵ年plan_range=5
    
        yyyyww_key   = []
    
    
    
        for data in node_data_list:
    
            # node別　3年～5年　月次需要予測値
    
            #print('data',data)
    
    
            
            # 辞書形式{year: S_week_list, }でデータ定義する
            sales_by_iso_year = {}
            
    
# 前後年付きの辞書 53週を初期セット 
# **********************************
# 空リストの初期設定
# start and end setting from S_month data # 月次Sのデータからmin&max 
# **********************************
            
            #前年の52週が発生する可能性あり # 計画の前後の-1年 +1年を見る
            work_year = plan_year_st - 1 
    
            for i in range(plan_range+2):   # 計画の前後の-1年 +1年を見る
            
                year_sales = [0] * 53 # 53週分の要素を初期セット
            
                # 年の辞書に週次Sをセット
                sales_by_iso_year[work_year] = year_sales 
            
                work_year += 1
            
    # *****************************************
    # initial setting end
    # *****************************************
    
    # *****************************************
    # start process
    # *****************************************
    
            # ********************************
            # generate weekly S from monthly S
            # ********************************
            
            # S_monthのcsv fileを読んでS_month_listを生成する
            # pandasでcsvからリストにして、node_nameをキーに順にM2W変換
            
            # ****************** year ****** Smonth_list ******
            monthly_sales_data[ data[2] ] = data[3:] 
            
            # data[0] = prod-A
            # data[1] = node_name
            # data[2] = year
    
            #print('monthly_sales_data',monthly_sales_data)

        # **************************************
        # 年月毎の販売数量の日平均を計算する
        # **************************************
        year_month_daily_average = {}
        
        #print('plan_year_st_st',plan_year_st)
        #print('plan_year_end',plan_year_end)
    
        for y in range(plan_year_st,plan_year_end):
        
            year_month_daily_average[y] = calc_average_sales(monthly_sales_data[    y], y)
    
    
        # 販売数量を年月から年ISO週に変換する
        for y in range(plan_year_st,plan_year_end):
        
            ##print('input monthly sales by year', y, monthly_sales_data[y])
    
            sales_by_iso_year[y] = calc_weekly_sales(node, monthly_sales_data[y], y, year_month_daily_average, sales_by_iso_year, yyyyww_value, yyyyww_key)
    
    
        work_yyyyww_value = [node] + yyyyww_value
        work_yyyyww_key   = [node] + yyyyww_key
    
        node_yyyyww_value.append( work_yyyyww_value )
        node_yyyyww_key.append( work_yyyyww_key )
    
    
        # 複数年のiso週毎の販売数を出力する
        for y in range(plan_year_st,plan_year_end):
        
            #for i in range(53):
            #
            #    #print('year week sales_by_iso_year',y,i+1,sales_by_iso_year[y]    [i])
    
    # *******************************************
    # 初期処理でheader書出し済み 
    # [prod-A,node_name,year.w0,w1,w2,w3,,,w51,w52,w53]
    # *******************************************
    #file_name_out = 'iso_week_S.csv'
    #with open(file_name_out, mode='w', newline='') as f:
    #    writer = csv.writer(f)
    #    writer.writerow(['product_name', 'node_name', 'year', 'w0', 'w1', 'w2',     'w3', 'w4', 'w5', 'w6', 'w7', 'w8', 'w9', 'w10', 'w11', 'w12','w13'])
    
            rowX = ['product-X'] + [node] + [y] + sales_by_iso_year[y]
            ##print('rowX',rowX)
    
            with open(file_name_out, mode='a', newline='') as f:
    
                writer = csv.writer(f)
    
                writer.writerow(rowX)
    
    
# **********************
# リスト形式のS出力
# **********************

#for i, node_key in enumerate(node_yyyyww_key):
#
#    print( i )
#    print( node_key[0] )
#    print( node_key[1:] )
#
#    node_val = node_yyyyww_value[ i ]
#
#    print( node_val[0] )
#    print( node_val[1:] )
#
#
#for node_val in node_yyyyww_value:
#    print( node_val )

#['SHA_N', 22.580645161290324, 22.580645161290324, 22.580645161290324, 22.580645161290324, 26.22914349276974, 28.96551724137931, 28.96551724137931, 28.96551724137931, 31.067853170189103, 33.87096774193549, 33.87096774193549, 33.87096774193549, 33.87096774193549, 30.33333333333333, 30.33333333333333, 30.33333333333333, 30.33333333333333, 31.247311827956988, 31.612903225806452,

#    print( node_val[0] )
#    print( node_val[1:] )


    # **********************
    # リスト形式のkey='node'+'yyyyww'出力
    # **********************
    #print('node_yyyyww_key',node_yyyyww_key)

    return node_yyyyww_value, node_yyyyww_key, plan_range

# *********************
# END of week data generation 
# node_yyyyww_value と node_yyyyww_keyに複数年の週次データがある
# *********************


# *******************************************************
# lot by lot PSI
# *******************************************************
def makeS(S_week, lot_size): # Sの値をlot単位に変換

    return [math.ceil(num / lot_size) for num in S_week]



def setS(psi_list, node_name, Slot, yyyyww_list ):

    #print('Slot',Slot)
    #print('yyyyww_list',yyyyww_list)

    for w, (lots, yyyyww) in enumerate(zip(Slot, yyyyww_list)):

        step_list = []

        for i in range(lots):

            lot_id = str(yyyyww) + str(i)
            #lot_id = node_name + str(yyyyww) + str(i)
            #lot_id = node_name + str(year) + str(w) + str(i)

            #print('str(yyyyww)',str(yyyyww))
            #print('lot_id',lot_id)

            step_list.append(lot_id)

        # week 0="S"
        psi_list[w][0] = step_list

        #print('step_list',step_list)

    return psi_list


# checking constraint to inactive week , that is "Long Vacation"
def check_lv_week(const_lst, check_week):

    #print('const_lst',const_lst)

    num = check_week

    if const_lst == []:

        #print('test const_lst',const_lst)

        pass

    else:

        while num in const_lst:

            num -= 1

    return num



def calcPS2I(psiS2P):

    plan_len = len(psiS2P)

    for w in range(1, plan_len): # starting_I = 0 = w-1 / ending_I = 53
    #for w in range(1,54): # starting_I = 0 = w-1 / ending_I = 53

        s   = psiS2P[w][0]
        co  = psiS2P[w][1]

        i0  = psiS2P[w-1][2]
        i1  = psiS2P[w][2]

        p   = psiS2P[w][3]

        # *********************
        # # I(n-1)+P(n)-S(n)
        # *********************

        #print('i0',i0)
        #print('p',p)


        work = i0 + p  


        #print('work',work)
        #print('s',s)


        #@230321 TOBT memo ここで、期末の在庫、S出荷=売上を操作している
        # S出荷=売上を明示的にlogにして、売上として記録し表示する処理
        # 出荷されたS=売上、在庫I、未出荷COの集合を正しく表現する

        # モノがお金に代わる瞬間

        diff_list = [x for x in work if x not in s] # I(n-1)+P(n)-S(n)

        psiS2P[w][2] = i1 = diff_list

    return psiS2P



def shiftS2P_LV(psiS, safety_stock_week, lv_week): # LV:long vacations

    #print('lv_week',lv_week)

    ss = safety_stock_week

    plan_len = len( psiS ) - 1 # -1 for week list position

    #print('plan_len & psiS', plan_len , psiS)


    for w in range(plan_len, ss, -1): # backward planningで需要を降順でシフト

#my_list = [1, 2, 3, 4, 5]
#for i in range(2, len(my_list)):
#    my_list[i] = my_list[i-1] + my_list[i-2] 

        # 0:S
        # 1:CO
        # 2:I
        # 3:P

        eta_plan = w - ss # ss:safty stock

        #print('eta_plan = w - ss', eta_plan, w, ss)

        eta_shift = check_lv_week(lv_week, eta_plan) #ETA:Eatimate Time Arrival

        ##print('w psiS[w][0] ', w, psiS[w][0])
        ##print('eta_plan psiS[eta_plan][3] ', eta_plan, psiS[eta_plan][3])

        # リスト追加 extend 
        # 安全在庫とカレンダ制約を考慮した着荷予定週Pに、w週Sからoffsetする
        psiS[eta_shift][3].extend( psiS[w][0] )  # P made by shifting S with 

        #print('psiS[eta_shift][3] appended',eta_shift, psiS[eta_plan][3])

    return psiS





# **************************************
# 可視化トライアル
# **************************************

# node dictの在庫Iを可視化
def show_node_I4bullwhip_color(node_I4bullwhip):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # x, y, z軸のデータを作成
    x = np.arange(len(node_I4bullwhip['HAM_N']))

    n = len(node_I4bullwhip.keys())
    y = np.arange(n)

    X, Y = np.meshgrid(x, y)

    z = list(node_I4bullwhip.keys())

    Z = np.zeros((n, len(x)))

    # node_I4bullwhipのデータをZに格納
    for i, node in enumerate(z):
        Z[i,:] = node_I4bullwhip[node]

    # 3次元の棒グラフを描画
    dx = dy = 1.2 # 0.8
    dz = Z
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    for i in range(n):
        ax.bar3d(X[i], Y[i], np.zeros_like(dz[i]), dx, dy, dz[i], color=colors[i % len(colors)], alpha=0.8)

    # 軸ラベルを設定
    ax.set_xlabel('Week')
    ax.set_ylabel('Node')
    ax.set_zlabel('Inventory')

    # y軸の目盛りをnode名に設定
    ax.set_yticks(y)
    ax.set_yticklabels(z)

    plt.show()



def show_psi_3D_graph_node(node):

    node_name = node.name

    #node_name = psi_list[0][0][0][:-7]
    #node_name = psiS2P[0][0][0][:-7]

    #print('node_name',node_name)

    psi_list = node.psi_list

    # 二次元マトリクスのサイズを定義する
    x_size = len(psi_list)
    y_size = len(psi_list[0])
    
    #x_size = len(psiS2P)
    #y_size = len(psiS2P[0])
    
    # x軸とy軸のグリッドを生成する
    x, y = np.meshgrid(range(x_size), range(y_size))
    

    # y軸の値に応じたカラーマップを作成
    color_map = plt.cm.get_cmap('cool')


    # z軸の値をリストから取得する
    z = []
    
    for i in range(x_size):
        row = []
        for j in range(y_size):

            row.append(len(psi_list[i][j]))
            #row.append(len(psiS2P[i][j]))

        z.append(row)
    
    #print('z',z)

    ravel_z = np.ravel(z)

    #print('ravel_z',ravel_z)

    norm = plt.Normalize(0,3)
    #norm = plt.Normalize(0,dz.max())


    # 3Dグラフを作成する
    fig = plt.figure()
    
    ax = fig.add_subplot(111, projection='3d')
    
    
    #print('x',x)
    #print('y',y)
    
    z_like = np.zeros_like(z)
    #print('z_like',z_like)
    
    #print("dx",0.05)
    #print("dy",0.05)
    
    #print('dz',z)
    
    
    # ********************
    # x/yの逆転
    # ********************
    original_matrix = z
    
    inverted_matrix = []

    for i in range(len(original_matrix[0])):
        inverted_row = []
        for row in original_matrix:
            inverted_row.append(row[i])
        inverted_matrix.append(inverted_row)
    
    z_inv = inverted_matrix
    
    
    
    #print(inverted_matrix)
    
    #print("liner X",np.ravel(x))
    #print("liner Y",np.ravel(y))
    #print("liner z",np.ravel(z))
    #print("liner z",np.ravel(z_inv))
    
    #print("z[0][1]",z[0][1])
    
    
    #colors = plt.cm.terrain_r(norm(z_inv))
    #colors = plt.cm.terrain_r(norm(dz))


    # ********************
    # 4色での色分け
    # ********************

    # 色分け用のデータ
    color_data = [1, 2, 3, 4]

    # 色は固定
    # colorsのリストは、S/CO/I/Pに対応する
    #colors = ['cyan', 'blue', 'red', 'gold']
    #colors = ['cyan', 'blue', 'maroon', 'gold']
    colors = ['cyan', 'blue', 'brown', 'gold']

    y_list = np.ravel(y)

    #print('y',y)
    #print('y_list',y_list)

    #print('colors',colors)

    c_map = []
    
    for index in y_list:

        c_map.append(colors[index])

    #print('c_map',c_map)


    # ********************
    # bar3D
    # ********************

    
    ax.bar3d(np.ravel(x), np.ravel(y), np.ravel(np.zeros_like(z)),0.05,0.05,np.ravel(z_inv), color=c_map )

    ax.set_title(node_name, fontsize='16') # タイトル

    plt.show()



def make_node_psi_dict( node_yyyyww_value, node_yyyyww_key, nodes ):

    for i, node_val in enumerate(node_yyyyww_value):
    
        node_name = node_val[0]
        S_week    = node_val[1:]
    
        #print('node_name',node_name)
        #print('S_week',S_week)

        node = nodes[node_name]   # node_nameからnodeインスタンスを取得

        # node.lot_sizeを使う
        lot_size = node.lot_size # Node()からセット
    

        # makeSでSlotを生成
        Slot = makeS(S_week, lot_size)

        # nodeに対応するpsi_listを生成する
        psi_list = [[[] for j in range(4)] for w in range( len(S_week) )] 


        node_key = node_yyyyww_key[i]

        ####node_name = node_key[0] # node_valと同じ

        yyyyww_list   = node_key[1:]

        # lot_listのリスト化
        psiS = setS(psi_list, node_name, Slot, yyyyww_list )

        node_psi_dict[node_name] = psiS #初期セットSを渡す。本来はleaf_nodeのみ

    return node_psi_dict



# 1. データを読む　データ長を調べる
# 2. class Nodeでtreeを作る
# 3. psi_listを作る node_psi_dicを作る
# 4. class Nodeのself.psi_listに、node_psi_dicのpsi_listをpointor接続する
# 5. Nodeのtree構造は、node間のサーチ・巡回用。psi操作は、接続元のpsiで処理

# 長さ、len(S_week) の値を 入力ファイルS_monthのyear_start/end/rangeから
#


# Slot_value = makeS 値をlot_sizeで割る

# setS   は、値をlot_idとlot_list構造に変換 Slot_value2id_list
#            lot_id = str(yyyyww) + str(i)
#
#    Slotのvalueを、Slot_id =  yyyyww + i のリスト構造に変換する
#
#    psiS = setS(psi_list, node_name, Slot, yyyyww_list )

# psiSをdict[node: psi_list]で外に持つか?、class Nodeのself.spi_listに持つか?
# 外にある辞書型node_psiを指すだけの方が「軽くなる」ハズ。
# self.psi_listで、Nodeインスタンスのspi_listに直接データを置くと「重くなる」?
# load/saveは別途。



# **********************************
# create tree
# **********************************
class Node:

    def __init__(self, name):
        self.name = name
        self.children = []

        # application attribute # nodeをインスタンスした後、初期値セット
        self.psi_list = None

        self.safety_stock_week = 0
        #self.safety_stock_week = 2

        #self.lv_week = []

        self.lot_size             = 1 # defalt set

        # leadtimeとsafety_stock_weekは、ここでは同じ
        self.leadtime             = 1 # defalt set

        self.long_vacation_weeks  = []



    def add_child(self, child):
        self.children.append(child)



    def set_attributes(self, row):
        self.lot_size            = int( row[3] )
        self.leadtime            = int( row[4] )
        self.long_vacation_weeks = eval( row[5] )



    def set_psi_list(self, psi_list):

        self.psi_list = psi_list



    def get_set_childrenS2psi(self, plan_range):

        ## 子node Pの収集、LT offsetによるS移動 リストの加算extend

        self.psi_list = [[[] for j in range(4)] for w in range(53*plan_range)]

        #print('self.name', self.name)
        #print('self.psi_list', self.psi_list)

        for child in self.children:

            #print('child.name', child.name)
            #print('child.psi_list', child.psi_list)

            for w in range( 53*plan_range ): 
            #for w in range( 53*5 ): 

                #print('child.psi_list[w][3]', w, child.psi_list[w][3])

                self.psi_list[w][0].extend(child.psi_list[w][3]) #setting P=S

                #print('self.psi_list[w][0]', w, self.psi_list[w][0])

        #print('self.psi_list', self.name,self.psi_list)



    def calcPS2I(self):
    
        #psiS2P = self.psi_list # copyせずに、直接さわる
    
        plan_len = len(self.psi_list)

        for w in range(1,plan_len): # starting_I = 0 = w-1 / ending_I =plan_len
        #for w in range(1,54): # starting_I = 0 = w-1 / ending_I = 53
    

            s   = self.psi_list[w][0]
            co  = self.psi_list[w][1]
    
            i0  = self.psi_list[w-1][2]
            i1  = self.psi_list[w][2]
    
            p   = self.psi_list[w][3]

            # *********************
            # # I(n-1)+P(n)-S(n)
            # *********************
    
            #print('i0',i0)
            #print('p',p)
    
    
            work = i0 + p  
    
    
            #print('work',work)
            #print('s',s)
    
    
            #@230321 TOBE memo ここで、期末の在庫、S出荷=売上を操作している
            # S出荷=売上を明示的にlogにして、売上として記録し、表示する処理
            # 出荷されたS=売上、在庫I、未出荷COの集合を正しく表現する
    
            # モノがお金に代わる瞬間
    
            diff_list = [x for x in work if x not in s] # I(n-1)+P(n)-S(n)
    
            self.psi_list[w][2] = i1 = diff_list
    
        #return psiS2P  # returnしなくて良い。self.psi_listを直接、操作。



    def calcS2P(self):

# **************************
# Safety Stock as LT shift
# **************************
        # leadtimeとsafety_stock_weekは、ここでは同じ
        safety_stock_week = self.leadtime

# **************************
# long vacation weeks 
# **************************
        lv_week           = self.long_vacation_weeks

        # S to P の計算処理
        self.psi_list = shiftS2P_LV(self.psi_list, safety_stock_week, lv_week)

        pass



def create_tree(csv_file):

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        next(reader)  # ヘッダー行をスキップ

        # nodeインスタンスの辞書を作り、親子の定義に使う
        nodes = {row[2]: Node(row[2]) for row in reader}

        #print('nodes',nodes)

        f.seek(0)  # ファイルを先頭に戻す

        next(reader)  # ヘッダー行をスキップ

        next(reader)  # root行をスキップ #@230501 JPNの属性がセットされない???

        for row in reader:

            #print('row',row)

            parent = nodes[row[0]]

            child = nodes[row[1]]

            parent.add_child(child)

            child.set_attributes(row) #子ノードにアプリケーション属性をセット

    return nodes           # すべてのインスタンス・ポインタを返して使う
    #return nodes['JPN']   # "JPN"のインスタンス・ポインタ



def set_psi_lists(node, node_psi_dict):
    # キーが存在する場合は対応する値valueが返り、存在しない場合はNoneが返る。
    if node.children == []: # 子nodeがないleaf nodeの場合

        #print('leaf', node.name )

        node.set_psi_list(node_psi_dict.get(node.name))

    else:

        #print('no leaf', node.name )

        node.get_set_childrenS2psi(plan_range)

    for child in node.children:

        set_psi_lists(child, node_psi_dict)



def set_psi_lists_postorder(node, node_psi_dict):

    for child in node.children:

        set_psi_lists_postorder(child, node_psi_dict)

    # キーが存在する場合は対応する値valueが返り、存在しない場合はNoneが返る。
    if node.children == []: # 子nodeがないleaf nodeの場合
        #print('leaf', node.name )

        # 辞書のgetメソッドでキーから値を取得。キーが存在しない場合はNone
        node.set_psi_list(node_psi_dict.get(node.name)) 

        # shifting S2P
        node.calcS2P()  # backward plan with postordering 


    else: 

        #print('no leaf', node.name )

        # gathering S and Setting S
        node.get_set_childrenS2psi(plan_range)

        # shifting S2P
        node.calcS2P()  # backward plan with postordering 



def get_all_psi(node):

    node_all_psi[node.name] = node.psi_list

    node_search.append(node)

    for child in node.children:

        get_all_psi(child)

    ####return( node_I4bullwhip )



def set_all_I4bullwhip(node):

    node_search.append(node)


    for child in node.children:

        set_all_I4bullwhip(child)


    # node辞書に時系列set
    #node.set_I4bullwhip()

    I_hi_len = [] #在庫の高さ=リストの長さ

    for w in range( len( node.psi_list ) ):

        I_hi_len.append( len(node.psi_list[w][2]) ) 


    node_I4bullwhip[node.name] = I_hi_len

    return( node_I4bullwhip )



def calc_all_psi2i(node):

    node_search.append(node)

    node.calcPS2I()

    for child in node.children:

        calc_all_psi2i(child)



def calc_all_psi2i_postorder(node):

    for child in node.children:

        calc_all_psi2i_postorder(child)

    node_search.append(node)

    node.calcPS2I()  # backward plan with postordering 



def calc_all_psiS2P_postorder(node):

    for child in node.children:

        calc_all_psiS2P_postorder(child)

    node_search.append(node)

    node.calcS2P()  # backward plan with postordering 


# ***************************
# tree definition initialise
# ***************************

node_search = []


node_I4bullwhip = {}

nodes = {}

#csv_file = 'supply_chain_tree_attributes_test_small3.csv'
#csv_file = 'supply_chain_tree_attributes_test_small.csv'
csv_file = 'supply_chain_tree_attributes.csv'


# M2Wで生成したpsi_listをnodeをキーとするdictに変換する
# node_psi_dictは生成済み


# ***************************
# create tree
# ***************************
nodes = create_tree(csv_file)  # nodesですべてのnodeインスタンスを取得

root_node = nodes['JPN']


# ***************************
# trans_month2week
# ***************************
#in_file    = "S_month_data_small3_2zero.csv"
#in_file    = "S_month_data_small3_2.csv"
#in_file    = "S_month_data_small3_1.csv"
#in_file    = "S_month_data_small3.csv"
#in_file    = "S_month_data_small2.csv"
#in_file    = "S_month_data_small.csv"
in_file    = "S_month_data.csv"
out_file   = "S_iso_week_data.csv"


plan_range = 1   #### 計画期間=1年

node_yyyyww_value, node_yyyyww_key, plan_range =trans_month2week(in_file, out_file)


# an image of data
#
#for node_val in node_yyyyww_value:
#    print( node_val )
#
##['SHA_N', 22.580645161290324, 22.580645161290324, 22.580645161290324, 22.580645161290324, 26.22914349276974, 28.96551724137931, 28.96551724137931, 28.96551724137931, 31.067853170189103, 33.87096774193549, 33.87096774193549, 33.87096774193549, 33.87096774193549, 30.33333333333333, 30.33333333333333, 30.33333333333333, 30.33333333333333, 31.247311827956988, 31.612903225806452,


#node_yyyyww_key [['CAN', 'CAN202401', 'CAN202402', 'CAN202403', 'CAN202404', 'CAN202405', 'CAN202406', 'CAN202407', 'CAN202408', 'CAN202409', 'CAN202410', 'CAN202411', 'CAN202412', 'CAN202413', 'CAN202414', 'CAN202415', 'CAN202416', 'CAN202417', 'CAN202418', 'CAN202419', 


# ********************************
# make_node_psi_dict
# ********************************

# 1. treeeを生成して、nodes[node_name]辞書で、各nodeのinstanceを操作する

# 2. 週次S yyyywwの値valueを月次Sから変換、
#    週次のlotの数Slotとlot_keyを生成、

# 3. ロット単位=lot_idとするリストSlot_id_listを生成しながらpsi_list生成

# 4. node_psi_dict=[node1: psi_list1,,,]を生成し、treeのnode.psi_listに接続する

S_week = []

node_psi_dict = {} # node_psi辞書

#make_node_psi_dictを作る
node_psi_dict = make_node_psi_dict( node_yyyyww_value, node_yyyyww_key, nodes )


# ***************************************
# set_psi_lists_postorder
# ***************************************

# Sをnode.psi_listにset
set_psi_lists_postorder(root_node, node_psi_dict) 

#print('root_node.psi_list',root_node.psi_list)

# STOP
#show_psi_3D_graph_node(root_node)


# ***************************************
# calc_all_psi2i
# ***************************************
node_search = []

calc_all_psi2i(root_node) # SP2I計算はpreorderingでForeward Planningする

# STOP
#show_psi_3D_graph_node(root_node)


#for n in node_search:
#
#    print('node_search node.name',n.name)


# *********************************
# visualise with Axes3D
# *********************************

# STOP
#node_I4bullwhip = set_all_I4bullwhip(root_node)
#
#show_node_I4bullwhip_color(node_I4bullwhip)



# *********************************
# node_all_psiからIを抽出してnode_I_list生成してvisualise
# *********************************
node_all_psi = {}

get_all_psi(root_node)

#print('node_all_psi', node_all_psi )


# X
week_len = len(node_yyyyww_key)

# Y
node_w_list = list( node_all_psi.keys() )
node_len = len(node_w_list)

#print('node_w_list', node_w_list)

#print('X;week_len  Y:node_len',week_len,node_len)


node_I_list = [[]*i for i in range(node_len)]

#print('node_I_list',node_I_list)

for node_name, psi_list in node_all_psi.items():

    node_index = node_w_list.index(node_name)

    supply_inventory_list = [[]*i for i in range(len(psi_list))]

    for week in range(len(psi_list)):

        step_lots = psi_list[week][2]

        #print('step_lots',step_lots)

        supply_inventory_list[week] = step_lots

    node_I_list[node_index] = supply_inventory_list 

visualise_psi_label(node_I_list, node_w_list)


