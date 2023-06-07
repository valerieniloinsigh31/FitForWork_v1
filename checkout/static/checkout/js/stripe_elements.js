var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);	
var clientSecret = $('#id_client_secret').text().slice(1, -1);	
var stripe = Stripe(stripePublicKey);	
var elements = stripe.elements();
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

//Handle real-time validation errors on the card element

card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
        <span class="icon" role="alert">
            <i class="fas fa-times"></i>
        </span>
        <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
 });

 // Handle form submit - taken from Stripe docs
var form = document.getElementById('payment-form'); //get form element

form.addEventListener('submit', function(ev) {
    ev.preventDefault(); //prevent default action to post
    card.update({ 'disabled': true}); //before call out to stripe-disable card element and submit button 
    $('#submit-button').attr('disabled', true); // to disable multiple submissions
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    stripe.confirmCardPayment(clientSecret, { //send card info securely to Stripe
        payment_method: {
            card: card,  //billing details to be filled
        }
    }).then(function(result) { //execute this function on the result
        if (result.error) {
            var errorDiv = document.getElementById('card-errors'); //if there is an error, as per above, put error into card errorDiv
            var html = `   
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            card.update({ 'disabled': false}); //if there is an error, we want to re-enable the card element and submit button to allow user to fix it
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});