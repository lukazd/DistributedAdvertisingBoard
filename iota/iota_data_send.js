var Mam = require('../lib/mam.node.js')
var IOTA = require('iota.lib.js')
var iota = new IOTA({provider: 'https://testnet140.tangle.works'})

var mamState = Mam.init(iota)

mamState = Mam.init(iota)

data_to_pulish = "Placeholder data";

mamState = Mam.changeMode(
    mamSTate,
    'restricted',
    process.env.dataKey
)

const publish = async packet => {
    var message = Mam.create(mamState, packet)

    mamState = message.state
    await Mam.attach(message.payload, message.address)

}

publish(data_to_publish)
