
<img src="https://axxndntrgpbdwsznupdx.supabase.co/storage/v1/object/public/Logo/BrushStrokes.jpeg" width="200" height="100" style="border-radius:70px;">

# BrushStrokes API
BrushStrokes API offers a seamless way to convert ordinary images into captivating paintings, effortlessly adding an artistic touch to your digital creations. Harness the power of this API to infuse your applications with the charm of traditional artistry, turning every pixel into a stroke of genius.

## For starters 
Firstly clone the Repo and change directory to the BrushStrokes folder.
<p>Click here for full<a href="https://www.notion.so/kousic/BrushStrokes-d28840c6aab04375ab63750819754d95?pvs=4"><button style="padding:5px;margin-left:10px;font-size:20px;border-radius:10px; border:none; font-weight:600; background-color:#dd8a1f;">Documentation</button></a>  .</p>
```bash

git clone https://github.com/ReddyKousic/BrushStrokes.git
cd BrushStrokes
```

Create a Python Virtual Environment for this project and activate it.
```bash
python -m venv BrushStrokesENV
./BrushStrokesENV/Scripts/activate


```

Next install the requirements.
```bash
pip install -r requirements.txt

```

Create an account in Supabase, create a new project and finally create a Storage bucket called `testbucket`.

And create a new file called `.env` in that file fill as below
```bash
SUPABASE_URL= <YOUR_SUPABASE_URL>
API_KEY= <YOUR-SERVICE_ROLE_API_KEY>

```
Start the server.
(Debug mode)
```bash
python main.py

```
I hope it runs, if not please open an issue.