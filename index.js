           // Template for roll results

document.addEventListener('DOMContentLoaded', () => {
    
    
      // Connect to websocket
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port, {'multiplex': false}) ;

      var dispname =  document.querySelector('#name').value;
      dispname =  sessionStorage.getItem('displayname');
      document.querySelector('#name').value = dispname;
      var currentchannelId = "" ;
      var i = 0;
     if (!socket.connected)
        socket.connect();
      // When connected, configure buttons
      socket.on('connect', () => {
// Each button should emit a "add channel" event
             document.querySelector('#newC').onclick = () => {
                console.log(`button clicked`);
                document.querySelector('.error').innerHTML = "";
                dispname =  sessionStorage.getItem('displayname');
                const newChannelName = document.querySelector('#NewChannelname').value ;
     
                if (dispname !== null && dispname.length > 0 && newChannelName !== null && newChannelName.length > 0) {
                        socket.emit('add channel', {'channel': newChannelName});
                }
                else
                if (dispname == null || dispname.length == 0) {
                    document.querySelector('.error').innerHTML = "Enter your name please";  
                }
                else
                if (newChannelName == null || newChannelName.length == 0){
                    document.querySelector('.error').innerHTML = "Enter a channel name please";  
                }
                
            };

            //    document.querySelectorAll('.buttonrow').forEach(div=> {div.onclick = () => {
             //       sessionStorage.setItem('currentchannel', div.id);
             //       console.log(`channel clicked ${div.id}`);
             //       document.querySelector('#btnmessage').innerHTML = "Submit Message for Channel " ;
 
             //       document.querySelector('#btnmessage').innerHTML += div.id ;
                    //if (dispname.length > 0) {
                    //   socket.emit('add channel', {'channel': dispname});
                    //}
             //   };
            //})

            
            document.querySelectorAll('.row.buttonrow').forEach(button=> {button.onclick = channelClick
                       });


            document.querySelector('#btnmessage').onclick = () => {
                console.log(`New message button clicked`);
                document.querySelector('.error').innerHTML = "";
                dispname = sessionStorage.getItem('displayname');
                console.log(`Got display name  ${dispname}`);
                currentchannelId = sessionStorage.getItem('currentchannel');
                // currentchannelId = sessionStorage.getitem("currentchannel");
                console.log(`Got current channel ${currentchannelId}`);
                var currentMessage = document.querySelector('#NewMessage').value;
                if (dispname !== null && dispname.length > 0 && currentchannelId !== null && currentchannelId.length > 0 && currentMessage != null && currentMessage.length > 0 )  {
                        socket.emit('add message', {'channelid': currentchannelId, 'message' : currentMessage, 'persononame' : dispname});
                }
                else
                if (dispname == null || dispname.length == 0) {
                    document.querySelector('.error').innerHTML = "Enter your name please";  
                }
                else
                if (currentchannelId == null || currentchannelId.length == 0){
                    document.querySelector('.error').innerHTML = "Choose a channel please";  
                }
                else
                if (currentMessage == null || currentMessage.length == 0){
                    document.querySelector('.error').innerHTML = "Enter your message please";  
                }
            };

    });   
      // When a new channel is announced, add to the button list
      socket.on('new channel', data => {
            console.log(` Error is ${data.errormessage}`);
            if (data.errormessage == null ) {
                var template = document.querySelector('#newchannel').innerHTML;                
                console.log(template);
                var templatescript = Handlebars.compile(template);
                var context = {"channelname": data.name, "channelid": data.id };
                var content = templatescript(context);
                var btnid = '#' + data.id
                console.log(content);
            //alert(`Hello ${content} `);
                document.querySelector('#channellist').innerHTML += content;
                //document.querySelector(btnid).onclick = channelClick;   
                document.querySelectorAll('.row.buttonrow').forEach(button=> {button.onclick = channelClick
                });
                //note: Drop the parenthesis!
                //Be careful not to use onclick = channelClick(); — channelClick will be run immediately and the value returned (undefined) will be assigned 
                //to the onclick property of the button. It may not throw an error, but your handler will never be called when the click event occurs.
                localStorage.setItem('channels', data.chaneels);
               }
            else
                document.querySelector('.error').innerHTML = data.errormessage;
        });
     // When a new channel is announced, add to the button list
     socket.on('new message', data => {
        //console.log(` Error is ${data.errormessage}`);
        //if (data.errormessage == null ) {
        //if (data.id == localStorage.setItem('channels', data.chaneels);
        var currentchannel = sessionStorage.getItem('currentchannel');
        console.log(`Current channel ${currentchannel} `);
        console.log(` Data ID ${data.id}`);
        if (currentchannel == data.id) {
            var template = document.querySelector('#newmessage').innerHTML;                
            console.log(template);
            var templatescript = Handlebars.compile(template);
            var context = {"newrmessage": data.fullmessage};
            var content = templatescript(context);
            console.log(content);
            document.querySelector('#messagelist').innerHTML += content;
         }
    });


});

function whatisthis(val) {
        document.querySelector('.error').innerHTML = "";
        sessionStorage.setItem('displayname', val);
        //if (val.length > 0 ) alert(`Hello ${val} `);
         
}


function channelClick() {
    sessionStorage.setItem('currentchannel', this.id);
    console.log(`channel clicked ${this.id}`);
//    document.querySelector('#btnmessage').innerHTML = "Submit Message for Channel " ;
 
 //   document.querySelector('#btnmessage').innerHTML += this.id ;
 //   var form = document.getElementById("chatform");
 //   form.submit();
 
}
