from flask import Flask, render_template, url_for, request, send_file
import docxtpl
from num_to_rus import Converter


def zeroCheck(num):
	if str(num)[-2:] == ".0":
		return str(num) + "0"
	return num


def convert_date(date_str):
    year, month, day = map(int, date_str.split('-'))

    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

    output1 = f"{day:02d}.{month:02d}.20{year%100:02d}г"
    output2 = f"{day} {months[month-1]} {year}"
    
    return output1, output2

def doc_generator(number, fulldate, mindate, fullname, address, term, tel, mail, pre_cost, cost):
		doc = docxtpl.DocxTemplate("Договор.docx")
		rub = cost[:-3]
		context = { 'number' : number,
					'fulldate' : fulldate,
					'mindate' : mindate,
					'fullname' : fullname, 
					'address' : address, 
					'term' : term, 
					'tel' : tel, 
					'mail' : mail,
					'pre_cost' : f"{pre_cost} рублей",
					'ncost': f"{Converter().convert(int(rub))} рублей {cost[-2:]} коп.",
					'cost' : f"{cost} коп",
					'post_cost' : f"{zeroCheck(round(float(cost) - float(pre_cost), 2))} рублей"}
		doc.render(context)
		doc.save("document.docx")

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/forward/", methods=["POST"])
def move_forward():
    number = request.form.get("user_number")
    input_date = request.form.get("user_date")
    fullname = request.form.get("user_name")
    address = request.form.get("user_address")
    term =  request.form.get("user_time")
    tel = request.form.get("user_tel")
    email = request.form.get("user_email")
    pre_cost = request.form.get("user_pre_cost")
    cost = request.form.get("user_cost")
    output1, output2 = convert_date(input_date)
    doc = doc_generator(number, output2, output1, fullname, address, term, tel, email, pre_cost, cost)
    return send_file("document.docx", as_attachment=True)

if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0')
