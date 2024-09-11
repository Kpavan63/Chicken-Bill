from flask import Flask, request, jsonify, make_response, render_template_string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from datetime import datetime
import pytz
import json
import requests
from PIL import Image

app = Flask(__name__)

# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chicken Billing System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }

        nav {
            width: 100%;
            background-color: #4CAF50; 
            overflow: auto;
        }

        nav ul {
            padding: 0;
            list-style: none;
            margin: 0;
            display: flex;
            justify-content: center;
        }

        nav ul li {
            display: inline;
        }

        nav ul li a {
            text-decoration: none;
            color: white;
            padding: 15px 20px;
            display: block;
        }

        nav ul li a:hover {
            background-color: #575757;
        }

        .container {
            text-align: center;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
            margin: 20px auto;
        }

        table {
            width: 80%;
            border-collapse: collapse;
            margin: 20px auto;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        table, th, td {
            border: 1px solid #ddd;
        }

        th, td {
            padding: 12px;
            text-align: left;
        }

        th {
            background-color: #f4f4f4;
            color: #333;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        tr:hover {
            background-color: #f1f1f1;
        }

    
        .btn {
            display: block;
            width: 200px;
            padding: 10px;
            margin: 10px auto;
            font-size: 18px;
            color: white;
            background-color: #007bff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .btn:hover {
            background-color: #0056b3;
        }

        .success-message {
            margin-top: 20px;
            color: green;
            font-weight: bold;
        }

        section {
            display: none;
            padding: 20px;
        }

        section.active {
            display: block;
        }
        caption{
            text-align:center;
            font-size:25px;
            font-weight:bold;
            margin-bottom:30px;
        }
        /* Styling for the label */
label {
    display: block; /* Ensures label and input are on separate lines */
    margin-bottom: 5px; /* Adds a small gap between label and input */
    font-weight: bold; /* Makes the label text bold */
}

/* Styling for the input field */
input[type="text"] {
    width: 100%; /* Makes the input field expand to fill its container */
    padding: 8px; /* Adds padding inside the input field */
    border: 1px solid #ccc; /* Adds a border around the input field */
    border-radius: 4px; /* Adds rounded corners to the input field */
    box-sizing: border-box; /* Ensures padding and border are included in the input's total width */
    font-size: 14px; /* Sets the font size of the input field */
}

/* Optional: Styling for the placeholder text */
input[type="text"]::placeholder {
    color: #999; /* Sets the color of the placeholder text */
}
/* Add this CSS to style the modal */
.modal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
    background-color: #fefefe;
    margin: 15% auto; /* 15% from the top and centered */
    padding: 20px;
    border: 1px solid #888;
    width: 80%; /* Could be more or less, depending on screen size */
}

/* Close Button */
.close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
}

.close:hover,
.close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
}


        .summary {
    display: flex;
    justify-content: space-between;
}

