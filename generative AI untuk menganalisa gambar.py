import os
import PIL.Image # Untuk file gambar

# Use environment variables or direct assignment for API keys

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '<your-api-key>')
# Replace 'YOUR_API_KEY_HERE' with your actual API key if not using environment variables

import google.generativeai as genai
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini API
try:
    gemini_model = genai.GenerativeModel('gemini-2.5-flash') # Or the model you successfully initialized
except NameError:
    print("Gemini model not initialized. Please run the API initialization cells.")

print("Mulai percakapan dengan AI (ketik '/exit' atau '/quit' untuk keluar):")
chat = gemini_model.start_chat(history=[])

while True:
    user_text_input = input("Anda: ")
    if user_text_input.lower() in ['/exit', '/quit']:
        print("Percakapan selesai.")
        break

    prompt_parts = [user_text_input]
    image_files_to_send = []

    add_images_str = input("Apakah Anda ingin menyertakan gambar? (ya/tidak): ").lower()
    if add_images_str == 'ya':
        while True:
            image_dir_input = input("Masukkan nama folder gambar (misal: 'file gambar'): ")
            image_filename_input = input("Masukkan nama file gambar (misal: 'pagani huarya.jpeg'): ")

            image_directory = os.path.join(image_dir_input.strip())
            image_path = os.path.join(image_directory, image_filename_input.strip())

            if os.path.exists(image_path):
                try:
                    img = PIL.Image.open(image_path)
                    image_files_to_send.append(img)
                    print(f"Gambar '{image_filename_input}' berhasil ditambahkan.")
                except Exception as e:
                    print(f"Terjadi kesalahan saat memuat gambar '{image_filename_input}': {e}")
            else:
                print(f"File gambar tidak ditemukan di: {image_path}. Harap periksa kembali path dan nama file.")

            add_more_images = input("Tambahkan gambar lain? (ya/tidak): ").lower()
            if add_more_images != 'ya':
                break

    if image_files_to_send:
        prompt_parts.extend(image_files_to_send)

    try:
        print("==========================================Pesan AI=========================================")
        response = chat.send_message(prompt_parts)
        print("AI:  ", response.text)
    except Exception as e:

        print(f"Terjadi kesalahan saat mengirim pesan ke model Gemini: {e}")
