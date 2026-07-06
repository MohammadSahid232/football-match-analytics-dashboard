def format_rating(rating):
    """
    Format rating to a single decimal point string.
    """
    return f"{float(rating):.1f}"

def get_rating_color(rating):
    """
    Return a Bootstrap color class based on player/team rating.
    """
    rating = float(rating)
    if rating >= 7.5:
        return "success"
    elif rating >= 7.0:
        return "primary"
    elif rating >= 6.5:
        return "warning"
    else:
        return "danger"

def calculate_percentage(part, whole):
    """
    Calculate percentage safely.
    """
    if whole == 0:
        return 0.0
    return round((part / whole) * 100, 2)
