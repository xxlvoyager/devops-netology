import yaml
import io
with open("docker-compose.yml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)
with io.open('data.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data_loaded, outfile, default_flow_style=False, allow_unicode=True)
