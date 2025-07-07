import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import time
import threading
from typing import Optional, Callable, List, Dict, Any
import streamlit as st

def get_available_microphones() -> List[Dict[str, Any]]:
    """
    Get list of available microphone devices
    
    Returns:
        List of dictionaries with device info
    """
    try:
        devices = sd.query_devices()
        microphones = []
        
        for i, device in enumerate(devices):
            if device.get('max_input_channels', 0) > 0:  # Device supports input
                microphones.append({
                    'index': i,
                    'name': device.get('name', f'Device {i}'),
                    'channels': device.get('max_input_channels', 1),
                    'sample_rate': device.get('default_samplerate', 44100),
                    'is_default': i == sd.default.device[0]
                })
        
        return microphones
    except Exception as e:
        st.error(f"Failed to get microphone list: {e}")
        return []

def get_default_microphone_index() -> int:
    """Get the default microphone device index"""
    try:
        idx = sd.default.device[0]
        if idx is None:
            return 0
        return int(idx)
    except Exception:
        return 0

class AudioRecorder:
    def __init__(self, samplerate: int = 44100, channels: int = 1, device_index: Optional[int] = None):
        self.samplerate = samplerate
        self.channels = channels
        self.device_index = device_index if device_index is not None else get_default_microphone_index()
        self.is_recording = False
        self.audio_buffer = []
        self.meter_callback = None
        
    def start_recording(self, duration: int = 15, meter_callback: Optional[Callable] = None) -> str:
        """
        Start recording with meter display
        
        Args:
            duration: Recording duration in seconds
            meter_callback: Callback function for meter updates
            
        Returns:
            Filename of the recorded audio
        """
        self.meter_callback = meter_callback
        self.is_recording = True
        self.audio_buffer = []
        
        filename = f"recorded_{int(time.time())}.wav"
        
        # Countdown before recording
        for i in range(3, 0, -1):
            if self.meter_callback:
                self.meter_callback(f"Recording in {i}...", 0)
            time.sleep(1)
        
        if self.meter_callback:
            self.meter_callback("Recording...", 0)
        
        try:
            # Start recording with specified device
            with sd.InputStream(
                samplerate=self.samplerate, 
                channels=self.channels, 
                dtype='int16',
                device=self.device_index,
                callback=self._audio_callback
            ):
                
                start_time = time.time()
                while time.time() - start_time < duration and self.is_recording:
                    # Update meter
                    if self.audio_buffer and self.meter_callback:
                        # Calculate RMS for meter
                        recent_audio = np.array(self.audio_buffer[-int(self.samplerate * 0.1):])  # Last 100ms
                        if len(recent_audio) > 0:
                            rms = np.sqrt(np.mean(recent_audio.astype(np.float32)**2))
                            # Convert to dB and normalize to -50 dB to 1 dB range
                            db = 20 * np.log10(max(rms, 1e-10))
                            # Normalize to 0-1 range: -50 dB = 0, 1 dB = 1
                            normalized_level = max(0, min(1, (db + 50) / 51))
                            self.meter_callback(f"Recording... ({duration - int(time.time() - start_time)}s left)", normalized_level)
                    
                    time.sleep(0.1)
                
                # Convert buffer to numpy array
                if self.audio_buffer:
                    audio_data = np.array(self.audio_buffer, dtype=np.int16)
                    write(filename, self.samplerate, audio_data)
                    
                    if self.meter_callback:
                        self.meter_callback("Recording saved!", 0)
                    
                    return filename
                else:
                    raise Exception("No audio data recorded")
                    
        except Exception as e:
            if self.meter_callback:
                self.meter_callback(f"Recording failed: {str(e)}", 0)
            raise e
    
    def stop_recording(self):
        """Stop recording"""
        self.is_recording = False
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio input"""
        if status:
            print(f"Audio callback status: {status}")
        
        if self.is_recording:
            # Store audio data
            self.audio_buffer.extend(indata.flatten())

def record_audio(filename: str = 'recorded.wav', duration: int = 15, 
                samplerate: int = 44100, device_index: Optional[int] = None,
                meter_callback: Optional[Callable] = None) -> str:
    """
    Record audio with meter display
    
    Args:
        filename: Output filename
        duration: Recording duration in seconds
        samplerate: Sample rate
        device_index: Microphone device index
        meter_callback: Callback for meter updates
        
    Returns:
        Filename of the recorded audio
    """
    try:
        recorder = AudioRecorder(
            samplerate=samplerate, 
            device_index=device_index
        )
        return recorder.start_recording(duration=duration, meter_callback=meter_callback)
    except Exception as e:
        print(f"Recording failed: {e}")
        raise e

def test_microphone(device_index: int, duration: float = 2.0) -> bool:
    """
    Test if a microphone is working
    
    Args:
        device_index: Device index to test
        duration: Test duration in seconds
        
    Returns:
        True if microphone works, False otherwise
    """
    try:
        # Record a short test
        test_audio = sd.rec(
            int(duration * 44100), 
            samplerate=44100, 
            channels=1, 
            dtype='int16',
            device=device_index
        )
        sd.wait()
        
        # Check if we got any audio data
        if np.any(test_audio):
            return True
        else:
            return False
            
    except Exception as e:
        st.error(f"Microphone test failed: {e}")
        return False