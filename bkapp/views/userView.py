from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.watchlists import Watchlist
from ..models.watchlist_stocks import WatchlistStock


@api_view(['GET'])
def get_user_first_stock(request):
    """Get all stock codes from the first watchlist of a user.
    
    Parameters:
        openid: User's openid (query parameter)
    
    Returns:
        {
            "code": 0
            "message": "success",
            "data": [
                {"stock_code": "AAPL", "added_at": "2025-11-20T10:30:00Z"},
                {"stock_code": "MSFT", "added_at": "2025-11-20T10:35:00Z"}
            ]
        }
    """
    #openid = request.query_params.get('openid')
    openid = "111"
    
    if not openid:
        return Response({
            "code": -1,
            "message": "openid parameter is required"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Get the first watchlist for this openid
        watchlist = Watchlist.objects.filter(openid=openid).first()
        
        if not watchlist:
            return Response({
                "code": 1,
                "message": "No watchlist found for this openid",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get all stocks in this watchlist
        stocks = WatchlistStock.objects.filter(watchlist=watchlist)
        
        if not stocks.exists():
            return Response({
                "code": 2,
                "message": "No stocks found in this watchlist",
                "data": []
            }, status=status.HTTP_200_OK)
        
        # Build response data
        stocks_code = []
        for stock in stocks:
            stocks_code.append({
                "stock_code": stock.stock_code,
                "added_at": stock.added_at.isoformat() if stock.added_at else None
            })
        
        stocks_data = get_stocks_from_codes(stocks_code)
        
        return Response({
            "code": 0,
            "message": "success",
            "data": stocks_data
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "code": 500,
            "message": f"Error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





def get_stocks_from_codes(stock_codes):
    logging.info(f"Fetching stock data for: {stock_codes}")

    stock_data = []
    all_stock_info = ak.stock_zh_a_spot_em()

    for code in stock_codes:
        try:
            # 从获取的所有股票数据中筛选目标股票
            stock_row = all_stock_info[all_stock_info['代码'] == code]
            if not stock_row.empty:
                stock_data.append({
                    "skId": code,
                    "skName": stock_row.iloc[0]['名称'],
                    "price": stock_row.iloc[0]['最新价'] if not pd.isna(stock_row.iloc[0]['最新价']) else 0,  # 处理 NaN
                    "movement": stock_row.iloc[0]['涨跌幅'] if not pd.isna(stock_row.iloc[0]['涨跌幅']) else 0  # 处理 NaN
                })
            else:
                logging.warning(f"Stock code {code} not found in all_stock_info")
        except Exception as e:
            logging.warning(f"Error processing data for {code}: {e}")

    return stock_data