# Mailbot

This Reactor can send an email message using the [MailGun][1] API. It
demonstrates integrating with a third party service and using a *secrets*
file to avoid including sensitive information in the Reactor's Docker image.
It also demonstrates non-trivial usage of message validation via [JSON schema][2].
It reports progress via Reactors library logging interface as it constructs and
exits with appropriate status depending on the outcome.

It is built on*[sd2e/reactors:python2][3]* base should also be compatible
with *[sd2e/reactors:python3][3]*.

## Build (and Test)

* Run `git clone https://github.com/SD2E/demo-mailbot-reactor`
* Customize `reactor.rc`
    * Put own username or organization into `DOCKER_HUB_ORG`
* Copy `config.yml.sample  and customize it as `config.yml`
    * :star: Set `sender` to an address you control via Mailgun
* Obtain a Mailgun API key
    * Copy `secrets.json.sample` to `secrets.json` and put the key there as illustrated
* If you will run unit tests, create test data files
    * Copy and customize `tests/data/executions.json.sample` as `tests/data/executions.json`
    * Copy and customize `tests/data/tests-deployed-message.json.sample` as `tests/data/tests-deployed-message.json`

### Test Design

Reactors rely on environment variables injected a Docker environment by the
Abaco runtime, making testing a bit challenging. This repository illustrates
one possible solution. The general outline is:

1. Build the container
    * Leverages `abaco deploy -R` + configuration in [reactor.rc](reactor.rc)
2. Run `pytest -s` inside the container via `docker run`
    * Injects the LOCALONLY variable into the environment
    * Mounts `~/.agave/` as `/root/.agave` to inject API credentials
    * Mounts $PWD as the working directory in the container
    * Runs in a Linux user namespace to for improved security
3. Inject requisite environment variables via the pytest [monkeypatch][4] fixture
    * Values provided by the Abaco runtime (`_abaco_*`)
    * Values provided by the function caller
        * x-nonce
        * MSG
        * LOCALONLY
        * Environent variables sent as URL parameters
    * Agave API client credentials
4. Perform tests via `pytest`:
    * Ensure a Reactor() object can be bootstrapped
    * Inspect and validate the Reactor object's properties
    * Ensure necessary environment overrides are set (API keys, etc.)
    * Check validity of JSON message against a schema (optional)
    * Ensure the Reactor's main() runs as expected
    * Inspect and validate contents of log messages
    * Validate `sys.exit()` response

#### Pytest Configuration

The repository is set up to run pytests defined in `tests/` but also to review
the code for style and portability using [flake8][5]. A few low-criticality
errors and warnings set as ignored in `setup.cfg/[flake8]`. Flake8 can be
deactivated entirely by commenting out `--flake8` under in `[tool:pyest]`.

### Test via Makefile

At present, the easiest approach to testing is to use the Makefile, which
relies on the Abaco CLI, rational configuration of this repo, and some bundled
support scripts to set up the test environments.

```
make container       # Uses abaco-deploy -R to test building the container
make tests-local     # Exercise the Reactor without necessarily running it
make tests-reactor   # Simulate the Reactor running in the TACC.cloud
make tests-deployed  # Deploy this Reactor and send it a test message
make clean           # Remove cache residue from testing
```

For the `tests-reactor` and `tests-local` target, the default setting for
Reactor.local (`True`) can be set to `False` via `REACTOR_OVERRIDE_LOCAL=1`

```
make tests-local REACTOR_OVERRIDE_LOCAL=1
```

:star: If the Reactor relies on any feature particular to the Abaco environment,
such as actual filesystem mounts, it may fail in the local test context. Also,
if the messaage and/or parameters sent to the Reactor will instruct it to take
actions such as launching a job or sending an email, and if those functions are
gated behind the status of `Reactor.local`, those actions _will_ be triggered,
so be forewarned.

## Interfaces

If this was a more complicated Reactor, there might be extensive documentation
about the expected message contents, communications with other Reactors, and
descriptions of the code's outputs.

### Inbound Message(s)

A JSON message of the following form is expected. Only `to` is mandatory.

```json
{ "to": "noreply@tacc.cloud",
   "subject": "Hello, computer.",
   "body":"A keyboard... how quaint."
}
```

Message validation is defined in [message.jsonschema]. The fields  and formats
therein should be pretty self-explanatory.

### Actions

This Reactor does not expect to send messages to other Reactors or Apps.

### Output Message(s)

This Reactor posts to the Mailgun API.

## Example Build and Test Log

```shell
$ make tests-local REACTOR_OVERRIDE_LOCAL=1
rm -rf .hypothesis .pytest_cache __pycache__ */__pycache__
Sending build context to Docker daemon  67.07kB
Step 1/3 : FROM sd2e/reactors:python2-edge
# Executing 5 build triggers
 ---> Running in 6f97a709c219
You must give at least one requirement to install (see "pip help install")
Removing intermediate container 6f97a709c219
 ---> a51d2f833b4d
Step 2/3 : ADD message.jsonschema /message.jsonschema
 ---> 01d86f421c7b
Step 3/3 : ADD tests /
 ---> ff61c04e0573
Successfully built ff61c04e0573
Successfully tagged sd2e/mailbot:0.6.0
[INFO] Stopping deployment as this was only a dry run!
[INFO] Working directory: /Users/mwvaughn/src/SD2/demo-mailbot-reactor
[INFO] Not running under continous integration
platform linux2 -- Python 2.7.12, pytest-3.5.0, py-1.5.3, pluggy-0.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /mnt/ephemeral-01, inifile: setup.cfg
plugins: flake8-1.0.0, hypothesis-3.53.0
collected 10 items

tests/agavefixtures.py PASSED
tests/test_jsonschema_message.py PASSED
tests/test_jsonschema_message.py::test_validate_message_schema PASSED
tests/test_reactor_main.py PASSED
tests/test_reactor_main.py::test_test_data PASSED
tests/test_reactor_main.py::test_reactor_init PASSED
tests/test_reactor_main.py::test_reactor_read_config PASSED
tests/test_reactor_main.py::test_reactor_main PASSED
tests/test_reactor_main.py::test_reactor_invalid_message PASSED
tests/testdata.py PASSED
```

[1]: https://documentation.mailgun.com/en/latest/api_reference.html
[2]: http://json-schema.org/
[3]: https://hub.docker.com/r/sd2e/reactors/
[4]: https://docs.pytest.org/en/latest/monkeypatch.html
[5]: http://flake8.pycqa.org/en/latest/

