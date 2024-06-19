import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re

app = Flask(__name__)

os.environ["GOOGLE_API_KEY"] = "-eyewIx8A"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    result_price = None
    error_message = None
    nama_kendaraan_koreksi = None

    if request.method == "POST":
        jenis_kendaraan = request.form["jenis_kendaraan"]
        nama_kendaraan = request.form["nama_kendaraan"]
        tahun_kendaraan = request.form["tahun_kendaraan"]
        km_kendaraan = request.form["km_kendaraan"]
        transmisi = request.form["transmisi"]
        bahan_bakar = request.form["bahan_bakar"]
        wilayah_kendaraan = request.form["wilayah_kendaraan"]

        try:
            # Koreksi nama kendaraan (opsional)
            nama_kendaraan_koreksi = nama_kendaraan  # Inisialisasi dengan nama asli
            if request.form.get("koreksi_nama"):
                response_koreksi = genai.GenerativeModel('gemini-1.5-pro')
                prompt_koreksi = response_koreksi.generate_content(f"Koreksi nama unit ini dengan nama yang benar dan singkat, anda bisa cari di internet. berikan response langsung nama nya tanpa perlu Nama unit yang benar adalah : {nama_kendaraan}")
                # Menampilkan hasil (asumsi atribut teks bernama 'text')
                if response_koreksi and hasattr(response_koreksi, 'text'):
                    print(response_koreksi.text)
                else:
                    print("Tidak ada respons yang dihasilkan atau format respons tidak valid.")

            # Analisis harga pasar (perbaikan pada prompt)
            
            response_harga = genai.GenerativeModel('gemini-1.5-pro')
            prompt_harga = response_harga.generate_content(f"Analisis kisaran harga pasar untuk {jenis_kendaraan} BEKAS {nama_kendaraan_koreksi} "
                            f"tahun {tahun_kendaraan} di wilayah {wilayah_kendaraan}. Sertakan informasi tentang: \n\n"
                            "1. Nama Mobil (lengkap sesuai pasar)\n"
                            "2. Tahun Mobil\n"
                            "3. Kota/Wilayah\n"
                            "4. Kisaran Harga Terendah\n"
                            "5. Kisaran Harga Tertinggi\n"
                            "6. Sumber informasi (misalnya situs web, platform jual beli, dll.)")
            # Menampilkan hasil (asumsi atribut teks bernama 'text')
            if response_harga and hasattr(response_harga, 'text'):
                print(response_harga.text)
            else:
                print("Tidak ada respons yang dihasilkan atau format respons tidak valid.")

        except Exception as e:
            error_message = f"Terjadi kesalahan: {e}"

    return render_template("index.html", result_price=result_price, error_message=error_message, nama_kendaraan_koreksi=nama_kendaraan_koreksi)


if __name__ == "__main__":
    app.run(debug=True)
