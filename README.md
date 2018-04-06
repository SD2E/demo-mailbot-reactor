# Mailbot

Send an email using the Mailgun API

## Deploy

1. Edit `reactor.rc` to set your Docker username or organization 
2. Configure `config.yml` with a Mailgun API endpoint
3. Acquire a Mailgun API key and put it in `secrets.json`
4. Run `abaco deploy`

```shell
abaco deploy
Sending build context to Docker daemon  20.48kB
Step 1/1 : FROM sd2e/reactor-base:python2
# Executing 4 build triggers
 ---> Using cache
 ---> Using cache
 ---> 9490e5e9e01e
Successfully built 9490e5e9e01e
Successfully tagged sd2e/mailbot:0.5.0
The push refers to repository [docker.io/sd2e/mailbot]
9c190bc81b55: Layer already exists 
eae6a401b788: Pushed 
0.5.0: digest: sha256:5deacc06d849fdd587483575d5b3e1d8d3e92a9e720db9026d7199f1eb808493 size: 5519
[INFO] Pausing to let Docker Hub register that the repo has been pushed
[INFO] Reading environment variables from secrets.json
Successfully deployed Actor with ID: mZjlepxY5eMe5
```

## Test

Edit the message in `test_actor_message.sh` to point to an email address you can receive message at.

```shell
cd tests
./test_actor_message.sh mZjlepxY5eMe5
Execution xLJMAolLxKOWy 
Wait .
Wait ..
 2 seconds
Logs for execution xLJMAolLxKOWy:
Status: 200
Body:   {
  "id": "<20180108231934.1.1C56D5CCF3903078@sd2e.org>",
  "message": "Queued. Thank you."
}
```
