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
        LocalStream = null
    }
    existingRoom.close();
    setupMakeCallUI();
    RoomLogin(false);
});

async function RoomLogin(is_video_flag){
    const RoomName = JSON.parse(document.getElementById('RoomNameURL').textContent);
    if(is_video_flag == true){
        const localVideo = document.getElementById('local-video');
        LocalStream = await navigator.mediaDevices.getDisplayMedia({video: {width:1000, height:800} , audio: true})
        $('#videos-container').show();
        setupEndCallUI();

        // render local video
        localVideo.muted = true;
        localVideo.srcObject = LocalStream;
        localVideo.playsInline = true;
        await localVideo.play().catch(console.error);

        // logged in Room
        room = peer.joinRoom(RoomName,{
            mode: 'sfu',
            stream: LocalStream,
        });
        console.log(room);
    }else{
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

        const newVideo = document.createElement('video');
        newVideo.srcObject = stream;
        newVideo.muted = true;
        newVideo.playsInline = true;
        newVideo.setAttribute('data-peer-id', stream.peerId);
        $('#remote-videos').append(newVideo);
        setUpUnMutedButton(stream.peerId);
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

function UnMuteRemoteVideo(video_id) {
    const remoteVideo = remoteVideos.querySelector('[data-peer-id="' + video_id + '"]');
    remoteVideo.muted = false;
    console.log('un muted');
    const unMutedButton = document.querySelector('[id="' + video_id + '"]');
    unMutedButton.remove();
}

function setUpUnMutedButton(StreamPeerID){
    const $remoteVideo = remoteVideos.querySelector('[data-peer-id="' + StreamPeerID + '"]');
    const UnMutedButton = document.createElement('button');
    UnMutedButton.setAttribute('type', 'submit');
    UnMutedButton.setAttribute('class', 'btn btn-primary un-muted mb-2 align-top');
    UnMutedButton.setAttribute('id', StreamPeerID);
    UnMutedButton.setAttribute('onclick', "UnMuteRemoteVideo(this.id);");
    UnMutedButton.innerHTML = '相手の音声を追加'
    $remoteVideo.before(UnMutedButton);
}

$(function(){
    // ページ読み込み時に実行したい処理
    $('#end-video').hide();
    $('#videos-container').hide();
});