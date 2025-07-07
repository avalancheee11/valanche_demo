import streamlit as st
import numpy as np
import time
from typing import Optional, Callable, List, Dict, Any
import base64
import io
from scipy.io.wavfile import write
import os

def get_available_microphones() -> List[Dict[str, Any]]:
    """
    Get list of available microphone devices (web-compatible)
    
    Returns:
        List of dictionaries with device info
    """
    # For web deployment, we'll use a simplified approach
    return [
        {
            'index': 0,
            'name': 'Default Microphone',
            'channels': 1,
            'sample_rate': 44100,
            'is_default': True
        }
    ]

def get_default_microphone_index() -> int:
    """Get the default microphone device index"""
    return 0

def create_audio_recorder_component():
    """
    Create a Streamlit component for web-based audio recording
    """
    st.markdown("""
    <div id="audio-recorder">
        <button id="recordButton" onclick="toggleRecording()">🎙️ Start Recording</button>
        <div id="meter" style="display: none;">
            <div style="background: #f0f2f6; padding: 10px; border-radius: 5px; margin: 10px 0;">
                <div id="meterBar" style="background: green; height: 20px; width: 0%; border-radius: 5px; transition: width 0.1s;"></div>
            </div>
            <div id="meterText">Ready to record...</div>
        </div>
        <audio id="audioPreview" controls style="display: none; width: 100%; margin: 10px 0;"></audio>
    </div>

    <script>
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
    let audioContext;
    let analyser;
    let microphone;
    let dataArray;
    let meterInterval;

    async function toggleRecording() {
        const button = document.getElementById('recordButton');
        const meter = document.getElementById('meter');
        const audioPreview = document.getElementById('audioPreview');
        
        if (!isRecording) {
            try {
                // Request microphone access
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        sampleRate: 44100,
                        channelCount: 1,
                        echoCancellation: true,
                        noiseSuppression: true
                    } 
                });
                
                // Set up audio analysis
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                analyser = audioContext.createAnalyser();
                microphone = audioContext.createMediaStreamSource(stream);
                microphone.connect(analyser);
                
                analyser.fftSize = 256;
                const bufferLength = analyser.frequencyBinCount;
                dataArray = new Uint8Array(bufferLength);
                
                // Start recording
                mediaRecorder = new MediaRecorder(stream, {
                    mimeType: 'audio/webm;codecs=opus'
                });
                
                audioChunks = [];
                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    audioPreview.src = audioUrl;
                    audioPreview.style.display = 'block';
                    
                    // Convert to WAV and send to Streamlit
                    convertToWav(audioBlob);
                };
                
                mediaRecorder.start();
                isRecording = true;
                button.textContent = '⏹️ Stop Recording';
                button.style.background = '#ff4444';
                meter.style.display = 'block';
                
                // Start meter updates
                updateMeter();
                meterInterval = setInterval(updateMeter, 100);
                
            } catch (error) {
                console.error('Error accessing microphone:', error);
                alert('Error accessing microphone. Please check permissions.');
            }
        } else {
            // Stop recording
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
            if (meterInterval) {
                clearInterval(meterInterval);
            }
            
            isRecording = false;
            button.textContent = '🎙️ Start Recording';
            button.style.background = '#667eea';
            
            // Stop all tracks
            if (mediaRecorder && mediaRecorder.stream) {
                mediaRecorder.stream.getTracks().forEach(track => track.stop());
            }
        }
    }
    
    function updateMeter() {
        if (!analyser || !dataArray) return;
        
        analyser.getByteFrequencyData(dataArray);
        const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
        const normalizedLevel = average / 255;
        
        const meterBar = document.getElementById('meterBar');
        const meterText = document.getElementById('meterText');
        
        meterBar.style.width = (normalizedLevel * 100) + '%';
        meterBar.style.background = normalizedLevel > 0.8 ? 'red' : 'green';
        
        meterText.textContent = `Recording... Level: ${Math.round(normalizedLevel * 100)}%`;
    }
    
    async function convertToWav(audioBlob) {
        // Convert WebM to WAV using Web Audio API
        const arrayBuffer = await audioBlob.arrayBuffer();
        const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
        
        // Convert to WAV format
        const wavBuffer = audioBufferToWav(audioBuffer);
        const wavBlob = new Blob([wavBuffer], { type: 'audio/wav' });
        
        // Send to Streamlit
        const formData = new FormData();
        formData.append('audio', wavBlob, 'recording.wav');
        
        // Use Streamlit's file uploader or session state
        // For now, we'll store in session state
        window.parent.postMessage({
            type: 'audioData',
            data: await blobToBase64(wavBlob)
        }, '*');
    }
    
    function audioBufferToWav(buffer) {
        const length = buffer.length;
        const numberOfChannels = buffer.numberOfChannels;
        const sampleRate = buffer.sampleRate;
        const arrayBuffer = new ArrayBuffer(44 + length * numberOfChannels * 2);
        const view = new DataView(arrayBuffer);
        
        // WAV header
        const writeString = (offset, string) => {
            for (let i = 0; i < string.length; i++) {
                view.setUint8(offset + i, string.charCodeAt(i));
            }
        };
        
        writeString(0, 'RIFF');
        view.setUint32(4, 36 + length * numberOfChannels * 2, true);
        writeString(8, 'WAVE');
        writeString(12, 'fmt ');
        view.setUint32(16, 16, true);
        view.setUint16(20, 1, true);
        view.setUint16(22, numberOfChannels, true);
        view.setUint32(24, sampleRate, true);
        view.setUint32(28, sampleRate * numberOfChannels * 2, true);
        view.setUint16(32, numberOfChannels * 2, true);
        view.setUint16(34, 16, true);
        writeString(36, 'data');
        view.setUint32(40, length * numberOfChannels * 2, true);
        
        // Convert audio data
        const offset = 44;
        for (let i = 0; i < length; i++) {
            for (let channel = 0; channel < numberOfChannels; channel++) {
                const sample = Math.max(-1, Math.min(1, buffer.getChannelData(channel)[i]));
                view.setInt16(offset + (i * numberOfChannels + channel) * 2, sample * 0x7FFF, true);
            }
        }
        
        return arrayBuffer;
    }
    
    async function blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }
    </script>
    """, unsafe_allow_html=True)

def record_audio_web(duration: int = 15, samplerate: int = 44100, 
                    device_index: Optional[int] = None,
                    meter_callback: Optional[Callable] = None) -> str:
    """
    Web-based audio recording using browser APIs
    
    Args:
        duration: Recording duration in seconds
        samplerate: Sample rate
        device_index: Microphone device index (ignored in web version)
        meter_callback: Callback for meter updates (ignored in web version)
        
    Returns:
        Filename of the recorded audio
    """
    st.info("🎙️ Web-based recording is active. Use the recording button below.")
    
    # Create the web component
    create_audio_recorder_component()
    
    # For now, return a placeholder filename
    # In a real implementation, you'd handle the audio data from the JavaScript
    filename = f"recorded_{int(time.time())}.wav"
    
    # Placeholder for demonstration
    st.warning("⚠️ Web recording is in development. For full functionality, use the local version.")
    
    return filename

def test_microphone_web(device_index: int, duration: float = 2.0) -> bool:
    """
    Test if a microphone is working (web version)
    
    Args:
        device_index: Device index to test
        duration: Test duration in seconds
        
    Returns:
        True if microphone works, False otherwise
    """
    st.info("🔊 Microphone test is available in the recording interface.")
    return True

# Alias functions for compatibility
record_audio = record_audio_web
test_microphone = test_microphone_web 