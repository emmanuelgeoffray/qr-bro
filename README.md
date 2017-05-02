# QR bro

![](https://rawgit.com/soixantecircuits/qr-bro/master/recipes/qrcode-path.svg)

QR bro is a tool to generate QR codes in the [spacebro](https://github.com/spacebro/spacebro) galaxy.


## 🌍 Installation

```
pip install -r requirements.txt
```

or 

```
pip2.7 install -r requirements.txt
```

or 

```
sudo pip install -r requirements.txt
```

## ⚙ Configuration

You can edit the `settings.default.json` in the `settings` folder.

```
"service": {
    "spacebro":{
      "host": "spacebro.space",
      "port": 3333,
      "clientName": "qr-bro",
      "channelName": "qr-bro",
      "inputMessage": "new-media-for-qr-bro",
      "outputMessage": "new-media-from-qr-bro"
    }
},
"recipe": "recipes/qrcode-path.svg",
"folder":{
  "output": "/tmp/qr-bro"
}
```

## 👋 Usage

```
python qr-bro.py
```

```
python qr-bro.py --settings path/to/settings.json
```

```
python qr-bro.py -s path/to/settings.json
```

### help

`python qr-bro.py --help`

## 📦 Dependencies

- [qrcode](https://pypi.python.org/pypi/qrcode)
- [pathlib](https://pypi.python.org/pypi/pathlib/)
- [socketIO_client](https://pypi.python.org/pypi/socketIO-client)
- [Wand](http://docs.wand-py.org/en/0.4.4/)

## 🕳 Troubleshooting

- [ ] Awaiting ...

## ❤️ Contribute

Share your thoughts and enjoy!

## Result

![](https://rawgit.com/soixantecircuits/qr-bro/master/recipes/qrcode-path.svg)
