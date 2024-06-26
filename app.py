import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import re

app = Flask(__name__)


# Access your API key as an environment variable.
os.environ["GOOGLE_API_KEY"] = "AIzaSyDPkQPzsnLh2uV_LSz9l93izD2MUP_z6U0"
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
    analisa_harga = None
    informasi_tambahan = ''
    linkArr = []
    image_kendaraan = ''
    array_text = ['', '', '', '', '', '']
    
    
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
            prompt_predict= f"Berikan Average Market Price untuk { jenis_kendaraan } Bekas {nama_kendaraan} tahun {tahun_kendaraan} wilayah {wilayah_kendaraan} dengan format sebagai berikut:\[Harga Terendah]\n[Harga Tertinggi]\nlink presisi Sumber Analisa Harga (cukup 2 sumber berbeda dari olx dan oto yang menjual mobil tesebut per baris)\nKalimat Informasi Tambahan\n1 link image kendaraan tersebut\nlangsung isi format dengan jawabannya nya saja tidak perlu mencantumkan kembali : dan tambahkan <br> di setiap akhir kalimat\n\n contoh hasil nya harus selalu seperti ini:\n\nRp. 260.000.000\nRp. 300.000.000 <br>\nhttps://www.olx.co.id/items/toyota-innova-2-0-g-mt-2021-second-semarang_i2367454232 <br>\nhttps://www.oto.com/mobil-bekas/toyota/innova/2021/semarang/toyota-innova-20-g-mt-2021-semarang-28145824 <br>\nHarga mobil bekas Toyota Innova 2.0 G MT tahun 2021 di Semarang berkisar antara Rp. 260.000.000 hingga Rp. 300.000.000. Harga ini dapat bervariasi tergantung kondisi, kilometer, dan kelengkapan mobil. <br>\nhttps://[link image mobil (non-encrypted) yang dapat ditampilkan]"
            response_predict = model.generate_content(prompt_predict)
            # print(response_predict.text)
            predict_text = response_predict.text
            array_text = response_predict.text.split('\n')  # --> ['Line 1', 'Line 2', 'Line 3']
            print(response_predict.text)
            print(array_text)
            bottom_filtered = ''
            top_filtered = ''
            bottom_filtered = array_text[0]
            bottom_filtered = bottom_filtered.replace('<br>', '')
            top_filtered = array_text[1]
            top_filtered = top_filtered.replace('<br>', '')
            informasi_tambahan = array_text[0]

            
            
            
            # Mengambil list sumber analisa harga
            def is_valid_url(url):
                url_regex = re.compile(r'https?://(?:www\.)?[a-zA-Z0-9./]+')
                return bool(url_regex.match(url))
            
            for x in array_text:
                if is_valid_url(x):
                    linkArr.append(x.replace('<br>',''))
            
        
            

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
        top_filtered = top_filtered,
        linkArr1 = array_text[2].replace('<br>' ,''),
        linkArr2 = array_text[3].replace('<br>' ,''),
        informasi_tambahan = array_text[4].replace('<br>' ,''),
        image_kendaraan = array_text[5].replace('<br>' ,'')
    )


if __name__ == "__main__":
    app.run(debug=True)
