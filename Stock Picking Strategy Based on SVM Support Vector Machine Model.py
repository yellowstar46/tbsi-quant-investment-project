# This code is automatically generated by the visual strategy environment 15:23, May 6, 2019 
# This code unit can only be edited in visual mode. You can also copy the code, paste it into a new code unit or strategy, and then modify it. 


# Python code entry function, input_1/2/3 corresponds to three input terminals, data_1/2/3 corresponds to three output terminals 
def  m6_run_bigquant_run ( input_1 ,  input_2 ,  input_3 ): 
    train_df  =  input_1 . Read () 
    features  =  input_2 . Read ( ) 
    feature_min  =  train_df [ features ] . quantile ( 0.005 ) 
    feature_max  =  train_df [ features ] .quantile(0.995)
    train_df[features] = train_df[features].clip(feature_min,feature_max,axis=1) #去极值
    data_1 = DataSource.write_df(train_df)
    test_df = input_3.read()
    test_df[features] = test_df[features].clip(feature_min , feature_max , axis = 1 ) 
    data_2  =  DataSource . write_df ( test_df ) 
    return  Outputs ( data_1 = data_1 ,  data_2 = data_2 ,  data_3 = None ) 

# Post-processing function, optional. The input is the output of the main function, where you can process the data or return a more friendly output data format. The output of this function will not be cached. 
def  m6_post_run_bigquant_run ( outputs ): 
    return  outputs 

# Backtest engine: daily data processing function, executed once a day 
def  m4_handle_data_bigquant_run (context ,  data ): 
    
    context . extension [ 'index' ]  +=  1 
    # return without the exchange date, which is equivalent to the following code will only run once a week, the stocks bought will hold one week 
    if   context . extension [ 'index ' ]  %  context . rebalance_days  !=  0 : 
        return  
    
    # current date 
    date  =  data . current_dt . strftime ( '%Y-%m- %d ' ) 
    
    cur_data  =  context . indicator_data [ context. indicator_data [ 'date' ]  ==  date ] 
    # Get the list of stocks to be transferred according to the date 
    #stock_to_buy = list(cur_data.instrument[:context.stock_num]) 
    cur_data  =  cur_data [ cur_data [ 'pred_label' ]  = =  1.0 ] 
    
    stock_to_buy  =   list ( cur_data . Sort_values ( 'instrument' , ascending = False ) . Instrument )[: context . Stock_num ] 
    if  date  == '2017-02-06' : 
        Print ( DATE ,  len ( stock_to_buy ),  stock_to_buy ) 
    #, a method using a list formula Positions obtained by the current position of the object stock list 
    stock_hold_now  =  [ Equity . Symbol  for  Equity  in  context . Portfolio . Positions ] 
    # Stocks that continue to be held: When transferring positions, if the purchased stocks already exist in the current position, then you should continue to hold 
    no_need_to_sell  =  [ i  for  i  in  stock_hold_now  if  i  in  stock_to_buy ] 
    # Stocks to be sold 
    stock_to_sell =  [ i  for  i  in  stock_hold_now  if  i  not  in  no_need_to_sell ] 
  
    # Sell 
    for  stock  in  stock_to_sell : 
        # If the stock is suspended, there is no way to close the deal. Therefore, you need to use the can_trade method to check the status of the stock 
        # If it returns a true value, you can place the order normally, otherwise you will make an error 
        # Because stock is a string format, we use the symbol method to convert it into an acceptable format for the platform: Equity format 

        if  data . can_trade ( context . symbol ( stock )): 
            # order_target_percent is an order interface of the platform, indicating that placing an order makes the weight of the stock 0, 
            # means to sell all stocks, please refer to the 
            backtest document context . order_target_percent ( context. symbol ( stock ),  0 ) 
    
    # If there are no stocks bought on the day, return 
    if  len ( stock_to_buy )  ==  0 : 
        return 

    # equal weight buy 
    weight  =   1  /  len ( stock_to_buy ) 
    
    # buy 
    for  stock  in  stock_to_buy : 
        if  data . can_trade ( context . symbol ( stock )): 
            # placing an order makes the position weight of a certain stock reach weight, because 
            # weight is greater than 0, so it is equal weight to buy 
            context .order_target_percent ( context . symbol ( stock ),  weight ) 
 
# 
backtest engine: prepare data, only execute def  m4_prepare_bigquant_run ( context ): 
    pass 

# 
backtest engine: initialize function, execute only once def  m4_initialize_bigquant_run ( context ): 
    # load prediction data 
    context . indicator_data  =  context . options [ 'data' ] . read_df () 

    # The system has set the default transaction fee and slippage, to modify the fee can use the following function 
    context . set_commission ( PerOrder( Buy_cost = 0.0003 ,  sell_cost = 0.0013 ,  (min_cost) = . 5 )) 
    context . Rebalance_days  =  . 5 
    context . Stock_num  =  50 
    IF  'index'  Not  in  context . Extension : 
        context . Extension [ 'index' ]  =  0 
     

