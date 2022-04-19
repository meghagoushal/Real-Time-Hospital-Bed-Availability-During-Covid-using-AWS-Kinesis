# Real-Time-Hospital-Bed-Availability-During-Covid-using-AWS-Kinesis

India is reporting more than 250,000 new COVID-19 cases a day in its worst phase of the pandemic. Hospitals are turning away patients and supplies of oxygen and medication are running short. In response, people are bypassing the conventional lines of communication and turning to Twitter to crowdsource help for oxygen cylinders, hospital beds and other requirements. People in need and those with information or resources share telephone numbers of volunteers, vendors who have oxygen cylinders or drugs, and details of which medical facility can take patients using hashtags like #COVIDSOS. Twitter is not as widely used in India as Facebook or WhatsApp but it is proving a more valuable tool to get pleas for help out in the coronavirus crisis, largely because of its "re-tweet" function that can quickly amplify a message through users' networks of contacts.

We created an analysis that will filter tweets containing keywords such as [ Urgently, beds required, bed, need, delhi] while also displaying the most up-to-date information on available beds from the https://coronabeds.jantasamvad.org/covid-info.js website.

Architecture Overview:

![Big Data Project Architecture](https://user-images.githubusercontent.com/78490598/164071868-4e25a635-7e54-4241-adb6-b2c236ee09ec.jpeg)


Prerequisites: (please read these carefully and do not jump ahead and start setting things up unless specifically called out)

AWS Account: In order to work on this project you'll need an AWS Account with access to create AWS IAM, S3, Kinesis, Elastic Search and API Kibana.

Steps: Step1: Create an AWS Account

Step2: Start an EC2 Instance The steps outlined in this tutorial assume that you are using an EC2 instance as the web server and tweet producer. (For detailed instructions, see Getting started with Amazon EC2 Linux instances.) -Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/

STEP:3 PUT PYTHON SCRIPT ON EC2 INSTANCE Connect to EC2 instance:

1)ssh -i WebLogsKeypair.pem userName@DNSpublicAddress 2)git clone https://github.com/gangotribiswal/Text-mining-on-Twitter-keyword-to-find-Covid-Hospital-Bed-availability/blob/main/Available_Beds_script.py 3)git clone https://github.com/gangotribiswal/Text-mining-on-Twitter-keyword-to-find-Covid-Hospital-Bed-availability/blob/main/twitter_script.ipynb

STEP:4 Create an Amazon Kinesis Data Firehose Delivery Stream

To create the Amazon Kinesis Data Firehose delivery stream: Open the Amazon Kinesis console at https://console.aws.amazon.com/kinesis.

For Destination, choose Amazon S3.

Step 3: Install and Configure the Amazon Kinesis Agent on the EC2 Instance

To install the agent, copy and paste the following command. sudo yum install –y aws-kinesis-agent

To configure the agent /etc/aws-kinesis/agent.json

sudo vi /etc/aws-kinesis/agent.json

Start the agent manually by issuing the following command: sudo service aws-kinesis-agent start

![ec2user](https://user-images.githubusercontent.com/78490598/164072002-999a9a69-255e-4d59-a412-4582c74d2ab0.png)


sudo service aws-kinesis-agent stop

Step 4: **Create an Amazon Elasticsearch Service Domain

https://console.aws.amazon.com/es.

Create a new domain

Step 5: Create a Second Amazon Kinesis Data Firehose Delivery Stream

-Open the Amazon Kinesis console at https://console.aws.amazon.com/kinesis. Create Delivery Stream.

For Destination, choose Amazon Elasticsearch Service.

-For Elasticsearch domain, choose the domain you created in Step 4.

-In the S3 backup section, for Backup mode, choose Failed Records Only.

Step 6: Create an Amazon Kinesis Data Analytics Application

Open the Amazon Kinesis Analytics console at https://console.aws.amazon.com/kinesisanalytics. Create new application. 
![KineticsAnalyticsPerform](https://user-images.githubusercontent.com/78490598/164072163-4c5a1e60-a475-4fe4-ba73-3e784b60ed9e.png)

CREATE OR REPLACE STREAM "DESTINATION_STREAM_NEW_001" ( Hospital_Name VARCHAR(255), Avg_Beds_Vacant REAL, Avg_Beds_Occupied REAL, Hospital_Type VARCHAR(32), Last_Updated VARCHAR(32), Total_Beds VARCHAR(8), Occupied Integer); CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "DESTINATION_STREAM_NEW_001" SELECT STREAM "name", avg("vacant") OVER W1 AS Avg_Beds_Vacant, avg("occupied") OVER W1 AS Avg_Beds_Occupied, "type", "last_updated_at", "total", "occupied" FROM "SOURCE_SQL_STREAM_001" WINDOW W1 AS ( PARTITION BY "name" RANGE INTERVAL '24' HOUR PRECEDING);

Twitter Analytics:

/**

Welcome to the SQL editor
=========================
The SQL code you write here will continuously transform your streaming data
when your application is running.
Get started by clicking "Add SQL from templates" or pull up the
documentation and start writing your own custom queries. / CREATE OR REPLACE STREAM "DESTINATION_SQL_STREAM" ( posted_at varchar(255), User_name varchar(255), Is_Retweet VARCHAR(8), Tweets VARCHAR(255), Count_Tweets Integer); CREATE OR REPLACE PUMP "STREAM_PUMP" AS INSERT INTO "DESTINATION_SQL_STREAM" SELECT STREAM "posted_at", "user_name", "is_retweet", "tweet_text", count() over W1 AS Count_Tweets FROM "SOURCE_SQL_STREAM_001" WINDOW W1 AS ( PARTITION BY "user_name" RANGE INTERVAL '1' HOUR PRECEDING);
Step 7: View the Aggregated Streaming Data 
![KibanaLogin](https://user-images.githubusercontent.com/78490598/164072221-67edd00d-64c3-464b-9947-49f1597a33b4.png)
