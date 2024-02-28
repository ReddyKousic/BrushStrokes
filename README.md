<p align="center">
  <img src="https://axxndntrgpbdwsznupdx.supabase.co/storage/v1/object/public/Logo/BrushStrokes_200.jpeg" alt="Image" style="width: 150px;"/>
  
</p>

> [!NOTE]
> Everything is up-to-date.

# BrushStrokes API
Here is the full [Documentation](https://github.com/ReddyKousic/BrushStrokes/wiki) before you begin...

BrushStrokes API offers a seamless way to convert ordinary images into captivating paintings, effortlessly adding an artistic touch to your digital creations. Harness the power of this API to infuse your applications with the charm of traditional artistry, turning every pixel into a stroke of genius.

## For starters 
Firstly clone the Repo and change directory to the BrushStrokes folder.


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
