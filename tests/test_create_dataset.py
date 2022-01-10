import requests


def test_label_endpoint():
    endpoint = "http://127.0.0.1:8000/label/mask"
    body = dict(
        video_path="/Users/ppcorrea/RMCLabs/SAFE/DVEN/dev/safe-trainer/create-dataset/sample_video.webm"
        )
    r = requests.post(endpoint, json=body)
    assert r.status_code == 200