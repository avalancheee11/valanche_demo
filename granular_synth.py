import numpy as np
import librosa
import soundfile as sf
from typing import Tuple, Optional
import random

class GranularSynthesizer:
    def __init__(self, grain_size_ms: int = 100, overlap: float = 0.5, randomize_grains: bool = True):
        """
        Initialize granular synthesizer
        
        Args:
            grain_size_ms: Size of each grain in milliseconds
            overlap: Overlap between grains (0.0 to 1.0)
            randomize_grains: Whether to randomize grain positions
        """
        self.grain_size_ms = grain_size_ms
        self.overlap = overlap
        self.randomize_grains = randomize_grains
    
    def create_granular_loop(self, input_file: str, output_file: str, 
                           loop_duration: float = 10.0, 
                           crossfade_duration: float = 0.1) -> str:
        """
        Create a seamless loop using granular synthesis
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output loop file
            loop_duration: Duration of the loop in seconds
            crossfade_duration: Crossfade duration at loop points
            
        Returns:
            Path to the generated loop file
        """
        # Load audio
        audio, sr = librosa.load(input_file, sr=None)
        
        # Calculate input RMS for volume matching
        input_rms = np.sqrt(np.mean(audio**2))
        
        # Convert grain size to samples
        grain_size_samples = int(self.grain_size_ms * sr / 1000)
        
        # Calculate number of grains needed
        samples_needed = int(loop_duration * sr)
        grain_hop = int(grain_size_samples * (1 - self.overlap))
        num_grains = int(samples_needed / grain_hop) + 1
        
        # Create output array
        output = np.zeros(samples_needed)
        
        # Generate grains
        for i in range(num_grains):
            if self.randomize_grains:
                # Random position within the audio
                start_pos = random.randint(0, max(0, len(audio) - grain_size_samples))
            else:
                # Sequential positions
                start_pos = (i * grain_size_samples // 2) % max(1, len(audio) - grain_size_samples)
            
            # Extract grain
            end_pos = min(start_pos + grain_size_samples, len(audio))
            grain = audio[start_pos:end_pos]
            
            # Apply window function for smooth transitions
            window = np.hanning(len(grain))
            grain = grain * window
            
            # Position in output
            output_start = i * grain_hop
            output_end = min(output_start + len(grain), len(output))
            
            # Add grain to output with overlap-add
            if output_end <= len(output):
                output[output_start:output_end] += grain[:output_end - output_start]
        
        # Normalize to match input volume
        output_rms = np.sqrt(np.mean(output**2))
        if output_rms > 0:
            output = output * (input_rms / output_rms)
        
        # Apply crossfade at loop points for seamless looping
        if crossfade_duration > 0:
            crossfade_samples = int(crossfade_duration * sr)
            if crossfade_samples < len(output) // 2:
                # Create crossfade at the end
                fade_out = np.linspace(1.0, 0.0, crossfade_samples)
                fade_in = np.linspace(0.0, 1.0, crossfade_samples)
                
                # Apply fade out at the end
                output[-crossfade_samples:] *= fade_out
                
                # Apply fade in at the beginning and add to the end
                output[-crossfade_samples:] += output[:crossfade_samples] * fade_in
        
        # Save the loop
        sf.write(output_file, output, sr)
        return output_file
    
    def create_texture_loop(self, input_file: str, output_file: str, 
                          loop_duration: float = 10.0, 
                          texture_density: float = 0.7) -> str:
        """
        Create a texture-based loop with multiple overlapping grains
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output loop file
            loop_duration: Duration of the loop in seconds
            texture_density: Density of grains (0.0 to 1.0)
        """
        # Load audio
        audio, sr = librosa.load(input_file, sr=None)
        
        # Calculate input RMS for volume matching
        input_rms = np.sqrt(np.mean(audio**2))
        
        # Smaller grains for texture
        grain_size_samples = int(50 * sr / 1000)  # 50ms grains
        
        # Calculate parameters
        samples_needed = int(loop_duration * sr)
        num_grains = int(samples_needed * texture_density / grain_size_samples)
        
        # Create output array
        output = np.zeros(samples_needed)
        
        # Generate overlapping grains
        for _ in range(num_grains):
            # Random position and slight pitch variation
            start_pos = random.randint(0, max(0, len(audio) - grain_size_samples))
            pitch_factor = random.uniform(0.8, 1.2)
            
            # Extract and process grain
            end_pos = min(start_pos + grain_size_samples, len(audio))
            grain = audio[start_pos:end_pos]
            
            # Apply pitch shift if needed
            if abs(pitch_factor - 1.0) > 0.01:
                grain = librosa.effects.pitch_shift(grain, sr=sr, n_steps=12 * np.log2(pitch_factor))
            
            # Apply window
            window = np.hanning(len(grain))
            grain = grain * window
            
            # Random position in output
            output_start = random.randint(0, max(0, len(output) - len(grain)))
            output_end = min(output_start + len(grain), len(output))
            
            # Add grain
            if output_end <= len(output):
                output[output_start:output_end] += grain[:output_end - output_start]
        
        # Normalize to match input volume
        output_rms = np.sqrt(np.mean(output**2))
        if output_rms > 0:
            output = output * (input_rms / output_rms)
        
        # Save
        sf.write(output_file, output, sr)
        return output_file 