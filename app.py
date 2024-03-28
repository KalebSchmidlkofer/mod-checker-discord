from subprocess import call

with open('run.sh', 'rb') as file:
    script = file.read()
rc = call(script, shell=True)