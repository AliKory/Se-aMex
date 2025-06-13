const options = {
    host: '9490def8d1484163895a70bd2a54355f.s1.eu.hivemq.cloud',
    port: 8883,
    protocol: 'mqtts',
    username: 'miapi2',
    password: 'cisco123T',
    rejectUnauthorized: false
};

const client = mqtt.connect(options);

client.on('connect', function () {
    console.log('Connected');
    client.subscribe('rasp/resultado');
});

client.on('error', function (error) {
    console.log('Error:', error);
});

client.on('message', function (topic, message) {
    console.log('Received message:', topic, message.toString());
    updateUI(message.toString());
});

function updateUI(msg) {
    document.getElementById('letraInput').value = msg;
    document.getElementById('letraImage').src = `/assets/${msg}.jpg`;
    document.getElementById('letraAudio').src = `/assets/${msg}.mp3`;
}
