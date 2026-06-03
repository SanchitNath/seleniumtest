# Create a virtual environment
```bash
  python3 -m venv venv
  source venv/bin/activate
```

# Now install your packages
```bash
  pip install selenium pytest pytest-html pytest-xdist
```

# To install requirements from a file
```bash
  pip install -r requirements.txt
```

# To run tests
```bash
  pytest -m marker_name
```

# To run tests in parallel
```bash
  pytest -m marker_name -n auto
```

Execute via test name:
```bash
  pytest -k  "test_invalid_login"
```

Rerun failed tests again after completion of current state:
```bash
  pytest --lf
```

# To generate allure report
```bash
  pip install allure-pytest
  pytest --alluredir=reports
  allure serve reports/ which generates report to temp directory and start a web server 127.0.0.1:1234
```

# To remove reports, screenshots, and logs
```bash
  rm -rf reports screenshots logs
```

# To install docker
```bash
  docker --version
  docker-compose --version
```

# To start containers as per docker-compose.yaml
```bash
  docker-compose up -d
```

# To create and start a container from an image
```bash
  docker run -d -p 8080:80 nginx
```

# To take ss and add it in allure report
```bash
  allure.attach(driver.get_screenshot_as_png(), name='ss', attachment_type=allure.attachment_type.PNG)
```

# pytest.ini has settings of pytest
```
* pythonpath=.
loads all file at once, so that import doesn't fail

* What -s does
    without -s, print statements aren't shown if the test passes
    When you add -s to your addopts in pytest.ini, you are telling pytest to disable output capturing.
    Real-time output: See print() statements and logs immediately as they happen, even if the test passes.
    Debugging: It is essential for debugging because it allows you to see the state of your variables ( 
    like print(url)) while the test is running.
```