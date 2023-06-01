import requests

x = requests.post(
    'http://127.0.0.1:8000/project-management/create_teams/',
    data={
        "Team": "Automation2",
        "Department": "Circuit and System Design",
        "Members": [
            "210113",
            "210601",
            "200710",
            "220813",
            "190503",
            "211105",
            "210115"
        ]
    }
)

print(x.text)