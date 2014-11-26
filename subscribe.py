#!/usr/bin/env python

import basket
import click
import requests


BASKET_URLS = {
    'dev': 'https://basket-dev.allizom.org',
    'stage': 'https://basket.allizom.org',
    'prod': 'https://basket.mozilla.org',
}
BASKET_TIMEOUT = 10


def request(environ, action, data=None, token=None, params=None, headers=None):
    """Call the basket API with the supplied http method and data."""
    url = BASKET_URLS[environ]

    # newsletters should be comma-delimited
    if data and 'newsletters' in data:
        if not isinstance(data['newsletters'], basestring):
            data['newsletters'] = ','.join(data['newsletters'])

    try:
        res = requests.request('post',
                               '{0}/news/{1}/'.format(url, action),
                               data=data,
                               params=params,
                               headers=headers,
                               timeout=BASKET_TIMEOUT)
    except requests.exceptions.ConnectionError:
        raise basket.BasketNetworkException("Error connecting to basket")
    except requests.exceptions.Timeout:
        raise basket.BasketNetworkException("Timeout connecting to basket")
    return basket.base.parse_response(res)


@click.command()
@click.argument('email')
@click.argument('newsletter')
@click.option('--env', type=click.Choice(['dev', 'stage', 'prod']), default='dev',
              help='Instance to use. Default is dev.')
@click.option('--lang', default='en')
def cli(email, newsletter, env, lang):
    click.echo('Sending request to {0}...'.format(env))
    try:
        resp = request(env, 'subscribe', {
            'newsletters': newsletter,
            'email': email,
            'lang': lang,
        })
    except basket.BasketException as e:
        click.secho('ERROR {0.code}: {0.desc}'.format(e), fg='red', bold=True)
    else:
        click.secho(str(resp), fg='green')


if __name__ == '__main__':
    cli()
