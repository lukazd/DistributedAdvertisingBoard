let Mam = require('./MAM/lib/mam.node.js');
let IOTA = require('iota.lib.js');

var iota = new IOTA({ provider: 'https://iotanode.us:443' })

let data = 'Temperature: 22, Humidity: 23, Traffic: 5'

let seed = process.env.IOTA_SEED;

let mamState = null;

async function fetchStartCount(){
    let trytes = iota.utils.toTrytes('START');
    let message = Mam.create(mamState, trytes);
    console.log('The first root:');
    console.log(message.root);
    console.log();
    // Fetch all the messages upward from the first root.
    return await Mam.fetch(message.root, 'public', null, null);
}

async function publish(packet){
    // Create the message.
    let trytes = iota.utils.toTrytes(JSON.stringify(packet))
    let message = Mam.create(mamState, trytes);
    // Set the mam state so we can keep adding messages.
    mamState = message.state;
    console.log('Sending message: ', packet);
    console.log('Root: ', message.root);
    console.log('Address: ', message.address);
    console.log();
    // Attach the message.
    return await Mam.attach(message.payload, message.address);
}

// Initiate the mam state with the given seed at index 0.
mamState = Mam.init(iota, seed, 2, 0);

// Fetch all the messages in the stream.
fetchStartCount().then(v => {
    // Log the messages.
    let startCount = v.messages.length;
    console.log('Messages already in the stream:');
    for (let i = 0; i < v.messages.length; i++){
        let msg = v.messages[i];
        console.log(JSON.parse(iota.utils.fromTrytes(msg)));
    }
    console.log();

    // To add messages at the end we need to set the startCount for the mam state to the current amount of messages.
    mamState = Mam.init(iota, seed, 2, startCount);

	let newMessage = Date.now() + ' ' + data;

    // Now the mam state is set, we can add the message.
    publish(newMessage);
}).catch(ex => {
    console.log(ex);
});
