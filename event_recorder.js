
document.addEventListener('click', function(event) {
    let path = [];
    let elem = event.target;
    while (elem) {
        let selector = elem.nodeName.toLowerCase();
        if (elem.id) {
            selector += '#' + elem.id;
            path.unshift(selector);
            break;
        } else {
            let siblingCount = 0;
            let siblingIndex = 0;

            for (let sib = elem.previousSibling; sib; sib = sib.previousSibling) {
                if (sib.nodeName === elem.nodeName) {
                    siblingCount++;
                }
            }
            for (let sib = elem.nextSibling; sib; sib = sib.nextSibling) {
                if (sib.nodeName === elem.nodeName) {
                    siblingIndex++;
                }
            }
            if (siblingCount > 0 || siblingIndex > 0) {
                selector += ':nth-of-type(' + (siblingCount + 1) + ')';
            }
        }
        path.unshift(selector);
        elem = elem.parentElement;
    }

    const elemPath = path.join(' > ');
    const elemText = event.target.innerText || event.target.textContent;
    console.log(`Clicked element: ${elemPath}, Text: ${elemText}`);

    // Store details in a temporary variable
    window.recordedEvents = window.recordedEvents || [];
    window.recordedEvents.push({
        element: elemPath,
        text: elemText,
        time: new Date().getTime(),
        event: 'click'
    });
});

// Add event listener for keypress events
document.addEventListener('keydown', function(event) {
    const elem = document.activeElement; // Get the currently focused element
    const elemPath = elem.tagName.toLowerCase() + (elem.id ? '#' + elem.id : '');
    
    console.log(`Key pressed: ${event.key} in element: ${elemPath}`);

    // Store details in a temporary variable
    window.recordedEvents = window.recordedEvents || [];
    window.recordedEvents.push({
        element: elemPath,
        key: event.key,
        time: new Date().getTime(),
        event: 'keypress'
    });
});

// Listen for change events on select, radio, and checkbox inputs
document.addEventListener('change', function(event) {
    const elem = event.target;
    const elemType = elem.type;

    if (elem.tagName.toLowerCase() === 'select' || elemType === 'radio' || elemType === 'checkbox') {
        const elemPath = elem.tagName.toLowerCase() + (elem.id ? '#' + elem.id : '');
        const selectedValue = (elemType === 'checkbox') ? elem.checked : elem.value;

        console.log(`Change detected in element: ${elemPath}, New value: ${selectedValue}`);
        
        // Store details in a temporary variable
        window.recordedEvents = window.recordedEvents || [];
        window.recordedEvents.push({
            element: elemPath,
            selectedValue: selectedValue,
            time: new Date().getTime(),
            event: 'change'
        });
    }
});

// Handler to retrieve recorded events
window.getRecordedEvents = function() {
    return JSON.stringify(window.recordedEvents || []);
};
