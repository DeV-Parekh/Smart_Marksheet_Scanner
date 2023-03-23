# Smart Marksheet Scanner

## About

Data collection and acquisition has been a problem for many organizations.
During COVID and post COVID period, one of the most affected sectors is
education. And with this increase in challenges, the main issue faced by
many organizations is data archiving and management. 

We have realized this problem and have decided to come up with a solution
which automates the entire process of data acquisition from the marksheet.
Using OCR model, it can read most marksheet of GSEB and CBSE with ease and store it in
the database with great accuracy and efficiency.




## Approach

1. We will be taking the pdf format uploaded by the user and convert it into an image.
2. That image will be processed by  EasyOCR module which will find the text inside the given image.
3. It will then add the unstructured text into a list.
4. Then, the processing module will process and analyse the unstructured text into structured text.
5. In the structured text, the module will find the subject and its corresponding marks and will display the result to the website.
6. Finally, it will store all the results into the database.




## Getting Started

### Dependencies
* EasyOCR
* Flask
* pdf2image
* poppler

### Installation
To run this project locally, open this project in any IDE of your choice and install all the dependencies.

### Giving PATH
In `main.py` file, give appropriate path to PATH variable.

### Run
Run the main.py file and it will start running on local machine.



## Usage

1. Select GSEB or CBSE as per your choice.

2. Upload the marksheet.

3. Click on Submit button.

4. After few seconds, you will be able to see marks output 
