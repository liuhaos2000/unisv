from django.contrib import admin
from .models import (
    Todo, Tag,
    BacktestRecord, BacktestStrategy, StockSelectionStrategy,
    Stock, StockDailyData, StockFinancialReport,
    User, Watchlist, WatchlistStock
)


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active', 'created_at')
    search_fields = ('title', 'body')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    search_fields = ('name',)
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BacktestRecord)
class BacktestRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'strategy', 'start_date', 'end_date', 'return_rate', 'status', 'created_at')
    search_fields = ('status', 'strategy__name')
    list_filter = ('status', 'start_date', 'end_date')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BacktestStrategy)
class BacktestStrategyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'strategy_class', 'created_at')
    search_fields = ('name', 'description', 'strategy_class')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StockSelectionStrategy)
class StockSelectionStrategyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'class_name', 'created_at')
    search_fields = ('name', 'description', 'class_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'price', 'market', 'industry', 'created_at')
    search_fields = ('code', 'name', 'market', 'industry', 'sector')
    list_filter = ('market', 'industry', 'sector', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StockDailyData)
class StockDailyDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock_code', 'trade_date', 'open_price', 'close_price', 'volume', 'created_at')
    search_fields = ('stock_code',)
    list_filter = ('trade_date', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StockFinancialReport)
class StockFinancialReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock_code', 'stock_name', 'report_date', 'quarter', 'eps', 'net_profit', 'created_at')
    search_fields = ('stock_code', 'stock_name', 'industry')
    list_filter = ('quarter', 'report_date', 'industry', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'created_at')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('created_at', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'name', 'created_at')
    search_fields = ('name', 'user_id')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WatchlistStock)
class WatchlistStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'watchlist', 'stock_code', 'added_at', 'created_at')
    search_fields = ('stock_code', 'watchlist__name')
    list_filter = ('added_at', 'created_at')
    readonly_fields = ('created_at', 'updated_at')