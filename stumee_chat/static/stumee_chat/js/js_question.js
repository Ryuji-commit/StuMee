const peer = new Peer({
    key: 'df9c591f-ec64-4dde-9edd-b3b376d881dd',
    debug: 3,
});

let room = null;
let existingRoom = null;
let LocalStream = null;

peer.on('open', function(){
    console.log('connected');
});

$('#start-video').on('click', function() {
    startVideo();
});

$('#end-video').on('click', function(room) {
    if (existingRoom) {
        existingRoom.close();
    };

    removeAllRemoteVideos();
    LocalStream.stop();
    setupMakeCallUI();
});

async function startVideo(){
    const localVideo = document.getElementById('local-video');

    LocalStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    $('#videos-container').show();
    setupEndCallUI();

    // render local video
    localVideo.muted = true;
    localVideo.srcObject = LocalStream;
    localVideo.playsInline = true;
    await localVideo.play().catch(console.error);
}

function setupRoomEventHandlers(room){
    if (existingRoom) {
        existingRoom.close();
    };

    existingRoom = room;
    $('#videos-container').show();

    room.on('stream', async function(stream){
        const newVideo = document.createElement('video');
        newVideo.srcObject = stream;
        newVideo.playsInline = true;
        newVideo.setAttribute('data-peer-id', stream.peerId);
        $('#remote-videos').append(newVideo);
        await newVideo.play().catch(console.error);
    });

    room.on('peerLeave', function(peerId){
        const remoteVideo = remoteVideos.querySelector(
        `[data-peer-id=${peerId}]`
        );
        remoteVideo.srcObject.getTracks().forEach(track => track.stop());
        remoteVideo.srcObject = null;
        remoteVideo.remove();
    });

    room.on('close', function(){
        removeAllRemoteVideos();
        setupMakeCallUI();
    });
}

function setupMakeCallUI(){
    $('#start-video').show();
    $('#end-video').hide();
}

function setupEndCallUI() {
    $('#start-video').hide();
    $('#end-video').show();
}

function removeAllRemoteVideos(){
    $('#remote-videos').empty();
    $('#videos-container').hide();
}

$(function(){
    // ページ読み込み時に実行したい処理
    $('#end-video').hide();
    $('#videos-container').hide();

    const RoomName = JSON.parse(document.getElementById('RoomNameURL').textContent);
    room = peer.joinRoom(RoomName,{
        mode: 'sfu',
        stream: LocalStream,
    });
    setupRoomEventHandlers(room);
});