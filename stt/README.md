STT DeepSpeech 0.9.3
====================
Tensorflow 2.x

###### Venv: 
###### python3.9
```bash
python -m venv stt/.venv && \
source stt/.venv/bin/activate && \
pip install -U pip && \
pip install -r stt/requirements.txt
```

### Unpack:
###### apt-get install p7zip-full
```bash
7za x stt/model/archive/output_graph.scorer.7z.001 -ostt/model/
```
### Run:
```bash
source stt/.venv/bin/activate && \
export QUART_APP=stt.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5001
```
### Tests:
- ###### Test async:
    ````bash
    export QUART_APP=stt.app:app && \
    export QUART_ENV=development && \
    quart test-async
    ````
- ###### Test model:
    ```bash
    export QUART_APP=stt.app:app && \
    export QUART_ENV=development && \
    quart test-model
    ```  
### Docker:
```bash
docker build -t stt . && \
docker run -it --rm -p 5001:5001 stt && \
docker rmi stt --force
```
**Note:** 
Mozilla DeepSpeech-0.9.3
Custom Tensorflow-lite model used, you can train your own...
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]()
- ###### [Link](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3) GithubLink to DeepSpeech 0-9-3...
- ###### [Link](https://github.com/Martin1403/STT-Tensorflow1.15.x-DeepSpeech) Train DeepSpeech model with your own data...