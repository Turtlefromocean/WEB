import investpy


def check_stock(stock):
	check_result = False

	try:
		investpy.get_stock_historical_data(stock=stock,
                                        country='South Korea')
		check_result = True
	except:
		check_result = False

	return check_result