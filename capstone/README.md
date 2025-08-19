# Capstone

## Specification

A sentiment analysis and visualizer tool for [New York Times (NYT) Opinion](https://www.nytimes.com/section/opinion) articles from [NYT APIs](https://developer.nytimes.com/apis). Built with Django on the back-end and JavaScript on the front-end.

Article fetching is supported with the [```pynytimes```](https://pynytimes.michadenheijer.com/) library. 

Sentiment analysis is supported with the [```nltk.sentiment.vader```](https://www.nltk.org/_modules/nltk/sentiment/vader.html) model.

Chart rendering is supported with the [Chart.js](https://www.chartjs.org/) library.

## Getting Started

To run this application:

1. Install [```pip```](https://pip.pypa.io/en/stable/installation/).
2. Clone this repository.
3. In your terminal, ```cd``` into the ```capstone``` directory.
4. Run ```touch .env``` to store environment variables.
5. Add [```API_KEY=your_nyt_api_key```](https://developer.nytimes.com/get-started) in your ```.env``` file.
6. Run ```pip install -r requirements.txt``` to install required Python packages.
7. Run ```python manage.py makemigrations sentiment``` to make migrations for ```sentiment``` app.
8. Run ```python manage.py migrate``` to apply migrations to your database.
9. Run ```python manage.py runserver``` and navigate to ```localhost``` in your browser.

## Demonstration

Demonstration: https://youtu.be/SEHLdOlhDn0
