const peer = new Peer({
    key: 'df9c591f-ec64-4dde-9edd-b3b376d881dd',
    debug: 3,
});

let room = null;
let existingRoom = null;
let LocalStream = null;
let remoteVideos = document.getElementById('remote-videos');

peer.on('open', function(){
    console.log('connected');
});

$('#start-video').on('click', function() {
    RoomLogin();
});

$('#end-video').on('click', function(room) {
    const localVideo = document.getElementById('local-video');
    if (localVideo != null){
        localVideo.srcObject.getTracks().forEach(track => track.stop());
        localVideo.srcObject = null;
    }
    existingRoom.close();
    setupMakeCallUI();
});

async function RoomLogin(){
    const localVideo = document.getElementById('local-video');

    LocalStream = await navigator.mediaDevices.getDisplayMedia({video: {width:800, height:600}})
    $('#videos-container').show();
    setupEndCallUI();

    // render local video
    localVideo.muted = true;
    localVideo.srcObject = LocalStream;
    localVideo.playsInline = true;
    await localVideo.play().catch(console.error);

    // logged in Room
    const RoomName = JSON.parse(document.getElementById('RoomNameURL').textContent);
    room = peer.joinRoom(RoomName,{
        mode: 'sfu',
        stream: LocalStream,
    });
    setupRoomEventHandlers(room);
}

function setupRoomEventHandlers(room){
    if (existingRoom) {
        existingRoom.close();
    };

    existingRoom = room;

    room.on('stream', async function(stream){
        $('#videos-container').show();
        console.log('receive stream');

        const newVideo = document.createElement('video');
        newVideo.srcObject = stream;
        newVideo.playsInline = true;
        newVideo.setAttribute('data-peer-id', stream.peerId);
        $('#remote-videos').append(newVideo);
        await newVideo.play().catch(console.error);
    });

    room.on('peerJoin', function(peerId){
        console.log(peerId + 'joined');
    });

    room.on('peerLeave', function(peerId){
        console.log(peerId + 'leaved');
        const remoteVideo = remoteVideos.querySelector('[data-peer-id="' + peerId + '"]');
        if (remoteVideo != null){
            remoteVideo.srcObject.getTracks().forEach(track => track.stop());
            remoteVideo.srcObject = null;
            remoteVideo.remove();
        }
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
});