import requests

x = requests.post(
    'https://www.ulka.autos/project-management/create_teams/',
    data={
        "Team": "Automation",
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