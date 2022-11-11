# WalleeSlackBot

## What is Wallee?
Wallee is a chat bot that is used to conveniently retrieve information and update
information across systems and applications without ever having to leave
Slack.

Wallee is a program that is attempting to be more humanized in its speech outside
of its data gathering and manipulation efforts.

## Getting Started
This application uses python 3.9+

### Installing requirements
To begin development on this application it is best to use [ngrok](https://ngrok.com/) as that will expose the local development server to a domain that can be called back to another application.

>For example, if you are running on localhost:3000, how does another web application know to speak with your webserver?  It would need to be exposed and that could take some additional setup.  Thanks to [ngrok](https://ngrok.com/) it is done super quickly.

After installing ngrok please run the below command
```bash
ngrok http 3000
```

When it is running you should see an output similar to the below
```bash
Session Status                online
Session Expires               1 hour, 22 minutes
Version                       2.3.40
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://7914471e8fab.ngrok.io -> http://localhost:3000
Forwarding                    https://7914471e8fab.ngrok.io -> http://localhost:3000

Connections                   ttl     opn     rt1     rt5     p50     p90     
                              9       0       0.00    0.00    49.06   111.09  

HTTP Requests
-------------
```

```bash
pip install requirements.txt
```

### Running the application
```bash
python app.py
```

### Testing the application
```bash
# Be in the root of the project and run the below command
python -m unittest discover tests
```

Now that is settled please follow the documentation on how to continue this kind of set up in your own slack workspace.  The getting started documentation for [bolt](https://slack.dev/bolt-python/tutorial/getting-started), will go over the above again somewhat and will also show you how to connect the bot to Slack.

## Supported Chat Services
- Okta - User API (Limited Scope)
  - list
  - query
  - create
  - update

## Chat Service Protocol
> Any token in the below syntax format denoted with a ? means it may be optional in some cases.

    {verb} {identifier}? {param1}? {param2}?

### Syntax breakdown
* verb - The type of action to take place such as "list" and "create".  This concept is simalar to HTTP verbs.  
* identifier - The identifier supported right now is just email.  This identifier is used in requests on a specific resource. Very similar to REST.
* param - ancillary parameters for certain verbs.  These can be assignments `title=Director` or they can be fields when querying `title`.  When using the `Query` verb the params act as you would expect from a GraphQL query.

## Examples

Chat Query
```bash
query eddie@gmail.com lastName city title
```
Returns
```bash
Email: eddie@gmail.com
lastName: Hou
City: Mountain View
Title: Customer Success Engineer
```

Chat Query
```bash
query eddie@gmail.com lastName city
```
Returns
```bash
Email: eddie@gmail.com
lastName: Hou
City: Mountain View
```

Chat Query
```bash
list
```
Returns
```bash
Employees:
John Smith – jsmith@gmail.com
Eddie Hou – eddie@gmail.com
Joey Wheeler – jwheeler@gmail.com
```

Request a list of users
```bash
create example@gmail.com firstName=Ethan lastName=Xample department=Facilities
```
Returns
```bash
[Creation: Success]
Email: example@gmail.com
FirstName: Ethan
LastName: Xample
Department: Facilities
```

Chat Query
```bash
update jsmith@gmail.com title=Director of IT city=San Francisco
```
Returns
```bash
[Update: Success]
Email: jsmith@gmail.com
Title: Director of IT
City: San Francisco
```
# SlackBotOktaQueryService
# SlackBotOktaQueryService
# SlackBotOktaQueryService
