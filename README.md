Must Requirements for hosting flask application using AWS beanstalk
```
- Main file name application.py
- Name inside application.py should be application = Flask(name)
- Requirement file is important for AWS beanstalk to know which dependencies need to be installed while deployment
```
Setup to host Flask Sample app on AWS beanstalk 

```
$ git clone <url>
```
Setup python Virtual environment 
 
> Note: Use pip3 and python3 if your default configuration is not python3.6 or above

 Virtual environments are independent groups of Python libraries, one for each project.Python 3 comes bundled with the <venv> module to create virtual environments.
 Create Python environment with name `venv`.Because .gitignore specifies `venv`
  
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

In my setup awscli is installed inside virtual environment not globally in system

```
$ pip install awscli

```
For the first time user of AWS, to create Your First IAM Admin User and Group for Elastic Beanstalk. Fill  `Access type: Programmatic access` and assign it the `policy name: AdministrationAccess` .Download the credetials.csv and use this command to configure your credentials.

```
$ aws configure
```

Install the `awsebcli` library to interact and manage our EB service on AWS
```
$ pip install awsebcli

```
Initialize the Elastic Bean interface
```
 Note: Create a new KeyPair or select an existing one according to the region you have selected.
```
Command:
```
$ eb init -i
```

Next you need to create your EB (use a unique name). This will zip up the data and upload it to the AWS cloud
```
$ eb create AWSFlaskSample

```
You should get a success message if all goes well.Then you can simply use the `eb open` command to view the flask application working

```
$ eb open AWSFlaskSample

 ```
 
 If you get failure message then you can checkout error logs with
 
 ```
$ eb logs
```

How to deploy updates in application
```
$ eb deploy AWSFlaskSample
```

> Note:  if git is installed, EB CLI uses the git archive command to create a .zip file from the contents of the most recent git commit command.
However, when .ebignore is present in your project directory, the EB CLI doesn't use git commands and semantics to create your source bundle. 
This means that EB CLI ignores files specified in .ebignore, and includes all other files. In particular, it includes uncommitted source files.






 
