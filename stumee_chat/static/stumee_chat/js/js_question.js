const peer = new Peer({
    key: 'df9c591f-ec64-4dde-9edd-b3b376d881dd',
    debug: 3,
});

let room = null;
let existingRoom = null;
let LocalStream = null;
let ScreenShareStream = null;
let AudioStream = null;
let remoteVideos = document.getElementById('remote-videos');
let isScreenShare = false;
let isAudio = false;

peer.on('open', function(){
    console.log('connected');
    RoomLogin();
});

$('#start-video').on('click', function() {
    stopTracksAllStream();
    existingRoom.close();
    isScreenShare = true;
    RoomLogin();
});

$('#end-video').on('click', function() {
    stopTracksAllStream();
    existingRoom.close();
    setupMakeCallUI();
    isScreenShare = false;
    RoomLogin();
});

$('#un-mute-button').on('click', function(){
    stopTracksAllStream();
    existingRoom.close();
    isAudio = true;
    RoomLogin();
});

$('#mute-button').on('click', function(){
    stopTracksAllStream();
    existingRoom.close();
    isAudio = false;
    showUnMuteButton();
    RoomLogin();
});

function stopTracksAllStream(){
    if (AudioStream){
        AudioStream.getTracks().forEach(track => track.stop());
    }
    if (ScreenShareStream){
        ScreenShareStream.getTracks().forEach(track => track.stop());
    }
    if (LocalStream){
        LocalStream.getTracks().forEach(track => track.stop());
    }
}

async function RoomLogin(){
    const RoomName = JSON.parse(document.getElementById('RoomNameURL').textContent);

    LocalStream = new MediaStream();
    if (isScreenShare && isAudio){
        ScreenShareStream = await navigator.mediaDevices.getDisplayMedia({video: {width:1920, height:1080} , audio: false});
        AudioStream = await navigator.mediaDevices.getUserMedia({video: false, audio: true});

        ScreenShareStream.getVideoTracks().forEach(track => {
            LocalStream.addTrack(track.clone())
        });
        AudioStream.getAudioTracks().forEach(track => {
            LocalStream.addTrack(track.clone())
        });
        setupEndCallUI();
        showMuteButton();
    }else if(isScreenShare){
        ScreenShareStream = await navigator.mediaDevices.getDisplayMedia({video: {width:1920, height:1080} , audio: false});
        ScreenShareStream.getVideoTracks().forEach(track => {
            LocalStream.addTrack(track.clone())
        });
        setupEndCallUI();
    }else if(isAudio){
        AudioStream = await navigator.mediaDevices.getUserMedia({video: false, audio: true});
        AudioStream.getAudioTracks().forEach(track => {
            LocalStream.addTrack(track.clone())
        });
        showMuteButton();
    }else{
        LocalStream = null;
    }
    // logged in Room
    room = peer.joinRoom(RoomName,{
        mode: 'sfu',
        stream: LocalStream,
    });
    console.log(room);
    setupRoomEventHandlers(room);
}

function setupRoomEventHandlers(room){
    existingRoom = room;

    room.on('stream', async function(stream){
        $('#videos-container').show();
        console.log('receive stream');
        console.log(stream);

        const newVideo = document.createElement('video');
        newVideo.srcObject = stream;
        newVideo.muted = true;
        newVideo.playsInline = true;
        newVideo.controls = true;
        newVideo.setAttribute('data-peer-id', stream.peerId);
        newVideo.classList.add('w-100');
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

        if (document.getElementById('remote-videos').childElementCount === 0){
            removeAllRemoteVideos();
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

function showMuteButton() {
    $('#mute-button').show();
    $('#un-mute-button').hide();
}

function showUnMuteButton() {
    $('#mute-button').hide();
    $('#un-mute-button').show();
}

function removeAllRemoteVideos(){
    $('#remote-videos').empty();
    $('#videos-container').hide();
}

$(function(){
    // ページ読み込み時に実行したい処理
    $('#end-video').hide();
    $('#videos-container').hide();
    $('#mute-button').hide();
});