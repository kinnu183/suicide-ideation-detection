# suicide-ideation-detection

Data Collection:
The data [1] used for this study is borrowed from a previous study and publicly available on github as linked in [1]. The text in this dataset was crawled from both Reddit and Twitter with the reddit data scraped from the r/suicide_watch, r/depression for positive/suicidal labels and other non-related subreddits for the negative/non-suicidal labels; while the twitter data is fetched by crawling for suicidal words such as ‘end my life’, ‘commit suicide’ and others. This dataset (linked in [1] and named `more_data_3.csv` in the data folder) is what is used to train and validate the models  while the other dataset (named `data_full.csv` in the data folder) also scraped from reddit using the `reddit_scraper.py` script is used for the model testing phase.
The train dataset contains 11,338 total posts. 
The twitter scraper,`/web_app/app/stream.py` which is used to crawl tweets from twitter in near real-time for continuous predictions as prompted, uses a number of configuration keys that are confidential for each user's twitter developer account and therefore these are not provided for public view.
These configuration keys are `CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN` and `ACCESS_TOKEN_SECRET` and these allow access to the twitter API through one's twitter developer account.

Model training:
Workflow:
Data loading, preprocessing and analysis
Baseline model training (using the xgboost and logistic regression models)
Evaluation of baselines
Deep learning model training with threshold based label correction using the best performing baseline on the test set. The label correction approach was inspired by this research paper
We experimented with 3 different variations of deep learning architectures with pre-trained 300-dimension glove vectors (downloaded from the stanford-nlp github repository) to initialize the our word embedding layers;
A Multi-channel 1D-Convolution Neural Network for suicide intent classification:
This architecture comprises two embedding layers (channels), one static.i.e `trainable` parameter is False and the other layer dynamic,.i.e, trainable parameter is True.

For each of the two embedding layer types, 3 1-dimensional convolutional neural networks with either size 3, 4 or 5 kernels representing the number of ‘grams’ or words to consider for each batch input, similar to how the n_grams parameter works in the bag of words approaches like CountVectorizer(), are each stacked onto the embedding layers and a 1D max pooling layer and a flatten layer are stacked on top of each Convolution layer and then finally concatenated for both static and dynamic channels and then finally a concatenation layer for the concatenated results from both embedding channels is added to feed into a dropout and a final classification dense layer.

A Multi-channel 1D-Convolution Neural Network with Attention for suicide intent classification:
This architecture is similar to the one above except that instead of using maxpool and flatten layers, we apply attention layers and concatenate results from each of the attention layers to try to capture the different contexts from each of the convolution layers.

LSTM with Attention:
This architecture comprises a single bi-directional LSTM layer feeding into an attention layer and both stacked on top of an embedding layer initialized with pre-trained glove vectors.


Model testing/inference:
We use the F1_score metric as the main evaluation criteria for our models along with the accuracy metric since we have a binary classification task as per our problem formulation.
The loss function for the deep learning models is binary cross entropy loss and we apply this as well to evaluate and select between the various different model architecture types trained along with the evaluation metrics stated prior.

Ref:
[1] https://github.com/soumyajit4419/AI_For_Social_Good/blob/master/Dataset/mergedData.csv
