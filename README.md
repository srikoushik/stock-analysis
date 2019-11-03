# stock-analysis
A pthon3 command line tool which will analyse the entered stock name and return the mean, standard deviation, best buy date, best sell date and the profit.

Step 1: Create a virtual environment ```python3 -m venv ./env``` 

Step 2: Activate environment ```. ./env/bin/activate```

Step 3: Install the requirements ```pip install -r requirements.txt```

Step 4: Run the script ```python3 main.py ./StockData.csv```

![Stock Analysis Demo](https://media.giphy.com/media/dBm0tVZQYj3mBlVQSo/giphy.gif)

## What I would do in further iterations:

1. Showing the previous search of the stock when tapping up arrow.
2. Support for more date input formats.
3. Auto-completing stock names on tapping the Tab.
4. Non-interactive mode where the user can pass the stock name, start date and end date using ```options```.
