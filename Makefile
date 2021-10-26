win-clean:
	rm -r .wvenv

win-build:
	.\.wvenv\Scripts\pyinstaller.exe --distpath ../build/dist --workpath ../build --onedir -n twittergettweets

win-install:
	python -m venv .wvenv
	.\.wvenv\Scripts\python.exe -m pip install --upgrade pip
	.\.wvenv\Scripts\python.exe -m pip install --upgrade wheel
	.\.wvenv\Scripts\python.exe -m pip install -r .\requirements.txt
	"$(get-location)" > .\.wvenv\Lib\site-packages\twittergettweets.pth

win-run:
	.\.wvenv\Scripts\python.exe .\app.py
