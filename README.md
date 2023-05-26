# Economica

### Requirements
    Python 3.10.5

### you need to install pyenv to use python versions
    choco install pyenv-win
    [System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
    [System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
    [System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
    [System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
    pyenv install {Número_Version_Python}
    pyenv local PYTHON_VERSION
    
### once pyenv is installed, the following should be done step by step
    .\.venv\Scripts\activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    

