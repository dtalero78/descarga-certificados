from flask import Flask, request, render_template, send_file
import asyncio
import nest_asyncio
from pyppeteer import launch
import io
import os

nest_asyncio.apply()

app = Flask(__name__)

async def url_to_pdf(url):
    browser = await launch(args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    await asyncio.sleep(5)  # espera adicional
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False, threaded=False)
