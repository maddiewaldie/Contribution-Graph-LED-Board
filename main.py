import logins
import network
import requests
import time

from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN as DISPLAY

''' Variables '''
# API Request
endpointURL = 'https://api.github.com/graphql'
query = """
query($userName: String!) { 
  user(login: $userName) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
          }
        }
      }
    }
  }
}
"""
headers = {
    'User-Agent': 'maddiewaldie',
    'Authorization': f'Bearer {logins.githubAccessToken}',
    'Content-Type': 'application/json'
}
variables = {
    'userName': logins.githubUser
}

# Display
gu = GalacticUnicorn()
display = PicoGraphics(DISPLAY)
width = GalacticUnicorn.WIDTH
height = GalacticUnicorn.HEIGHT

''' Functions '''
# Connect to Wi-Fi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(logins.ssid, logins.password)
    while not wlan.isconnected():
        print('Waiting for connection...')
        time.sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

# Fetch contribution data
def getContributions():
    response = requests.post(
        endpointURL,
        headers=headers,
        json={'query': query, 'variables': variables}
    )

    if response.status_code != 200:
        raise Exception(f"Query failed to run with a {response.status_code}.")

    return response.json()

# Draw border around the LED board
def draw_border():
    for x in range(width):
        display.set_pen(display.create_pen(*(0, 0, 40)))
        display.pixel(x, 0)
        display.pixel(x, height - 1)
        display.set_pen(display.create_pen(*(20, 20, 20)))
        display.pixel(x, height - 2)
    
    for x in range(width - 1):
        display.set_pen(display.create_pen(*(20, 20, 20)))
        display.pixel(x + 9, height - 3)

    for y in range(height):
        display.set_pen(display.create_pen(*(0, 0, 40)))
        display.pixel(0, y)
        display.pixel(width - 1, y)

# Draw contribution graph on LED board
def draw_contribution_graph(contributions):
    display.set_backlight(1.0)
    display.clear()
    effective_width = width - 2
    effective_height = height - 2

    total_days = 365
    normalized_contributions = [0] * total_days
    for i, count in enumerate(contributions):
        normalized_contributions[i] = count

    r, g, b = 0, 0, 0
    for x in range(effective_width):
        for y in range(effective_height):
            index = y * effective_width + x
            if index < len(normalized_contributions):
                count = normalized_contributions[index]
                if count == 0:
                    r, g, b = 20, 20, 20  # Darker Gray
                elif count == 1:
                    r, g, b = 0, 0, 40  # Darker Blue
                elif count == 2:
                    r, g, b = 0, 32, 64  # Darker Light Blue
                elif count == 3:
                    r, g, b = 32, 0, 64  # Darker Purple
                elif count == 4:
                    r, g, b = 64, 0, 64  # Darker Magenta
                elif count == 5:
                    r, g, b = 64, 26, 45  # Darker Pink
                else:  # For contributions greater than 5
                    r, g, b = 64, 5, 37  # Darker Deep Pink

                display.set_pen(display.create_pen(r, g, b))
                display.pixel(x + 1, y + 1)

    draw_border()
    gu.update(display)

''' Main Code '''
def main():
    try:
        connect()
    except Exception as e:
        print(f"Failed to connect to Wi-Fi: {e}")
        return
    
    while True:
        if gu.is_pressed(GalacticUnicorn.SWITCH_A):
            try:
                print("Getting contributions")
                data = getContributions().get('data', {})
                contributions = data.get('user', {}).get('contributionsCollection', {}).get('contributionCalendar', {})
                weeks = contributions.get('weeks', [])
                
                daily_contributions = [0] * 365
                day_index = 0
                
                for week in weeks:
                    for day in week.get('contributionDays', []):
                        if day_index < len(daily_contributions):
                            daily_contributions[day_index] = day['contributionCount']
                        day_index += 1
                
                # print(f"Total Contributions: {contributions.get('totalContributions', 0)}")
                # for day in daily_contributions:
                #     print(f"Contributions: {day}")
                
                print("Drawing graph")
                draw_contribution_graph(daily_contributions)
            
            except Exception as e:
                print(f"Failed to get or display contributions: {e}")

if __name__ == "__main__":
    main()
