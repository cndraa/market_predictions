import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re

app = Flask(__name__)


# Access your API key as an environment variable.
os.environ["GOOGLE_API_KEY"] = "AIzaSyC-HjO8_T88mEugQ6Pb2Ih8IiZRv9Te_NA"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))# Choose a model that's appropriate for your use case.
model = genai.GenerativeModel('gemini-1.5-flash')


@app.route("/", methods=["GET", "POST"])
def index():
    result_price = None
    error_message = None
    nama_kendaraan_koreksi = None
    jenis_kendaraan = None
    nama_kendaraan = None
    tahun_kendaraan = None
    km_kendaraan = None
    transmisi = None
    bahan_bakar = None
    wilayah_kendaraan = None
    predict_text = None
    bottom_filtered = None
    top_filtered = None
    
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
            prompt = f"Koreksi nama unit ini dengan nama yang benar dan singkat, anda bisa cari di internet. berikan response langsung nama nya tanpa perlu Nama unit yang benar adalah : {nama_kendaraan}"
            response = model.generate_content(prompt)
            nama_kendaraan = response.text
            
            # Analisis harga pasar
            prompt_predict= f"Berikan Average Market Price untuk { jenis_kendaraan } Bekas {nama_kendaraan} tahun {tahun_kendaraan} wilayah {wilayah_kendaraan} dengan format sebagai berikut:\n1. Nama Kendaraan:\n2. Tahun Kendaraaan:\n3. Wilayah Kendaraan\n4. Harga Terendah: {{ Harga Terendah }}\n5. Harga Tertinggi: {{ Harga Tertinggi }}\n6. Sumber Analisa Harga: {{ Olx, Oto.com, dan sebagainya }}\n\nbuat secara singkat, tanpa catatan dan informasi tambahan, hanya isi formatnya saja\ndan tambahkan<br> di setiap  akhir kalimat"
            response_predict = model.generate_content(prompt_predict)
            predict_text = response_predict.text
            array_text = response_predict.text.split('\n')  # --> ['Line 1', 'Line 2', 'Line 3']
            bottom_filtered = ''
            top_filtered = ''
            bottom_filtered = array_text[3].replace('4. Harga Terendah: ', '')
            bottom_filtered = bottom_filtered.replace('<br>', '')
            top_filtered = array_text[4].replace('5. Harga Tertinggi: ', '')
            top_filtered = top_filtered.replace('<br>', '')

        except Exception as e:
            error_message = f"Terjadi kesalahan: {e}"

    #     try:
    #         # Koreksi nama kendaraan (opsional)
    #         nama_kendaraan_koreksi = nama_kendaraan  # Inisialisasi dengan nama asli
    #         if request.form.get("koreksi_nama"):
    #             response_koreksi = genai.GenerativeModel('gemini-1.5-pro')
    #             prompt_koreksi = response_koreksi.generate_content(f"Koreksi nama unit ini dengan nama yang benar dan singkat, anda bisa cari di internet. berikan response langsung nama nya tanpa perlu Nama unit yang benar adalah : {nama_kendaraan}")
    #             # Menampilkan hasil (asumsi atribut teks bernama 'text')
    #             if response_koreksi and hasattr(response_koreksi, 'text'):
    #                 print(response_koreksi.text)
    #             else:
    #                 print("Tidak ada respons yang dihasilkan atau format respons tidak valid.")

    #         # Analisis harga pasar (perbaikan pada prompt)

    #         response_harga = genai.GenerativeModel('gemini-1.5-pro')
    #         prompt_harga = response_harga.generate_content(f"Analisis kisaran harga pasar untuk {jenis_kendaraan} BEKAS {nama_kendaraan_koreksi} "
    #                         f"tahun {tahun_kendaraan} di wilayah {wilayah_kendaraan}. Sertakan informasi tentang: \n\n"
    #                         "1. Nama Mobil (lengkap sesuai pasar)\n"
    #                         "2. Tahun Mobil\n"
    #                         "3. Kota/Wilayah\n"
    #                         "4. Kisaran Harga Terendah\n"
    #                         "5. Kisaran Harga Tertinggi\n"
    #                         "6. Sumber informasi (misalnya situs web, platform jual beli, dll.)")
    #         # Menampilkan hasil (asumsi atribut teks bernama 'text')
    #         if response_harga and hasattr(response_harga, 'text'):
    #             print(response_harga.text)
    #         else:
    #             print("Tidak ada respons yang dihasilkan atau format respons tidak valid.")

    #     except Exception as e:
    #         error_message = f"Terjadi kesalahan: {e}"

    # return render_template("index.html", result_price=result_price, error_message=error_message, nama_kendaraan_koreksi=nama_kendaraan_koreksi)

    return render_template(
        "index.html",
        jenis_kendaraan = jenis_kendaraan,
        nama_kendaraan = nama_kendaraan,
        nama_kendaraan_koreksi = nama_kendaraan_koreksi,    
        tahun_kendaraan = tahun_kendaraan,
        km_kendaraan = km_kendaraan,
        transmisi = transmisi,
        bahan_bakar = bahan_bakar,
        wilayah_kendaraan = wilayah_kendaraan,
        predict_text = predict_text,
        bottom_filtered = bottom_filtered,
        top_filtered = top_filtered
    )


if __name__ == "__main__":
    app.run(debug=True)
