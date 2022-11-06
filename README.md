# Smart_Marksheet_Scanner

## About

Data collection and acquisition has been a problem for many organizations.
During COVID and post COVID period, one of the most affected sectors is
education. And with this increase in challenges, the main issue faced by
many organizations is data archiving and management. 

We have realized this problem and have decided to come up with a solution
which automate the entire process of data acquisition from the marksheet.
Using OCR model, it can read any marksheet pdf with ease and store it in
the database with very great accuracy and efficiency.




## Approach

1. We will be taking the pdf format uploaded by the user and convert it into an image.
2. That image will be processed by an OCR module which will find the text inside the given image.
3. It will then add the unstructured text into a list.
4. Then, the processing module will process and analyse the unstructured text into structured text.
5. In the structured text, the module will find the subject and its corresponding marks,
6. Then it will return the output in JSON format which will be sent by API to the database.




## Built With


* Python
* OCR
* Firebase
* React
* HTML/CSS
* JavaScript




## Getting Started

### Installation
To run this project locally, open this project in Pycharm IDE and install all the dependencies.

### Giving PATH
In `main.py` file, give appropriate path to PATH variable.

### Run
Run the main.py file and it will start running on local machine.




## Usage

1. Select GSEB or CBSE as per your choice.

2. Upload the marksheet.

3. Click on Submit button.

4. After few seconds, you will be able to see marks output 
