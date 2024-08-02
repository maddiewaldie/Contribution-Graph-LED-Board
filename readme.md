# Contribution Graph LED Board

This project displays GitHub contribution data on the [Galactic Unicorn LED matrix display](https://shop.pimoroni.com/products/space-unicorns?variant=40842033561683), fetching the contribution data from GitHub and visualizing it.

# Hardware Requirements

* [Galactic Unicorn LED matrix display](https://shop.pimoroni.com/products/space-unicorns?variant=40842033561683)
* Raspberry Pi Pico or similar microcontroller
* Wi-Fi connectivity

# Software Requirements

* [MicroPython](https://github.com/pimoroni/pimoroni-pico/releases/tag/v1.23.0-1) installed on your Raspberry Pi Pico-W
* [Galactic Unicorn Pimoroni MicroPython libraries](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/galactic_unicorn)

## Software Setup

1. **Clone the Repository**

```
git clone https://github.com/maddiewaldie/Contribution-Graph-LED-Board.git
```

2. **Configure Wi-Fi and GitHub Access:** Create a python file called `logins.py` and replace the following variables with your Wi-Fi and GitHub details:

```
ssid = 'YourSSID'
password = 'YourPassword'
githubUser = "YourGitHubUsername"
githubAccessToken = 'YourGitHubAccessToken'
```

3. Install MicroPython Libraries, following instructions [here](https://github.com/pimoroni/pimoroni-pico/blob/main/setting-up-micropython.md).
