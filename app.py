from flask import Flask, request, render_template, send_file
import asyncio
from pyppeteer import launch
import io

app = Flask(__name__)

async def url_to_pdf(url):
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    # Espera adicional de 5 segundos para que cargue todo el contenido
    await asyncio.sleep(5)
    pdf_bytes = await page.pdf(format='A4')
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
                download_name="salida.pdf",
                as_attachment=True,
                mimetype='application/pdf'
            )
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=False, port=5001)
