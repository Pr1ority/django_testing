from news.forms import CommentForm


def test_news_count(client, home_url):
    response = client.get(home_url)
    news = response.context['object_list']
    news_count = news.count()
    assert news_count == len(news)


def test_news_order(client, news, home_url):
    response = client.get(home_url)
    news = response.context['object_list']
    all_dates = [news_item.date for news_item in news]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comments_order(client, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps


def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
