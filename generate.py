#!/usr/bin/env python3

import yaml
from pathlib import Path

this_dir = Path(__file__).absolute().parent

genrated_paths = set()
generated_lines = 0

for config_path in this_dir.glob("*.yaml"):
    config = yaml.load(config_path.open())
    apps = config['applications']
    defaults = config['defaults']

    for app_name, app_data in apps.items():

        data = {"app_name": app_name, **defaults, **app_data}

        # Handle one level of nested templating by doing final template
        for k in data:
            if isinstance(data[k], str):
                data[k] = data[k].format(**data)
        final = config["template"].format(**data)

        config_path = (this_dir / f"{app_name}.subdomain.conf.sample")
        print(f"Generating {config_path}")

        with config_path.open("wt") as fout:
            print(final, file=fout)

        genrated_paths.add(config_path)
        generated_lines += len(final.splitlines())

not_genrated_paths = [(len(path.open().read().splitlines()), path) for path in set(this_dir.glob("*.subdomain.conf.sample")) - genrated_paths]
not_genrated_lines = 0
for n_lines, path in sorted(not_genrated_paths):
    print(f"{n_lines} lines got generated from {path}")
    not_genrated_lines += n_lines

print(f"{generated_lines}/{generated_lines + not_genrated_lines} lines were generated, {not_genrated_lines} were not")
