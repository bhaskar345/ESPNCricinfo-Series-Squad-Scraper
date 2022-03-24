# ESPNCricinfo Series Squad Scraper

> This is an Api based scraper that scraps series squad from ESPNCricinfo site. 

## Setup Project :

>Clone the repository first.

>Create a virtual environment to install dependencies in and activate it.

>Install the dependencies.

>Now, navigate to project folder and run **python manage.py runserver** to run the project.

>Now, to scrape series squad Hit the endpoint `localhost:8000/scrape-squads/` with the `POST` request.

request body e.g :

```json
{
    "url":"https://www.espncricinfo.com/series/sri-lanka-in-india-2021-22-1278665"
}
```
>It will save squads into database and it will return saved series squads in response.

>You can get all the saved squads from the databse by hitting `localhost:8000/show-squads/` with the `GET` request.

>To get squads of perticular series, just hit `localhost:8000/show-squads/` with the `POST` request.

request body : 

```json
{
    "series":"Sri Lanka tour of India 2021/22"
}
