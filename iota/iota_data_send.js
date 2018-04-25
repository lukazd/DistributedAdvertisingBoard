let Mam = require('./MAM/lib/mam.node.js');
let IOTA = require('iota.lib.js');

//var iota = new IOTA({ provider: 'https://iotanode.us:443' })
var iota = new IOTA({ provider: 'http://node04.iotatoken.nl:14265' })

let data = 'KDHGKCGIEJAKCKNGdagiengkakdhgkaidoqhdjgnajbajdfqpoifasdjknflakndgsdlfkjsldkfjsldkfjlksdflkjsdflkjsdlfkjsdfkljsdflkjsdflkjsdflkjsdflkjsdflkjsflkjsdflkjsdflkjsdflkjsdflkjsdflkjsdflkjsdlfkjsdflkjsflkjsdlfkjsdflkjsdflkjsfdlkjsflkjsdlkjsfkljsdflkjsflkjsflkjsflkjsdflkjsflkjsflkjsdlfkjsdfkj'

let seed = process.env.IOTA_SEED;

let mamState = null;

// Initiate the mam state with the given seed at index 0.
mamState = Mam.init(iota, seed, 2, 0);

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

function publishData(data){
    // Fetch all the messages in the stream.
    if (mamState != null) {
        publish(data)
        return
    }

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

        // Now the mam state is set, we can add the message.
        publish(data);
    }).catch(ex => {
        console.log(ex);
    });
}
