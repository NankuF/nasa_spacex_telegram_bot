import environs

env = environs.Env()
env.read_env()
NASA_API_KEY = env.str('NASA_API_KEY')

HEADERS = {'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}
