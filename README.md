## Test Locally

### Attention, if you have python installed on your local machine, check your python command running the code below: If this message is shown, please check your Python installation command not found: python

```bash
python3.12 --version
# or
python3 --version
# or 
python --version
```

### If one of these commands runs successfully, use it with your pip command like, e.g python3.12 runs successfully, your pip command should be implemented like this pip3.12 install..

- Select the test folder

```bash
cd test
```

- Create venv 

```bash
python -m venv venv
```

- Activate venv

```bash
source venv/bin/activate
```

- Install packages

```bash
pip install -r requirements.txt
```

- Setup environment variables: 

    - Copy ibmcloudVariables_env.txt to .env, fill in the credentials and source

    ```bash
    source ibmcloudVariables.env
    ```

- Get an example JSON log from watsonx Assistant's Log Webhook and name it params.json

- Run 

```bash
python main_test.py params.json
```