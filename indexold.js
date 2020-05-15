id="result" type="text/template"
<li>
    You rolled:
    {{#each values}}
        <img alt="{{ this }}" title="{{ this }}" src="img/{{ this }}.png">
    {{/each}}
    (Total: {{ total }})
</li>


document.addEventListener('DOMContentLoaded', () => {
    
      // Connect to websocket
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

      var dispname =  document.querySelector('#name').value;
      dispname =  sessionStorage.getItem('displayname');
      document.querySelector('#name').value = dispname;
     
      // When connected, configure buttons
      socket.on('connect', () => {
// Each button should emit a "submit vote" event
             document.querySelectorAll('button').forEach(button => {                button.onclick = () => {
                    dispname =  sessionStorage.getItem('displayname');
                    if (dispname.length > 0) {
                        const selection = button.dataset.vote;
                        socket.emit('submit vote', {'selection': selection});
                    }
                };
            });
        });
        
      // When a new vote is announced, add to the unordered list
      socket.on('voter totals', data => {
            document.querySelector('#yes').innerHTML = `${data.votes["yes"]}`;
            document.querySelector('#no').innerHTML = `${data.votes["no"]}`;
            document.querySelector('#maybe').innerHTML =`${data.votes["maybe"]}`;
      });

     
    
  });

function whatisthis(val) {
        sessionStorage.setItem('displayname', val);
        if (val.length > 0 ) alert(`Hello ${val} `);
         
}