# back test engine: Per It is called once before the start of each unit time, that is, once before the daily opening. 
def  m4_before_trading_start_bigquant_run ( context ,  data ):
    pass


m1 = M.instruments.v2(
    start_date='2015-01-01',
    end_date='2016-05-31',
    market='CN_STOCK_A',
    instrument_list='',
    max_count=0
)

m2 = M.advanced_auto_labeler.v2(
    instruments=m1.data,
    label_expr="""shift(close, -5) / shift(open, -1)-1
rank(label) #收益率排名
#where(label>=0.95,1,where(label<=0.1, 0, NaN)) 
# The first 1/4 of the return rate is labeled 1, the last 1/4 is labeled 0, and the middle is NA 
where(label > = 0.95,1,0) "" " , 
    START_DATE = '' , 
    END_DATE = '' , 
    Benchmark = '000300.SHA' , 
    drop_na_label = False , 
    cast_label_int = False 
) 

M3  =  M . input_features . V1 ( 
    Features = " " "(close_0-mean(close_0,12))/mean(close_0,12)*100 
rank(std(amount_0,15)) 
rank_avg_amount_0/rank_avg_amount_8 
ts_argmin(low_0,20)
rank_return_30
(low_1-close_0)/close_0
ta_bbands_lowerband_14_0
mean(mf_net_pct_s_0,4)
amount_0/avg_amount_3
return_0/return_5
return_1/return_5
rank_avg_amount_7/rank_avg_amount_10
ta_sma_10_0/close_0
sqrt(high_0*low_0)-amount_0/volume_0*adjust_factor_0
avg_turn_15/(turn_0+1e-5)
return_10
mf_net_pct_s_0
(close_0-open_0)/close_1
 """
)

m15 = M.general_feature_extractor.v7(
    instruments=m1.data,
    features=m3.data,
    start_date='',
    end_date='',
    before_start_days=0
)

m16 = M.derived_feature_extractor.v3(
    input_data=m15.data,
    features=m3.data,
    date_col='date',
    instrument_col='instrument',
    drop_na=False,
    remove_extra_columns=False
)

m7 = M.join.v3(
    data1=m2.data,
    data2=m16.data,
    on='date,instrument',
    how='inner',
    sort=False
)

m13 = M.dropnan.v1(
    input_data=m7.data
)

m9 = M.instruments.v2(
    start_date=T.live_run_param('trading_date', '2016-06-01'),
    end_date=T.live_run_param('trading_date', '2017-01-01'),
    market='CN_STOCK_A',
    instrument_list='',
    max_count=0
)

m17 = M.general_feature_extractor.v7(
    instruments=m9.data,
    features=m3.data,
    start_date='',
    end_date='',
    before_start_days=0
)

m18 = M.derived_feature_extractor.v3(
    input_data=m17.data,
    features=m3.data,
    date_col='date',
    instrument_col='instrument',
    drop_na=False,
    remove_extra_columns=False
)

m14 = M.dropnan.v1(
    input_data=m18.data
)

m6 = M.cached.v3(
    input_1=m13.data,
    input_2=m3.data,
    input_3=m14.data,
    run=m6_run_bigquant_run,
    post_run=m6_post_run_bigquant_run,
    input_ports='',
    params='{}',
    output_ports=''
)

m8 = M.RobustScaler.v13(
    train_ds=m6.data_1,
    features=m3.data,
    test_ds=m6.data_2,
    scale_type='standard',
    quantile_range_min=0.01,
    quantile_range_max=0.99,
    global_scale=True
)

m10 = M.svc.v1(
    training_ds=m8.train_data,
    features=m3.data,
    predict_ds=m8.test_data,
    C=1,
    kernel='rbf',
    degree=3,
    gamma=-1,
    coef0=0,
    tol=0.1,
    max_iter=100,
    key_cols='date,instrument',
    other_train_parameters={}
)

m4 = M.trade.v4(
    instruments=m9.data,
    options_data=m10.predictions,
    start_date='',
    end_date='',
    handle_data=m4_handle_data_bigquant_run,
    prepare=m4_prepare_bigquant_run,
    initialize=m4_initialize_bigquant_run,
    before_trading_start=m4_before_trading_start_bigquant_run,
    volume_limit=0,
    order_price_field_buy='open',
    order_price_field_sell='open',
    capital_base=10000000,
    auto_cancel_non_tradable_orders=True,
    data_frequency='daily',
    price_type='后复权',
    product_type='股票',
    plot_charts=True,
    backtest_only=False,
    benchmark=''
)
