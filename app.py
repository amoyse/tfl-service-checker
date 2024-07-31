import os
import requests
import http.client
import urllib

LINES_TO_CHECK = ["elizabeth", "hammersmith-city"]

def check_tube_status():
    issues = []
    for line in LINES_TO_CHECK:
        response = requests.get(f"https://api.tfl.gov.uk/Line/{line}/Disruption")
        data = response.json()
        if len(data) > 0:
            closure_text = data[0].get('closureText')
            issues.append({
                'line': line,
                'status': closure_text,
                'details': data[0].get('description')
            })
    return issues

def send_notification(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": os.getenv("PUSHOVER_APP_TOKEN"),
                     "user": os.getenv("PUSHOVER_USER_KEY"),
                     "message": message,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()


def main():
    issues = check_tube_status()
    
    if len(issues) > 0:
        message = "Tube Line Issues:\n"
        for issue in issues:
            message += f"{issue['line']}: {issue['status']}\n"

        for issue in issues:
            if LINES_TO_CHECK[0] == issue['line']:
                message += f"\nLiz Details: {issue['details']}"
        message += "\nhttps://tfl.gov.uk/tube-dlr-overground/status/"
        send_notification(message)


if __name__ == "__main__":
    main()
