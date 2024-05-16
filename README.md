# Voice Typing App

The Voice Typing App is a Python-based application designed to convert speech to text in real-time. It utilizes the SpeechRecognition and pyttsx3 libraries for speech recognition and text-to-speech functionalities, respectively. The application features a simple GUI built with Tkinter, allowing users to start and stop voice typing with the click of a button.

## Features

- **Real-time Speech to Text**: Converts spoken words into text and types them wherever the cursor is positioned.
- **Voice Commands**: Supports special voice commands like "exit", "pause", "stop", "new line", and "next line" for control over typing.
- **Theme Switching**: Users can switch between light and dark themes for the application interface.
- **Simple GUI**: A user-friendly interface with buttons to control the application and display the current status (listening/not listening).

## Installation

Before running the application, ensure you have Python installed on your system. Then, install the required libraries using pip:

```bash
pip install -r requirements.txt
```

For Linux users, PyAudio might require additional steps:

```bash
sudo apt-get install python-pyaudio python3-pyaudio
```

## Usage

To start the application, navigate to the application directory in your terminal and run:

```bash
python main.py
```

Once the application is running, use the GUI buttons to start and stop voice typing. Adjust settings like the application theme through the settings window.

## Dependencies

- Tkinter
- SpeechRecognition
- pyttsx3
- pyautogui
- audioplayer
- pyperclip
- ttkthemes

## Contributing

Contributions to the Voice Typing App are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## License
This project is open-source and available under the [MIT License](LICENSE.md).

