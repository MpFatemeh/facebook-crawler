# Facebook crawler

2020 learning project: a Python crawler for profiles (education, work) and posts, built with Selenium and BeautifulSoup. Each crawled profile or post is published as a message to a RabbitMQ queue (`profile`, `post`) for downstream processing.

## Run

```sh
pip install selenium beautifulsoup4 lxml pika
```

Needs a local RabbitMQ on `localhost` and a Chrome WebDriver. Written against Facebook's 2020 page layout, so the selectors no longer match the current site.
