from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_reply(msg):
    msg = msg.lower().strip()

    if 'hi' in msg or 'hello' in msg or 'hey' in msg:
        return "Hello! Welcome to Spice Garden restaurant. How can I help you?"

    elif 'menu' in msg or 'food' in msg or 'eat' in msg or 'dish' in msg:
        return "Our menu has Biryani, Karahi, Nihari, Burgers, Pasta and Grilled items. We also have fresh juices and desserts."

    elif 'price' in msg or 'cost' in msg or 'how much' in msg or 'rate' in msg:
        return "Biryani is Rs.350, Karahi is Rs.500, Burgers start from Rs.200, Pasta is Rs.280. Drinks are Rs.80 to Rs.150."

    elif 'time' in msg or 'open' in msg or 'hour' in msg or 'close' in msg:
        return "We are open daily from 12pm to 12am midnight. On fridays we open at 1pm due to prayers."

    elif 'location' in msg or 'address' in msg or 'where' in msg:
        return "We are at Plot 12, Main Boulevard, Gulberg Lahore. Near the petrol pump."

    elif 'reservation' in msg or 'book' in msg or 'table' in msg or 'reserve' in msg:
        return "To book a table call us at 042-35761234. We recommend booking 1 day before for weekends."

    elif 'delivery' in msg or 'order online' in msg or 'deliver' in msg:
        return "Yes we do home delivery! Order on our number 042-35761234 or through foodpanda. Delivery in 45 minutes."

    elif 'parking' in msg or 'park' in msg:
        return "Yes free parking is available in front and behind the restaurant."

    elif 'wifi' in msg or 'internet' in msg or 'password' in msg:
        return "Free wifi is available. Password is SpiceGarden2024."

    elif 'special' in msg or 'deal' in msg or 'offer' in msg:
        return "Today special is Mutton Karahi + Naan + Drink for Rs.700 only. Every Tuesday we have family deal for Rs.1500."

    elif 'vegetarian' in msg or 'veg' in msg:
        return "Yes we have vegetarian options like daal, vegetable pasta, cheese pizza and salads."

    elif 'birthday' in msg or 'event' in msg or 'party' in msg:
        return "We do birthday parties and events! Call us to arrange. We decorate the area for free for groups of 10 or more."

    elif 'bye' in msg or 'goodbye' in msg or 'thanks' in msg or 'thank you' in msg:
        return "Thank you! Visit us again. Have a good day!"

    else:
        return "Sorry I didn't understand. You can ask about our menu, prices, timing, location or delivery."


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    user_msg = request.json['msg']
    bot_reply = get_reply(user_msg)
    return jsonify({'reply': bot_reply})


if __name__ == '__main__':
    app.run(debug=True)
