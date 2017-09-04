from stockmarket import baselinemodel

agents, firms, stocks, order_books = baselinemodel.stockMarketSimulation(seed=0,
                                                                         simulation_time=1100,
                                                                         init_backward_simulated_time=200,
                                                                         number_of_agents=100,
                                                                         # use this to calculate amount noise mean momentum and mean reversion
                                                                         share_chartists=0.3,
                                                                         share_mean_reversion=0.5,
                                                                         amount_of_firms=1,
                                                                         # divide this over the agents
                                                                         initial_total_money=(100,200),
                                                                         initial_profit=(200, 200),
                                                                         discount_rate=0.11,
                                                                         # init using the midpoint of the init_price_to_earnings
                                                                         init_price_to_earnings_window=((4, 7), (10, 14)),
                                                                         order_expiration_time=200,
                                                                         # new init bid_ask
                                                                         agent_order_price_variability=(1,1),
                                                                         agent_order_variability=1.5,
                                                                         agent_ma_short=(20, 40),
                                                                         agent_ma_long=(120, 150),
                                                                         agents_hold_thresholds=(0.9995, 1.0005),
                                                                         agent_volume_risk_aversion=0.1,
                                                                         agent_propensity_to_switch=1.1,
                                                                         # profit process variables
                                                                         firm_profit_mu=0.058,
                                                                         firm_profit_delta=0.00396825396,
                                                                         firm_profit_sigma=0.125,
                                                                         profit_announcement_working_days=20,
                                                                         printProgress=True,
                                                                         )
