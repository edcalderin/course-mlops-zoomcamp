import httpx
from prefect import flow, task

@task(name='Fetch cat')
def fetch_cat_fact():
    cat_fact = httpx.get('https://f3-vyx5c2hfpq-ue.a.run.app')
    if cat_fact.status_code>=400:
        raise Exception()
    print(cat_fact.text)

@flow
def fetch():
    fetch_cat_fact()

if __name__=='__main__':
    fetch()