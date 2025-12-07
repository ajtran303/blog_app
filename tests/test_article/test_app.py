import json
import pathlib

import pytest
from jsonschema import validate, RefResolver  # RefResolver is deprecated in v4.18.0

from blog.app import app
from blog.models import Article

@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def validate_payload(payload, schema_name):
    schemas_dir = str(
        f"{pathlib.Path(__file__).parent.absolute()}/schemas"
    )
    schema = json.loads(pathlib.Path(f"{schemas_dir}/{schema_name}").read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            "file://" + str(pathlib.Path(f"{schemas_dir}/{schema_name}").absolute()),
            schema
        )
    )

def test_create_article(client):
    data = {
        "author": "john@doe.com",
        "title": "New Article",
        "content": "Some extra awesome content"
    }
    response = client.post(
        "/create-article/",
        data=json.dumps(
            data
        ),
        content_type="application/json",
    )

    validate_payload(response.json, "Article.json")

def test_get_article(client):
    article = Article(
        author="jane@doe.com",
        title="New Article",
        content="Super extra awesome article"
    ).save()
    response = client.get(
        f"/article/{article.id}/",
        content_type="application/json",
    )

    validate_payload(response.json, "Article.json")

def test_list_articles(client):
    Article(
        author="jane@doe.com",
        title="New Article",
        content="Super extra awesome article"
    ).save()
    response = client.get(
        "/article-list/",
        content_type="application/json",
    )

    validate_payload(response.json, "ArticleList.json")


@pytest.mark.parametrize(
    "data",
    [
        {
            "author": "John Doe",
            "title": "New Article",
            "content": "Some extra awesome content"
        },
        {
            "author": "John Doe",
            "title": "New Article"
        },
        {
            "author": "John Doe",
            "title": None,
            "content": "Some extra awesome content"
        }
    ]
)
def test_create_article_bad_request(client, data):
    response = client.post(
        "/create-article/",
        data=json.dumps(
            data
        ),
        content_type="application/json",
    )

    assert response.status_code == 400
