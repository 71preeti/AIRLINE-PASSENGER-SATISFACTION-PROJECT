from flask import Flask , render_template, url_for,request,redirect
import joblib   # used to import model file to get algorithm
import sqlite3


model_file_path= ".\models\logisticregre.lb"
model=joblib.load(model_file_path)

app=Flask(__name__)

@app.route('/')       # home url 
def home():
    return render_template("home.html")



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        
        # Save the contact to a file
        with open('contact.txt', 'a') as f:
            f.write(f"Name: {name}, Email: {email}, Message: {message}\n")
        
        return redirect(url_for('thank_you'))
    
    return render_template('contact.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')




@app.route('/about')
def about():
    return render_template("about.html")

@ app.route('/userdata')     # function ka namm url ke name se same hona chaiye
def userdata():
    return render_template('project.html')

@ app.route('/project')     # function ka namm url ke name se same hona chaiye
def project():
    return render_template('project.html')

@app.route('/predict',methods=['GET','POST'])   # form m submit button dbane ke bd data is url pr seen hoga
def predict():
    if request.method == 'POST':       # agr data post method se hoga tbi show hoga
        age = int(request.form['age'])    # form m age m jo value input hoge bo age variable m store hogi
        flight_distance = int(request.form['flight_distance'])
        inflight_entertainment = int(request.form['inflight_entertainment'])
        baggage_handling = int(request.form['baggage_handling'])
        cleanliness =int (request.form['cleanliness'])
        departure_delay = int(request.form['departure_delay'])
        arrival_delay =int( request.form['arrival_delay'])
        gender = int(request.form['gender'])
        customer_type = int(request.form['customer_type'])
        travel_type = int(request.form['travel_type'])
        class_type = request.form['class_type']

        economy=0  # output m eco,eco_plus,business ko numerical value m convert krna h 
        economy_plus=0
        if class_type == "ECO":
            economy=1
        elif class_type =="ECO_PLUS":
            economy_plus=1
        

        # output user data ko seen krne ke liye
        UNSEEN_DATA=[[age,flight_distance,inflight_entertainment,baggage_handling,cleanliness,departure_delay,arrival_delay,gender,customer_type,travel_type,economy,economy_plus]]
        # x_train variable :   unseen data must be in same orderr in x_train data
        # Age	Flight Distance	Inflight entertainment	Baggage handling	Cleanliness	Departure Delay in Minutes	Arrival Delay in Minutes	Gender_Male	Customer Type_disloyal Customer	Type of Travel_Personal Travel	Class_Eco	Class_Eco Plus

        # return UNSEEN_DATA # ye data bydefault hume string m show hota h to isse int m convert krte h jise data transformation kehte h isse data ko typecasting kehte h 

# ab algorithm se customer satisfaction ko predict krenegy 

        PREDICTION = model.predict(UNSEEN_DATA)[0]
        # print(PREDICTION)

        label_dict={0:' ☹️ DISSATISFIED ',1:' 😎 SATISFIED'}
        # return str(PREDICTION)

        query_to_insert="""
        Insert into CustomerDetails values(?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        conn=sqlite3.connect('customerdata.db')
        cur=conn.cursor()
        data=(age,flight_distance,inflight_entertainment,baggage_handling,cleanliness,departure_delay,arrival_delay,gender,customer_type,travel_type,economy,economy_plus,label_dict[PREDICTION])
        cur.execute(query_to_insert,data)
        conn.commit()
        print("Your record has been stored in database . ")
        cur.close()
        conn.close()





        return render_template('output.html',output=label_dict[PREDICTION])





if __name__=="__main__":
    app.run(debug=True)