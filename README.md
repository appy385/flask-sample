# Setup to deploy Flask Sample app on AWS beanstalk with a free domain, SSL certificate and AWS Code Pipeline 


Must Requirements for hosting flask application using AWS beanstalk
```
1. Main python file name should be application.py
2. Name inside application.py should be application = Flask(name)
3. Requirements.txt file is important for AWS beanstalk to know which dependencies need to be installed while deployment
```

## Setup Flask Sample Appliation

Clone the repository

```
$ git clone https://github.com/appy385/flask-sample.git
```
Setup python Virtual environment 
 
> Note: Use pip3 and python3 if your default configuration is not python3.6 or above

 Virtual environments are independent groups of Python libraries, one for each project.Python 3 comes bundled with the <venv> module to create virtual environments.
Create Python environment with name `venv`. Because .gitignore specifies `venv`
  
  ```
$ python -m venv venv
  
  ```
  Before you work on your project, activate the corresponding environment:
  ```
$ source venv/bin/activate
```
Now, install dependencies from requirement file ` requirements.txt`

```
$ pip install -r requirements.txt
```

Your Flask setup is ready.To check your flask application is running successfully. Run your flask application in local environment. Make sure your python virtual environment is activate.
```
$ export FLASK_APP=application.py
$ flask run
```

## Deploy Flask application with AWS Elastick Beanstalk 

In my setup process, `awscli` and `awsebcli` are installed inside Python Virtual Environment not globally

```
$ pip install awscli

```
For the first time user of AWS, create Your First IAM Admin User and Group to use AWS services. Fill  `Access type: Programmatic access` and assign it the `policy name: AdministrationAccess`.Download the credetials.csv and use the command below to configure your credentials.

```
$ aws configure
```
Alternatively deactivate your environment and go to  ~/.aws/config file to configure your credentials. 
```
$ cd .aws
$ sudo vim credentials

```
Install the `awsebcli` library to interact and manage your EB service on AWS
```
$ pip install awsebcli

```
Initialize the Elastic Bean interface
```
 Note: 
 1. Select python 3.6 not 3.7 . Initializing EC2 instance fails on 3.7 Amazon linux system.
 2. Create a new KeyPair or select an existing one according to the region you have selected in eb initialisation.
 3. Go to AWS EC2 to create new key-pair.
 4. Key-pair is required to link your AWS beanstalk environment with ssh client.
 5. key-pair should belong to the same region you have chosen for AWS beanstalk environment. 
 6. Download the <key-pair>.pem file. Keep it safe.
```
Before running this command make sure the above prerequisites is completed:
```
$ eb init -i
```

Next, you need to create your EB (use a unique name). This will zip up the data and upload it to the AWS cloud
```
$ eb create AWSFlaskSample

```
You should get a success message if all goes well.Then you can simply use the `eb open` command to view the flask application working.Congratulations! the flask application has been deployed to AWS Elastick Beanstalk successfully.

```
$ eb open AWSFlaskSample

 ```
 
 If you get a failure message then you can checkout error logs with
 
 ```
$ eb logs
```

### How to deploy updates in flask application
```
$ eb deploy AWSFlaskSample
```

> Note:  if git is installed, EB CLI uses the git archive command to create a .zip file from the contents of the most recent git commit command.
However, when .ebignore is present in your project directory, the EB CLI doesn't use git commands and semantics to create your source bundle. 
This means that EB CLI ignores files specified in .ebignore, and includes all other files. In particular, it includes uncommitted source files.


## Setup continuous deployment pipeline using AWS Elastick Beanstalk, Github and Code Pipeline

Follow the link given below:-
https://aws.amazon.com/getting-started/tutorials/continuous-deployment-pipeline/


## Deploy Flask application with free domain and SSL certifcate

### Get Free domain

Get a free domain from [www.freenom.com.] 
Enter the domain name of your choice. If you want the domain for free you can only select one of these .ml, .tk, .cf, .ga, .gq . When you checkout make sure you select 12 Months @ FREE. 

> Note: After checkout, it will ask for your email address. Make sure you use sign up with new email address. Otherwise, it will not give you the new domain name. Use this to get random email address https://temp-mail.org/en/ and this for address generation https://www.fakeaddressgenerator.com/usa_address_generator.

To verify free domain is assigned to you, go to Navigation Tab **Services > MyDomains**. If there is an entry with the chosen  domain name then domain is registered to you successfully.


### Create an Alias Record

Next, you need to point domain name to your EB environment URL. URL can be found on Elastic Beanstalk Dashboard.
Open `Route53` from AWS services and create a hosted zone.

- Create a hosted zone with your domain name and set type as a “public hosted zone”.Leave the comment box as it is.
- You will find 4 name servers, copy it.
- Go to your freenom account then click on Navigation Tab **services**  > **mydomains** .Click on **Manage domain** and from **management tools** drop-down > click on **nameservers** and paste the 4 AWS name servers on **custom nameservers** option.
- Visit this site [www.dnschecker.org/#NS] and enter your domain if everything is right then you should see your AWS name servers within 5–10min.

### Get SSL certificate













References
1. http://amunategui.github.io/aws-beanstalk/
2. https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
3. https://medium.com/analytics-vidhya/tutorial-how-to-deploy-an-angular-app-with-a-free-domain-and-ssl-to-aws-s3-and-cloudfront-d0143de53d2d
4. https://medium.com/@jameshamann/configuring-your-elastic-beanstalk-app-for-ssl-9065ca091f49








 
