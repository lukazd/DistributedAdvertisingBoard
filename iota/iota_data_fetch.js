// Firestore setup
const admin = require('firebase-admin');
var serviceAccount = require('../keys/distributedadvertisingboard-firebase-adminsdk-uolqk-2634f4c974.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

var db = admin.firestore();

// IOTA setup
var Mam = require('./MAM/lib/mam.node.js')
var IOTA = require('iota.lib.js')
var iota = new IOTA({ provider: 'http://node04.iotatoken.nl:14265' })

// Init State
//let root = 'ZMYUUZSLALHDLXXQGAKZSZNIDWXJEHYDIWBVRJFCOYDTXSDXMFQBODQGWLU9YEDHOIKOREDYHPXHMBAPI'
let root = "XMHQELYZVSDEMWVCSNKCFUMMWJZOJGBCD9EKZVNLETHIBIZEIHBGFEBWQLEVQYKEMBOPPDRGJSNE9WRHB"
root = "MFVBJH9FPOEANMMVIJFIKEEYCZZN9EJZGJMYWQQZEGBKTULAEEOQRVGMIPJLPOU9ZFFDJZVMH9KVMTWYE"
let nextRoot = root

// Initialise MAM State
var mamState = Mam.init(iota)

// Publish to tangle
const publish = async packet => {
  var trytes = iota.utils.toTrytes(JSON.stringify(packet))
  var message = Mam.create(mamState, trytes)
  mamState = message.state
  await Mam.attach(message.payload, message.address)
  return message.root
}


// Callback used to pass data out of the fetch
const logData = data => console.log(JSON.parse(iota.utils.fromTrytes(data)))

async function execute() {
  var resp = await Mam.fetchSingle(nextRoot, 'public', null)

  if (resp != null) {
    // This is needed to get the next data
    nextRoot = resp.nextRoot
    //messages = iota.utils.fromTrytes(resp.messages)
    messages = iota.utils.fromTrytes(resp.payload)
    console.log(messages)
  }

  setTimeout(() => execute(), 1000)
}

execute()
