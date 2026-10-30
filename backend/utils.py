# backend/utils.py
import urllib.parse

def generate_maps_url(location_name: str, city: str) -> str:
    """
    Constructs a zero-auth Google Maps Search URL.
    Takes a location name and city, URL-encodes them, and formats the link.
    """
    query = f"{location_name} {city}"
    encoded_query = urllib.parse.quote(query)
    maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_query}"
    
    return maps_url


def generate_calendar_url(event_title: str = "Digital Detox", location: str = "") -> str:
    """
    Constructs a zero-auth Google Calendar Event Template URL.
    Blocks out a generic 2-hour window for a screen-free session.
    """
    encoded_title = urllib.parse.quote(event_title)
    encoded_location = urllib.parse.quote(location)
    
    cal_url = (
        f"https://calendar.google.com/calendar/render?action=TEMPLATE"
        f"&text={encoded_title}"
        f"&details=Take+a+break+from+the+screen.+Enjoy+your+offline+time."
        f"&location={encoded_location}"
        f"&dates=20261027T180000Z/20261027T200000Z"
    )
    
    return cal_url