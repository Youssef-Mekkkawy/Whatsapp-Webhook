# Whatsapp Webhook.

## Simple Webhook Using Python.

## (1)- Install Requirements.

```powershell
pip install -r requirements
```

## (2)- Import Modules Needs For This Projects.

```python
import os
import json
from dotenv import load_dotenv
from flask import Flask, request
```

## (3)- Create File Name {.env} To Store Your Token & Secret Key.

> - [ ]  Create File named .env.
> 
> - [ ]  Add Some Variables.
>   
>   1. Access_Token=Your Access Token.
>   
>   2. Secret_key =Your Secret Key Can be Any Thing But. Try Choose Strong Password Example:- rup87-cn6s-kl9a-0scz-qey6ozbxmb.
>      
>      
>      
>      

## Need ngrok. You need to Googling it To Know To use it if Not Know. Website:- https://ngrok.com



## To Read {.ENV} File.

```python
load_dotenv(".env")
Access_Token = os.getenv('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('SECRET_KEY')
Authorization = os.getenv('Authorization')
```












