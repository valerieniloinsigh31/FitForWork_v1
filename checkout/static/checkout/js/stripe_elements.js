var stripe_public_key = $('#id_stripe_public_key').text.slice(1,-1); //using jquery. script elements contain the values we need as their text
//retrieve them using their ids and .text function. 
var client_secret = $('#id_client_secret').text.slice(1,-1);
var stripe = Stripe(stripe_public_key); //made possible by stripe js included in base.html, to set up stripe, create variable using public key
var elements = stripe.elements(); //use it to create an instance of stripe elements
var style = {
    base: {
        color: '#000', //default color of black
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545', //updated to match text-danger class
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style}); //use elements variable to create a card element
card.mount('#card-element',);//mount card element to the div create in the last video. Card element can accept style args