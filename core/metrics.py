from prometheus_client import Counter

cache_hits = Counter(
    "stockflow_cache_hits_total",
    "Total number of cache hits",
    ["resource"],
)

cache_misses = Counter(
    "stockflow_cache_misses_total",
    "Total number of cache misses",
    ["resource"],
)

stock_movements = Counter(
    "stockflow_stock_movements_total",
    "Total number of stock movements",
    ["type"],
)