.card {
    width: calc(33.33% - 20px); /* Three cards in a row with margin */
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.card h2{
    text-align:center;
}
.card div{
    text-align:center;
}
/* Media query for responsive design */
@media (max-width: 768px) {
    .summary {
        flex-wrap: wrap; /* Wrap cards in a row for smaller screens */
    }

    .card {
        width: calc(100% - 20px); /* Two cards in a row for smaller screens */
        margin-bottom: 20px; /* Add margin at the bottom of each card */
    }
}

@media (max-width: 480px) {
    .card {
        width: calc(100% - 20px); /* Single card per row for small screens */
    }
}


    </style>

</head>
<body>

    <nav>
        <ul>
            <li><a href="#billing-boiler" onclick="showSection('billing-boiler')">Boiler Chicken</a></li>
            <li><a href="#billing-nattukodi" onclick="showSection('billing-nattukodi')">Nattukodi Chicken</a></li>
            <li><a href="#billing-juttukodi" onclick="showSection('billing-juttukodi')">Juttukodi Chicken</a></li>
            <li><a href="#entries" onclick="showSection('entries')">Entries</a></li>
        </ul>
    </nav>
    <section id="billing-boiler">
        <div class="container">
            <h1>Boiler Chicken Billing</h1>
            <button class="btn" onclick="insertData('Boiler Chicken', '100 Rupees')">100 Rupees</button>
            <button class="btn" onclick="insertData('Boiler Chicken', '50 Rupees')">50 Rupees</button>
            <button class="btn" onclick="insertData('Boiler Chicken', '200 Rupees')">200 Rupees</button>
            <button class="btn" onclick="insertData('Boiler Chicken', '1 KG', '220 Rupees', '1 KG')">1 KG</button>
            <button class="btn" onclick="insertData('Boiler Chicken', '500 Grams', '110 Rupees', '500 Grams')">500 Grams</button>
            <button class="btn" onclick="insertData('Boiler Chicken', '250 Grams', '55 Rupees', '250 Grams')">250 Grams</button>
            <button class="btn" onclick="insertData('Boiler Chicken', '750 Grams', '165 Rupees', '750 Grams')">750 Grams</button>
            <label for="boiler-amount">Amount:</label>
        <input type="text" id="boiler-amount" placeholder="Enter amount">
        <button class="btn" onclick="insertData('Boiler Chicken', document.getElementById('boiler-amount').value + ' Rupees')">Add Entry</button>
            <div id="success-message-boiler" class="success-message"></div>
        </div>
    </section>

    <section id="billing-nattukodi">
        <div class="container">
            <h1>Nattukodi Chicken Billing</h1>
            <button class="btn" onclick="insertData('Nattukodi Chicken', '100 Rupees')">100 Rupees</button>
            <button class="btn" onclick="insertData('Nattukodi Chicken', '50 Rupees')">50 Rupees</button>
            <button class="btn" onclick="insertData('Nattukodi Chicken', '200 Rupees')">200 Rupees</button>
            <button class="btn" onclick="insertData('Nattukodi Chicken', '1 KG', '620 Rupees', '1 KG')">1 KG</button>
            <button class="btn" onclick="insertData('Nattukodi Chicken', '500 Grams', '310 Rupees', '500 Grams')">500 Grams</button>
            <button class="btn" onclick="insertData('Nattukodi Chicken', '250 Grams', '155 Rupees', '250 Grams')">250 Grams</button>
            <button class="btn" onclick="insertData('Nattukodi Chicken', '750 Grams', '465 Rupees', '750 Grams')">750 Grams</button>
            <label for="nattukodi-amount">Amount:</label>
        <input type="text" id="nattukodi-amount" placeholder="Enter amount">
        <button class="btn" onclick="insertData('Nattukodi Chicken', document.getElementById('nattukodi-amount').value + ' Rupees')">Add Entry</button>
            <div id="success-message-nattukodi" class="success-message"></div>
        </div>
    </section>

    <section id="billing-juttukodi">
        <div class="container">
            <h1>Juttukodi Chicken Billing</h1>
            <button class="btn" onclick="insertData('Juttukodi Chicken', '100 Rupees')">100 Rupees</button>
            <button class="btn" onclick="insertData('Juttukodi Chicken', '50 Rupees')">50 Rupees</button>
            <button class="btn"  onclick="insertData('Juttukodi Chicken', '200 Rupees')">200 Rupees</button>
            <button class="btn" onclick="insertData('Juttukodi Chicken', '1 KG', '220 Rupees', '1 KG')">1 KG</button>
            <button class="btn" onclick="insertData('Juttukodi Chicken', '500 Grams', '110 Rupees', '500 Grams')">500 Grams</button>
            <button class="btn" onclick="insertData('Juttukodi Chicken', '250 Grams', '55 Rupees', '250 Grams')">250 Grams</button>
            <button class="btn" onclick="insertData('Juttukodi Chicken', '750 Grams', '165 Rupees', '750 Grams')">750 Grams</button>
            <label for="juttukodi-amount">Amount:</label>
        <input type="text" id="juttukodi-amount" placeholder="Enter amount">
        <button class="btn" onclick="insertData('Juttukodi Chicken', document.getElementById('juttukodi-amount').value + ' Rupees')">Add Entry</button>
            <div id="success-message-juttukodi" class="success-message"></div>
        </div>
    </section>

    <section id="entries">
        <div class="container-pp">
            <h1 style="text-align:center;">Entries</h1>
            <!-- Tables here -->
            <table id="boiler-table">
                <caption>Boiler Chicken Entries</caption>
                <thead>
                    <tr>
                        <th>Amount</th>
                        <th>Price</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Weight</th>
                        <th>Print</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
            <table id="nattukodi-table">
                <caption>Nattukodi Chicken Entries</caption>
                <thead>
                    <tr>
                        <th>Amount</th>
                        <th>Price</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Weight</th>
                        <th>Print</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
            <table id="juttukodi-table">
                <caption>Juttukodi Chicken Entries</caption>
                <thead>
                    <tr>
                        <th>Amount</th>
                        <th>Price</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Weight</th>
                        <th>Print</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
            <div class="summary">
    <div class="card">
        <h2>Boiler</h2>
        <div id="boiler-total-price"></div>
        <div id="boiler-total-weight"></div>
    </div>
    <div class="card">
        <h2>Nattukodi</h2>
        <div id="nattukodi-total-price"></div>
        <div id="nattukodi-total-weight"></div>
    </div>
    <div class="card">
        <h2>Juttukodi</h2>
        <div id="juttukodi-total-price"></div>
        <div id="juttukodi-total-weight"></div>
    </div>
</div>
        </div>
    </section>
     
    <!-- Add this HTML for the modal at the end of your body tag -->
<div id="printOptionsModal" class="modal">
    <div class="modal-content">
        <span class="close">&times;</span>
        <div id="printOptionsContent"></div>
    </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.4.0/jspdf.umd.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.13/jspdf.plugin.autotable.min.js"></script>

<script>
    // Function to generate PDF
    async function generatePDF(type, date, time, amount, price, weight) {
        // Create a new jsPDF instance
        const doc = new jsPDF();

        // Add content to the PDF
        doc.text(`Type: ${type}, Date: ${date}, Time: ${time}, Amount: ${amount}, Price: ${price}, Weight: ${weight}`, 10, 10);

        // Save the PDF
        doc.save(`${type}_${date}.pdf`);
    }

    // Function to handle print options modal
    function showPrintOptions(type, date, time, amount, price, weight) {
        const printOptionsHtml = `
            <div>
                <button onclick="printToPOS('${type}', '${date}', '${time}', '${amount}', '${price}', '${weight}')">Print to POS</button>
                <button onclick="generatePDF('${type}', '${date}', '${time}', '${amount}', '${price}', '${weight}')">Generate PDF</button>
            </div>
        `;

        // Set the content of the modal
        document.getElementById('printOptionsContent').innerHTML = printOptionsHtml;

        // Show the modal
        document.getElementById('printOptionsModal').style.display = 'block';
    }

    // Function to close modal
    function closeModal() {
        document.getElementById('printOptionsModal').style.display = 'none';
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        const modal = document.getElementById('printOptionsModal');
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
</script>













    <script>
        async function fetchData() {
            try {
                const response = await fetch('/get-entries');
                const data = await response.json();
                populateTable(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }

        function populateTable(data) {
            const boilerTableBody = document.querySelector('#boiler-table tbody');
            const nattukodiTableBody = document.querySelector('#nattukodi-table tbody');
            const juttukodiTableBody = document.querySelector('#juttukodi-table tbody');
            boilerTableBody.innerHTML = '';
            nattukodiTableBody.innerHTML = '';
            juttukodiTableBody.innerHTML = '';

            data.forEach(entry => {
            const date = new Date(entry.timestamp);
            const formattedDate = date.toLocaleDateString('en-IN');
            const formattedTime = date.toLocaleTimeString('en-IN');
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${entry.amount}</td>
                <td>${entry.price}</td>
                <td>${formattedDate}</td>
                <td>${formattedTime}</td>
                <td>${entry.weight || ''}</td>
                <td>
                    <button onclick="showPrintOptions('${entry.type}', '${formattedDate}', '${formattedTime}', '${entry.amount}', '${entry.price}', '${entry.weight || ''}')">Print</button>
                </td>
            `;

            if (entry.type === 'Boiler Chicken') {
                boilerTableBody.appendChild(row);
            } else if (entry.type === 'Nattukodi Chicken') {
                nattukodiTableBody.appendChild(row);
            } else if (entry.type === 'Juttukodi Chicken') {
                juttukodiTableBody.appendChild(row);
            }
        });
            calculateSummary(data);
        }

        function showPrintOptions(type, date, time, amount, price, weight) {
    const printOptionsHtml = `
        <div>
            <button onclick="printToPOS('${type}', '${date}', '${time}', '${amount}', '${price}', '${weight}')">Print to POS</button>
            <button onclick="generatePDF('${type}', '${date}', '${time}', '${amount}', '${price}', '${weight}')">Generate PDF</button>
        </div>
    `;

    // Set the content of the modal
    document.getElementById('printOptionsContent').innerHTML = printOptionsHtml;

    // Show the modal
    document.getElementById('printOptionsModal').style.display = 'block';
}

// When the user clicks on <span> (x), close the modal
document.querySelector('.close').onclick = function() {
    document.getElementById('printOptionsModal').style.display = 'none';
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    const modal = document.getElementById('printOptionsModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}


        async function printToPOS(type, date, time, amount, price, weight) {
            // Implement the POS printing logic here
            console.log('Printing to POS:', type, date, time, amount, price, weight);
        }

        async function generatePDF(type, date, time, amount, price, weight) {
            const response = await fetch('/generate-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ type, date, time, amount, price, weight })
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${type}_${date}.pdf`;
                document.body.appendChild(a);
                a.click();
                a.remove();
            } else {
                console.error('Error generating PDF');
            }
        }

        function calculateSummary(data) {
            let boilerTotalPrice = 0;
            let boilerTotalWeight = 0;
            let nattukodiTotalPrice = 0;
            let nattukodiTotalWeight = 0;
            let juttukodiTotalPrice = 0;
            let juttukodiTotalWeight = 0;

            data.forEach(entry => {
                if (entry.price) {
                    const priceValue = parseInt(entry.price.replace(/[^0-9]/g, ''));
                    if (entry.type === 'Boiler Chicken') {
                        boilerTotalPrice += priceValue;
                    } else if (entry.type === 'Nattukodi Chicken') {
                        nattukodiTotalPrice += priceValue;
                    } else if (entry.type === 'Juttukodi Chicken') {
                        juttukodiTotalPrice += priceValue;
                    }
                }
                if (entry.weight) {
                    const weightValue = parseFloat(entry.weight.split(' ')[0]);
                    const weightUnit = entry.weight.split(' ')[1];
                    if (entry.type === 'Boiler Chicken') {
                        if (weightUnit === 'KG') {
                            boilerTotalWeight += weightValue;
                        } else if (weightUnit === 'Grams') {
                            boilerTotalWeight += weightValue / 1000;
                        }
                    } else if (entry.type === 'Nattukodi Chicken') {
                        if (weightUnit === 'KG') {
                            nattukodiTotalWeight += weightValue;
                        } else if (weightUnit === 'Grams') {
                            nattukodiTotalWeight += weightValue / 1000;
                        }
                    } else if (entry.type === 'Juttukodi Chicken') {
                        if (weightUnit === 'KG') {
                            juttukodiTotalWeight += weightValue;
                        } else if (weightUnit === 'Grams') {
                            juttukodiTotalWeight += weightValue / 1000;
                        }
                    }
                }
            });

            document.getElementById('boiler-total-price').textContent = `Total Price: ${boilerTotalPrice} Rupees`;
            document.getElementById('boiler-total-weight').textContent = `Total Weight: ${boilerTotalWeight.toFixed(2)} KG`;

            document.getElementById('nattukodi-total-price').textContent = `Total Price: ${nattukodiTotalPrice} Rupees`;
            document.getElementById('nattukodi-total-weight').textContent = `Total Weight: ${nattukodiTotalWeight.toFixed(2)} KG`;

            document.getElementById('juttukodi-total-price').textContent = `Total Price: ${juttukodiTotalPrice} Rupees`;
            document.getElementById('juttukodi-total-weight').textContent = `Total Weight: ${juttukodiTotalWeight.toFixed(2)} KG`;
        }

        async function insertData(type, amount, price = null, weight = null) {
            const entry = { type, amount, price: price || amount, weight: weight || null };

            try {
                const response = await fetch('/add-entry', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(entry)
                });

                if (response.ok) {
                    showSuccessMessage(type);
                    await fetchData();
                } else {
                    console.error('Error adding entry');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }

        function showSuccessMessage(type) {
            let successMessageDiv;
            if (type === 'Boiler Chicken') {
                successMessageDiv = document.getElementById('success-message-boiler');
            } else if (type === 'Nattukodi Chicken') {
                successMessageDiv = document.getElementById('success-message-nattukodi');
            } else if (type === 'Juttukodi Chicken') {
                successMessageDiv = document.getElementById('success-message-juttukodi');
            }

            successMessageDiv.textContent = `Entry added successfully for ${type}`;
            setTimeout(() => {
                successMessageDiv.textContent = '';
            }, 3000);
        }

        function showSection(sectionId) {
            document.querySelectorAll('section').forEach(section => {
                section.classList.remove('active');
            });
            document.getElementById(sectionId).classList.add('active');
            if (sectionId === 'entries') {
                fetchData();
            }
        }

        window.onload = () => {
            showSection('billing-boiler');
        };
    </script>
    </body>
</html>
"""
# Function to download image from a URL
def download_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# Flask routes
@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/get-entries', methods=['GET'])
def get_entries():
    try:
        with open('entries.json', 'r') as file:
            entries = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        entries = []  # Use empty list if no data found

    return jsonify(entries)

@app.route('/add-entry', methods=['POST'])
def add_entry():
    try:
        data = request.json
        entry_type = data['type']
        amount = data['amount']
        price = data['price']
        weight = data.get('weight')
        timestamp = datetime.now(pytz.timezone('Asia/Kolkata')).isoformat()
        entry = {'type': entry_type, 'amount': amount, 'price': price, 'timestamp': timestamp, 'weight': weight}

        try:
            with open('entries.json', 'r') as file:
                entries = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            entries = []

        entries.append(entry)

        with open('entries.json', 'w') as file:
            json.dump(entries, file, indent=2)

        return jsonify({'message': 'Entry added'}), 201
    except Exception as e:
        print(f"Error adding entry: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

# Function to calculate the center position of the page
def center_text(c, text, font_size, page_width):
    text_width = c.stringWidth(text, "Helvetica", font_size)
    return (page_width - text_width) / 2

# Flask routes
@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.json
        entry_type = data['type']
        date = data['date']
        time = data['time']
        amount = data['amount']
        price = data['price']
        weight = data['weight']

        # Download background image from URL
        background_image_url = "https://img.freepik.com/premium-photo/stage-white-smoke-spotlight_327072-352.jpg?w=1060"
        background_image = download_image(background_image_url)

        # Save the background image to a buffer
        img_buffer = BytesIO()
        background_image.save(img_buffer, format='JPEG')
        img_buffer.seek(0)

        # Create a PDF buffer
        buffer = BytesIO()

        # Create a canvas
        c = canvas.Canvas(buffer, pagesize=letter)

        # Draw the background image
        c.drawImage(ImageReader(img_buffer), 0, 0, width=letter[0], height=letter[1])

        # Draw the shop name in the center
        shop_name = "Your Shop Name"
        shop_name_x = center_text(c, shop_name, 24, letter[0])
        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(1, 1, 1)  # Set font color to white
        c.drawString(shop_name_x, 750, shop_name)

        # Write the content to the PDF
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(1, 1, 1)  # Set font color to white
        c.drawString(center_text(c, f"Type: {entry_type}", 12, letter[0]), 700, f"Type: {entry_type}")
        c.drawString(center_text(c, f"Date: {date}", 12, letter[0]), 680, f"Date: {date}")
        c.drawString(center_text(c, f"Time: {time}", 12, letter[0]), 660, f"Time: {time}")
        c.drawString(center_text(c, f"Amount: {amount}", 12, letter[0]), 640, f"Amount: {amount}")
        c.drawString(center_text(c, f"Price: {price}", 12, letter[0]), 620, f"Price: {price}")
        c.drawString(center_text(c, f"Weight: {weight}", 12, letter[0]), 600, f"Weight: {weight}")

        # Save the PDF
        c.save()

        # Reset the buffer position
        buffer.seek(0)

        # Create a response and set headers
        response = make_response(buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

        return response
    except Exception as e:
        print("Error generating PDF:", e)
        return jsonify({'error': 'Error generating PDF'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5500)
