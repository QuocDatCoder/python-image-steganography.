from PIL import Image
import numpy as np
import os

class Steganography:
    @staticmethod
    def hide_data(image_path: str, data: str, output_path: str):
        """Hides string data inside an image using LSB."""
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Convert data to bytes then bits
        data_bytes = data.encode('utf-8')
        data_len = len(data_bytes)
        
        # Header: 4 bytes for length (32 bits)
        header = data_len.to_bytes(4, byteorder='big')
        full_data = header + data_bytes
        
        bits = []
        for byte in full_data:
            for i in range(8):
                bits.append((byte >> (7 - i)) & 1)
        
        # Load pixels
        pixels = np.array(img)
        orig_shape = pixels.shape
        flat_pixels = pixels.flatten()
        
        if len(bits) > len(flat_pixels):
            raise ValueError(f"Data size ({len(bits)} bits) exceeds image capacity ({len(flat_pixels)} bits).")
        
        # Modify LSB
        # Use 0xFE (254) instead of ~1 to prevent OverflowError on uint8 array
        bits_arr = np.array(bits, dtype=np.uint8)
        flat_pixels[:len(bits)] = (flat_pixels[:len(bits)] & 0xFE) | bits_arr
        
        # Save image
        new_img = Image.fromarray(flat_pixels.reshape(orig_shape))
        new_img.save(output_path, format="PNG") # Use PNG to avoid lossy compression
        return output_path

    @staticmethod
    def extract_data(image_path: str) -> str:
        """Extracts hidden string data from an image's LSB."""
        img = Image.open(image_path)
        pixels = np.array(img).flatten()
        
        # Extract length (first 32 bits)
        len_bits = pixels[:32] & 1
        data_len = 0
        for bit in len_bits:
            data_len = (data_len << 1) | int(bit)
            
        if data_len <= 0 or data_len > (len(pixels) - 32) // 8:
            return "Error: Extracted length is invalid or image is not stego-protected."
            
        # Extract data bits
        data_bits = pixels[32 : 32 + data_len * 8] & 1
        
        # Convert bits back to bytes
        data_bytes = bytearray()
        for i in range(0, len(data_bits), 8):
            byte_bits = data_bits[i:i+8]
            byte_val = 0
            for bit in byte_bits:
                byte_val = (byte_val << 1) | int(bit)
            data_bytes.append(byte_val)
            
        try:
            return data_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return "Error: Could not decode extracted data. Key might be wrong or image corrupted."
