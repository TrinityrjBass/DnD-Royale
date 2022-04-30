# DnD-Royale
An update to the DnD Encounter Simulator app with some extra features.



To start dev environment using VS Code, create bat file in battleRoyale folder and paste this inside :

CALL env\Scripts\activate
set FLASK_APP=DnD-Royale\newFlask\app.py
set FLASK_ENV=development
flask run

================================================

Call this .bat file from the terminal to start.

For debugging, create a config in the battleRoayale folder with the following configurations (replace {NAME} with your own configuration name) : 
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "{NAME}",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "DnD-Royale\\newFlask\\DnDRoyale\\__init__.py",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run"
            ],
            "jinja": true,
            "justMyCode": true
        }
    ]
}

================================================
NOTE : 
You do not need to run the .bat file in order to debug. Just run the "Run and Debug" with the configurations list above.
