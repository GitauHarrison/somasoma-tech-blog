# somaSoma Tech Blog

![Somasoma Home Page](/app/static/img/somasoma_blog.png)

This is a simple tech blog. It features an admin who can remotely update the blog. Anonymous users can interact with the blog contents using the user forms in each blog post.

## Features

* Anonymous user can post comments
* Admin authentication and authorization
* Admin session management
* Database Management
* Pagination of some contents
* File Upload

## Tools Used

* Flask microframework
* Python for programming
* SQLite3 database (during development)
* Flask WTF forms
* Flask Bootstrap for styling and cross-browser responsiveness
* Moment.js for date formatting
* Gunicorn and Psycopg2 for live deployment

## Features Lacking

* Markdown support for blog posts
* Blog post editing
* Two-factor authentication
* Multi-upload of files

## Deployment

* [Somasoma on Heroku](https://somasoma-tech-blog.herokuapp.com/)

## License

* MIT

## Contributors

* See all [contributors here](https://github.com/GitauHarrison/somasoma-tech-blog/graphs/contributors)

## Run the Application Locally

1. Clone the project

```python
$ git clone git@github.com:GitauHarrison/somasoma-tech-blog.git
```

2. Move into the cloned directory

```python
$ cd somasoma-tech-blog
```

3. Create and activate a virtual environment

```python
$ mkvirtualenv venv # I am using virtualenvwrapper
```

4. Install project dependencies

```python
(venv)$ pip3 install -r requirements.txt
```

5. Update environment variables following the template seen in `.env.template`

6. Run the application

```python
(venv)$ flask run # from the top-level directory
```

7. See the application

```python
# Paste the following into a browser: http://127.0.0.1:5000/
```

8. Intersted in testing the locally running application on another device? Run the command below in your terminal:

```python
(venv)$ ngrok http 5000
```

NOTE:

You will see this output:

```python
ngrok by @inconshreveable                                                                (Ctrl+C to quit)
                                                                                                         
Session Status                online                                                                     
Session Expires               1 hour, 59 minutes                                                         
Version                       2.3.40                                                                     
Region                        United States (us)                                                         
Web Interface                 http://127.0.0.1:4040                                                      
Forwarding                    http://3472-197-237-0-37.ngrok.io -> http://localhost:5000                 
Forwarding                    https://3472-197-237-0-37.ngrok.io -> http://localhost:5000                
                                                                                                         
Connections                   ttl     opn     rt1     rt5     p50     p90                                
                              0       0       0.00    0.00    0.00    0.00 
```

There are two public URLs being mapped to localhost. These URLs begin with the word _Forwarding_.

```python
Forwarding                    http://3472-197-237-0-37.ngrok.io -> http://localhost:5000                 
Forwarding                    https://3472-197-237-0-37.ngrok.io -> http://localhost:5000
```

Paste, for example, "https://3472-197-237-0-37.ngrok.io" on another device such as your phone. You will be required to sign up for an ngrok account (if you haven't already) and install your authtoken.

9. Want to start ngrok when the server fires up? 

```python
Uncomment these lines in app/__init__.py (30 - 37)

# def start_ngrok():
    #     from pyngrok import ngrok

    #     url = ngrok.connect(5000)
    #     print('* Tunnel URL: *', url)

    # if current_app.config['START_NGROK']:
    #     start_ngrok()
```

_Note that if you uncomment these lines, you can skip step 8 above, because ngrok will start authomatically when you fire up the flask server_. You will see ngrok public URLs in your terminal.

## References

You can add the lacking features to your flask blog. Check out some of these resources to get started:

* [Learn how to add two-factor authentication to your Flask application here](https://github.com/GitauHarrison/notes/blob/master/two_factor_authentication/twilio_verify_2fa.md)
* [Learn how to integrate comment moderation to your flask blog](https://github.com/GitauHarrison/notes/blob/master/comment_moderation.md)
* [Add markdown support to your flask forms](https://github.com/GitauHarrison/notes/blob/master/handling_rich_text.md)
* [Testing your locally running flask application on another device](https://github.com/GitauHarrison/notes/blob/master/localhost_testing.md)

If you are just starting out in Flask, consider this:

* [Running your application in a flask server](https://github.com/GitauHarrison/notes/blob/master/start_flask_server.md)