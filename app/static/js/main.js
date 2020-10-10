console.log('Sanity check!')

// get stripe publishable key
fetch('/config')
.then(
    (result) => { return result.json();}
)
.then(
    (data) => {
        // Initialize stripe
        const stripe = Stripe(data.publicKey);
    }
);