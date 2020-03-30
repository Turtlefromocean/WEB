from gensim.summarization.summarizer import summarize
from newspaper import Article


def get_summary(url, ratio):

    news = Article(url, language='ko')
    news.download()
    news.parse()

    return summarize(news.text, ratio=ratio)
