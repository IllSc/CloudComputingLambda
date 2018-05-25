# Lambda for Cloud Computing Project

## What is this?
The `handler.hello` method fetches the credentials from DynamoDB, calls transport API with fetched credentials every 10 minutes (defined on the AWS Lambda dashboard) and put the result on the Elasticsearch.


## What should I do to develop?

### Create a Python virtual environment and instal
If you use anaconda create one with this command
```
conda create --name [name] python=3.6
```

Activate the environment by (for Windows)

```
activate [name]
```
or (for Linux)
```
source activate [name]
```

Install requirements with

```
pip install -r requirements.txt
```

### Install Serverless
Install serverless tool, make sure you have `npm` already

`npm install -g serverless`

We need an extra plugin for enabling external library for serverless

`npm install --save serverless-python-requirements`


