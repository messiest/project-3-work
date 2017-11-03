# Determinants of Reddit Post Engagement
## DSI-6 Project 3

### Executive Summary
It’s fascinating to find what catches the eye of a reader.
With the glut of information in the social media age, understanding what grabs the attention of a user is important.
What is far more important though, is understanding what gets a user to engage with the content.
In an attempt to understand this, I have collected information from more than 2.5 million posts on the link sharing site Reddit.
From this I constructed a model, a Random Forest, that can predict whether a post will be within the top 10% comments with 90% accuracy.
In doing so though, a greater area of research was illuminated.
As we work to understand more complex social behavior, the tools with which we do this become more complex as well.
This effort highlighted the role that interpretability plays in prediction.
While we may be able to predict a top post with incredibly high accuracy, it is largely impossible to understand what leads to such high engagement. 
The easily interpreted decision tree grows into a dense jungle of a random forest, east of understanding is easily lost in the undergrowth.

### Unerstanding the Workflow
To collect data, run the python program `reddit_scrape.py`.
The data collected here will be found in the directory, `raw_data/`.
After this has completed, run the program found in the iPython notebook titled `clean-data.ipynb`.
This will produce a cleaned version of the data in the folder `cleaned_data/`.
From this run the file `process_data.py`, to build the natural language processing.
This will complete the data preparation.

To then perform the analysis, run the programs found in the directory `models`
This will build a fitted model, corresponding to the name of the file, and save it in the `jar/` directory as a serialized `pickle` object (`pickle`, `jar/`, get it??? hohoho).
To then perform the analysis, open the jupyter notebook, in the `notebooks/` directory, corresponding to the model.
Running the notebook will produce a report of the model's accuracy, in the notebook itself.
