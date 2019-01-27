# braillify
Converts images to braille patterns

## Requirements

Requires Python **3.6+** plus to run

## Running

To download the program, create a virtual enviorment and install required packages run this:

```
git clone https://github.com/Sateviss/braillify
cd braillify
python3 -m venv venv
./venv/bin/pip3 install -r requirements.txt
chmod +x braillify.py && ./braillify.py -h

```

You can run the sample by running this in your terminal
```
./braillify.py -i sample.jpg -s=0.9 -w 60 -t
```
## License
Distributed under GPL 3.0, see LICENSE.txt for more information
