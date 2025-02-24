# Project Title
Agoda trip flight unit test and flight search unit test
# Description
This test checks the round trip option in the flight tab and different features in the flight tab as well as navigating to the searched flights and prints them out 
# How/where to download your program
This program playwright and Python versions 3.10 and later. To run the test cases please follow these steps:
- Clone this repository
- Change root directory 
<cd path/to/file>
- Create a virtual environment if you have not done so
<python3 -m venv venv>
- Activate it on Mac using 
<source venv/bin/activate>
- Install requirements.txt packages in your venv
<pip install -r requirements.txt>

# Executing program
- Run  playwright install in IDE terminal to download the browser extension
<playwright install>
- Run pytest (-s prints out terminal output in detail and . runs tests in whole directory)
<pytest -s .>
- If you want to run individual test modules
<pytest path/to/file/filename.py>
- or even individual tests
<pytest path/to/file/filename.py::test_name>


# Contributors
Zaki Sabir Shaikh (zaki.sabir@arbisoft.com)




