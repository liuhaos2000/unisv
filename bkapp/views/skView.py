from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models.watchlists import Watchlist
from ..models.watchlist_stocks import WatchlistStock
import requests
from datetime import datetime, timedelta

@api_view(['GET'])
def get_sk_k(request):
    try:
        skId = request.query_params.get('skId')

        today = datetime.today()
        endDate = today.strftime('%Y%m%d')
        one_year_ago = today - timedelta(days=365)
        startDate = one_year_ago.strftime('%Y%m%d')

        url = f"http://api.momaapi.com/hsstock/history/{skId}/d/n/34E1BB45-2D59-4761-AB47-CEBC7A676A57?st={startDate}&et={endDate}&lt=300"
        response = requests.get(url)
        data = response.json()
        
        print(url)
        print(data)


        converted_data = []

        for item in data:
            # 提取日期并格式化
            date = datetime.strptime(item["t"], "%Y-%m-%d %H:%M:%S").strftime("%Y/%m/%d")
            
            # 提取其他数值
            open_price = item["o"]
            high_price = item["h"]
            low_price = item["l"]
            close_price = item["c"]
            
            # 将数据添加到转换后的列表中
            converted_data.append([date, open_price, high_price, low_price, close_price])


        return Response({
            "code": 0,
            "message": "success",
            "data": {
                "title":f"上证指数（{skId}）",
                "raw":converted_data
            }
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "code": 500,
            "message": f"Error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

