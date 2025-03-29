from flask import Flask, request, render_template, send_file
import asyncio
import nest_asyncio
from pyppeteer import launch
import io
import os

app = Flask(__name__)
nest_asyncio.apply()  # Para permitir asyncio.run en Flask

async def url_to_pdf(url):
    # Obtener la ruta de Chromium desde CHROME_BIN (definida en Dockerfile) o usar /usr/bin/chromium
    chrome_path = os.environ.get('PUPPETEER_EXECUTABLE_PATH', '/usr/bin/chromium-browser')
    browser = await launch(
        executablePath=chrome_path,
        args=[
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-setuid-sandbox'
        ]
    )
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await asyncio.sleep(5)  # Esperar que Wix (o tu página) cargue completamente
    pdf_bytes = await page.pdf(format='A4', printBackground=True)
    await browser.close()
    return pdf_bytes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if url:
            pdf = asyncio.run(url_to_pdf(url))
            return send_file(
                io.BytesIO(pdf),
                download_name="certificado.pdf",
                as_attachment=True,
                mimetype='application/pdf'
            )
    return render_template('index.html')

if __name__ == '__main__':
    # En local, Flask se ejecuta en 0.0.0.0:8080
    app.run(host="0.0.0.0", port=8080)
