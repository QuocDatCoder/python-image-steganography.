import tkinter as tk
from tkinter import filedialog, messagebox
import os
from core.crypto import AESCrypt
from core.steganography import Steganography
from core.compression import LZW
from core.email_utils import EmailSender

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Steganography - Python Version")
        self.root.geometry("600x500")
        self.root.configure(bg="#2c3e50")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Header
        header = tk.Label(self.root, text="Image Steganography", font=("Arial", 24, "bold"), 
                         fg="white", bg="#2c3e50", pady=20)
        header.pack()
        
        # Main Buttons Container
        btn_frame = tk.Frame(self.root, bg="#2c3e50")
        btn_frame.pack(expand=True)
        
        btn_style = {
            "font": ("Arial", 12),
            "width": 25,
            "height": 2,
            "bd": 0,
            "cursor": "hand2",
            "activebackground": "#34495e",
            "activeforeground": "white"
        }
        
        tk.Button(btn_frame, text="Encode Text into Image", bg="#2980b9", fg="white", 
                  command=self.show_encode, **btn_style).pack(pady=10)
        
        tk.Button(btn_frame, text="Decode from Image", bg="#27ae60", fg="white", 
                  command=self.show_decode, **btn_style).pack(pady=10)
        
        tk.Button(btn_frame, text="About / Help", bg="#95a5a6", fg="white", 
                  command=self.show_about, **btn_style).pack(pady=10)
        
        tk.Button(btn_frame, text="Exit", bg="#c0392b", fg="white", 
                  command=self.root.quit, **btn_style).pack(pady=10)

    def show_encode(self):
        EncodeWindow(self.root)

    def show_decode(self):
        DecodeWindow(self.root)

    def show_about(self):
        about_text = "Image Steganography Hybrid Approach\n\nFeatures:\nAES Encryption\nLZW Compression\nLSB Steganography\n\nConverted to Python."
        messagebox.showinfo("About", about_text)


class EncodeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Encode Data")
        self.geometry("500x750")
        self.configure(bg="#34495e")
        
        self.image_path = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Encode Message", font=("Arial", 18, "bold"), fg="white", bg="#34495e", pady=10).pack()
        
        # Image Selection
        tk.Label(self, text="Step 1: Select Image", fg="white", bg="#34495e").pack(pady=5)
        self.btn_select_img = tk.Button(self, text="Browse Image", command=self.select_image)
        self.btn_select_img.pack()
        self.lbl_img_path = tk.Label(self, text="No image selected", fg="#bdc3c7", bg="#34495e", wraplength=400)
        self.lbl_img_path.pack()

        # Secret Key
        tk.Label(self, text="Step 2: Enter Secret Key (AES)", fg="white", bg="#34495e").pack(pady=5)
        self.ent_key = tk.Entry(self, show="*")
        self.ent_key.insert(0, "1Hbfh667adfDEJ78") # Default key
        self.ent_key.pack()

        # Message
        tk.Label(self, text="Step 3: Enter Message", fg="white", bg="#34495e").pack(pady=5)
        self.txt_msg = tk.Text(self, height=5, width=40)
        self.txt_msg.pack(pady=5)

        # Email Section (Optional)
        email_frame = tk.LabelFrame(self, text="Step 4: Email Secret Key (Optional)", fg="white", bg="#34495e", padx=10, pady=10)
        email_frame.pack(pady=10, fill="x", padx=20)
        
        tk.Label(email_frame, text="Your Gmail:", fg="white", bg="#34495e").grid(row=0, column=0, sticky="w")
        self.ent_sender = tk.Entry(email_frame)
        self.ent_sender.grid(row=0, column=1, pady=2)
        
        tk.Label(email_frame, text="App Password:", fg="white", bg="#34495e").grid(row=1, column=0, sticky="w")
        self.ent_pass = tk.Entry(email_frame, show="*")
        self.ent_pass.grid(row=1, column=1, pady=2)
        
        tk.Label(email_frame, text="Receiver Email:", fg="white", bg="#34495e").grid(row=2, column=0, sticky="w")
        self.ent_receiver = tk.Entry(email_frame)
        self.ent_receiver.grid(row=2, column=1, pady=2)

        # Encode Button
        self.btn_encode = tk.Button(self, text="ENCODE & SAVE", bg="#2980b9", fg="white", 
                                   font=("Arial", 12, "bold"), pady=10, command=self.process_encode)
        self.btn_encode.pack(pady=20)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.image_path = file_path
            self.lbl_img_path.config(text=os.path.basename(file_path))

    def process_encode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image first.")
            return
        
        msg = self.txt_msg.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showerror("Error", "Please enter a message.")
            return

        try:
            # Lấy khóa động từ ô nhập liệu
            key = self.ent_key.get()
            
            # 1. Encrypt (Truyền key vào)
            encrypted = AESCrypt.encrypt(msg, key)
            
            # 2. Compress
            compressed = LZW.compress_to_string(encrypted)
            
            # 3. Steganography
            out_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if not out_path:
                return
                
            Steganography.hide_data(self.image_path, compressed, out_path)
            
            # 4. Optional Email
            sender = self.ent_sender.get().strip()
            if sender:
                pwd = self.ent_pass.get().strip()
                recv = self.ent_receiver.get().strip()
                if EmailSender.send_key_mail(sender, pwd, recv, key):
                    messagebox.showinfo("Success", "Data encoded and key emailed!")
                else:
                    messagebox.showwarning("Warning", "Data encoded, but email failed.")
            else:
                messagebox.showinfo("Success", f"Data encoded successfully!\nSaved to: {out_path}")
            
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


class DecodeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Decode Data")
        self.geometry("500x550")
        self.configure(bg="#34495e")
        
        self.image_path = None
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self, text="Decode Message", font=("Arial", 18, "bold"), fg="white", bg="#34495e", pady=10).pack()
        
        # Image Selection
        tk.Label(self, text="Step 1: Select Stego Image", fg="white", bg="#34495e").pack(pady=5)
        self.btn_select_img = tk.Button(self, text="Browse Image", command=self.select_image)
        self.btn_select_img.pack()
        self.lbl_img_path = tk.Label(self, text="No image selected", fg="#bdc3c7", bg="#34495e", wraplength=400)
        self.lbl_img_path.pack()

        # Secret Key (THÊM MỚI Ở ĐÂY)
        tk.Label(self, text="Step 2: Enter Secret Key (AES)", fg="white", bg="#34495e").pack(pady=5)
        self.ent_key = tk.Entry(self, show="*")
        self.ent_key.insert(0, "1Hbfh667adfDEJ78") # Khóa mặc định khớp với bên encode
        self.ent_key.pack()

        # Decode Button
        self.btn_decode = tk.Button(self, text="EXTRACT & DECODE", bg="#27ae60", fg="white", 
                                   font=("Arial", 12, "bold"), pady=10, command=self.process_decode)
        self.btn_decode.pack(pady=20)

        # Result
        tk.Label(self, text="Decoded Message:", fg="white", bg="#34495e").pack(pady=5)
        self.txt_result = tk.Text(self, height=5, width=40, state=tk.DISABLED)
        self.txt_result.pack(pady=5)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if file_path:
            self.image_path = file_path
            self.lbl_img_path.config(text=os.path.basename(file_path))

    def process_decode(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select a stego image.")
            return

        try:
            # 1. Extract
            compressed = Steganography.extract_data(self.image_path)
            if compressed.startswith("Error"):
                messagebox.showerror("Error", compressed)
                return
            
            # 2. Decompress
            encrypted = LZW.decompress_from_string(compressed)
            
            # 3. Decrypt (Lấy khóa từ ô nhập liệu và truyền vào)
            key = self.ent_key.get()
            decrypted = AESCrypt.decrypt(encrypted, key)
            
            if decrypted:
                self.txt_result.config(state=tk.NORMAL)
                self.txt_result.delete("1.0", tk.END)
                self.txt_result.insert(tk.END, decrypted)
                self.txt_result.config(state=tk.DISABLED)
            else:
                messagebox.showerror("Error", "Could not decrypt data. Invalid key or data.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()