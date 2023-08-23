"""kube-data-collector
"""

# Map signals to numerical values
signals = ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]
signal_num_map = {
    "Strong Buy": 2,
    "Buy": 1,
    "Hold": 0,
    "Sell": -1,
    "Strong Sell": -2,
}
