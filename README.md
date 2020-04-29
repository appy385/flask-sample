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
$ python application.py
-----------OR------------------------
$ export FLASK_APP=application.py
$ flask run
```

## Deploy Flask application with AWS Elastick Beanstalk 

In my setup process, `awscli` and `awsebcli` are already installed inside Python Virtual Environment `venv` using `requiremnets.txt` file. For sake of compeletion these are the steps:-

Install `awscli` and  `awsebcli` library to interact and manage your EB service on AWS
```
$ pip install awscli
$ pip install awsebcli
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


### Initialize the Elastic Beanstalk interface

Create a new KeyPair if you don't have one. Key-pair is required to setup your AWS beanstalk environment with ssh client.
 
 #### Steps to create Key-pair
 
  > Note: key-pair should belong to the same region as your AWS Elastick beanstalk environment. 
  
 Open the Amazon EC2 console at [https://console.aws.amazon.com/ec2/]. Select the region in the navigation pane, choose **Key Pairs**.Choose **Create key pair**. Download the .pem file. Keep it safe. This file contains your private-key.

 
> Note:
> 1. Before running this command make sure that you have **key-pair** ready if you want to setup SSH client for your instance 
> 2. Select python 3.6 not 3.7 . Initializing EC2 instance fails on python 3.7 Amazon linux system.

Now, Initialize the Elastic Beanstalk interface
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

### Create SSL certificate with ACM

You can get your SSL certificate for free at AWS services. Open `Certificate Manager` from AWS services and select the same region you have chosen for your EB environmemnt.
- Click on **Request a certificate** button and go with the default option **public certificate**.
- Add your domain name and click **Next**.
- Choose **DNS validation** to validate that you are the owner of the domain.
- Adding **Tag** not required, click on  **Review** and then click on **Confirm Request**.

Request for validation will be displayed as `Pending`.Certificate will be issued only after verification via DNS is done successfully.

- To verify via DNS, you need to add the CNAME record in your `Route53` under your hosted zone with your domain name.
- This step can be completed from `Certificate Manager` itself. Simply click on the **create record in Route 53** button to the CNAME record.

If you have done everything right then within 5–10 mins the status of certificate will be changed to **issued**.

### Apply the newly created SSL Certificate to Application Load Balancer.

In order to make HTTPS request we need to add this SSL certificate to the load balancer.

- Navigate to the Configuration Tab of your Elastic Beanstalk App. Click on **Edit** button of Load Balancer.
- Add listener to the load balancer with following details and assign the newly created SSL certificate.
```
Listener Port: 443
Listener Protocol: HTTPS
Instance Port: 80
Instance Protocol: HTTP
```
**Apply** these changes. Once completeled, navigate to https://yourdomain and you should see your site served through HTTPS.



















References
1. http://amunategui.github.io/aws-beanstalk/
2. https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
3. https://medium.com/analytics-vidhya/tutorial-how-to-deploy-an-angular-app-with-a-free-domain-and-ssl-to-aws-s3-and-cloudfront-d0143de53d2d
4. https://medium.com/@jameshamann/configuring-your-elastic-beanstalk-app-for-ssl-9065ca091f49








 
