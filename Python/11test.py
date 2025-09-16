import yaml
jasur = str(input(": "))
info = {'user': jasur}
with open('data.yaml', 'w') as file:
    yaml.dump(info, file)

