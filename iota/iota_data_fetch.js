var Mam = require('./MAM/lib/mam.node.js')
var IOTA = require('iota.lib.js')
//var iota = new IOTA({ provider: 'https://iotanode.us:443'})
var iota = new IOTA({ provider: 'http://node04.iotatoken.nl:14265' })

// Init State
//let root = 'ZMYUUZSLALHDLXXQGAKZSZNIDWXJEHYDIWBVRJFCOYDTXSDXMFQBODQGWLU9YEDHOIKOREDYHPXHMBAPI'
let root = "XMHQELYZVSDEMWVCSNKCFUMMWJZOJGBCD9EKZVNLETHIBIZEIHBGFEBWQLEVQYKEMBOPPDRGJSNE9WRHB"
let nextRoot = ""

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

const execute = async () => {
  var resp = await Mam.fetch(root, 'public', null, logData)

  // This is needed to get the next data
  nextRoot = resp['nextRoot'])
}

execute()
