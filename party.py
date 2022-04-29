"""Flask site for Balloonicorn's Party."""

from flask import Flask, session, render_template, request, flash, redirect

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


def is_mel(name, email):
    """Is this user Mel?

    >>> is_mel('Judith Butler', 'judith@awesome.com')
    False

    >>> is_mel('Mel Melitpolski', 'mel@ubermelon.com')
    True

    >>> is_mel('Mel', 'mel@ubermelon.com')
    True
    """

    return name == "Mel Melitpolski" or email == "mel@ubermelon.com"


def most_and_least_common_type(treats):
    """Given list of treats, return most and least common treat types.

    :param: list of dictionaries where each dictionary has at least one key, "type"

    Return most and least common treat types in tuple of format (most, least).

    >>> treats = [
    ...     {'type': 'dessert'},
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'dessert'},
    ...     {'type': 'appetizer'},
    ...     {'type': 'drink'},
    ... ]
    
    >>> most_and_least_common_type(treats)
    ('dessert', 'drink')

    >>> most_and_least_common_type([])
    (None, None)

    >>> most_and_least_common_type([{'type': 'dessert'}])
    ('dessert', 'dessert')
    """
    # Initialize an empty dictionary
    types = {}

    # Count number of each type from our list of dictionaries
    for treat in treats:
        # If the treat exists in our types dictionary, update it by incrementing by one; otherwise, add one 
        types[treat['type']] = types.get(treat['type'], 0) + 1

    # Initialize most_type as None and assign the value to most_count
    most_count = most_type = None
    # Initialize least_type as None and assign the value to least_count
    least_count = least_type = None

    # Find most, least common
    # for key (treat_type), value(count) in dictionary(types):
    for treat_type, count in types.items():
        if most_count is None or count > most_count:
            most_count = count
            most_type = treat_type

        if least_count is None or count < least_count:
            least_count = count
            least_type = treat_type

    return (most_type, least_type)


def get_treats():
    """Return treats being brought to the party.

    One day, I'll move this into a database! -- Balloonicorn
    """

    return [
        {'type': 'dessert',
         'description': 'Chocolate mousse',
         'who': 'Leslie'},
        {'type': 'dessert',
         'description': 'Cardamom-Pear pie',
         'who': 'Joel'},
        {'type': 'appetizer',
         'description': 'Humboldt Fog cheese',
         'who': 'Meggie'},
        {'type': 'dessert',
         'description': 'Lemon bars',
         'who': 'Bonnie'},
        {'type': 'appetizer',
         'description': 'Mini-enchiladas',
         'who': 'Katie'},
        {'type': 'drink',
         'description': 'Sangria',
         'who': 'Anges'},
        {'type': 'dessert',
         'description': 'Chocolate-raisin cookies',
         'who': 'Henry'},
        {'type': 'dessert',
         'description': 'Brownies',
         'who': 'Sarah'}
    ]


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/treats")
def show_treats():
    """Show treats people are bringing."""

    treats = get_treats()

    most, least = most_and_least_common_type(get_treats())

    return render_template("treats.html",
                           treats=treats,
                           most=most,
                           least=least)


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    if not is_mel(name, email):
        session['rsvp'] = True
        flash("Yay!")
        return redirect("/")

    else:
        flash("Sorry, Mel. This is kind of awkward.")
        return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")
