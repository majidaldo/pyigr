try:
    from icecream import ic
    _ = globals()
    _['ic'] = ic
except ImportError: pass