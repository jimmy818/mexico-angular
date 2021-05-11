// Register event listener for the 'push' event.
self.addEventListener('push', function(event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
    const eventInfo = event.data.text() || {
        "head": "No Content",
        "body": "No Content",
        "icon": ""
    };
    const data = JSON.parse(eventInfo);
    const head = data.head || 'Solo-performance2 🕺🕺';
    const body = data.body || 'This is default content. Your notification didn\'t have one 🙄🙄';
    const icon = data.icon || 'https://oms-edu.org/wp-content/uploads/2019/11/solo-performance.png';

    url = data.url ? data.url : self.location.origin;

    const options = {
            "body": body,
            "icon": icon,

        }
        // Keep the service worker alive until the notification is created.
    event.waitUntil(
        self.registration.showNotification(head, options)

    );
});