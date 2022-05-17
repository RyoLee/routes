addEventListener("fetch", event => {
    event.respondWith(handleRequest(event.request))
  })
  
  async function handleRequest(request) {
    
    const { searchParams } = new URL(request.url)
    let device = searchParams.get('device')
    let mode = searchParams.get('mode')
    console.log(device)
    if(null===mode||mode!='6'){
      mode='4'
    }
    if(null===device){
      device='eth0'
    }
    let data_url = 'https://raw.githubusercontent.com/RyoLee/routes/gh-pages/eth0/routes' + mode + '.conf'
    if (request.method !== 'GET') return MethodNotAllowed(request)
    const response = await fetch(data_url)
    if (response.ok) {
      const body = await response.text();
      return new Response(body.replaceAll('eth0',device))
    } else {
      return InternalServerError(request)
    }
  }
  function MethodNotAllowed(request) {
    return new Response(`Method ${request.method} not allowed.`, {
      status: 405,
      headers: {
        Allow: 'GET',
      },
    });
  }
  function InternalServerError(request) {
    return new Response(`Internal Server Error.`, {
      status: 500,
    });
  }