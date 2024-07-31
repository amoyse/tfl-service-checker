import requests

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
                'status': closure_text
            })
    return issues


def main():
    issues = check_tube_status()
    
    if len(issues) > 0:
        message = "Tube Line Issues:\n"
        for issue in issues:
            message += f"{issue['line']}: {issue['status']}\n"


if __name__ == "__main__":
    main()
