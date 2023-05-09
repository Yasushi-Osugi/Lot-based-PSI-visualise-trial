# Lot-based-PSI-visualise-trial
this is a trial code for "Lot based PSI" visualisation.

主な資料は以下のとおりです。
● pythonのソースコード
    visualise_bullwhip040X4github.py
● 入力ファイル
    S_month_data.csv    月次需要計画
    supply_chain_tree_attributes.csv サプライチェーンnodeの親子定義
● 出力ファイル
    iso_week_S.csv 週次需要計画
● 画面サンプルのpdfファイル

you can see, supply shain bullwhip images with plotly 3d scatter graph(see "visualise_psi_sample20230508.pdf").

Lot based PSI is "Global Supply Chain Planning" that is handling with weekly lots.
this is some visualise sample code for Lot based PSI.

visualise_bullwhip040X4github.py is main process as below.
1. "supply chain tree" is build.
2. "Monthly forcast or business plan" is broken down to ISO-week forecast.
3. Lot based PSI makes PSI plan status.
4. some visualise sample show you plotly 3d scatter grapphs.

TODO in near future is, 
1. adding supply chain plan optimizers and solvers.
   those are, buffer stock level, mother plant shipping priority, total plant capacity level to demand and so on.
2. transportation boat/air/etc definition and planning
3. supply chain plan and business plan linkage that is "shipped status = revenue up"
4. multi-products representation in this PSI planner.
5. and so on...
