# 🎙️ Valanche Ambience Recorder

A sophisticated ambient audio recorder and granular synthesis tool that captures environmental sounds and transforms them into seamless, loopable ambient soundscapes.

## ✨ Features

### 🎤 Advanced Recording
- **Real-time Audio Meter**: Visual feedback during recording with level indicators
- **Configurable Duration**: Record from 5 to 60 seconds
- **Multiple Sample Rates**: Support for 22.05kHz, 44.1kHz, and 48kHz
- **Countdown Timer**: 3-second countdown before recording starts
- **Audio Quality Analysis**: Automatic assessment of recording quality

### 🔍 AI-Powered Analysis
- **Environment Detection**: Uses YAMNet (You Only Look Once Audio Neural Network) to classify audio
- **Quality Metrics**: Analyzes signal level, noise, and spectral characteristics
- **Confidence Scoring**: Provides confidence levels for environment detection

### 🔁 Granular Synthesis
- **Granular Loop**: Creates seamless loops by cutting audio into small grains and reassembling
- **Texture Loop**: Generates ambient textures with overlapping grains and pitch variations
- **Customizable Parameters**:
  - Grain size (20-500ms)
  - Grain overlap (0-90%)
  - Loop duration (5-60 seconds)
  - Texture density for texture loops

### 🎛️ User Experience
- **Modern UI**: Beautiful Streamlit interface with gradient styling
- **Real-time Feedback**: Progress indicators and status updates
- **Audio Preview**: Listen to recordings before processing
- **Download Support**: Easy download of generated loops
- **Session Management**: Maintains state between operations

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Microphone access
- Internet connection (for YAMNet model download)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd valanche_demo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 📖 Usage

### 1. Recording
1. Adjust recording settings in the sidebar (duration, sample rate)
2. Click "🎙️ Start Recording"
3. Wait for the 3-second countdown
4. Speak or capture ambient sounds
5. Monitor the real-time audio meter

### 2. Analysis
1. After recording, click "🔍 Analyze Environment"
2. View the detected environment type and confidence score
3. Check audio quality metrics and recommendations

### 3. Loop Generation
1. Configure granular synthesis parameters in the sidebar
2. Choose between "Granular Loop" or "Texture Loop"
3. Click "🎵 Generate Granular Loop"
4. Preview the generated loop
5. Download the final audio file

## 🔧 Configuration

### Recording Settings
- **Duration**: 5-60 seconds
- **Sample Rate**: 22.05kHz, 44.1kHz, 48kHz

### Granular Synthesis Settings
- **Grain Size**: 20-500ms (smaller = more detailed, larger = smoother)
- **Overlap**: 0-90% (higher = more seamless transitions)
- **Loop Duration**: 5-60 seconds
- **Synthesis Type**:
  - **Granular Loop**: Traditional granular synthesis for seamless loops
  - **Texture Loop**: Ambient texture generation with pitch variations

## 🏗️ Architecture

### Core Modules

#### `app.py`
- Main Streamlit application
- UI components and user interaction
- Session state management

#### `record.py`
- Audio recording with real-time meter
- `AudioRecorder` class with callback support
- Countdown and progress tracking

#### `analyze.py`
- YAMNet integration for environment detection
- Audio quality analysis
- Model caching for performance

#### `granular_synth.py`
- `GranularSynthesizer` class
- Two synthesis modes: granular loop and texture loop
- Crossfade and windowing for seamless transitions

### Dependencies

- **Streamlit**: Web interface
- **Sounddevice**: Audio recording
- **Librosa**: Audio processing and analysis
- **TensorFlow**: YAMNet model
- **NumPy**: Numerical computations
- **Soundfile**: Audio file I/O

## 🎯 Use Cases

### Music Production
- Create ambient backgrounds for tracks
- Generate atmospheric soundscapes
- Sample environmental sounds

### Sound Design
- Design game audio environments
- Create film sound effects
- Generate nature soundscapes

### Meditation & Relaxation
- Create calming ambient loops
- Generate white noise variations
- Design sleep soundscapes

## 🔮 Future Enhancements

### Planned Features
- [ ] Multiple audio input sources
- [ ] Real-time granular synthesis
- [ ] Advanced audio effects (reverb, delay, filters)
- [ ] Batch processing of multiple recordings
- [ ] Export to multiple formats (MP3, FLAC, OGG)
- [ ] Cloud storage integration
- [ ] Collaborative sharing features

### Technical Improvements
- [ ] GPU acceleration for processing
- [ ] Advanced audio analysis algorithms
- [ ] Machine learning for loop quality optimization
- [ ] Real-time collaboration features

## 🐛 Troubleshooting

### Common Issues

**Recording not working**:
- Check microphone permissions
- Ensure microphone is not muted
- Try different sample rates

**YAMNet model loading fails**:
- Check internet connection
- Clear TensorFlow cache: `rm -rf ~/.cache/tensorflow`

**Audio quality issues**:
- Reduce background noise
- Increase recording duration
- Adjust microphone position

**Performance issues**:
- Close other audio applications
- Reduce sample rate
- Use shorter recording durations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Made with ❤️ for ambient sound enthusiasts** 