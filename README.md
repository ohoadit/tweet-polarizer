# tweet-polarizer
Live twitter sentiment analysis based on a given search term 


1. You'll need to install the following libraries in a conda env or venv or globally on your PC

    -- tweepy for scraping tweets<br>
    -- afinn for getting the sentiments<br>
    -- confluent_kafka to stream tweets to kafka<br>
    -- socket for kafka connection<br>

2. Create a twitter developer account and get and paste your bearer_token where it is written YOUR_BEARER_TOKEN_GOES_HERE in stream_tweets.py and replace the search term accordingly.
3. Run zookeeper command: bin/zookeeper-server-start.sh config/zookeeper.properties
4. Start Kafka after a few seconds, once zookeeper is up and running using the command: bin/kafka-server-start.sh config/server.properties
5. Create a kafka topic named tweet-polarizer
6. Configure logstash pipeline as per logstash.config file and use the config as: bin/logstash -f config/logstash.conf
7. Create elastic search index named search-tweet_polarizer
8. I have used Elastic Cloud to save and view the data, you may configure it and add your cloud key in logstash config.
9. Run stream_tweets.py and visualize the data as per the requirement.
