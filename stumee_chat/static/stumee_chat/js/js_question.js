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

peer.on('open', function(){
    console.log('connected');
    RoomLogin(false);
});

$('#start-video').on('click', function() {
    existingRoom.close();
    RoomLogin(true);
});

$('#end-video').on('click', function() {
    const localVideo = document.getElementById('local-video');
    if (localVideo != null){
        localVideo.srcObject.getTracks().forEach(track => track.stop());
        localVideo.srcObject = null;
        ScreenShareStream.getTracks().forEach(track => track.stop());
        AudioStream.getTracks().forEach(track => track.stop());
        LocalStream.getTracks().forEach(track => track.stop());
    }
    existingRoom.close();
    setupMakeCallUI();
    RoomLogin(false);
});

async function RoomLogin(is_video_flag){
    const RoomName = JSON.parse(document.getElementById('RoomNameURL').textContent);
    if(is_video_flag == true){
        const localVideo = document.getElementById('local-video');

        LocalStream = new MediaStream();
        ScreenShareStream = await navigator.mediaDevices.getDisplayMedia({video: {width:1920, height:1080} , audio: false})
        AudioStream = await navigator.mediaDevices.getUserMedia({video: false, audio: true})

        ScreenShareStream.getVideoTracks().forEach(track => {
            LocalStream.addTrack(track.clone())
        });
        AudioStream.getAudioTracks().forEach(track => {
            LocalStream.addTrack(track.clone())
        });

        $('#videos-container').show();
        setupEndCallUI();

        // render local video
        localVideo.muted = true;
        localVideo.srcObject = LocalStream;
        localVideo.playsInline = true;
        localVideo.classList.add('w-100');
        await localVideo.play().catch(console.error);

        // logged in Room
        room = peer.joinRoom(RoomName,{
            mode: 'sfu',
            stream: LocalStream,
        });
        console.log(room);
    }else{
        LocalStream = null;
        room = peer.joinRoom(RoomName,{
            mode: 'sfu',
            stream: null,
        });
    }
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
        const unMutedButton = document.querySelector('[id="' + peerId + '"]');
        if (unMutedButton != null){
            unMutedButton.remove();
        }

        if (remoteVideo != null){
            remoteVideo.srcObject.getTracks().forEach(track => track.stop());
            remoteVideo.srcObject = null;
            remoteVideo.remove();
        }

        if (LocalStream == null){
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

function removeAllRemoteVideos(){
    $('#remote-videos').empty();
    $('#videos-container').hide();
}

$(function(){
    // ページ読み込み時に実行したい処理
    $('#end-video').hide();
    $('#videos-container').hide();
});