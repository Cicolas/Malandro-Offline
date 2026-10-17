// Keep accounts, telemetry and multiplayer out of the local edition.
(() => {
  const originalFetch = window.fetch.bind(window);
  window.fetch = (input, options) => {
    const url = new URL(input instanceof Request ? input.url : input, location.href);
    if (/^\/(?:pvp\/)?api(?:\/|$)/.test(url.pathname)) {
      return Promise.resolve(new Response(JSON.stringify({erro: "Indisponível na versão local"}), {
        status: 401, headers: {"Content-Type": "application/json"}
      }));
    }
    return originalFetch(input, options);
  };
  navigator.sendBeacon = () => false;
  window.WebSocket = class {
    static CONNECTING = 0; static OPEN = 1; static CLOSING = 2; static CLOSED = 3;
    constructor() { throw new Error("Multiplayer is unavailable in the local edition"); }
  };
})();
