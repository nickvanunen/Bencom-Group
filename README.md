1. Clone this repository.

2. Install necessary packages:
```
pip install -r requirements.txt
```
3. Install tkinter (for the visual version (applicatie_gui.py)):
```
sudo apt-get install python3-tk
```

4. Run the "ophalen_leveranciers.py" to get a .txt file which contains all the energieleveranciers (to run this daily we would recommend to use a cronjob):
```
python3 ophalen_leveranciers.py
```

5. Run the terminal OR Graphical User Interface version:
```
python3 applicatie_terminal.py
```
```
python3 applicatie_gui.py
```
